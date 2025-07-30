"""Exception classes for LAX client SDK."""


class LaxClientError(Exception):
    """Base exception for all LAX client errors."""
    pass


class ConnectionError(LaxClientError):
    """Raised when connection to NATS or gRPC fails."""
    pass


class PublishError(LaxClientError):
    """Raised when publishing a message fails."""
    pass


class CircuitBreakerOpen(LaxClientError):
    """Raised when circuit breaker is open due to too many failures."""
    pass


class ConfigurationError(LaxClientError):
    """Raised when client configuration is invalid."""
    pass