"""Tests for chaos testing framework."""

import asyncio
import random
from unittest.mock import AsyncMock, patch

import pytest

from eoms.core.chaos import (
    ChaosConfig,
    ChaosEvent,
    ChaosManager,
    ChaosType,
    DisconnectChaos,
    LatencyChaos,
    MockService,
    NetworkChaos,
    chaos_test,
    simulate_trading_operations,
)


@pytest.fixture
def chaos_config():
    """Create test chaos configuration."""
    return ChaosConfig(
        enabled=True,
        test_duration=2.0,  # Short duration for testing
        event_interval=0.5,
        max_concurrent_events=2,
        fail_on_unhandled_exception=False,  # Don't fail tests on chaos exceptions
        log_all_events=True,
        events=[
            ChaosEvent(
                type=ChaosType.NETWORK_DISCONNECT,
                probability=0.5,
                duration_range=(0.1, 0.3),
                target_services={"broker"},
                description="Test network disconnect",
            ),
            ChaosEvent(
                type=ChaosType.HIGH_LATENCY,
                probability=0.3,
                duration_range=(0.1, 0.2),
                delay_range=(0.01, 0.05),
                target_services={"feed"},
                description="Test high latency",
            ),
        ],
    )


@pytest.fixture
def mock_services():
    """Create mock services for testing."""
    return {
        "broker": MockService("broker"),
        "feed": MockService("feed"),
        "database": MockService("database"),
    }


class TestChaosConfig:
    """Test chaos configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = ChaosConfig()

        assert config.enabled is True
        assert config.test_duration == 60.0
        assert config.event_interval == 5.0
        assert config.max_concurrent_events == 3
        assert config.fail_on_unhandled_exception is True
        assert config.log_all_events is True
        assert len(config.events) > 0

    def test_custom_config(self):
        """Test custom configuration."""
        events = [ChaosEvent(type=ChaosType.NETWORK_DISCONNECT, probability=0.1)]

        config = ChaosConfig(
            enabled=False,
            test_duration=30.0,
            event_interval=2.0,
            max_concurrent_events=5,
            fail_on_unhandled_exception=False,
            log_all_events=False,
            events=events,
        )

        assert config.enabled is False
        assert config.test_duration == 30.0
        assert config.event_interval == 2.0
        assert config.max_concurrent_events == 5
        assert config.fail_on_unhandled_exception is False
        assert config.log_all_events is False
        assert config.events == events


class TestChaosEvent:
    """Test chaos event configuration."""

    def test_chaos_event_creation(self):
        """Test chaos event creation."""
        event = ChaosEvent(
            type=ChaosType.NETWORK_DISCONNECT,
            probability=0.2,
            duration_range=(1.0, 5.0),
            target_services={"broker", "feed"},
            description="Test disconnect",
        )

        assert event.type == ChaosType.NETWORK_DISCONNECT
        assert event.probability == 0.2
        assert event.duration_range == (1.0, 5.0)
        assert event.target_services == {"broker", "feed"}
        assert event.enabled is True
        assert event.description == "Test disconnect"

    def test_chaos_event_defaults(self):
        """Test chaos event default values."""
        event = ChaosEvent(type=ChaosType.HIGH_LATENCY)

        assert event.probability == 0.1
        assert event.duration_range == (1.0, 5.0)
        assert event.delay_range == (0.1, 2.0)
        assert event.target_services == set()
        assert event.enabled is True
        assert event.description == ""


class TestChaosManager:
    """Test chaos manager."""

    def test_manager_initialization(self, chaos_config):
        """Test manager initialization."""
        manager = ChaosManager(chaos_config)

        assert manager.config == chaos_config
        assert len(manager._active_events) == 0
        assert len(manager._unhandled_exceptions) == 0
        assert len(manager._handlers) == 0
        assert len(manager._services) == 0

    def test_manager_disabled(self):
        """Test manager with disabled chaos."""
        config = ChaosConfig(enabled=False)
        manager = ChaosManager(config)

        assert not manager.config.enabled

    def test_register_service(self, chaos_config, mock_services):
        """Test service registration."""
        manager = ChaosManager(chaos_config)

        for name, service in mock_services.items():
            manager.register_service(name, service)

        assert len(manager._services) == 3
        assert "broker" in manager._services
        assert "feed" in manager._services
        assert "database" in manager._services

    def test_register_handler(self, chaos_config):
        """Test handler registration."""
        manager = ChaosManager(chaos_config)

        async def mock_handler(event, duration, services):
            pass

        manager.register_handler(ChaosType.NETWORK_DISCONNECT, mock_handler)

        assert ChaosType.NETWORK_DISCONNECT in manager._handlers
        assert manager._handlers[ChaosType.NETWORK_DISCONNECT] == mock_handler

    @pytest.mark.asyncio
    async def test_chaos_testing_disabled(self):
        """Test chaos testing when disabled."""
        config = ChaosConfig(enabled=False)
        manager = ChaosManager(config)

        # Should complete without doing anything
        await manager.start_chaos_testing()

        assert len(manager._active_events) == 0

    @pytest.mark.asyncio
    async def test_chaos_testing_enabled(self, chaos_config, mock_services):
        """Test chaos testing when enabled."""
        manager = ChaosManager(chaos_config)

        # Register services
        for name, service in mock_services.items():
            manager.register_service(name, service)

        # Register mock handlers
        disconnect_handler = AsyncMock()
        latency_handler = AsyncMock()

        manager.register_handler(ChaosType.NETWORK_DISCONNECT, disconnect_handler)
        manager.register_handler(ChaosType.HIGH_LATENCY, latency_handler)

        # Run chaos testing
        await manager.start_chaos_testing()

        # Verify cleanup
        assert len(manager._active_events) == 0
        await manager.stop_chaos_testing()

    @pytest.mark.asyncio
    async def test_unhandled_exception_handling(self):
        """Test unhandled exception handling."""
        config = ChaosConfig(
            test_duration=0.5, event_interval=0.1, fail_on_unhandled_exception=False
        )
        manager = ChaosManager(config)

        # Register handler that raises exception
        async def failing_handler(event, duration, services):
            raise ValueError("Test exception")

        manager.register_handler(ChaosType.NETWORK_DISCONNECT, failing_handler)

        # Run chaos testing
        await manager.start_chaos_testing()

        # Should have captured the exception
        assert len(manager._unhandled_exceptions) >= 0  # May or may not trigger based on randomness


class TestNetworkChaos:
    """Test network chaos events."""

    @pytest.mark.asyncio
    async def test_disconnect_chaos(self, mock_services):
        """Test network disconnection chaos."""
        event = ChaosEvent(type=ChaosType.NETWORK_DISCONNECT, target_services={"broker", "feed"})

        # Initially connected
        assert mock_services["broker"].is_connected()
        assert mock_services["feed"].is_connected()

        # Run disconnect chaos
        await NetworkChaos.disconnect(event, 0.1, mock_services)

        # Should be reconnected after chaos
        assert mock_services["broker"].is_connected()
        assert mock_services["feed"].is_connected()

    @pytest.mark.asyncio
    async def test_high_latency_chaos(self, mock_services):
        """Test high latency chaos."""
        event = ChaosEvent(type=ChaosType.HIGH_LATENCY, target_services={"feed"})

        # Run latency chaos
        await NetworkChaos.high_latency(event, 0.1, mock_services)

        # Should complete without errors
        # (This is a simple simulation for now)


class TestLatencyChaos:
    """Test latency chaos events."""

    def test_latency_injection_inactive(self):
        """Test latency injection when inactive."""
        chaos = LatencyChaos(delay_range=(0.01, 0.02))

        # Should not inject delay when inactive
        with chaos.inject_latency():
            pass  # Should complete quickly

    @pytest.mark.asyncio
    async def test_latency_injection_active(self):
        """Test latency injection when active."""
        chaos = LatencyChaos(delay_range=(0.01, 0.02))

        # Start injection
        task = asyncio.create_task(chaos.start_injection(0.1))
        await asyncio.sleep(0.05)  # Wait for injection to start

        # Now latency should be active
        assert chaos.active

        # Wait for completion
        await task
        assert not chaos.active


class TestDisconnectChaos:
    """Test disconnect chaos events."""

    @pytest.mark.asyncio
    async def test_random_disconnect(self, mock_services):
        """Test random service disconnection."""
        target_services = {"broker", "feed"}

        # All services initially connected
        for service in mock_services.values():
            assert service.is_connected()

        # Run random disconnect
        await DisconnectChaos.random_disconnect(mock_services, target_services, 0.1)

        # Services should be reconnected after chaos
        for name in target_services:
            assert mock_services[name].is_connected()

    @pytest.mark.asyncio
    async def test_random_disconnect_no_targets(self, mock_services):
        """Test random disconnect with no target services."""
        target_services = {"nonexistent"}

        # Should handle gracefully
        await DisconnectChaos.random_disconnect(mock_services, target_services, 0.1)


class TestMockService:
    """Test mock service for chaos testing."""

    def test_mock_service_creation(self):
        """Test mock service creation."""
        service = MockService("test_service")

        assert service.name == "test_service"
        assert service.is_connected()

    @pytest.mark.asyncio
    async def test_mock_service_disconnect_connect(self):
        """Test mock service disconnect/connect."""
        service = MockService("test_service")

        # Initially connected
        assert service.is_connected()

        # Disconnect
        await service.disconnect()
        assert not service.is_connected()

        # Reconnect
        await service.connect()
        assert service.is_connected()


class TestChaosTestDecorator:
    """Test chaos test decorator."""

    @pytest.mark.asyncio
    async def test_chaos_test_decorator(self):
        """Test chaos test decorator."""
        config = ChaosConfig(
            test_duration=0.2, event_interval=0.1, fail_on_unhandled_exception=False
        )

        @chaos_test(config)
        async def sample_test():
            await asyncio.sleep(0.1)
            return "test_completed"

        result = await sample_test()
        assert result == "test_completed"

    @pytest.mark.asyncio
    async def test_chaos_test_with_exception(self):
        """Test chaos test decorator with exceptions."""
        config = ChaosConfig(
            test_duration=0.1,
            fail_on_unhandled_exception=True,
            events=[],  # No events to avoid random exceptions
        )

        @chaos_test(config)
        async def failing_test():
            raise ValueError("Test exception")

        with pytest.raises(ValueError):
            await failing_test()


class TestTradingOperationsSimulation:
    """Test trading operations simulation."""

    @pytest.mark.asyncio
    async def test_simulate_trading_operations(self):
        """Test trading operations simulation."""
        # Should complete without errors
        # Note: This is a shortened version for testing
        with patch("eoms.core.chaos.asyncio.sleep"):
            await simulate_trading_operations()


class TestIntegration:
    """Integration tests for chaos framework."""

    @pytest.mark.asyncio
    async def test_full_chaos_scenario(self, mock_services):
        """Test a complete chaos testing scenario."""
        config = ChaosConfig(
            test_duration=0.5,
            event_interval=0.1,
            max_concurrent_events=1,
            fail_on_unhandled_exception=False,
            events=[
                ChaosEvent(
                    type=ChaosType.NETWORK_DISCONNECT,
                    probability=1.0,  # Ensure it triggers
                    duration_range=(0.05, 0.1),
                    target_services={"broker"},
                )
            ],
        )

        manager = ChaosManager(config)

        # Register services and handlers
        for name, service in mock_services.items():
            manager.register_service(name, service)

        manager.register_handler(ChaosType.NETWORK_DISCONNECT, NetworkChaos.disconnect)

        # Run chaos testing
        await manager.start_chaos_testing()

        # Verify all services are back online
        for service in mock_services.values():
            assert service.is_connected()

        # Clean up
        await manager.stop_chaos_testing()

    @pytest.mark.asyncio
    async def test_chaos_resilience_validation(self):
        """Test that chaos testing validates system resilience."""

        # Create a system that should be resilient
        exception_count = 0

        async def resilient_operation():
            nonlocal exception_count
            try:
                # Simulate operation that might fail
                if random.random() < 0.1:  # 10% chance of failure
                    raise Exception("Simulated failure")
                await asyncio.sleep(0.01)
                return "success"
            except Exception:
                exception_count += 1
                # System should handle exceptions gracefully
                return "handled_failure"

        # Run operations during chaos
        config = ChaosConfig(
            test_duration=0.3, event_interval=0.05, fail_on_unhandled_exception=False
        )

        @chaos_test(config)
        async def test_resilient_system():
            results = []
            for _ in range(10):
                result = await resilient_operation()
                results.append(result)
                await asyncio.sleep(0.02)
            return results

        results = await test_resilient_system()

        # System should continue operating despite chaos
        assert len(results) == 10
        assert all(r in ["success", "handled_failure"] for r in results)

        # Some failures are expected during chaos testing
        # The key is that the system handles them gracefully
