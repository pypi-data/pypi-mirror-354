"""Base classes for broker adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Protocol


class OrderSide(Enum):
    """Order side enumeration."""

    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """Order type enumeration."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(Enum):
    """Order status enumeration."""

    NEW = "NEW"
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass
class OrderRequest:
    """Represents an order request to be sent to a broker."""

    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "DAY"
    client_order_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert order request to dictionary."""
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "order_type": self.order_type.value,
            "quantity": self.quantity,
            "price": self.price,
            "stop_price": self.stop_price,
            "time_in_force": self.time_in_force,
            "client_order_id": self.client_order_id,
        }


@dataclass
class BrokerEvent:
    """Represents an event from the broker (ack, fill, reject, etc.)."""

    event_type: str  # "ACK", "FILL", "CANCEL", "REJECT"
    order_id: str
    symbol: str
    timestamp: datetime
    quantity: Optional[float] = None
    price: Optional[float] = None
    filled_quantity: Optional[float] = None
    remaining_quantity: Optional[float] = None
    status: Optional[OrderStatus] = None
    message: Optional[str] = None
    broker_order_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert broker event to dictionary."""
        return {
            "event_type": self.event_type,
            "order_id": self.order_id,
            "symbol": self.symbol,
            "timestamp": self.timestamp.isoformat(),
            "quantity": self.quantity,
            "price": self.price,
            "filled_quantity": self.filled_quantity,
            "remaining_quantity": self.remaining_quantity,
            "status": self.status.value if self.status else None,
            "message": self.message,
            "broker_order_id": self.broker_order_id,
        }


class EventCallback(Protocol):
    """Protocol for broker event callbacks."""

    async def __call__(self, event: BrokerEvent) -> None:
        """Handle a broker event."""
        ...


class BrokerBase(ABC):
    """Abstract base class for all broker adapters.

    This class defines the interface that all broker implementations must follow.
    It handles connection management, order placement, amendments, and cancellations,
    and streams events back to the calling system.
    """

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize broker adapter.

        Args:
            name: Name of the broker adapter
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.connected = False
        self.event_callback: Optional[EventCallback] = None

    @abstractmethod
    async def connect(self) -> bool:
        """Connect to the broker.

        Returns:
            True if connection successful, False otherwise
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from the broker."""
        pass

    @abstractmethod
    async def place_order(self, order: OrderRequest) -> bool:
        """Place a new order.

        Args:
            order: The order request to place

        Returns:
            True if order was successfully sent, False otherwise
        """
        pass

    @abstractmethod
    async def amend_order(self, order_id: str, **kwargs) -> bool:
        """Amend an existing order.

        Args:
            order_id: ID of the order to amend
            **kwargs: Fields to amend (price, quantity, etc.)

        Returns:
            True if amendment was successfully sent, False otherwise
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order.

        Args:
            order_id: ID of the order to cancel

        Returns:
            True if cancellation was successfully sent, False otherwise
        """
        pass

    def set_event_callback(self, callback: EventCallback) -> None:
        """Set the callback function for broker events.

        Args:
            callback: Async function to call when events occur
        """
        self.event_callback = callback

    async def _emit_event(self, event: BrokerEvent) -> None:
        """Emit a broker event to the callback.

        Args:
            event: The broker event to emit
        """
        if self.event_callback:
            try:
                await self.event_callback(event)
            except Exception as e:
                # Log error but don't let it crash the broker
                print(f"Error in broker event callback: {e}")

    def is_connected(self) -> bool:
        """Check if broker is connected.

        Returns:
            True if connected, False otherwise
        """
        return self.connected

    def get_name(self) -> str:
        """Get broker adapter name.

        Returns:
            The name of this broker adapter
        """
        return self.name
