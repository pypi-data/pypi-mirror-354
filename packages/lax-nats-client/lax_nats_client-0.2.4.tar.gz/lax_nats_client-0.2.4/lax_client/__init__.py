"""LAX NATS JetStream Python Client SDK

A high-performance client SDK with intelligent routing between direct NATS 
(for ultra-low latency) and gRPC (for advanced features).
"""

from .client import LaxClient
from .options import ClientOptions, PublishOptions, SubscribeOptions, ConsumerGroupConfig, Tier
from .message import Message
from .exceptions import (
    LaxClientError,
    ConnectionError,
    PublishError,
    CircuitBreakerOpen,
)

__version__ = "0.2.4"
__all__ = [
    "LaxClient",
    "ClientOptions",
    "PublishOptions",
    "SubscribeOptions",
    "ConsumerGroupConfig",
    "Tier",
    "Message",
    "LaxClientError",
    "ConnectionError",
    "PublishError",
    "CircuitBreakerOpen",
]