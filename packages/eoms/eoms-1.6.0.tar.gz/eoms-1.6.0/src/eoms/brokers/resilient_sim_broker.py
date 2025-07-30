"""
Resilient simulation broker with auto-reconnect capabilities.

Extends SimBroker with connection resilience for testing auto-reconnect functionality.
"""

import asyncio
import logging
import random
from typing import Any, Dict, Optional

from eoms.brokers.sim_broker import SimBroker
from eoms.core.resilience import AutoReconnectMixin

logger = logging.getLogger(__name__)


class ResilientSimBroker(AutoReconnectMixin, SimBroker):
    """
    Resilient simulation broker with auto-reconnect capabilities.

    This broker extends SimBroker with connection failure simulation
    and auto-reconnect functionality for testing resilience features.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize resilient simulation broker."""
        # Initialize SimBroker first
        SimBroker.__init__(self, config)

        # Initialize AutoReconnectMixin second
        AutoReconnectMixin.__init__(self)

        # Resilience testing configuration
        self._simulate_failures = config.get("simulate_failures", False) if config else False
        self._failure_probability = config.get("failure_probability", 0.1) if config else 0.1
        self._connection_drops = 0
        self._recovery_count = 0

        # Connection simulation state
        self._simulated_connection_lost = False

        # Set up callbacks for testing
        self.add_connection_lost_callback(self._on_connection_lost)
        self.add_connection_restored_callback(self._on_connection_restored)

        # Configure auto-reconnect from config
        if self.config.get("auto_reconnect"):
            reconnect_config = self.config["auto_reconnect"]
            self.configure_auto_reconnect(
                enabled=reconnect_config.get("enabled", True),
                initial_delay=reconnect_config.get("initial_delay", 1.0),
                max_delay=reconnect_config.get("max_delay", 300.0),
                backoff_factor=reconnect_config.get("backoff_factor", 2.0),
                max_attempts=reconnect_config.get("max_attempts", 0),
            )

    async def _do_connect(self) -> bool:
        """Perform the actual connection (SimBroker's connect logic)."""
        # Simulate connection failure for testing
        if self._simulate_failures and random.random() < self._failure_probability:
            logger.warning("Simulated connection failure")
            return False

        # Call parent connect logic but without auto-reconnect setup
        await asyncio.sleep(0.01)  # Simulate connection delay
        self.connected = True
        self._running = True
        self._simulated_connection_lost = False

        # Start the fill engine
        if not self._fill_task or self._fill_task.done():
            self._fill_task = asyncio.create_task(self._fill_loop())

        logger.info(f"SimBroker {self.name} connected")
        return True

    async def connect(self) -> bool:
        """Connect with auto-reconnect if enabled."""
        if self._auto_reconnect_enabled:
            return await self.connect_with_auto_reconnect()
        else:
            return await self._do_connect()

    async def _do_disconnect(self) -> None:
        """Perform the actual disconnection (SimBroker's disconnect logic)."""
        self.connected = False
        self._running = False
        self._simulated_connection_lost = True

        # Stop fill engine
        if self._fill_task and not self._fill_task.done():
            self._fill_task.cancel()
            try:
                await self._fill_task
            except asyncio.CancelledError:
                pass

        logger.info(f"SimBroker {self.name} disconnected")

    async def disconnect(self) -> None:
        """Disconnect and stop auto-reconnect."""
        await self.disconnect_and_stop_reconnect()

    def _is_connection_healthy(self) -> bool:
        """Check if connection is healthy."""
        if self._simulated_connection_lost:
            return False

        # Simulate random connection drops for testing
        if self._simulate_failures and self.connected:
            if (
                random.random() < self._failure_probability / 10
            ):  # Lower probability for health checks
                logger.warning("Simulated connection health check failure")
                self._simulated_connection_lost = True
                return False

        return self.connected and self._running

    def simulate_connection_drop(self) -> None:
        """Manually simulate a connection drop for testing."""
        logger.info("Manually simulating connection drop")
        self._simulated_connection_lost = True
        # Trigger connection monitoring to detect the failure
        if hasattr(self, "_monitor_connection"):
            asyncio.create_task(self._handle_connection_loss())

    def _on_connection_lost(self) -> None:
        """Handle connection lost event."""
        self._connection_drops += 1
        logger.warning(f"Connection lost event triggered (total drops: {self._connection_drops})")

    def _on_connection_restored(self) -> None:
        """Handle connection restored event."""
        self._recovery_count += 1
        logger.info(
            f"Connection restored event triggered (total recoveries: {self._recovery_count})"
        )

    def get_resilience_stats(self) -> Dict[str, Any]:
        """Get resilience statistics for testing."""
        stats = self.get_reconnect_stats()
        stats.update(
            {
                "connection_drops": self._connection_drops,
                "recovery_count": self._recovery_count,
                "simulate_failures": self._simulate_failures,
                "failure_probability": self._failure_probability,
            }
        )
        return stats

    async def place_order(self, order) -> bool:
        """Place order with connection check."""
        if not self.is_connected() or self._simulated_connection_lost:
            logger.warning("Cannot place order: not connected")
            return False
        return await super().place_order(order)

    async def amend_order(self, order_id: str, **kwargs) -> bool:
        """Amend order with connection check."""
        if not self.is_connected() or self._simulated_connection_lost:
            logger.warning("Cannot amend order: not connected")
            return False
        return await super().amend_order(order_id, **kwargs)

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel order with connection check."""
        if not self.is_connected() or self._simulated_connection_lost:
            logger.warning("Cannot cancel order: not connected")
            return False
        return await super().cancel_order(order_id)
