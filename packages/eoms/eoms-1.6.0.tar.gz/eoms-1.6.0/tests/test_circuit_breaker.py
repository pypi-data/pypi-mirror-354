"""Tests for circuit breaker functionality."""

import asyncio
import time

import pytest

from eoms.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitState,
    GlobalCircuitBreakerManager,
)


class CircuitBreakerTestException(Exception):
    """Test exception for circuit breaker testing."""

    pass


class TestCircuitBreaker:
    """Test cases for CircuitBreaker functionality."""

    @pytest.fixture
    def circuit_breaker(self):
        """Create a circuit breaker for testing."""
        return CircuitBreaker(
            name="test_breaker",
            failure_threshold=3,
            timeout=1.0,
            expected_exception=CircuitBreakerTestException,
            half_open_max_calls=1,
        )

    def test_circuit_breaker_creation(self, circuit_breaker):
        """Test circuit breaker creation."""
        assert circuit_breaker.name == "test_breaker"
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.failure_threshold == 3
        assert circuit_breaker.timeout == 1.0
        assert circuit_breaker.failure_count == 0

    def test_successful_operation(self, circuit_breaker):
        """Test successful operation in CLOSED state."""

        def test_func():
            return "success"

        result = circuit_breaker.call_sync(test_func)
        assert result == "success"
        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.total_calls == 1
        assert circuit_breaker.total_successes == 1
        assert circuit_breaker.failure_count == 0

    def test_failure_operation(self, circuit_breaker):
        """Test failed operation in CLOSED state."""

        def test_func():
            raise CircuitBreakerTestException("test failure")

        with pytest.raises(CircuitBreakerTestException):
            circuit_breaker.call_sync(test_func)

        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.total_calls == 1
        assert circuit_breaker.total_failures == 1
        assert circuit_breaker.failure_count == 1

    def test_circuit_opens_after_threshold(self, circuit_breaker):
        """Test that circuit opens after failure threshold."""

        def failing_func():
            raise CircuitBreakerTestException("failure")

        # Trigger failures up to threshold
        for _i in range(circuit_breaker.failure_threshold):
            with pytest.raises(CircuitBreakerTestException):
                circuit_breaker.call_sync(failing_func)

        # Circuit should now be OPEN
        assert circuit_breaker.state == CircuitState.OPEN

        # Next call should raise CircuitBreakerError
        with pytest.raises(CircuitBreakerError):
            circuit_breaker.call_sync(failing_func)

    def test_circuit_half_open_after_timeout(self, circuit_breaker):
        """Test circuit transitions to HALF_OPEN after timeout."""

        def failing_func():
            raise CircuitBreakerTestException("failure")

        # Open the circuit
        for _i in range(circuit_breaker.failure_threshold):
            with pytest.raises(CircuitBreakerTestException):
                circuit_breaker.call_sync(failing_func)

        assert circuit_breaker.state == CircuitState.OPEN

        # Wait for timeout
        time.sleep(circuit_breaker.timeout + 0.1)

        # Check circuit state - should transition to HALF_OPEN on next call
        def success_func():
            return "success"

        result = circuit_breaker.call_sync(success_func)
        assert result == "success"
        assert circuit_breaker.state == CircuitState.CLOSED  # Should close after success

    def test_half_open_success_closes_circuit(self, circuit_breaker):
        """Test that success in HALF_OPEN state closes circuit."""
        # Force circuit to HALF_OPEN
        circuit_breaker.state = CircuitState.HALF_OPEN
        circuit_breaker.last_failure_time = time.time() - circuit_breaker.timeout - 1

        def success_func():
            return "success"

        result = circuit_breaker.call_sync(success_func)
        assert result == "success"
        assert circuit_breaker.state == CircuitState.CLOSED

    def test_half_open_failure_opens_circuit(self, circuit_breaker):
        """Test that failure in HALF_OPEN state opens circuit."""
        # Force circuit to HALF_OPEN
        circuit_breaker.state = CircuitState.HALF_OPEN
        circuit_breaker.last_failure_time = time.time() - circuit_breaker.timeout - 1

        def failing_func():
            raise CircuitBreakerTestException("failure")

        with pytest.raises(CircuitBreakerTestException):
            circuit_breaker.call_sync(failing_func)

        assert circuit_breaker.state == CircuitState.OPEN

    @pytest.mark.asyncio
    async def test_async_function_protection(self, circuit_breaker):
        """Test circuit breaker with async functions."""

        async def async_func():
            await asyncio.sleep(0.01)
            return "async_success"

        result = await circuit_breaker.call_async(async_func)
        assert result == "async_success"
        assert circuit_breaker.total_calls == 1
        assert circuit_breaker.total_successes == 1

    @pytest.mark.asyncio
    async def test_async_function_failure(self, circuit_breaker):
        """Test circuit breaker with async function failures."""

        async def async_failing_func():
            await asyncio.sleep(0.01)
            raise CircuitBreakerTestException("async failure")

        with pytest.raises(CircuitBreakerTestException):
            await circuit_breaker.call_async(async_failing_func)

        assert circuit_breaker.total_calls == 1
        assert circuit_breaker.total_failures == 1

    def test_decorator_usage(self, circuit_breaker):
        """Test using circuit breaker as a decorator."""

        @circuit_breaker
        def decorated_func(value):
            if value == "fail":
                raise CircuitBreakerTestException("decorated failure")
            return f"decorated_{value}"

        # Test success
        result = decorated_func("success")
        assert result == "decorated_success"

        # Test failure
        with pytest.raises(CircuitBreakerTestException):
            decorated_func("fail")

        assert circuit_breaker.total_calls == 2
        assert circuit_breaker.total_successes == 1
        assert circuit_breaker.total_failures == 1

    @pytest.mark.asyncio
    async def test_async_decorator_usage(self, circuit_breaker):
        """Test using circuit breaker as a decorator with async functions."""

        @circuit_breaker
        async def async_decorated_func(value):
            await asyncio.sleep(0.01)
            if value == "fail":
                raise CircuitBreakerTestException("async decorated failure")
            return f"async_decorated_{value}"

        # Test success
        result = await async_decorated_func("success")
        assert result == "async_decorated_success"

        # Test failure
        with pytest.raises(CircuitBreakerTestException):
            await async_decorated_func("fail")

        assert circuit_breaker.total_calls == 2
        assert circuit_breaker.total_successes == 1
        assert circuit_breaker.total_failures == 1

    def test_force_open_close(self, circuit_breaker):
        """Test forcing circuit open and closed."""
        assert circuit_breaker.state == CircuitState.CLOSED

        # Force open
        circuit_breaker.force_open()
        assert circuit_breaker.state == CircuitState.OPEN

        # Force close
        circuit_breaker.force_close()
        assert circuit_breaker.state == CircuitState.CLOSED

    def test_reset_functionality(self, circuit_breaker):
        """Test circuit breaker reset."""

        # Trigger some activity
        def test_func():
            return "test"

        circuit_breaker.call_sync(test_func)
        circuit_breaker.failure_count = 2

        assert circuit_breaker.total_calls == 1
        assert circuit_breaker.failure_count == 2

        # Reset
        circuit_breaker.reset()

        assert circuit_breaker.state == CircuitState.CLOSED
        assert circuit_breaker.total_calls == 0
        assert circuit_breaker.failure_count == 0
        assert circuit_breaker.total_successes == 0
        assert circuit_breaker.total_failures == 0

    def test_statistics_collection(self, circuit_breaker):
        """Test circuit breaker statistics."""

        def success_func():
            return "success"

        def failing_func():
            raise CircuitBreakerTestException("failure")

        # Generate some activity
        circuit_breaker.call_sync(success_func)

        try:
            circuit_breaker.call_sync(failing_func)
        except CircuitBreakerTestException:
            pass

        stats = circuit_breaker.get_stats()

        assert stats["name"] == "test_breaker"
        assert stats["state"] == CircuitState.CLOSED.value
        assert stats["total_calls"] == 2
        assert stats["total_successes"] == 1
        assert stats["total_failures"] == 1
        assert stats["success_rate_percent"] == 50.0
        assert stats["failure_threshold"] == 3

    def test_unexpected_exception_handling(self, circuit_breaker):
        """Test that unexpected exceptions don't count as failures."""

        def unexpected_error_func():
            raise ValueError("unexpected error")  # Not CircuitBreakerTestException

        with pytest.raises(ValueError):
            circuit_breaker.call_sync(unexpected_error_func)

        # Should not count as a failure
        assert circuit_breaker.failure_count == 0
        assert circuit_breaker.total_failures == 0
        assert circuit_breaker.state == CircuitState.CLOSED


class TestGlobalCircuitBreakerManager:
    """Test cases for GlobalCircuitBreakerManager functionality."""

    @pytest.fixture
    def manager(self):
        """Create a fresh manager for testing."""
        return GlobalCircuitBreakerManager()

    def test_manager_creation(self, manager):
        """Test manager creation."""
        assert len(manager.circuit_breakers) == 0
        assert manager.global_error_threshold == 100
        assert manager.global_error_window == 60.0

    def test_create_circuit_breaker(self, manager):
        """Test creating circuit breakers through manager."""
        cb = manager.create_circuit_breaker("test_cb", failure_threshold=5)

        assert cb.name == "test_cb"
        assert cb.failure_threshold == 5
        assert "test_cb" in manager.circuit_breakers
        assert manager.get_circuit_breaker("test_cb") == cb

    def test_duplicate_circuit_breaker_error(self, manager):
        """Test error when creating duplicate circuit breaker."""
        manager.create_circuit_breaker("duplicate")

        with pytest.raises(ValueError, match="already exists"):
            manager.create_circuit_breaker("duplicate")

    def test_remove_circuit_breaker(self, manager):
        """Test removing circuit breakers."""
        manager.create_circuit_breaker("removable")
        assert "removable" in manager.circuit_breakers

        success = manager.remove_circuit_breaker("removable")
        assert success is True
        assert "removable" not in manager.circuit_breakers

        # Remove non-existent
        success = manager.remove_circuit_breaker("nonexistent")
        assert success is False

    def test_global_error_recording(self, manager):
        """Test global error recording and surge detection."""
        # Set low threshold for testing
        manager.global_error_threshold = 3
        manager.global_error_window = 1.0

        # Create test circuit breakers
        cb1 = manager.create_circuit_breaker("cb1")
        cb2 = manager.create_circuit_breaker("cb2")

        # Record errors below threshold
        for _i in range(2):
            manager.record_global_error()

        assert manager.global_error_count == 2
        assert cb1.state == CircuitState.CLOSED
        assert cb2.state == CircuitState.CLOSED

        # Trigger error surge
        manager.record_global_error()

        assert manager.global_error_count == 3
        # Circuit breakers should be opened due to surge
        assert cb1.state == CircuitState.OPEN
        assert cb2.state == CircuitState.OPEN

    def test_global_error_window_cleanup(self, manager):
        """Test that old errors are cleaned up."""
        manager.global_error_window = 0.1  # Very short window for testing

        # Record an error
        manager.record_global_error()
        assert len(manager.global_error_timestamps) == 1

        # Wait for window to expire
        time.sleep(0.2)

        # Record another error (should clean up old one)
        manager.record_global_error()

        # Should only have one recent error
        assert len(manager.global_error_timestamps) == 1
        assert manager.global_error_count == 2  # Total count doesn't decrease

    def test_global_statistics(self, manager):
        """Test global statistics collection."""
        # Create circuit breakers
        manager.create_circuit_breaker("stats_cb1")
        manager.create_circuit_breaker("stats_cb2")

        # Generate some activity
        manager.record_global_error()
        manager.record_global_error()

        stats = manager.get_global_stats()

        assert stats["total_circuit_breakers"] == 2
        assert stats["global_error_count"] == 2
        assert "stats_cb1" in stats["circuit_breakers"]
        assert "stats_cb2" in stats["circuit_breakers"]
        assert stats["error_threshold"] == 100
        assert stats["error_window_seconds"] == 60.0

    def test_reset_all(self, manager):
        """Test resetting all circuit breakers."""
        # Create and activate circuit breakers
        cb1 = manager.create_circuit_breaker("reset_cb1")
        cb2 = manager.create_circuit_breaker("reset_cb2")

        # Generate activity
        manager.record_global_error()
        cb1.failure_count = 2
        cb2.total_calls = 5

        # Reset all
        manager.reset_all()

        assert manager.global_error_count == 0
        assert len(manager.global_error_timestamps) == 0
        assert cb1.failure_count == 0
        assert cb1.total_calls == 0
        assert cb2.total_calls == 0


class TestCircuitBreakerIntegration:
    """Integration tests for circuit breaker functionality."""

    @pytest.mark.asyncio
    async def test_event_loop_starvation_prevention(self):
        """Test that circuit breaker prevents event loop starvation."""
        cb = CircuitBreaker("starvation_test", failure_threshold=10)

        # Create a function that would normally block the event loop
        async def potentially_blocking_func():
            # Circuit breaker should yield control automatically
            return "completed"

        # Run many operations concurrently
        tasks = []
        for _i in range(100):
            task = asyncio.create_task(cb.call_async(potentially_blocking_func))
            tasks.append(task)

        # This should complete without hanging
        results = await asyncio.gather(*tasks)

        assert len(results) == 100
        assert all(result == "completed" for result in results)
        assert cb.total_calls == 100
        assert cb.total_successes == 100

    def test_circuit_breaker_coordination(self):
        """Test coordination between multiple circuit breakers."""
        manager = GlobalCircuitBreakerManager()
        manager.global_error_threshold = 5

        # Create multiple circuit breakers
        cb1 = manager.create_circuit_breaker("service1", failure_threshold=3)
        cb2 = manager.create_circuit_breaker("service2", failure_threshold=3)
        cb3 = manager.create_circuit_breaker("service3", failure_threshold=3)

        # Simulate error surge
        for _i in range(6):  # Exceed global threshold
            manager.record_global_error()

        # All circuit breakers should be opened
        assert cb1.state == CircuitState.OPEN
        assert cb2.state == CircuitState.OPEN
        assert cb3.state == CircuitState.OPEN

        # Verify they prevent further operations
        def test_func():
            return "test"

        with pytest.raises(CircuitBreakerError):
            cb1.call_sync(test_func)

        with pytest.raises(CircuitBreakerError):
            cb2.call_sync(test_func)

        with pytest.raises(CircuitBreakerError):
            cb3.call_sync(test_func)

    def test_real_world_scenario(self):
        """Test a realistic scenario with multiple services and failures."""
        manager = GlobalCircuitBreakerManager()

        # Create circuit breakers for different services
        db_cb = manager.create_circuit_breaker(
            "database",
            failure_threshold=5,
            timeout=30.0,
            expected_exception=ConnectionError,
        )

        api_cb = manager.create_circuit_breaker(
            "external_api",
            failure_threshold=3,
            timeout=60.0,
            expected_exception=TimeoutError,
        )

        # Simulate database operations
        def db_operation():
            # Simulate intermittent database failures
            import random

            if random.random() < 0.3:  # 30% failure rate
                raise ConnectionError("Database connection failed")
            return "db_success"

        def api_operation():
            # Simulate API call
            return "api_success"

        # Run operations and track results
        db_results = []
        api_results = []

        for _i in range(20):
            # Database operations
            try:
                result = db_cb.call_sync(db_operation)
                db_results.append(result)
            except (ConnectionError, CircuitBreakerError):
                db_results.append("failed")

            # API operations (should mostly succeed)
            try:
                result = api_cb.call_sync(api_operation)
                api_results.append(result)
            except (TimeoutError, CircuitBreakerError):
                api_results.append("failed")

        # Database circuit may have opened due to failures
        db_stats = db_cb.get_stats()
        api_stats = api_cb.get_stats()

        print(f"Database circuit breaker stats: {db_stats}")
        print(f"API circuit breaker stats: {api_stats}")

        # API should be mostly successful
        api_success_count = sum(1 for r in api_results if r == "api_success")
        assert api_success_count >= 15  # Most API calls should succeed

        # Verify circuit breaker statistics are collected
        assert db_stats["total_calls"] > 0
        assert api_stats["total_calls"] > 0
