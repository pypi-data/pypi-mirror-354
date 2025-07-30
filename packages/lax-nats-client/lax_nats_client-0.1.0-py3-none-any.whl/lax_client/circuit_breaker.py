"""Circuit breaker implementation for fault tolerance."""

import asyncio
import time
from enum import Enum
from typing import Optional, Callable
from dataclasses import dataclass, field
import logging


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """Async circuit breaker for fault tolerance."""
    
    failure_threshold: int = 10
    timeout: float = 30.0  # seconds
    half_open_requests: int = 3
    
    _state: CircuitState = field(default=CircuitState.CLOSED, init=False)
    _failure_count: int = field(default=0, init=False)
    _last_failure_time: Optional[float] = field(default=None, init=False)
    _half_open_count: int = field(default=0, init=False)
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, init=False)
    
    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute a function with circuit breaker protection."""
        async with self._lock:
            if self._state == CircuitState.OPEN:
                if await self._should_attempt_reset():
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_count = 0
                    self.logger.info("Circuit breaker entering half-open state")
                else:
                    raise CircuitBreakerOpen("Circuit breaker is open")
        
        try:
            # Execute the function
            result = await func(*args, **kwargs)
            
            # Success - update state
            async with self._lock:
                if self._state == CircuitState.HALF_OPEN:
                    self._half_open_count += 1
                    if self._half_open_count >= self.half_open_requests:
                        self._state = CircuitState.CLOSED
                        self._failure_count = 0
                        self.logger.info("Circuit breaker closed after successful recovery")
                elif self._state == CircuitState.CLOSED:
                    self._failure_count = 0
            
            return result
            
        except Exception as e:
            # Failure - update state
            async with self._lock:
                self._failure_count += 1
                self._last_failure_time = time.time()
                
                if self._state == CircuitState.HALF_OPEN:
                    self._state = CircuitState.OPEN
                    self.logger.warning("Circuit breaker reopened due to failure in half-open state")
                elif self._failure_count >= self.failure_threshold:
                    self._state = CircuitState.OPEN
                    self.logger.warning(f"Circuit breaker opened after {self._failure_count} failures")
            
            raise e
    
    async def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self._last_failure_time is None:
            return True
        
        elapsed = time.time() - self._last_failure_time
        return elapsed >= self.timeout
    
    @property
    def state(self) -> CircuitState:
        """Get current circuit breaker state."""
        return self._state
    
    @property
    def is_open(self) -> bool:
        """Check if circuit breaker is open."""
        return self._state == CircuitState.OPEN
    
    @property
    def is_closed(self) -> bool:
        """Check if circuit breaker is closed."""
        return self._state == CircuitState.CLOSED
    
    async def reset(self):
        """Manually reset the circuit breaker."""
        async with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_failure_time = None
            self._half_open_count = 0
            self.logger.info("Circuit breaker manually reset")


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open."""
    pass