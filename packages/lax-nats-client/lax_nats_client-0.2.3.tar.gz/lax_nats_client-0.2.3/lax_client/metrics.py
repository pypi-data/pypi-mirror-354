"""Metrics collection for LAX client SDK."""

from prometheus_client import Counter, Histogram, Gauge, Info
from typing import Optional
import time


class Metrics:
    """Prometheus metrics for the LAX client."""
    
    def __init__(self, prefix: str = "lax_client", enabled: bool = True):
        self.enabled = enabled
        self.prefix = prefix
        
        if not enabled:
            return
            
        # Publish metrics
        self.publish_total = Counter(
            f"{prefix}_publish_total",
            "Total number of publish operations",
            ["tier", "status"]
        )
        
        self.publish_latency = Histogram(
            f"{prefix}_publish_latency_seconds",
            "Publish operation latency",
            ["tier", "method"],
            buckets=(0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005, 
                    0.01, 0.05, 0.1, 0.5, 1.0, 5.0)
        )
        
        self.publish_errors = Counter(
            f"{prefix}_publish_errors_total",
            "Total number of publish errors",
            ["tier", "error_type"]
        )
        
        # Routing metrics
        self.direct_nats_total = Counter(
            f"{prefix}_direct_nats_total",
            "Total messages sent directly to NATS"
        )
        
        self.grpc_total = Counter(
            f"{prefix}_grpc_total",
            "Total messages sent via gRPC"
        )
        
        # Connection metrics
        self.nats_connections = Gauge(
            f"{prefix}_nats_connections",
            "Current number of NATS connections"
        )
        
        self.grpc_connections = Gauge(
            f"{prefix}_grpc_connections",
            "Current number of gRPC connections"
        )
        
        self.connection_errors = Counter(
            f"{prefix}_connection_errors_total",
            "Total number of connection errors",
            ["type"]
        )
        
        # Circuit breaker metrics
        self.circuit_breaker_state = Gauge(
            f"{prefix}_circuit_breaker_state",
            "Circuit breaker state (0=closed, 1=open, 2=half-open)"
        )
        
        self.circuit_breaker_trips = Counter(
            f"{prefix}_circuit_breaker_trips_total",
            "Total number of circuit breaker trips"
        )
        
        # Client info
        self.client_info = Info(
            f"{prefix}_info",
            "LAX client information"
        )
        self.client_info.info({
            "version": "0.1.0",
            "language": "python"
        })
    
    def record_publish(self, tier: str, method: str, latency: float, 
                      success: bool, error_type: Optional[str] = None):
        """Record a publish operation."""
        if not self.enabled:
            return
            
        self.publish_total.labels(
            tier=tier,
            status="success" if success else "error"
        ).inc()
        
        self.publish_latency.labels(
            tier=tier,
            method=method
        ).observe(latency)
        
        if not success and error_type:
            self.publish_errors.labels(
                tier=tier,
                error_type=error_type
            ).inc()
        
        if method == "nats":
            self.direct_nats_total.inc()
        else:
            self.grpc_total.inc()
    
    def set_circuit_breaker_state(self, state: str):
        """Update circuit breaker state."""
        if not self.enabled:
            return
            
        state_map = {"closed": 0, "open": 1, "half_open": 2}
        self.circuit_breaker_state.set(state_map.get(state, 0))
        
        if state == "open":
            self.circuit_breaker_trips.inc()
    
    def set_connection_count(self, conn_type: str, count: int):
        """Update connection count."""
        if not self.enabled:
            return
            
        if conn_type == "nats":
            self.nats_connections.set(count)
        elif conn_type == "grpc":
            self.grpc_connections.set(count)
    
    def record_connection_error(self, conn_type: str):
        """Record a connection error."""
        if not self.enabled:
            return
            
        self.connection_errors.labels(type=conn_type).inc()


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self):
        self.start_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start_time
        return False