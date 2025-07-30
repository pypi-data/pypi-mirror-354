"""
Auto-reconnect capabilities for brokers and feeds.

Provides exponential backoff reconnection logic to handle connection failures
and maintain reliable connections to external services.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


class AutoReconnectMixin(ABC):
    """
    Mixin class providing auto-reconnect capabilities with exponential backoff.

    This mixin can be used by broker and feed classes to automatically
    handle connection failures and implement resilient reconnection logic.
    """

    def __init__(self, *args, **kwargs):
        """Initialize auto-reconnect parameters."""
        super().__init__(*args, **kwargs)

        # Auto-reconnect configuration
        self._auto_reconnect_enabled = True
        self._initial_reconnect_delay = 1.0  # Start with 1 second
        self._max_reconnect_delay = 300.0  # Max 5 minutes
        self._reconnect_backoff_factor = 2.0  # Double delay each time
        self._max_reconnect_attempts = 0  # 0 = unlimited
        self._health_check_interval = 5.0  # Health check every 5 seconds

        # Reconnect state
        self._reconnect_attempts = 0
        self._current_reconnect_delay = self._initial_reconnect_delay
        self._reconnect_task: Optional[asyncio.Task] = None
        self._last_disconnect_time: Optional[float] = None
        self._connection_lost_callbacks: list[Callable[[], None]] = []
        self._connection_restored_callbacks: list[Callable[[], None]] = []

    def configure_auto_reconnect(
        self,
        enabled: bool = True,
        initial_delay: float = 1.0,
        max_delay: float = 300.0,
        backoff_factor: float = 2.0,
        max_attempts: int = 0,
        health_check_interval: float = 5.0,
    ) -> None:
        """
        Configure auto-reconnect parameters.

        Args:
            enabled: Whether auto-reconnect is enabled
            initial_delay: Initial delay between reconnect attempts (seconds)
            max_delay: Maximum delay between reconnect attempts (seconds)
            backoff_factor: Factor to multiply delay by after each failed attempt
            max_attempts: Maximum number of reconnect attempts (0 = unlimited)
            health_check_interval: Interval between health checks (seconds)
        """
        self._auto_reconnect_enabled = enabled
        self._initial_reconnect_delay = initial_delay
        self._max_reconnect_delay = max_delay
        self._reconnect_backoff_factor = backoff_factor
        self._max_reconnect_attempts = max_attempts
        self._health_check_interval = health_check_interval

    def add_connection_lost_callback(self, callback: Callable[[], None]) -> None:
        """Add callback to be called when connection is lost."""
        self._connection_lost_callbacks.append(callback)

    def add_connection_restored_callback(self, callback: Callable[[], None]) -> None:
        """Add callback to be called when connection is restored."""
        self._connection_restored_callbacks.append(callback)

    def remove_connection_lost_callback(self, callback: Callable[[], None]) -> None:
        """Remove connection lost callback."""
        if callback in self._connection_lost_callbacks:
            self._connection_lost_callbacks.remove(callback)

    def remove_connection_restored_callback(self, callback: Callable[[], None]) -> None:
        """Remove connection restored callback."""
        if callback in self._connection_restored_callbacks:
            self._connection_restored_callbacks.remove(callback)

    @abstractmethod
    async def _do_connect(self) -> bool:
        """
        Perform the actual connection.

        This method should be implemented by the concrete class to perform
        the actual connection logic without auto-reconnect handling.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def _do_disconnect(self) -> None:
        """
        Perform the actual disconnection.

        This method should be implemented by the concrete class to perform
        the actual disconnection logic.
        """
        pass

    @abstractmethod
    def _is_connection_healthy(self) -> bool:
        """
        Check if the connection is healthy.

        This method should be implemented by the concrete class to check
        if the connection is still working properly.

        Returns:
            True if connection is healthy, False otherwise
        """
        pass

    async def connect_with_auto_reconnect(self) -> bool:
        """
        Connect with auto-reconnect enabled.

        This method should be called instead of the regular connect() method
        when auto-reconnect is desired.

        Returns:
            True if initial connection successful, False otherwise
        """
        success = await self._do_connect()

        if success:
            self._reset_reconnect_state()
            logger.info("Connected successfully with auto-reconnect enabled")

            # Start monitoring connection health if auto-reconnect is enabled
            if self._auto_reconnect_enabled:
                self._start_connection_monitoring()

        return success

    async def disconnect_and_stop_reconnect(self) -> None:
        """Disconnect and stop any auto-reconnect attempts."""
        self._auto_reconnect_enabled = False

        # Stop reconnect task if running
        if self._reconnect_task and not self._reconnect_task.done():
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass

        await self._do_disconnect()
        logger.info("Disconnected and stopped auto-reconnect")

    def _start_connection_monitoring(self) -> None:
        """Start monitoring connection health."""
        if not self._reconnect_task or self._reconnect_task.done():
            self._reconnect_task = asyncio.create_task(self._monitor_connection())

    async def _monitor_connection(self) -> None:
        """Monitor connection health and trigger reconnect if needed."""
        try:
            while self._auto_reconnect_enabled:
                # Check connection health periodically
                await asyncio.sleep(self._health_check_interval)

                if not self._is_connection_healthy():
                    logger.warning("Connection health check failed, triggering reconnect")
                    await self._handle_connection_loss()
                    break

        except asyncio.CancelledError:
            logger.debug("Connection monitoring cancelled")
        except Exception as e:
            logger.error(f"Error in connection monitoring: {e}")

    async def _handle_connection_loss(self) -> None:
        """Handle connection loss and start reconnect attempts."""
        if not self._auto_reconnect_enabled:
            return

        self._last_disconnect_time = time.time()

        # Notify listeners
        for callback in self._connection_lost_callbacks:
            try:
                callback()
            except Exception as e:
                logger.error(f"Error in connection lost callback: {e}")

        logger.warning("Connection lost, starting auto-reconnect")

        # Start reconnect attempts
        await self._attempt_reconnect()

    async def _attempt_reconnect(self) -> None:
        """Attempt to reconnect with exponential backoff."""
        while self._auto_reconnect_enabled:
            # Check if we've exceeded max attempts
            if (
                self._max_reconnect_attempts > 0
                and self._reconnect_attempts >= self._max_reconnect_attempts
            ):
                logger.error(
                    f"Max reconnect attempts ({self._max_reconnect_attempts}) exceeded, "
                    "giving up"
                )
                self._auto_reconnect_enabled = False
                break

            self._reconnect_attempts += 1

            logger.info(
                f"Reconnect attempt {self._reconnect_attempts}, "
                f"waiting {self._current_reconnect_delay:.1f}s"
            )

            # Wait with exponential backoff
            try:
                await asyncio.sleep(self._current_reconnect_delay)
            except asyncio.CancelledError:
                return

            # Attempt to reconnect
            try:
                success = await self._do_connect()

                if success and self._is_connection_healthy():
                    logger.info(
                        f"Reconnected successfully after {self._reconnect_attempts} attempts"
                    )

                    # Reset reconnect state
                    self._reset_reconnect_state()

                    # Notify listeners
                    for callback in self._connection_restored_callbacks:
                        try:
                            callback()
                        except Exception as e:
                            logger.error(f"Error in connection restored callback: {e}")

                    # Restart connection monitoring
                    self._start_connection_monitoring()
                    return
                else:
                    logger.warning(f"Reconnect attempt {self._reconnect_attempts} failed")

            except Exception as e:
                logger.error(f"Error during reconnect attempt {self._reconnect_attempts}: {e}")

            # Increase delay for next attempt (exponential backoff)
            self._current_reconnect_delay = min(
                self._current_reconnect_delay * self._reconnect_backoff_factor,
                self._max_reconnect_delay,
            )

        logger.error("Auto-reconnect failed or disabled")

    def _reset_reconnect_state(self) -> None:
        """Reset reconnect state after successful connection."""
        self._reconnect_attempts = 0
        self._current_reconnect_delay = self._initial_reconnect_delay

    def get_reconnect_stats(self) -> dict[str, Any]:
        """Get reconnect statistics."""
        uptime = None
        if self._last_disconnect_time:
            uptime = time.time() - self._last_disconnect_time

        return {
            "auto_reconnect_enabled": self._auto_reconnect_enabled,
            "reconnect_attempts": self._reconnect_attempts,
            "current_delay": self._current_reconnect_delay,
            "max_attempts": self._max_reconnect_attempts,
            "uptime_since_last_disconnect": uptime,
            "is_monitoring": self._reconnect_task is not None and not self._reconnect_task.done(),
        }


class ResilientBrokerBase(AutoReconnectMixin):
    """
    Base class for resilient brokers with auto-reconnect capabilities.

    This class combines BrokerBase functionality with AutoReconnectMixin
    to provide robust connection management.
    """

    def __init__(self, name: str, config: Optional[dict[str, Any]] = None):
        """Initialize resilient broker."""
        # Initialize both parent classes
        super().__init__()

        self.name = name
        self.config = config or {}
        self.connected = False
        self.event_callback: Optional[Callable] = None

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

    def _is_connection_healthy(self) -> bool:
        """Default implementation checks connected flag."""
        return self.connected

    async def connect(self) -> bool:
        """Connect with auto-reconnect if enabled."""
        if self._auto_reconnect_enabled:
            return await self.connect_with_auto_reconnect()
        else:
            return await self._do_connect()

    async def disconnect(self) -> None:
        """Disconnect and stop auto-reconnect."""
        await self.disconnect_and_stop_reconnect()

    def is_connected(self) -> bool:
        """Check if broker is connected."""
        return self.connected

    def get_name(self) -> str:
        """Get broker adapter name."""
        return self.name
