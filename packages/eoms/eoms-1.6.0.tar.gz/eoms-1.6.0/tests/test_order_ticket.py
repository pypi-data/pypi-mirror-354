"""Test for Order Ticket functionality (M4-E1-T1)."""

import asyncio

import pytest

from eoms.brokers.base import OrderSide, OrderType
from eoms.brokers.sim_broker import SimBroker


class TestOrderTicketFunctionality:
    """Test the core functionality that OrderTicketWidget uses."""

    @pytest.mark.asyncio
    async def test_sim_broker_order_placement(self):
        """Test that we can place orders through SimBroker."""
        broker = SimBroker({"latency_ms": 1})
        await broker.connect()

        # Track events
        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Create an order like OrderTicketWidget would
        from eoms.brokers.base import OrderRequest

        order = OrderRequest(
            order_id="TEST001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        # Place order
        success = await broker.place_order(order)
        assert success is True

        # Wait for events
        await asyncio.sleep(0.1)

        # Should have at least ACK event
        assert len(events) >= 1
        ack_event = events[0]
        assert ack_event.event_type == "ACK"
        assert ack_event.order_id == "TEST001"
        assert ack_event.symbol == "AAPL"

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_sim_broker_limit_order(self):
        """Test limit order placement like OrderTicketWidget would do."""
        broker = SimBroker({"latency_ms": 1, "fill_probability": 0.0})  # Don't fill for this test
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Get market price first
        market_price = broker.get_market_price("AAPL")
        assert market_price > 0

        # Create limit order
        from eoms.brokers.base import OrderRequest

        order = OrderRequest(
            order_id="TEST002",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=market_price - 1.0,  # Limit below market
        )

        success = await broker.place_order(order)
        assert success is True

        await asyncio.sleep(0.1)

        # Should have ACK
        assert len(events) >= 1
        assert events[0].event_type == "ACK"
        assert events[0].order_id == "TEST002"

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_sim_broker_cancel_order(self):
        """Test order cancellation like OrderTicketWidget would do."""
        broker = SimBroker({"latency_ms": 1, "fill_probability": 0.0})
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order first
        from eoms.brokers.base import OrderRequest

        order = OrderRequest(
            order_id="TEST003",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=50.0,  # Well below market, won't fill
        )

        await broker.place_order(order)
        await asyncio.sleep(0.05)

        # Cancel the order
        success = await broker.cancel_order("TEST003")
        assert success is True

        await asyncio.sleep(0.05)

        # Should have ACK and CANCEL events
        event_types = [e.event_type for e in events]
        assert "ACK" in event_types
        assert "CANCEL" in event_types

        await broker.disconnect()

    def test_market_price_retrieval(self):
        """Test market price functionality used by OrderTicketWidget."""
        broker = SimBroker()

        # Should work without connection for price queries
        price = broker.get_market_price("AAPL")
        assert price > 0
        assert isinstance(price, float)

        # Different symbols should give different prices
        price1 = broker.get_market_price("AAPL")
        price2 = broker.get_market_price("MSFT")
        # Prices might be the same occasionally due to randomization,
        # but the function should work for both
        assert price1 > 0
        assert price2 > 0

    @pytest.mark.asyncio
    async def test_order_tracking_like_widget(self):
        """Test order tracking functionality like OrderTicketWidget."""
        broker = SimBroker({"latency_ms": 1})
        await broker.connect()

        # Track orders like the widget does
        placed_orders = {}

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place multiple orders
        from eoms.brokers.base import OrderRequest

        for i in range(3):
            order_id = f"TEST00{i+1}"
            order = OrderRequest(
                order_id=order_id,
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100.0,
                price=50.0,  # Won't fill
            )

            success = await broker.place_order(order)
            assert success
            placed_orders[order_id] = order

        await asyncio.sleep(0.1)

        # Should have 3 orders placed
        assert len(placed_orders) == 3

        # Should have at least 3 ACK events
        ack_events = [e for e in events if e.event_type == "ACK"]
        assert len(ack_events) >= 3

        # Cancel last order (like "Cancel Last" button)
        last_order_id = list(placed_orders.keys())[-1]
        success = await broker.cancel_order(last_order_id)
        assert success

        # Remove from tracking
        del placed_orders[last_order_id]
        assert len(placed_orders) == 2

        await broker.disconnect()
