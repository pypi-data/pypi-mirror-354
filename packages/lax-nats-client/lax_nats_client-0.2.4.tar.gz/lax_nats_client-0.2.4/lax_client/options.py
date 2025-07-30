"""Configuration options for LAX client SDK."""

from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from enum import Enum
import time


class Tier(str, Enum):
    """Storage tier for messages."""
    MEMORY = "memory"
    REPLICATED = "replicated"
    PERSISTENT = "persistent"


@dataclass
class ClientOptions:
    """Configuration options for the LAX client."""
    
    # NATS connection settings
    nats_urls: List[str] = field(default_factory=lambda: ["nats://localhost:4222"])
    nats_connect_timeout: float = 5.0
    nats_max_reconnect_attempts: int = -1  # -1 = infinite
    nats_reconnect_wait: float = 2.0
    
    # gRPC connection settings
    broker_addr: str = "localhost:50051"
    grpc_timeout: float = 30.0
    use_tls: bool = False
    tls_cert_path: Optional[str] = None
    
    # Performance settings
    connection_pool_size: int = 10
    publish_timeout: float = 5.0
    retry_attempts: int = 3
    retry_delay: float = 0.1  # seconds
    retry_multiplier: float = 2.0  # exponential backoff
    max_retry_delay: float = 5.0
    
    # Circuit breaker settings
    circuit_breaker_threshold: int = 10
    circuit_breaker_timeout: float = 30.0
    circuit_breaker_half_open_requests: int = 3
    
    # Metrics settings
    enable_metrics: bool = True
    metrics_prefix: str = "lax_client"
    
    # Logging
    log_level: str = "INFO"
    
    # Async settings
    max_concurrent_publishes: int = 1000
    
    def __post_init__(self):
        """Validate configuration."""
        if self.connection_pool_size < 1:
            raise ValueError("connection_pool_size must be at least 1")
        if self.publish_timeout <= 0:
            raise ValueError("publish_timeout must be positive")
        if self.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
        if self.circuit_breaker_threshold < 1:
            raise ValueError("circuit_breaker_threshold must be at least 1")


@dataclass
class PublishOptions:
    """Options for publishing a message."""
    
    # Tier determines routing: "memory" uses direct NATS, others use gRPC
    tier: Tier = Tier.MEMORY
    
    # Force gRPC path even for memory tier
    require_ack: bool = False
    
    # Timeout for this specific publish operation
    timeout: Optional[float] = None
    
    # Headers to include with the message
    headers: Optional[Dict[str, str]] = None
    
    # Priority for message ordering (higher = more important)
    priority: int = 0
    
    # Custom retry count for this message
    retry_count: Optional[int] = None
    
    # Unique message ID (auto-generated if not provided)
    message_id: Optional[str] = None
    
    # Deduplication ID (for exactly-once semantics)
    dedup_id: Optional[str] = None
    
    def should_use_nats(self) -> bool:
        """Determine if this message should use direct NATS."""
        return self.tier == Tier.MEMORY and not self.require_ack


@dataclass
class SubscribeOptions:
    """Options for subscribing to messages."""
    
    # Maximum number of messages in flight (unacknowledged)
    max_inflight: int = 100
    
    # Whether to require manual acknowledgment
    manual_ack: bool = True
    
    # Acknowledgment timeout in seconds
    ack_wait_seconds: int = 30
    
    # Maximum delivery attempts before message is dead-lettered
    max_deliver: int = 5
    
    # Number of messages to prefetch for performance
    prefetch: int = 10
    
    # Enable flow control to prevent overwhelming the client
    enable_flow_control: bool = True
    
    # Start position: "new", "last", "first", or "sequence:N"
    start_position: str = "new"
    
    # Timeout for the subscription stream
    timeout: Optional[float] = None


@dataclass
class ConsumerGroupConfig:
    """Configuration for consumer groups."""
    
    # Delivery policy: "all", "last", "new", "by_start_sequence", "by_start_time"
    deliver_policy: str = "new"
    
    # Maximum redelivery attempts
    max_deliver: int = 5
    
    # Acknowledgment timeout in seconds
    ack_wait_seconds: int = 30
    
    # Maximum pending acknowledgments
    max_ack_pending: int = 1000
    
    # Enable flow control
    flow_control: bool = True
    
    # Idle heartbeat interval in seconds
    idle_heartbeat_seconds: int = 30
    
    # Replay policy: "instant", "original"
    replay_policy: str = "instant"
    
    # Rate limit (messages per second, 0 = unlimited)
    rate_limit: int = 0