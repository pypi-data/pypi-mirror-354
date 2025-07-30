"""Base classes for trading strategies."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class StrategyStatus(Enum):
    """Strategy execution status."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


@dataclass
class StrategyEvent:
    """Strategy status event."""

    strategy_name: str
    status: StrategyStatus
    timestamp: datetime
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@dataclass
class PriceUpdate:
    """Price update event."""

    symbol: str
    price: float
    timestamp: datetime
    volume: Optional[float] = None


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.

    All trading strategies must inherit from this class and implement
    the required methods for signal generation and order management.
    """

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the strategy.

        Args:
            name: Strategy name
            config: Strategy configuration
        """
        self.name = name
        self.config = config or {}
        self.status = StrategyStatus.STOPPED
        self._event_callback = None

    def set_event_callback(self, callback):
        """Set callback for strategy events."""
        self._event_callback = callback

    def _emit_event(self, status: StrategyStatus, message: str = None, data: Dict[str, Any] = None):
        """Emit a strategy status event."""
        event = StrategyEvent(
            strategy_name=self.name,
            status=status,
            timestamp=datetime.now(),
            message=message,
            data=data,
        )

        if self._event_callback:
            try:
                self._event_callback(event)
            except Exception as e:
                logger.error(f"Error in strategy event callback: {e}")

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the strategy.

        Returns:
            True if initialization successful, False otherwise
        """
        pass

    @abstractmethod
    def start(self) -> bool:
        """
        Start the strategy.

        Returns:
            True if start successful, False otherwise
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop the strategy.

        Returns:
            True if stop successful, False otherwise
        """
        pass

    @abstractmethod
    def on_price_update(self, price_update: PriceUpdate) -> None:
        """
        Handle price update.

        Args:
            price_update: Price update event
        """
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get strategy information."""
        return {"name": self.name, "status": self.status.value, "config": self.config}


class SampleStrategy(BaseStrategy):
    """Sample strategy for demonstration purposes."""

    def __init__(self, name: str = "SampleStrategy", config: Optional[Dict[str, Any]] = None):
        super().__init__(name, config)
        self.last_price = None
        self.signal_count = 0

    def initialize(self) -> bool:
        """Initialize the sample strategy."""
        try:
            logger.info(f"Initializing strategy {self.name}")
            self.status = StrategyStatus.STOPPED
            self._emit_event(StrategyStatus.STOPPED, "Strategy initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize strategy {self.name}: {e}")
            self.status = StrategyStatus.ERROR
            self._emit_event(StrategyStatus.ERROR, f"Initialization failed: {e}")
            return False

    def start(self) -> bool:
        """Start the sample strategy."""
        try:
            logger.info(f"Starting strategy {self.name}")
            self.status = StrategyStatus.STARTING
            self._emit_event(StrategyStatus.STARTING, "Strategy starting")

            # Simulate start logic
            self.status = StrategyStatus.RUNNING
            self._emit_event(StrategyStatus.RUNNING, "Strategy running")
            return True
        except Exception as e:
            logger.error(f"Failed to start strategy {self.name}: {e}")
            self.status = StrategyStatus.ERROR
            self._emit_event(StrategyStatus.ERROR, f"Start failed: {e}")
            return False

    def stop(self) -> bool:
        """Stop the sample strategy."""
        try:
            logger.info(f"Stopping strategy {self.name}")
            self.status = StrategyStatus.STOPPING
            self._emit_event(StrategyStatus.STOPPING, "Strategy stopping")

            # Simulate stop logic
            self.status = StrategyStatus.STOPPED
            self._emit_event(StrategyStatus.STOPPED, "Strategy stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop strategy {self.name}: {e}")
            self.status = StrategyStatus.ERROR
            self._emit_event(StrategyStatus.ERROR, f"Stop failed: {e}")
            return False

    def on_price_update(self, price_update: PriceUpdate) -> None:
        """Handle price update for sample strategy."""
        self.last_price = price_update.price
        self.signal_count += 1

        # Simple signal generation example
        if self.signal_count % 10 == 0:  # Every 10th price update
            logger.info(f"Strategy {self.name} signal: price={price_update.price}")
            self._emit_event(
                self.status,
                f"Generated signal for {price_update.symbol}",
                {"price": price_update.price, "signal_count": self.signal_count},
            )
