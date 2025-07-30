"""Main client implementation for LAX NATS JetStream SDK."""

import asyncio
import json
import logging
import uuid
from typing import Optional, Dict, Any, List, Union

import nats
import grpc
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

from .options import ClientOptions, PublishOptions
from .metrics import Metrics, Timer
from .circuit_breaker import CircuitBreaker, CircuitBreakerOpen
from .exceptions import ConnectionError, PublishError
try:
    from .proto import broker_pb2, broker_pb2_grpc
except ImportError:
    # Fallback for testing without generated protos
    broker_pb2 = None
    broker_pb2_grpc = None


class LaxClient:
    """Smart client that routes between NATS and gRPC based on requirements."""
    
    def __init__(self, options: Optional[ClientOptions] = None):
        self.options = options or ClientOptions()
        self.logger = self._setup_logger()
        self.metrics = Metrics(
            prefix=self.options.metrics_prefix,
            enabled=self.options.enable_metrics
        )
        
        # Connection pools
        self._nc: Optional[nats.NATS] = None
        self._grpc_channels: List[grpc.aio.Channel] = []
        self._grpc_stubs: List[broker_pb2_grpc.BrokerServiceStub] = []
        self._pool_index = 0
        self._pool_lock = asyncio.Lock()
        
        # Circuit breaker
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=self.options.circuit_breaker_threshold,
            timeout=self.options.circuit_breaker_timeout,
            half_open_requests=self.options.circuit_breaker_half_open_requests,
        )
        
        # State
        self._closed = False
        self._connect_lock = asyncio.Lock()
        self._connected = False
        
        # Rate limiting
        self._semaphore = asyncio.Semaphore(self.options.max_concurrent_publishes)
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logger with configured level."""
        logger = logging.getLogger("lax_client")
        logger.setLevel(getattr(logging, self.options.log_level.upper()))
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    async def connect(self):
        """Connect to NATS and gRPC broker."""
        async with self._connect_lock:
            if self._connected:
                return
            
            try:
                # Connect to NATS
                await self._connect_nats()
                
                # Create gRPC connection pool
                await self._connect_grpc_pool()
                
                self._connected = True
                self.logger.info("LAX client connected successfully")
                
            except Exception as e:
                self.logger.error(f"Failed to connect: {e}")
                raise ConnectionError(f"Failed to connect: {e}") from e
    
    async def _connect_nats(self):
        """Connect to NATS server."""
        try:
            self._nc = await nats.connect(
                servers=self.options.nats_urls,
                connect_timeout=self.options.nats_connect_timeout,
                max_reconnect_attempts=self.options.nats_max_reconnect_attempts,
                reconnect_time_wait=self.options.nats_reconnect_wait,
                error_cb=self._nats_error_cb,
                disconnected_cb=self._nats_disconnected_cb,
                reconnected_cb=self._nats_reconnected_cb,
            )
            
            self.metrics.set_connection_count("nats", 1)
            self.logger.info(f"Connected to NATS: {self.options.nats_urls}")
            
        except Exception as e:
            self.metrics.record_connection_error("nats")
            raise ConnectionError(f"Failed to connect to NATS: {e}") from e
    
    async def _connect_grpc_pool(self):
        """Create gRPC connection pool."""
        for i in range(self.options.connection_pool_size):
            try:
                # Create channel
                if self.options.use_tls:
                    # TODO: Implement TLS support
                    channel = grpc.aio.insecure_channel(self.options.broker_addr)
                else:
                    channel = grpc.aio.insecure_channel(
                        self.options.broker_addr,
                        options=[
                            ('grpc.max_send_message_length', 64 * 1024 * 1024),
                            ('grpc.max_receive_message_length', 64 * 1024 * 1024),
                            ('grpc.keepalive_time_ms', 10000),
                            ('grpc.keepalive_timeout_ms', 5000),
                            ('grpc.keepalive_permit_without_calls', True),
                        ]
                    )
                
                # Create stub
                stub = broker_pb2_grpc.BrokerServiceStub(channel)
                
                self._grpc_channels.append(channel)
                self._grpc_stubs.append(stub)
                
            except Exception as e:
                # Clean up already created channels
                for ch in self._grpc_channels:
                    await ch.close()
                self._grpc_channels.clear()
                self._grpc_stubs.clear()
                
                self.metrics.record_connection_error("grpc")
                raise ConnectionError(f"Failed to create gRPC pool: {e}") from e
        
        self.metrics.set_connection_count("grpc", len(self._grpc_channels))
        self.logger.info(
            f"Created gRPC connection pool: {self.options.broker_addr} "
            f"(size: {self.options.connection_pool_size})"
        )
    
    async def publish(
        self,
        subject: str,
        data: Union[bytes, str, dict],
        options: Optional[PublishOptions] = None,
    ) -> str:
        """Publish a message with smart routing.
        
        Args:
            subject: The subject/topic to publish to
            data: The message data (bytes, string, or dict)
            options: Publishing options
            
        Returns:
            Message ID
            
        Raises:
            PublishError: If publishing fails
            CircuitBreakerOpen: If circuit breaker is open
        """
        if not self._connected:
            await self.connect()
        
        # Convert data to bytes
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')
        
        # Apply default options
        opts = options or PublishOptions()
        
        # Generate message ID if not provided
        if not opts.message_id:
            opts.message_id = str(uuid.uuid4())
        
        # Check circuit breaker
        if self._circuit_breaker.is_open:
            self.metrics.record_publish(
                tier=opts.tier.value,
                method="none",
                latency=0,
                success=False,
                error_type="circuit_open"
            )
            raise CircuitBreakerOpen("Circuit breaker is open")
        
        # Use semaphore for rate limiting
        async with self._semaphore:
            with Timer() as timer:
                try:
                    # Smart routing decision
                    if opts.should_use_nats():
                        result = await self._publish_nats(subject, data, opts)
                        method = "nats"
                    else:
                        result = await self._publish_grpc(subject, data, opts)
                        method = "grpc"
                    
                    # Record success
                    self.metrics.record_publish(
                        tier=opts.tier.value,
                        method=method,
                        latency=timer.elapsed,
                        success=True
                    )
                    
                    return result
                    
                except Exception as e:
                    # Record failure
                    error_type = type(e).__name__
                    self.metrics.record_publish(
                        tier=opts.tier.value,
                        method="unknown",
                        latency=timer.elapsed,
                        success=False,
                        error_type=error_type
                    )
                    raise
    
    async def _publish_nats(
        self,
        subject: str,
        data: bytes,
        options: PublishOptions
    ) -> str:
        """Publish directly to NATS."""
        try:
            # Add headers if provided
            headers = {}
            if options.headers:
                headers.update(options.headers)
            if options.message_id:
                headers['Message-Id'] = options.message_id
            
            # Publish with headers (if any)
            await self._nc.publish(subject, data, headers=headers if headers else None)
            
            self.logger.debug(f"Published to NATS: {subject} ({len(data)} bytes)")
            return options.message_id
            
        except Exception as e:
            raise PublishError(f"NATS publish failed: {e}") from e
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=0.1, max=5),
        retry=retry_if_exception_type(grpc.RpcError),
        before_sleep=before_sleep_log(logging.getLogger("lax_client"), logging.WARNING)
    )
    async def _publish_grpc(
        self,
        subject: str,
        data: bytes,
        options: PublishOptions
    ) -> str:
        """Publish through gRPC broker."""
        # Get stub from pool
        stub = await self._get_grpc_stub()
        
        # Create request
        request = broker_pb2.PublishRequest(
            subject=subject,
            payload=data,
            headers=options.headers or {},
            options=broker_pb2.PublishOptions(
                tier=options.tier.value,
                require_ack=options.require_ack,
                timeout_ms=int((options.timeout or self.options.publish_timeout) * 1000),
            )
        )
        
        try:
            # Set timeout
            timeout = options.timeout or self.options.publish_timeout
            
            # Call with circuit breaker
            response = await self._circuit_breaker.call(
                stub.Publish,
                request,
                timeout=timeout
            )
            
            self.logger.debug(f"Published via gRPC: {subject} ({len(data)} bytes)")
            return response.message_id
            
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:  # pylint: disable=no-member
                raise PublishError("Publish timeout") from e
            elif e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:  # pylint: disable=no-member
                raise PublishError("Resource exhausted (buffer full)") from e
            else:
                raise PublishError(f"gRPC error: {e.details()}") from e  # pylint: disable=no-member
    
    async def _get_grpc_stub(self) -> broker_pb2_grpc.BrokerServiceStub:
        """Get next gRPC stub from pool (round-robin)."""
        async with self._pool_lock:
            stub = self._grpc_stubs[self._pool_index]
            self._pool_index = (self._pool_index + 1) % len(self._grpc_stubs)
            return stub
    
    def publish_sync(
        self,
        subject: str,
        data: Union[bytes, str, dict],
        options: Optional[PublishOptions] = None,
    ) -> str:
        """Synchronous publish wrapper for non-async code."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.publish(subject, data, options))
    
    async def batch_publish(
        self,
        messages: List[Dict[str, Any]],
        default_options: Optional[PublishOptions] = None,
    ) -> Dict[str, Any]:
        """Publish multiple messages efficiently.
        
        Args:
            messages: List of dicts with 'subject', 'data', and optional 'options'
            default_options: Default options for all messages
            
        Returns:
            Dict with 'success_count', 'failure_count', and 'message_ids'
        """
        if not self._connected:
            await self.connect()
        
        results = {
            "success_count": 0,
            "failure_count": 0,
            "message_ids": [],
            "errors": []
        }
        
        # Group messages by routing decision
        nats_messages = []
        grpc_messages = []
        
        for msg in messages:
            opts = msg.get("options", default_options) or PublishOptions()
            if opts.should_use_nats():
                nats_messages.append((msg, opts))
            else:
                grpc_messages.append((msg, opts))
        
        # Publish NATS messages concurrently
        if nats_messages:
            nats_tasks = [
                self.publish(msg["subject"], msg["data"], opts)
                for msg, opts in nats_messages
            ]
            nats_results = await asyncio.gather(*nats_tasks, return_exceptions=True)
            
            for i, result in enumerate(nats_results):
                if isinstance(result, Exception):
                    results["failure_count"] += 1
                    results["errors"].append(str(result))
                else:
                    results["success_count"] += 1
                    results["message_ids"].append(result)
        
        # Publish gRPC messages (could optimize with batch API)
        if grpc_messages:
            grpc_tasks = [
                self.publish(msg["subject"], msg["data"], opts)
                for msg, opts in grpc_messages
            ]
            grpc_results = await asyncio.gather(*grpc_tasks, return_exceptions=True)
            
            for i, result in enumerate(grpc_results):
                if isinstance(result, Exception):
                    results["failure_count"] += 1
                    results["errors"].append(str(result))
                else:
                    results["success_count"] += 1
                    results["message_ids"].append(result)
        
        return results
    
    # NATS callbacks
    async def _nats_error_cb(self, e: Exception):
        """NATS error callback."""
        self.logger.error(f"NATS error: {e}")
        self.metrics.record_connection_error("nats")
    
    async def _nats_disconnected_cb(self):
        """NATS disconnected callback."""
        self.logger.warning("NATS disconnected")
        self.metrics.set_connection_count("nats", 0)
    
    async def _nats_reconnected_cb(self):
        """NATS reconnected callback."""
        self.logger.info("NATS reconnected")
        self.metrics.set_connection_count("nats", 1)
    
    async def close(self):
        """Close all connections."""
        if self._closed:
            return
        
        self._closed = True
        
        # Close NATS
        if self._nc and not self._nc.is_closed:
            await self._nc.close()
            self.metrics.set_connection_count("nats", 0)
        
        # Close gRPC channels
        for channel in self._grpc_channels:
            await channel.close()
        self._grpc_channels.clear()
        self._grpc_stubs.clear()
        self.metrics.set_connection_count("grpc", 0)
        
        self.logger.info("LAX client closed")
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._connected and not self._closed
