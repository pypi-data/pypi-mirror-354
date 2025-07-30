"""
Global Circuit Breaker for EOMS.

Provides circuit breaker functionality to prevent event-loop starvation
during error surges and maintain system stability.
"""

import asyncio
import logging
import time
from enum import Enum
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"  # Circuit is open, blocking operations
    HALF_OPEN = "HALF_OPEN"  # Testing if circuit can be closed


class CircuitBreakerError(Exception):
    """Raised when circuit breaker is open."""

    pass


class CircuitBreaker:
    """
    Circuit breaker implementation to prevent system overload.

    Features:
    - Configurable failure threshold and timeout
    - State transitions: CLOSED -> OPEN -> HALF_OPEN -> CLOSED
    - Automatic recovery attempts
    - Metrics collection for monitoring
    - Event-loop starvation prevention
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: type = Exception,
        half_open_max_calls: int = 1,
    ):
        """
        Initialize circuit breaker.

        Args:
            name: Name of the circuit breaker for identification
            failure_threshold: Number of failures before opening circuit
            timeout: Time in seconds before attempting to close circuit
            expected_exception: Exception type that counts as a failure
            half_open_max_calls: Max calls allowed in HALF_OPEN state
        """
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.half_open_max_calls = half_open_max_calls

        # State tracking
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_call_count = 0

        # Metrics
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0
        self.state_transitions = {state: 0 for state in CircuitState}

        # Timing metrics
        self.last_state_change_time = time.time()
        self.time_in_states = {state: 0.0 for state in CircuitState}

        logger.info(f"Circuit breaker '{name}' initialized")

    def __call__(self, func: Callable) -> Callable:
        """Decorator to wrap functions with circuit breaker."""
        if asyncio.iscoroutinefunction(func):

            async def async_wrapper(*args, **kwargs):
                return await self.call_async(func, *args, **kwargs)

            return async_wrapper
        else:

            def sync_wrapper(*args, **kwargs):
                return self.call_sync(func, *args, **kwargs)

            return sync_wrapper

    async def call_async(self, func: Callable, *args, **kwargs) -> Any:
        """Execute an async function with circuit breaker protection."""
        self._check_circuit()

        try:
            self.total_calls += 1

            # Yield control to prevent event loop starvation
            await asyncio.sleep(0)

            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception:
            self._on_failure()
            raise
        except Exception as e:
            # Unexpected exceptions don't count as failures
            logger.warning(f"Unexpected exception in {self.name}: {e}")
            raise

    def call_sync(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a sync function with circuit breaker protection."""
        self._check_circuit()

        try:
            self.total_calls += 1
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except self.expected_exception:
            self._on_failure()
            raise
        except Exception as e:
            # Unexpected exceptions don't count as failures
            logger.warning(f"Unexpected exception in {self.name}: {e}")
            raise

    def _check_circuit(self) -> None:
        """Check circuit state and update if necessary."""
        current_time = time.time()

        if self.state == CircuitState.OPEN:
            # Check if we should transition to HALF_OPEN
            if current_time - self.last_failure_time >= self.timeout:
                self._transition_to(CircuitState.HALF_OPEN)
            else:
                raise CircuitBreakerError(
                    f"Circuit breaker '{self.name}' is OPEN. "
                    f"Retry after {self.timeout - (current_time - self.last_failure_time):.1f}s"
                )

        elif self.state == CircuitState.HALF_OPEN:
            # Check if we've exceeded half-open call limit
            if self.half_open_call_count >= self.half_open_max_calls:
                raise CircuitBreakerError(
                    f"Circuit breaker '{self.name}' is HALF_OPEN and at call limit"
                )

    def _on_success(self) -> None:
        """Handle successful operation."""
        self.total_successes += 1

        if self.state == CircuitState.HALF_OPEN:
            self.half_open_call_count += 1
            # After successful calls in HALF_OPEN, close the circuit
            self._transition_to(CircuitState.CLOSED)

        # Reset failure count on success
        self.failure_count = 0

    def _on_failure(self) -> None:
        """Handle failed operation."""
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            # Failure in HALF_OPEN state opens the circuit again
            self.half_open_call_count = 0
            self._transition_to(CircuitState.OPEN)

        elif self.state == CircuitState.CLOSED:
            # Check if we should open the circuit
            if self.failure_count >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)

    def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new circuit state."""
        current_time = time.time()

        # Update time spent in previous state
        time_in_previous_state = current_time - self.last_state_change_time
        self.time_in_states[self.state] += time_in_previous_state

        old_state = self.state
        self.state = new_state
        self.last_state_change_time = current_time

        # Update transition counter
        self.state_transitions[new_state] += 1

        # Reset counters based on new state
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.half_open_call_count = 0
        elif new_state == CircuitState.HALF_OPEN:
            self.half_open_call_count = 0

        logger.info(
            f"Circuit breaker '{self.name}' transitioned: {old_state.value} -> {new_state.value}"
        )

    def force_open(self) -> None:
        """Force the circuit breaker to OPEN state."""
        self.last_failure_time = time.time()
        self._transition_to(CircuitState.OPEN)
        logger.warning(f"Circuit breaker '{self.name}' forced OPEN")

    def force_close(self) -> None:
        """Force the circuit breaker to CLOSED state."""
        self._transition_to(CircuitState.CLOSED)
        logger.info(f"Circuit breaker '{self.name}' forced CLOSED")

    def reset(self) -> None:
        """Reset circuit breaker to initial state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_call_count = 0

        # Reset metrics
        self.total_calls = 0
        self.total_failures = 0
        self.total_successes = 0

        logger.info(f"Circuit breaker '{self.name}' reset")

    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics."""
        current_time = time.time()

        # Update time in current state
        time_in_current_state = current_time - self.last_state_change_time
        self.time_in_states[self.state] + time_in_current_state

        success_rate = 0.0
        if self.total_calls > 0:
            success_rate = (self.total_successes / self.total_calls) * 100

        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "total_calls": self.total_calls,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "success_rate_percent": success_rate,
            "state_transitions": self.state_transitions.copy(),
            "time_in_states": {
                state.value: duration + (time_in_current_state if state == self.state else 0)
                for state, duration in self.time_in_states.items()
            },
            "last_failure_time": self.last_failure_time,
            "timeout": self.timeout,
        }


class GlobalCircuitBreakerManager:
    """
    Global manager for circuit breakers in the EOMS system.

    Provides centralized circuit breaker management to prevent
    event-loop starvation and coordinate system-wide error handling.
    """

    def __init__(self):
        """Initialize global circuit breaker manager."""
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.global_error_threshold = 100  # Errors per minute
        self.global_error_window = 60.0  # 1 minute window
        self.global_error_count = 0
        self.global_error_timestamps: list[float] = []

        logger.info("Global circuit breaker manager initialized")

    def create_circuit_breaker(
        self,
        name: str,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: type = Exception,
        half_open_max_calls: int = 1,
    ) -> CircuitBreaker:
        """Create and register a new circuit breaker."""
        if name in self.circuit_breakers:
            raise ValueError(f"Circuit breaker '{name}' already exists")

        circuit_breaker = CircuitBreaker(
            name=name,
            failure_threshold=failure_threshold,
            timeout=timeout,
            expected_exception=expected_exception,
            half_open_max_calls=half_open_max_calls,
        )

        self.circuit_breakers[name] = circuit_breaker
        logger.info(f"Created circuit breaker '{name}'")

        return circuit_breaker

    def get_circuit_breaker(self, name: str) -> Optional[CircuitBreaker]:
        """Get an existing circuit breaker by name."""
        return self.circuit_breakers.get(name)

    def remove_circuit_breaker(self, name: str) -> bool:
        """Remove a circuit breaker."""
        if name in self.circuit_breakers:
            del self.circuit_breakers[name]
            logger.info(f"Removed circuit breaker '{name}'")
            return True
        return False

    def record_global_error(self) -> None:
        """Record a global error and check for error surge."""
        current_time = time.time()
        self.global_error_count += 1
        self.global_error_timestamps.append(current_time)

        # Clean old timestamps outside the window
        cutoff_time = current_time - self.global_error_window
        self.global_error_timestamps = [
            ts for ts in self.global_error_timestamps if ts > cutoff_time
        ]

        # Check for error surge
        errors_in_window = len(self.global_error_timestamps)
        if errors_in_window >= self.global_error_threshold:
            logger.critical(
                f"Global error surge detected: {errors_in_window} errors "
                f"in {self.global_error_window}s window"
            )
            self._handle_error_surge()

    def _handle_error_surge(self) -> None:
        """Handle global error surge by opening all circuit breakers."""
        logger.warning("Opening all circuit breakers due to error surge")

        for circuit_breaker in self.circuit_breakers.values():
            if circuit_breaker.state != CircuitState.OPEN:
                circuit_breaker.force_open()

    def get_global_stats(self) -> Dict[str, Any]:
        """Get global circuit breaker statistics."""
        current_time = time.time()
        cutoff_time = current_time - self.global_error_window

        recent_errors = len([ts for ts in self.global_error_timestamps if ts > cutoff_time])

        circuit_stats = {}
        for name, cb in self.circuit_breakers.items():
            circuit_stats[name] = cb.get_stats()

        return {
            "total_circuit_breakers": len(self.circuit_breakers),
            "global_error_count": self.global_error_count,
            "recent_errors": recent_errors,
            "error_threshold": self.global_error_threshold,
            "error_window_seconds": self.global_error_window,
            "circuit_breakers": circuit_stats,
        }

    def reset_all(self) -> None:
        """Reset all circuit breakers."""
        for circuit_breaker in self.circuit_breakers.values():
            circuit_breaker.reset()

        self.global_error_count = 0
        self.global_error_timestamps.clear()

        logger.info("Reset all circuit breakers")


# Global instance for system-wide use
global_circuit_breaker_manager = GlobalCircuitBreakerManager()
