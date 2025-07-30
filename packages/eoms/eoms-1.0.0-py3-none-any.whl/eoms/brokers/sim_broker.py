"""Simulation broker with in-memory fill engine."""

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import (
    BrokerBase,
    BrokerEvent,
    OrderRequest,
    OrderSide,
    OrderStatus,
    OrderType,
)


@dataclass
class SimulatedFill:
    """Represents a simulated fill."""

    order_id: str
    symbol: str
    side: OrderSide
    quantity: float
    price: float
    timestamp: datetime
    fill_id: str = field(default_factory=lambda: f"F{random.randint(1000, 9999)}")


@dataclass
class SimulatedOrder:
    """Represents an order in the simulation engine."""

    request: OrderRequest
    status: OrderStatus
    filled_quantity: float = 0.0
    remaining_quantity: float = 0.0
    fills: List[SimulatedFill] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Initialize remaining quantity."""
        if self.remaining_quantity == 0.0:
            self.remaining_quantity = self.request.quantity


class FillEngine:
    """In-memory fill engine that simulates market behavior."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the fill engine.

        Args:
            config: Configuration parameters for the fill engine
        """
        self.config = config or {}
        self.market_prices: Dict[str, float] = {}
        self.volatility = self.config.get("volatility", 0.01)  # 1% default volatility
        self.fill_probability = self.config.get("fill_probability", 0.8)  # 80% fill chance
        self.partial_fill_prob = self.config.get(
            "partial_fill_probability", 0.3
        )  # 30% partial fills
        self.latency_ms = self.config.get("latency_ms", 50)  # 50ms default latency

        # Initialize some default market prices
        default_prices = {
            "AAPL": 150.0,
            "MSFT": 300.0,
            "GOOGL": 2500.0,
            "TSLA": 200.0,
            "SPY": 400.0,
        }
        self.market_prices.update(self.config.get("market_prices", default_prices))

    def get_market_price(self, symbol: str) -> float:
        """Get current market price for a symbol.

        Args:
            symbol: Symbol to get price for

        Returns:
            Current market price
        """
        if symbol not in self.market_prices:
            # Generate a random price for unknown symbols
            self.market_prices[symbol] = random.uniform(10.0, 1000.0)

        # Add some random movement
        current_price = self.market_prices[symbol]
        change = current_price * random.gauss(0, self.volatility)
        new_price = max(0.01, current_price + change)
        self.market_prices[symbol] = new_price

        return new_price

    def should_fill_order(self, order: SimulatedOrder) -> bool:
        """Determine if an order should be filled.

        Args:
            order: The order to evaluate

        Returns:
            True if order should be filled
        """
        market_price = self.get_market_price(order.request.symbol)

        # Market orders always fill
        if order.request.order_type == OrderType.MARKET:
            return True

        # Limit orders fill based on price and probability
        if order.request.order_type == OrderType.LIMIT:
            if order.request.price is None:
                return False

            # Check if price is favorable
            if order.request.side == OrderSide.BUY:
                price_favorable = market_price <= order.request.price
            else:  # SELL
                price_favorable = market_price >= order.request.price

            # Apply random fill probability
            return price_favorable and random.random() < self.fill_probability

        return False

    def calculate_fill_quantity(self, order: SimulatedOrder) -> float:
        """Calculate how much of an order to fill.

        Args:
            order: The order to calculate fill for

        Returns:
            Quantity to fill
        """
        remaining = order.remaining_quantity

        # Sometimes do partial fills
        if random.random() < self.partial_fill_prob and remaining > 1:
            return random.uniform(1, remaining)

        return remaining

    def calculate_fill_price(self, order: SimulatedOrder) -> float:
        """Calculate the fill price for an order.

        Args:
            order: The order to calculate price for

        Returns:
            Fill price
        """
        market_price = self.get_market_price(order.request.symbol)

        if order.request.order_type == OrderType.MARKET:
            # Market orders get market price with minimal slippage
            slippage = random.gauss(0, 0.0005)  # 0.05% slippage
            return market_price * (1 + slippage)

        elif order.request.order_type == OrderType.LIMIT:
            # Limit orders get price improvement sometimes
            if random.random() < 0.3:  # 30% chance of price improvement
                improvement = random.uniform(0, 0.002)  # Up to 0.2% improvement
                if order.request.side == OrderSide.BUY:
                    return order.request.price * (1 - improvement)
                else:
                    return order.request.price * (1 + improvement)
            else:
                return order.request.price

        return market_price


class SimBroker(BrokerBase):
    """Simulation broker with in-memory fill engine.

    This broker simulates realistic trading behavior including:
    - Market price movements
    - Partial fills
    - Order latency
    - Fill probability based on order type and market conditions
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the simulation broker.

        Args:
            config: Configuration for the broker and fill engine
        """
        super().__init__("SimBroker", config)
        self.fill_engine = FillEngine(config)
        self.orders: Dict[str, SimulatedOrder] = {}  # Active orders
        self.all_orders: Dict[str, SimulatedOrder] = {}  # All orders history
        self.order_sequence = 0
        self._fill_task: Optional[asyncio.Task] = None
        self._running = False

    async def connect(self) -> bool:
        """Connect to the simulation broker.

        Returns:
            Always returns True
        """
        await asyncio.sleep(0.01)  # Simulate connection delay
        self.connected = True
        self._running = True

        # Start the fill engine
        self._fill_task = asyncio.create_task(self._fill_loop())

        return True

    async def disconnect(self) -> None:
        """Disconnect from the simulation broker."""
        self._running = False

        if self._fill_task and not self._fill_task.done():
            self._fill_task.cancel()
            try:
                await self._fill_task
            except asyncio.CancelledError:
                pass
            finally:
                self._fill_task = None

        self.connected = False

    def __del__(self) -> None:
        """Cleanup any remaining tasks on deletion."""
        if hasattr(self, "_fill_task") and self._fill_task and not self._fill_task.done():
            self._fill_task.cancel()

    async def place_order(self, order: OrderRequest) -> bool:
        """Place a new order in the simulation.

        Args:
            order: The order request to place

        Returns:
            True if order was accepted
        """
        if not self.connected:
            return False

        # Simulate network latency
        await asyncio.sleep(self.fill_engine.latency_ms / 1000.0)

        # Create simulated order
        sim_order = SimulatedOrder(request=order, status=OrderStatus.ACKNOWLEDGED)

        # Store the order in both active and history
        self.orders[order.order_id] = sim_order
        self.all_orders[order.order_id] = sim_order

        # Emit acknowledgment
        await self._emit_event(
            BrokerEvent(
                event_type="ACK",
                order_id=order.order_id,
                symbol=order.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.ACKNOWLEDGED,
                broker_order_id=f"SIM{self.order_sequence:06d}",
            )
        )

        self.order_sequence += 1
        return True

    async def amend_order(self, order_id: str, **kwargs) -> bool:
        """Amend an existing order.

        Args:
            order_id: ID of the order to amend
            **kwargs: Fields to amend

        Returns:
            True if amendment was successful
        """
        if not self.connected:
            return False

        if order_id not in self.orders:
            await self._emit_event(
                BrokerEvent(
                    event_type="REJECT",
                    order_id=order_id,
                    symbol="UNKNOWN",
                    timestamp=datetime.now(),
                    status=OrderStatus.REJECTED,
                    message=f"Order {order_id} not found",
                )
            )
            return False

        order = self.orders[order_id]

        # Update order fields
        for key, value in kwargs.items():
            if hasattr(order.request, key):
                setattr(order.request, key, value)

        # Simulate latency
        await asyncio.sleep(self.fill_engine.latency_ms / 1000.0)

        # Emit acknowledgment
        await self._emit_event(
            BrokerEvent(
                event_type="ACK",
                order_id=order_id,
                symbol=order.request.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.ACKNOWLEDGED,
                message=f"Order {order_id} amended",
            )
        )

        return True

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order.

        Args:
            order_id: ID of the order to cancel

        Returns:
            True if cancellation was successful
        """
        if not self.connected:
            return False

        if order_id not in self.orders:
            await self._emit_event(
                BrokerEvent(
                    event_type="REJECT",
                    order_id=order_id,
                    symbol="UNKNOWN",
                    timestamp=datetime.now(),
                    status=OrderStatus.REJECTED,
                    message=f"Order {order_id} not found",
                )
            )
            return False

        order = self.orders[order_id]

        # Simulate latency
        await asyncio.sleep(self.fill_engine.latency_ms / 1000.0)

        # Update order status
        order.status = OrderStatus.CANCELLED

        # Emit cancellation
        await self._emit_event(
            BrokerEvent(
                event_type="CANCEL",
                order_id=order_id,
                symbol=order.request.symbol,
                timestamp=datetime.now(),
                status=OrderStatus.CANCELLED,
                remaining_quantity=order.remaining_quantity,
            )
        )

        # Remove from active orders only (keep in history)
        del self.orders[order_id]

        return True

    async def _fill_loop(self) -> None:
        """Main fill engine loop."""
        while self._running:
            try:
                await self._process_fills()
                await asyncio.sleep(0.1)  # Check for fills every 100ms
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in fill loop: {e}")
                await asyncio.sleep(1.0)  # Back off on error

    async def _process_fills(self) -> None:
        """Process potential fills for all orders."""
        orders_to_remove = []

        for order_id, order in self.orders.items():
            if order.status in [OrderStatus.CANCELLED, OrderStatus.FILLED]:
                continue

            if self.fill_engine.should_fill_order(order):
                fill_quantity = self.fill_engine.calculate_fill_quantity(order)
                fill_price = self.fill_engine.calculate_fill_price(order)

                # Create fill
                fill = SimulatedFill(
                    order_id=order_id,
                    symbol=order.request.symbol,
                    side=order.request.side,
                    quantity=fill_quantity,
                    price=fill_price,
                    timestamp=datetime.now(),
                )

                # Update order
                order.fills.append(fill)
                order.filled_quantity += fill_quantity
                order.remaining_quantity -= fill_quantity

                # Determine new status
                if order.remaining_quantity <= 0.001:  # Account for floating point precision
                    order.status = OrderStatus.FILLED
                    orders_to_remove.append(order_id)
                else:
                    order.status = OrderStatus.PARTIALLY_FILLED

                # Emit fill event
                await self._emit_event(
                    BrokerEvent(
                        event_type="FILL",
                        order_id=order_id,
                        symbol=order.request.symbol,
                        timestamp=fill.timestamp,
                        quantity=fill_quantity,
                        price=fill_price,
                        filled_quantity=order.filled_quantity,
                        remaining_quantity=order.remaining_quantity,
                        status=order.status,
                    )
                )

        # Remove fully filled orders from active orders only (keep in history)
        for order_id in orders_to_remove:
            del self.orders[order_id]

    def get_orders(self) -> Dict[str, SimulatedOrder]:
        """Get all active orders.

        Returns:
            Dictionary of order_id -> SimulatedOrder
        """
        return self.orders.copy()

    def get_market_price(self, symbol: str) -> float:
        """Get current market price for a symbol.

        Args:
            symbol: Symbol to get price for

        Returns:
            Current market price
        """
        return self.fill_engine.get_market_price(symbol)

    def get_fill_history(self, order_id: Optional[str] = None) -> List[SimulatedFill]:
        """Get fill history.

        Args:
            order_id: Optional order ID to filter by

        Returns:
            List of fills
        """
        fills = []
        for order in self.all_orders.values():
            if order_id is None or order.request.order_id == order_id:
                fills.extend(order.fills)
        return fills

    def calculate_pnl(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Calculate simple PNL for testing.

        Args:
            symbol: Optional symbol to filter by

        Returns:
            PNL summary
        """
        position = 0.0
        realized_pnl = 0.0
        avg_price = 0.0

        fills = self.get_fill_history()
        if symbol:
            fills = [f for f in fills if f.symbol == symbol]

        for fill in fills:
            if fill.side == OrderSide.BUY:
                position += fill.quantity
                realized_pnl -= fill.quantity * fill.price
            else:  # SELL
                position -= fill.quantity
                realized_pnl += fill.quantity * fill.price

        if position != 0 and fills:
            # Calculate average price (simplified)
            total_cost = sum(f.quantity * f.price for f in fills if f.side == OrderSide.BUY)
            total_bought = sum(f.quantity for f in fills if f.side == OrderSide.BUY)
            if total_bought > 0:
                avg_price = total_cost / total_bought

        return {
            "position": position,
            "realized_pnl": realized_pnl,
            "avg_price": avg_price,
            "fill_count": len(fills),
        }
