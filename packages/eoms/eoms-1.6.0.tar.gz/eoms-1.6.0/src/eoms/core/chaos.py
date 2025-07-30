"""Chaos testing framework for EOMS resilience testing.

This module provides tools for testing system resilience by introducing
controlled failures, network issues, and performance degradation.
"""

import asyncio
import logging
import random
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from threading import Event
from typing import Any, Callable, Dict, List, Optional, Set

__all__ = [
    "ChaosConfig",
    "ChaosType",
    "ChaosEvent",
    "ChaosManager",
    "NetworkChaos",
    "LatencyChaos",
    "DisconnectChaos",
    "chaos_test",
]


class ChaosType(Enum):
    """Types of chaos events."""

    NETWORK_DISCONNECT = "network_disconnect"
    HIGH_LATENCY = "high_latency"
    PACKET_LOSS = "packet_loss"
    BROKER_DISCONNECT = "broker_disconnect"
    FEED_DISCONNECT = "feed_disconnect"
    CPU_SPIKE = "cpu_spike"
    MEMORY_PRESSURE = "memory_pressure"
    EXCEPTION_INJECTION = "exception_injection"


@dataclass
class ChaosEvent:
    """Configuration for a chaos event."""

    type: ChaosType
    probability: float = 0.1  # Probability of occurrence (0.0 to 1.0)
    duration_range: tuple = (1.0, 5.0)  # Duration range in seconds
    delay_range: tuple = (0.1, 2.0)  # Delay range for latency injection
    target_services: Set[str] = field(default_factory=set)  # Services to target
    enabled: bool = True
    description: str = ""


@dataclass
class ChaosConfig:
    """Configuration for chaos testing."""

    enabled: bool = True
    test_duration: float = 60.0  # Total test duration in seconds
    event_interval: float = 5.0  # Interval between chaos events
    max_concurrent_events: int = 3  # Maximum concurrent chaos events
    fail_on_unhandled_exception: bool = True
    log_all_events: bool = True

    # Pre-configured chaos events
    events: List[ChaosEvent] = field(
        default_factory=lambda: [
            ChaosEvent(
                type=ChaosType.NETWORK_DISCONNECT,
                probability=0.2,
                duration_range=(2.0, 8.0),
                target_services={"broker", "feed"},
                description="Simulate network disconnection",
            ),
            ChaosEvent(
                type=ChaosType.HIGH_LATENCY,
                probability=0.3,
                duration_range=(3.0, 10.0),
                delay_range=(0.1, 1.0),
                target_services={"broker", "feed"},
                description="Add artificial latency to network calls",
            ),
            ChaosEvent(
                type=ChaosType.BROKER_DISCONNECT,
                probability=0.15,
                duration_range=(1.0, 5.0),
                target_services={"broker"},
                description="Force broker disconnection",
            ),
            ChaosEvent(
                type=ChaosType.FEED_DISCONNECT,
                probability=0.15,
                duration_range=(1.0, 3.0),
                target_services={"feed"},
                description="Force market data feed disconnection",
            ),
        ]
    )


class ChaosManager:
    """Central manager for chaos testing events."""

    def __init__(self, config: Optional[ChaosConfig] = None):
        """Initialize chaos manager.

        Args:
            config: Chaos configuration. Uses defaults if None.
        """
        self.config = config or ChaosConfig()
        self.logger = logging.getLogger(__name__)

        self._active_events: Dict[str, asyncio.Task] = {}
        self._exception_count = 0
        self._unhandled_exceptions: List[Exception] = []
        self._stop_event = Event()
        self._chaos_task: Optional[asyncio.Task] = None

        # Registered chaos handlers
        self._handlers: Dict[ChaosType, Callable] = {}

        # Services registry for targeting
        self._services: Dict[str, Any] = {}

        if not self.config.enabled:
            self.logger.info("Chaos testing disabled")

    def register_service(self, name: str, service: Any) -> None:
        """Register a service for chaos testing.

        Args:
            name: Service name (e.g., "broker", "feed")
            service: Service instance
        """
        self._services[name] = service
        self.logger.debug(f"Registered service '{name}' for chaos testing")

    def register_handler(self, chaos_type: ChaosType, handler: Callable) -> None:
        """Register a handler for a chaos event type.

        Args:
            chaos_type: Type of chaos event
            handler: Async handler function
        """
        self._handlers[chaos_type] = handler
        self.logger.debug(f"Registered handler for {chaos_type.value}")

    async def start_chaos_testing(self) -> None:
        """Start the chaos testing framework."""
        if not self.config.enabled:
            self.logger.info("Chaos testing is disabled")
            return

        self.logger.info(f"Starting chaos testing for {self.config.test_duration}s")
        self._stop_event.clear()

        try:
            self._chaos_task = asyncio.create_task(self._chaos_loop())
            await asyncio.wait_for(self._chaos_task, timeout=self.config.test_duration)
        except asyncio.TimeoutError:
            self.logger.info("Chaos testing completed")
        except Exception as e:
            self.logger.error(f"Chaos testing failed: {e}")
            if self.config.fail_on_unhandled_exception:
                raise
        finally:
            try:
                await self.stop_chaos_testing()
            except RuntimeError as e:
                if "Event loop is closed" in str(e):
                    # Gracefully ignore if event loop is already closed
                    self.logger.debug("Event loop closed during chaos testing cleanup")
                else:
                    raise

    async def stop_chaos_testing(self) -> None:
        """Stop chaos testing and clean up."""
        self.logger.info("Stopping chaos testing")
        self._stop_event.set()

        # Cancel active chaos events
        for _event_id, task in list(self._active_events.items()):
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                except RuntimeError as e:
                    if "Event loop is closed" not in str(e):
                        raise

        self._active_events.clear()

        if self._chaos_task and not self._chaos_task.done():
            self._chaos_task.cancel()
            try:
                await self._chaos_task
            except asyncio.CancelledError:
                pass
            except RuntimeError as e:
                if "Event loop is closed" not in str(e):
                    raise

        self._report_results()

    async def _chaos_loop(self) -> None:
        """Main chaos testing loop."""
        while not self._stop_event.is_set():
            try:
                await self._trigger_random_chaos()
                await asyncio.sleep(self.config.event_interval)
            except Exception as e:
                self._unhandled_exceptions.append(e)
                self.logger.error(f"Unhandled exception in chaos loop: {e}")
                if self.config.fail_on_unhandled_exception:
                    break

    async def _trigger_random_chaos(self) -> None:
        """Trigger a random chaos event."""
        if len(self._active_events) >= self.config.max_concurrent_events:
            return

        # Select enabled events
        enabled_events = [e for e in self.config.events if e.enabled]
        if not enabled_events:
            return

        # Choose event based on probability
        for event in enabled_events:
            if random.random() < event.probability:
                await self._execute_chaos_event(event)
                break

    async def _execute_chaos_event(self, event: ChaosEvent) -> None:
        """Execute a specific chaos event.

        Args:
            event: Chaos event configuration
        """
        event_id = f"{event.type.value}_{int(time.time() * 1000)}"
        duration = random.uniform(*event.duration_range)

        if self.config.log_all_events:
            self.logger.info(
                f"Starting chaos event: {event.description} (duration: {duration:.1f}s)"
            )

        try:
            task = asyncio.create_task(self._run_chaos_event(event, duration))
            self._active_events[event_id] = task
            await task
        except Exception as e:
            self.logger.error(f"Chaos event {event_id} failed: {e}")
            self._unhandled_exceptions.append(e)
        finally:
            self._active_events.pop(event_id, None)

    async def _run_chaos_event(self, event: ChaosEvent, duration: float) -> None:
        """Run a specific chaos event for the given duration.

        Args:
            event: Chaos event configuration
            duration: Duration to run the event
        """
        handler = self._handlers.get(event.type)
        if not handler:
            self.logger.warning(f"No handler registered for {event.type.value}")
            return

        try:
            await handler(event, duration, self._services)
        except Exception as e:
            self.logger.error(f"Chaos event handler failed: {e}")
            raise

    def _report_results(self) -> None:
        """Report chaos testing results."""
        self.logger.info("=== Chaos Testing Results ===")
        self.logger.info(f"Total unhandled exceptions: {len(self._unhandled_exceptions)}")

        if self._unhandled_exceptions:
            self.logger.warning("Unhandled exceptions during chaos testing:")
            for i, exc in enumerate(self._unhandled_exceptions, 1):
                self.logger.warning(f"  {i}. {type(exc).__name__}: {exc}")
        else:
            self.logger.info("✓ No unhandled exceptions - system is resilient!")


class NetworkChaos:
    """Network-related chaos events."""

    @staticmethod
    async def disconnect(event: ChaosEvent, duration: float, services: Dict[str, Any]) -> None:
        """Simulate network disconnection.

        Args:
            event: Chaos event configuration
            duration: Duration of the disconnection
            services: Available services
        """
        logger = logging.getLogger(__name__)

        # Disconnect targeted services
        disconnected_services = []
        for service_name in event.target_services:
            service = services.get(service_name)
            if service and hasattr(service, "disconnect"):
                try:
                    await service.disconnect()
                    disconnected_services.append((service_name, service))
                    logger.info(f"Disconnected {service_name}")
                except Exception as e:
                    logger.error(f"Failed to disconnect {service_name}: {e}")

        # Wait for duration, but ensure cleanup even if cancelled
        try:
            await asyncio.sleep(duration)
        except asyncio.CancelledError:
            logger.info("Chaos disconnect event cancelled, cleaning up...")
            raise
        finally:
            # Always reconnect services, even if cancelled
            for service_name, service in disconnected_services:
                if hasattr(service, "connect"):
                    try:
                        await service.connect()
                        logger.info(f"Reconnected {service_name}")
                    except Exception as e:
                        logger.error(f"Failed to reconnect {service_name}: {e}")

    @staticmethod
    async def high_latency(event: ChaosEvent, duration: float, services: Dict[str, Any]) -> None:
        """Introduce artificial latency.

        Args:
            event: Chaos event configuration
            duration: Duration to maintain high latency
            services: Available services
        """
        logger = logging.getLogger(__name__)
        logger.info(f"Introducing high latency for {duration:.1f}s")

        # This would need integration with actual services to inject delays
        # For now, just simulate the chaos event
        await asyncio.sleep(duration)

        logger.info("High latency simulation completed")


class LatencyChaos:
    """Latency injection chaos events."""

    def __init__(self, delay_range: tuple = (0.1, 1.0)):
        """Initialize latency chaos.

        Args:
            delay_range: Range of delays to inject (min, max) in seconds
        """
        self.delay_range = delay_range
        self.active = False
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def inject_latency(self):
        """Context manager to inject latency in operations."""
        if self.active:
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
        yield

    async def start_injection(self, duration: float) -> None:
        """Start latency injection for specified duration.

        Args:
            duration: Duration to inject latency
        """
        self.active = True
        self.logger.info(f"Starting latency injection for {duration:.1f}s")

        try:
            await asyncio.sleep(duration)
        finally:
            self.active = False
            self.logger.info("Latency injection completed")


class DisconnectChaos:
    """Service disconnection chaos events."""

    @staticmethod
    async def random_disconnect(
        services: Dict[str, Any], target_services: Set[str], duration: float
    ) -> None:
        """Randomly disconnect services for a duration.

        Args:
            services: Available services
            target_services: Services to potentially disconnect
            duration: Duration of disconnection
        """
        logger = logging.getLogger(__name__)

        # Select random service to disconnect
        available_targets = [name for name in target_services if name in services]
        if not available_targets:
            logger.warning("No target services available for disconnection")
            return

        target = random.choice(available_targets)
        service = services[target]

        if not hasattr(service, "disconnect") or not hasattr(service, "connect"):
            logger.warning(f"Service {target} doesn't support disconnect/connect")
            return

        try:
            # Disconnect
            await service.disconnect()
            logger.info(f"Chaos: Disconnected {target}")

            # Wait, but ensure cleanup even if cancelled
            try:
                await asyncio.sleep(duration)
            except asyncio.CancelledError:
                logger.info("Chaos disconnect event cancelled, cleaning up...")
                raise
            finally:
                # Always reconnect, even if cancelled
                await service.connect()
                logger.info(f"Chaos: Reconnected {target}")

        except Exception as e:
            logger.error(f"Chaos disconnect failed for {target}: {e}")
            raise


def chaos_test(config: Optional[ChaosConfig] = None):
    """Decorator for running chaos tests.

    Args:
        config: Chaos testing configuration

    Example:
        @chaos_test(ChaosConfig(test_duration=30.0))
        async def test_system_resilience():
            # Your test code here
            pass
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            manager = ChaosManager(config)

            # Register default handlers
            manager.register_handler(ChaosType.NETWORK_DISCONNECT, NetworkChaos.disconnect)
            manager.register_handler(ChaosType.HIGH_LATENCY, NetworkChaos.high_latency)

            # Start chaos testing in background
            asyncio.create_task(manager.start_chaos_testing())

            try:
                # Run the actual test
                result = await func(*args, **kwargs)
                return result
            finally:
                # Stop chaos testing
                await manager.stop_chaos_testing()

                # Check for unhandled exceptions
                if manager._unhandled_exceptions and config and config.fail_on_unhandled_exception:
                    unhandled_count = len(manager._unhandled_exceptions)
                    raise Exception(
                        f"Chaos testing revealed {unhandled_count} unhandled exceptions"
                    )

        return wrapper

    return decorator


# Example usage functions for testing
async def simulate_trading_operations():
    """Simulate normal trading operations during chaos testing."""
    logger = logging.getLogger(__name__)

    for i in range(10):
        try:
            # Simulate order placement
            logger.info(f"Placing order {i+1}")
            await asyncio.sleep(0.1)

            # Simulate fill processing
            logger.info(f"Processing fill for order {i+1}")
            await asyncio.sleep(0.05)

        except Exception as e:
            logger.error(f"Trading operation failed: {e}")
            # Continue with next operation - test resilience

        await asyncio.sleep(1.0)


class MockService:
    """Mock service for chaos testing."""

    def __init__(self, name: str):
        self.name = name
        self.connected = True
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """Connect the service."""
        self.connected = True
        self.logger.info(f"Mock {self.name} connected")

    async def disconnect(self):
        """Disconnect the service."""
        self.connected = False
        self.logger.info(f"Mock {self.name} disconnected")

    def is_connected(self) -> bool:
        """Check if service is connected."""
        return self.connected
