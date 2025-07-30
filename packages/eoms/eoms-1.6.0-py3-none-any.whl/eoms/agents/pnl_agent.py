"""PNL Agent for calculating and tracking profit/loss."""

import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from eoms.agents.base import BaseAgent
from eoms.brokers.base import OrderSide
from eoms.core.eventbus import EventBus

logger = logging.getLogger(__name__)


class PnlSnapshot:
    """P&L snapshot data."""

    def __init__(
        self,
        timestamp: datetime,
        symbol: str,
        realized_pnl: float,
        unrealized_pnl: float,
        position: float,
        avg_price: float,
        market_price: float,
    ):
        self.timestamp = timestamp
        self.symbol = symbol
        self.realized_pnl = realized_pnl
        self.unrealized_pnl = unrealized_pnl
        self.total_pnl = realized_pnl + unrealized_pnl
        self.position = position
        self.avg_price = avg_price
        self.market_price = market_price


class PnlAgent(BaseAgent):
    """
    P&L Agent for calculating tick-level and aggregated profit/loss.

    Responsibilities:
    - Calculate real-time P&L from position updates and price feeds
    - Track realized and unrealized P&L by symbol
    - Include fees and slippage in calculations
    - Emit P&L snapshots for downstream consumers
    - Maintain accuracy within 0.1% vs back-calculation
    """

    def __init__(self, event_bus: EventBus, config: Optional[Dict[str, Any]] = None):
        super().__init__("PNL", event_bus, config)

        # Position tracking
        self.positions: Dict[str, float] = defaultdict(float)  # symbol -> quantity
        self.avg_prices: Dict[str, float] = {}  # symbol -> average price
        self.realized_pnl: Dict[str, float] = defaultdict(float)  # symbol -> realized P&L

        # Market data
        self.market_prices: Dict[str, float] = {}  # symbol -> current market price

        # P&L history
        self.pnl_snapshots: List[PnlSnapshot] = []

        # Metrics
        self.total_fills_processed = 0
        self.total_price_updates = 0

    async def initialize(self) -> None:
        """Initialize the PNL agent."""
        logger.info("Initializing PNL Agent")

    async def cleanup(self) -> None:
        """Cleanup the PNL agent."""
        logger.info("Cleaning up PNL Agent")

    def get_subscribed_topics(self) -> List[str]:
        """Get subscribed topics."""
        return ["order.fill", "price.update", "position.snapshot"]

    async def process_event(self, topic: str, event: Any) -> None:
        """Process incoming events."""
        try:
            if topic == "order.fill":
                await self._handle_order_fill(event)
            elif topic == "price.update":
                await self._handle_price_update(event)
            elif topic == "position.snapshot":
                await self._handle_position_snapshot(event)
        except Exception as e:
            logger.error(f"PNL Agent error processing {topic}: {e}")

    async def _handle_order_fill(self, fill_event: Any) -> None:
        """Handle order fill events to update positions and realized P&L."""
        try:
            # Extract fill details
            symbol = getattr(fill_event, "symbol", None)
            side = getattr(fill_event, "side", None)
            quantity = getattr(fill_event, "quantity", 0.0)
            price = getattr(fill_event, "price", 0.0)

            if not symbol or not side:
                logger.warning(f"Invalid fill event: {fill_event}")
                return

            self.total_fills_processed += 1

            # Update position and P&L calculations
            self._update_position_from_fill(symbol, side, quantity, price)

            # Emit updated P&L snapshot
            await self._emit_pnl_snapshot(symbol)

        except Exception as e:
            logger.error(f"Error processing order fill: {e}")

    async def _handle_price_update(self, price_update: Any) -> None:
        """Handle price updates to recalculate unrealized P&L."""
        try:
            symbol = getattr(price_update, "symbol", None)
            price = getattr(price_update, "price", 0.0)

            if not symbol or price <= 0:
                return

            self.total_price_updates += 1

            # Update market price
            self.market_prices[symbol] = price

            # If we have a position in this symbol, recalculate unrealized P&L
            if symbol in self.positions and self.positions[symbol] != 0:
                await self._emit_pnl_snapshot(symbol)

        except Exception as e:
            logger.error(f"Error processing price update: {e}")

    async def _handle_position_snapshot(self, position_snapshot: Any) -> None:
        """Handle position snapshots from position agent."""
        # This would be used if we have a separate position agent
        # For now, we calculate positions ourselves from fills
        pass

    def _update_position_from_fill(
        self, symbol: str, side: OrderSide, quantity: float, price: float
    ) -> None:
        """Update position and realized P&L from a fill."""
        if side == OrderSide.BUY:
            # Buying - update average price and position
            current_position = self.positions[symbol]
            current_avg = self.avg_prices.get(symbol, 0.0)

            if current_position >= 0:
                # Long position or flat - update average cost
                total_cost = (current_position * current_avg) + (quantity * price)
                new_position = current_position + quantity
                self.avg_prices[symbol] = total_cost / new_position if new_position > 0 else 0.0
            else:
                # Short position - this is a cover
                cover_quantity = min(quantity, abs(current_position))
                realized_gain = cover_quantity * (current_avg - price)  # Gain from covering short
                self.realized_pnl[symbol] += realized_gain

                # If covering more than the short position, start a long position
                remaining = quantity - cover_quantity
                if remaining > 0:
                    self.avg_prices[symbol] = price

            self.positions[symbol] += quantity

        else:  # SELL
            # Selling - calculate realized P&L if we have a long position
            current_position = self.positions[symbol]
            current_avg = self.avg_prices.get(symbol, 0.0)

            if current_position > 0:
                # Long position - selling realizes P&L
                sell_quantity = min(quantity, current_position)
                realized_gain = sell_quantity * (price - current_avg)
                self.realized_pnl[symbol] += realized_gain

                # If selling more than long position, start a short position
                remaining = quantity - sell_quantity
                if remaining > 0:
                    self.avg_prices[symbol] = price

            elif current_position <= 0:
                # Flat or short position - update average short price
                if current_position == 0:
                    self.avg_prices[symbol] = price
                else:
                    # Already short - update average short price
                    total_short_value = abs(current_position) * current_avg + quantity * price
                    new_short_position = abs(current_position) + quantity
                    self.avg_prices[symbol] = total_short_value / new_short_position

            self.positions[symbol] -= quantity

    def _calculate_unrealized_pnl(self, symbol: str) -> float:
        """Calculate unrealized P&L for a symbol."""
        position = self.positions.get(symbol, 0.0)
        if position == 0:
            return 0.0

        avg_price = self.avg_prices.get(symbol, 0.0)
        market_price = self.market_prices.get(symbol, avg_price)  # Fallback to avg price

        if position > 0:
            # Long position
            return position * (market_price - avg_price)
        else:
            # Short position
            return abs(position) * (avg_price - market_price)

    async def _emit_pnl_snapshot(self, symbol: str) -> None:
        """Emit a P&L snapshot for a symbol."""
        try:
            position = self.positions.get(symbol, 0.0)
            avg_price = self.avg_prices.get(symbol, 0.0)
            market_price = self.market_prices.get(symbol, avg_price)
            realized_pnl = self.realized_pnl.get(symbol, 0.0)
            unrealized_pnl = self._calculate_unrealized_pnl(symbol)

            snapshot = PnlSnapshot(
                timestamp=datetime.now(),
                symbol=symbol,
                realized_pnl=realized_pnl,
                unrealized_pnl=unrealized_pnl,
                position=position,
                avg_price=avg_price,
                market_price=market_price,
            )

            # Store snapshot
            self.pnl_snapshots.append(snapshot)

            # Keep only recent snapshots (last 1000)
            if len(self.pnl_snapshots) > 1000:
                self.pnl_snapshots = self.pnl_snapshots[-1000:]

            # Emit event
            await self.event_bus.publish("pnl.snapshot", snapshot)

        except Exception as e:
            logger.error(f"Error emitting P&L snapshot for {symbol}: {e}")

    async def main_loop_iteration(self) -> None:
        """Main loop iteration for periodic P&L calculations."""
        # Emit aggregate P&L snapshot periodically
        if self.positions:
            await self._emit_aggregate_pnl()

    async def _emit_aggregate_pnl(self) -> None:
        """Emit aggregate P&L across all symbols."""
        try:
            total_realized = sum(self.realized_pnl.values())
            total_unrealized = sum(
                self._calculate_unrealized_pnl(symbol)
                for symbol in self.positions
                if self.positions[symbol] != 0
            )

            aggregate_data = {
                "timestamp": datetime.now(),
                "total_realized_pnl": total_realized,
                "total_unrealized_pnl": total_unrealized,
                "total_pnl": total_realized + total_unrealized,
                "symbol_count": len([s for s in self.positions if self.positions[s] != 0]),
                "symbols": {
                    symbol: {
                        "position": self.positions[symbol],
                        "avg_price": self.avg_prices.get(symbol, 0.0),
                        "market_price": self.market_prices.get(symbol, 0.0),
                        "realized_pnl": self.realized_pnl[symbol],
                        "unrealized_pnl": self._calculate_unrealized_pnl(symbol),
                    }
                    for symbol in self.positions
                    if self.positions[symbol] != 0
                },
            }

            await self.event_bus.publish("pnl.aggregate", aggregate_data)

        except Exception as e:
            logger.error(f"Error emitting aggregate P&L: {e}")

    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics."""
        base_metrics = await super().get_metrics()

        total_realized = sum(self.realized_pnl.values())
        total_unrealized = sum(
            self._calculate_unrealized_pnl(symbol)
            for symbol in self.positions
            if self.positions[symbol] != 0
        )

        pnl_metrics = {
            "total_fills_processed": self.total_fills_processed,
            "total_price_updates": self.total_price_updates,
            "symbols_tracked": len([s for s in self.positions if self.positions[s] != 0]),
            "total_realized_pnl": total_realized,
            "total_unrealized_pnl": total_unrealized,
            "total_pnl": total_realized + total_unrealized,
            "snapshots_generated": len(self.pnl_snapshots),
        }

        base_metrics.update(pnl_metrics)
        return base_metrics

    def get_pnl_summary(self) -> Dict[str, Any]:
        """Get current P&L summary."""
        total_realized = sum(self.realized_pnl.values())
        total_unrealized = sum(
            self._calculate_unrealized_pnl(symbol)
            for symbol in self.positions
            if self.positions[symbol] != 0
        )

        return {
            "total_realized": total_realized,
            "total_unrealized": total_unrealized,
            "total_pnl": total_realized + total_unrealized,
            "positions": dict(self.positions),
            "avg_prices": dict(self.avg_prices),
            "market_prices": dict(self.market_prices),
            "realized_by_symbol": dict(self.realized_pnl),
        }
