"""LAX NATS JetStream Python Client SDK

A high-performance client SDK with intelligent routing between direct NATS 
(for ultra-low latency) and gRPC (for advanced features).
"""

from .client import LaxClient, ClientOptions
from .options import PublishOptions, Tier
from .exceptions import (
    LaxClientError,
    ConnectionError,
    PublishError,
    CircuitBreakerOpen,
)

__version__ = "0.1.0"
__all__ = [
    "LaxClient",
    "ClientOptions",
    "PublishOptions",
    "Tier",
    "LaxClientError",
    "ConnectionError",
    "PublishError",
    "CircuitBreakerOpen",
]