"""Base classes for market data feeds."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol


class MarketDataType(Enum):
    """Market data type enumeration."""

    TICK = "TICK"
    QUOTE = "QUOTE"
    TRADE = "TRADE"
    BOOK = "BOOK"
    BAR = "BAR"


@dataclass
class SubscriptionRequest:
    """Represents a market data subscription request."""

    symbol: str
    data_types: List[MarketDataType]
    subscription_id: Optional[str] = None
    params: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription request to dictionary."""
        return {
            "symbol": self.symbol,
            "data_types": [dt.value for dt in self.data_types],
            "subscription_id": self.subscription_id,
            "params": self.params or {},
        }


@dataclass
class MarketDataEvent:
    """Represents a market data event (tick, quote, trade, etc.)."""

    event_type: MarketDataType
    symbol: str
    timestamp: datetime
    data: Dict[str, Any]
    feed_name: Optional[str] = None
    sequence_number: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert market data event to dictionary."""
        return {
            "event_type": self.event_type.value,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "data": self.data,
            "feed_name": self.feed_name,
            "sequence_number": self.sequence_number,
        }


@dataclass
class QuoteData:
    """Quote data structure."""

    bid_price: float
    ask_price: float
    bid_size: float
    ask_size: float
    bid_exchange: Optional[str] = None
    ask_exchange: Optional[str] = None


@dataclass
class TradeData:
    """Trade data structure."""

    price: float
    size: float
    exchange: Optional[str] = None
    trade_id: Optional[str] = None


@dataclass
class BookLevel:
    """Order book level."""

    price: float
    size: float
    order_count: Optional[int] = None


@dataclass
class BookData:
    """Order book data structure."""

    bids: List[BookLevel]
    asks: List[BookLevel]
    exchange: Optional[str] = None


class DataCallback(Protocol):
    """Protocol for market data callbacks."""

    async def __call__(self, event: MarketDataEvent) -> None:
        """Handle a market data event."""
        ...


class FeedBase(ABC):
    """Abstract base class for all market data feeds.

    This class defines the interface that all feed implementations must follow.
    It handles subscription management, data streaming, and snapshot requests.
    """

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize feed adapter.

        Args:
            name: Name of the feed adapter
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.connected = False
        self.subscriptions: Dict[str, SubscriptionRequest] = {}
        self.data_callback: Optional[DataCallback] = None
        self.sequence_number = 0

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the market data feed.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the market data feed."""
        pass

    @abstractmethod
    async def subscribe(self, request: SubscriptionRequest) -> bool:
        """Subscribe to market data.

        Args:
            request: The subscription request

        Returns:
            True if subscription was successful, False otherwise
        """
        pass

    @abstractmethod
    async def unsubscribe(self, symbol: str) -> bool:
        """Unsubscribe from market data.

        Args:
            symbol: Symbol to unsubscribe from

        Returns:
            True if unsubscription was successful, False otherwise
        """
        pass

    @abstractmethod
    async def snapshot(
        self, symbol: str, data_types: List[MarketDataType]
    ) -> Optional[Dict[str, Any]]:
        """Get a snapshot of current market data.

        Args:
            symbol: Symbol to get snapshot for
            data_types: Types of data to include in snapshot

        Returns:
            Dictionary containing snapshot data, or None if not available
        """
        pass

    def set_data_callback(self, callback: DataCallback) -> None:
        """Set the callback function for market data events.

        Args:
            callback: Async function to call when data events occur
        """
        self.data_callback = callback

    async def _emit_data(self, event: MarketDataEvent) -> None:
        """Emit a market data event to the callback.

        Args:
            event: The market data event to emit
        """
        if self.data_callback:
            try:
                await self.data_callback(event)
            except Exception as e:
                # Log error but don't let it crash the feed
                print(f"Error in market data callback: {e}")

    def _next_sequence_number(self) -> int:
        """Get the next sequence number."""
        self.sequence_number += 1
        return self.sequence_number

    def is_connected(self) -> bool:
        """Check if feed is connected.

        Returns:
            True if connected, False otherwise
        """
        return self.connected

    def get_name(self) -> str:
        """Get feed adapter name.

        Returns:
            The name of this feed adapter
        """
        return self.name

    def get_subscriptions(self) -> Dict[str, SubscriptionRequest]:
        """Get all active subscriptions.

        Returns:
            Dictionary of symbol -> SubscriptionRequest
        """
        return self.subscriptions.copy()

    def is_subscribed(self, symbol: str) -> bool:
        """Check if subscribed to a symbol.

        Args:
            symbol: Symbol to check

        Returns:
            True if subscribed, False otherwise
        """
        return symbol in self.subscriptions
