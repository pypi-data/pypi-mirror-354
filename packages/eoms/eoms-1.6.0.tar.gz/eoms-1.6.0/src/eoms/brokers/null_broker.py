"""Null broker implementation for testing."""

import asyncio
from datetime import datetime
from typing import Any, Dict

from .base import BrokerBase, BrokerEvent, OrderRequest, OrderStatus


class NullBroker(BrokerBase):
    """A null broker implementation that simulates basic broker operations.

    This broker accepts all operations but doesn't actually execute them.
    It's useful for testing and development when you don't want to connect
    to a real broker.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the null broker.

        Args:
            config: Optional configuration dictionary
        """
        super().__init__("NullBroker", config)
        self._orders: Dict[str, OrderRequest] = {}

    async def connect(self) -> bool:
        """Simulate connection to broker.

        Returns:
            Always returns True
        """
        await asyncio.sleep(0.01)  # Simulate connection delay
        self.connected = True
        return True

    async def disconnect(self) -> None:
        """Simulate disconnection from broker."""
        await asyncio.sleep(0.01)  # Simulate disconnection delay
        self.connected = False

    async def place_order(self, order: OrderRequest) -> bool:
        """Simulate placing an order.

        Args:
            order: The order request to place

        Returns:
            Always returns True
        """
        if not self.connected:
            return False

        # Store the order
        self._orders[order.order_id] = order

        # Simulate acknowledgment
        await self._emit_event(
            BrokerEvent(
                event_type="ACK",
                order_id=order.order_id,
                symbol=order.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.ACKNOWLEDGED,
                message="Order acknowledged by NullBroker",
            )
        )

        return True

    async def amend_order(self, order_id: str, **kwargs) -> bool:
        """Simulate amending an order.

        Args:
            order_id: ID of the order to amend
            **kwargs: Fields to amend

        Returns:
            True if order exists, False otherwise
        """
        if not self.connected:
            return False

        if order_id not in self._orders:
            # Emit reject event for non-existent order
            await self._emit_event(
                BrokerEvent(
                    event_type="REJECT",
                    order_id=order_id,
                    symbol="UNKNOWN",
                    timestamp=datetime.now(),
                    status=OrderStatus.REJECTED,
                    message=f"Order {order_id} not found for amendment",
                )
            )
            return False

        # Update order fields
        order = self._orders[order_id]
        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)

        # Emit acknowledgment
        await self._emit_event(
            BrokerEvent(
                event_type="ACK",
                order_id=order_id,
                symbol=order.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.ACKNOWLEDGED,
                message=f"Order {order_id} amendment acknowledged",
            )
        )

        return True

    async def cancel_order(self, order_id: str) -> bool:
        """Simulate cancelling an order.

        Args:
            order_id: ID of the order to cancel

        Returns:
            True if order exists, False otherwise
        """
        if not self.connected:
            return False

        if order_id not in self._orders:
            # Emit reject event for non-existent order
            await self._emit_event(
                BrokerEvent(
                    event_type="REJECT",
                    order_id=order_id,
                    symbol="UNKNOWN",
                    timestamp=datetime.now(),
                    status=OrderStatus.REJECTED,
                    message=f"Order {order_id} not found for cancellation",
                )
            )
            return False

        order = self._orders[order_id]

        # Emit cancellation acknowledgment
        await self._emit_event(
            BrokerEvent(
                event_type="CANCEL",
                order_id=order_id,
                symbol=order.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.CANCELLED,
                message=f"Order {order_id} cancelled",
            )
        )

        # Remove from orders
        del self._orders[order_id]

        return True

    def get_orders(self) -> Dict[str, OrderRequest]:
        """Get all stored orders.

        Returns:
            Dictionary of order_id -> OrderRequest
        """
        return self._orders.copy()

    def clear_orders(self) -> None:
        """Clear all stored orders."""
        self._orders.clear()
