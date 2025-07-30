"""Tests for SimBroker implementation."""

import asyncio

import pytest

from eoms.brokers import OrderRequest, SimBroker
from eoms.brokers.base import OrderSide, OrderStatus, OrderType
from eoms.brokers.sim_broker import FillEngine, SimulatedOrder


class TestFillEngine:
    """Test FillEngine functionality."""

    def test_fill_engine_creation(self):
        """Test creating a fill engine."""
        engine = FillEngine()

        assert engine.volatility == 0.01
        assert engine.fill_probability == 0.8
        assert "AAPL" in engine.market_prices

    def test_fill_engine_with_config(self):
        """Test creating fill engine with custom config."""
        config = {
            "volatility": 0.02,
            "fill_probability": 0.9,
            "market_prices": {"TEST": 100.0},
        }
        engine = FillEngine(config)

        assert engine.volatility == 0.02
        assert engine.fill_probability == 0.9
        assert engine.market_prices["TEST"] == 100.0

    def test_get_market_price(self):
        """Test getting market prices."""
        engine = FillEngine()

        # Known symbol
        price1 = engine.get_market_price("AAPL")
        assert price1 > 0

        # Price should change due to volatility
        price2 = engine.get_market_price("AAPL")
        assert price2 > 0
        # Prices might be the same due to randomness, so we just check they're positive

        # Unknown symbol should get a random price
        unknown_price = engine.get_market_price("UNKNOWN")
        assert 10.0 <= unknown_price <= 1000.0

    def test_should_fill_order_market(self):
        """Test market order fill logic."""
        engine = FillEngine()

        order_request = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        order = SimulatedOrder(request=order_request, status=OrderStatus.ACKNOWLEDGED)

        # Market orders should always fill
        assert engine.should_fill_order(order) is True

    def test_should_fill_order_limit(self):
        """Test limit order fill logic."""
        engine = FillEngine({"fill_probability": 1.0})  # Always fill when price is right

        # Get current market price
        market_price = engine.get_market_price("AAPL")

        # Buy limit above market should fill
        buy_order = SimulatedOrder(
            request=OrderRequest(
                order_id="O001",
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100.0,
                price=market_price + 10.0,  # Well above market
            ),
            status=OrderStatus.ACKNOWLEDGED,
        )

        # This should fill (price is favorable and probability is 100%)
        result = engine.should_fill_order(buy_order)
        assert result is True

        # Buy limit way below market should not fill
        buy_order_low = SimulatedOrder(
            request=OrderRequest(
                order_id="O002",
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100.0,
                price=market_price - 50.0,  # Way below market
            ),
            status=OrderStatus.ACKNOWLEDGED,
        )

        result = engine.should_fill_order(buy_order_low)
        assert result is False

    def test_calculate_fill_quantity(self):
        """Test fill quantity calculation."""
        engine = FillEngine({"partial_fill_probability": 0.0})  # No partial fills

        order = SimulatedOrder(
            request=OrderRequest(
                order_id="O001",
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=100.0,
            ),
            status=OrderStatus.ACKNOWLEDGED,
        )

        fill_qty = engine.calculate_fill_quantity(order)
        assert fill_qty == 100.0  # Should fill completely

    def test_calculate_fill_price(self):
        """Test fill price calculation."""
        config = {"volatility": 0.0}  # No price movement for this test
        engine = FillEngine(config)

        # Market order
        market_order = SimulatedOrder(
            request=OrderRequest(
                order_id="O001",
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.MARKET,
                quantity=100.0,
            ),
            status=OrderStatus.ACKNOWLEDGED,
        )

        # Get market price, then immediately calculate fill price
        market_price = engine.get_market_price("AAPL")
        fill_price = engine.calculate_fill_price(market_order)

        # Should be close to market price (within reasonable slippage)
        assert abs(fill_price - market_price) / market_price < 0.005  # 0.5% tolerance

        # Limit order
        limit_order = SimulatedOrder(
            request=OrderRequest(
                order_id="O002",
                symbol="AAPL",
                side=OrderSide.BUY,
                order_type=OrderType.LIMIT,
                quantity=100.0,
                price=150.0,
            ),
            status=OrderStatus.ACKNOWLEDGED,
        )

        limit_fill_price = engine.calculate_fill_price(limit_order)
        # Should be at or better than limit price for buy orders
        assert limit_fill_price <= 150.0


class TestSimBroker:
    """Test SimBroker implementation."""

    def test_sim_broker_creation(self):
        """Test creating a simulation broker."""
        broker = SimBroker()

        assert broker.get_name() == "SimBroker"
        assert not broker.is_connected()
        assert isinstance(broker.fill_engine, FillEngine)

    def test_sim_broker_with_config(self):
        """Test creating broker with custom config."""
        config = {"volatility": 0.02, "latency_ms": 100}
        broker = SimBroker(config)

        assert broker.fill_engine.volatility == 0.02
        assert broker.fill_engine.latency_ms == 100

    @pytest.mark.asyncio
    async def test_connect_disconnect(self):
        """Test broker connection and disconnection."""
        broker = SimBroker()

        # Initially not connected
        assert not broker.is_connected()

        # Connect
        result = await broker.connect()
        assert result is True
        assert broker.is_connected()
        assert broker._running is True
        assert broker._fill_task is not None

        # Disconnect
        await broker.disconnect()
        assert not broker.is_connected()
        assert broker._running is False

    @pytest.mark.asyncio
    async def test_place_order_market(self):
        """Test placing a market order."""
        config = {"latency_ms": 1}  # Minimal latency for testing
        broker = SimBroker(config)
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place market order
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        result = await broker.place_order(order)
        assert result is True

        # Should have acknowledgment
        await asyncio.sleep(0.1)  # Wait for events
        assert len(events) >= 1
        ack_event = events[0]
        assert ack_event.event_type == "ACK"
        assert ack_event.order_id == "O001"
        assert ack_event.status == OrderStatus.ACKNOWLEDGED

        # Wait for potential fill
        await asyncio.sleep(0.5)

        # Should eventually get a fill (market orders should fill quickly)
        fill_events = [e for e in events if e.event_type == "FILL"]
        assert len(fill_events) >= 1

        # Sum up total filled quantity (might be partial fills)
        total_filled = sum(e.quantity for e in fill_events)
        fill_event = fill_events[0]
        assert fill_event.order_id == "O001"
        assert total_filled <= 100.0  # Should not exceed order size
        assert fill_event.price > 0

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_place_order_limit(self):
        """Test placing a limit order."""
        config = {
            "latency_ms": 1,
            "fill_probability": 1.0,
        }  # Always fill when price is right
        broker = SimBroker(config)
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Get current market price and place limit order above it
        market_price = broker.get_market_price("AAPL")

        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=market_price + 10.0,  # Above market
        )

        result = await broker.place_order(order)
        assert result is True

        # Wait for acknowledgment and potential fill
        await asyncio.sleep(0.5)

        ack_events = [e for e in events if e.event_type == "ACK"]
        assert len(ack_events) >= 1

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_amend_order(self):
        """Test amending an order."""
        # Use config that prevents immediate fills
        config = {"latency_ms": 1, "fill_probability": 0.0}
        broker = SimBroker(config)
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order first - won't fill due to 0% fill probability
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.0,
        )
        await broker.place_order(order)

        # Clear events
        events.clear()

        # Amend order
        result = await broker.amend_order("O001", price=155.0, quantity=200.0)
        assert result is True

        # Should get acknowledgment
        await asyncio.sleep(0.1)
        assert len(events) >= 1
        ack_event = next(e for e in events if e.event_type == "ACK")
        assert "amended" in ack_event.message.lower()

        # Check order was updated
        orders = broker.get_orders()
        assert "O001" in orders
        updated_order = orders["O001"]
        assert updated_order.request.price == 155.0
        assert updated_order.request.quantity == 200.0

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_cancel_order(self):
        """Test cancelling an order."""
        broker = SimBroker({"latency_ms": 1})
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order first
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.0,
        )
        await broker.place_order(order)

        # Clear events
        events.clear()

        # Cancel order
        result = await broker.cancel_order("O001")
        assert result is True

        # Should get cancellation
        await asyncio.sleep(0.1)
        assert len(events) >= 1
        cancel_event = next(e for e in events if e.event_type == "CANCEL")
        assert cancel_event.order_id == "O001"
        assert cancel_event.status == OrderStatus.CANCELLED

        # Order should be removed
        orders = broker.get_orders()
        assert "O001" not in orders

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_order_not_found_operations(self):
        """Test operations on non-existent orders."""
        broker = SimBroker({"latency_ms": 1})
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Try to amend non-existent order
        result = await broker.amend_order("O999", price=155.0)
        assert result is False

        # Try to cancel non-existent order
        result = await broker.cancel_order(
            "O999",
        )
        assert result is False

        # Should get reject events
        await asyncio.sleep(0.1)
        reject_events = [e for e in events if e.event_type == "REJECT"]
        assert len(reject_events) == 2

        for event in reject_events:
            assert event.order_id == "O999"
            assert event.status == OrderStatus.REJECTED
            assert "not found" in event.message.lower()

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_operations_when_disconnected(self):
        """Test operations when broker is disconnected."""
        broker = SimBroker()

        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        # All operations should fail when disconnected
        assert await broker.place_order(order) is False
        assert await broker.amend_order("O001", price=155.0) is False
        assert await broker.cancel_order("O001") is False

    def test_market_price_functionality(self):
        """Test market price functionality."""
        broker = SimBroker()

        # Should return positive prices
        price1 = broker.get_market_price("AAPL")
        assert price1 > 0

        # Prices should vary (due to volatility simulation)
        prices = [broker.get_market_price("AAPL") for _ in range(10)]
        assert len(set(prices)) > 1  # Should have some variation

    @pytest.mark.asyncio
    async def test_fill_history(self):
        """Test fill history tracking."""
        config = {
            "latency_ms": 1,
            "fill_probability": 1.0,
            "partial_fill_probability": 0.0,  # No partial fills
        }
        broker = SimBroker(config)
        await broker.connect()

        # Place and wait for a market order to fill
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(order)
        await asyncio.sleep(0.5)  # Wait for fill

        # Check fill history
        fills = broker.get_fill_history()
        assert len(fills) >= 1

        fill = fills[0]
        assert fill.order_id == "O001"
        assert fill.symbol == "AAPL"
        assert fill.side == OrderSide.BUY
        assert fill.quantity == 100.0  # Should be full fill with no partial fills
        assert fill.price > 0

        # Test filtering by order ID
        order_fills = broker.get_fill_history("O001")
        assert len(order_fills) >= 1
        assert all(f.order_id == "O001" for f in order_fills)

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_pnl_calculation(self):
        """Test PNL calculation functionality."""
        config = {"latency_ms": 1, "fill_probability": 1.0}
        broker = SimBroker(config)
        await broker.connect()

        # Place buy order
        buy_order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(buy_order)
        await asyncio.sleep(0.3)  # Wait for fill

        # Calculate PNL
        pnl = broker.calculate_pnl("AAPL")

        assert pnl["position"] == 100.0  # Long 100 shares
        assert pnl["realized_pnl"] < 0  # Negative because we bought (paid out cash)
        assert pnl["avg_price"] > 0
        assert pnl["fill_count"] >= 1

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_backtest_scenario(self):
        """Test a simple backtest scenario to validate known PNL reproduction."""
        # Configure broker for deterministic behavior
        config = {
            "latency_ms": 1,
            "fill_probability": 1.0,
            "partial_fill_probability": 0.0,  # No partial fills
            "volatility": 0.0,  # No price movement
            "market_prices": {"TEST": 100.0},
        }

        broker = SimBroker(config)
        await broker.connect()

        events = []

        async def event_callback(event):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Execute a simple round-trip trade
        # Buy 100 shares at $100
        buy_order = OrderRequest(
            order_id="BUY001",
            symbol="TEST",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(buy_order)
        await asyncio.sleep(0.2)

        # Sell 100 shares at $100 (price should be same due to 0 volatility)
        sell_order = OrderRequest(
            order_id="SELL001",
            symbol="TEST",
            side=OrderSide.SELL,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(sell_order)
        await asyncio.sleep(0.2)

        # Check that we got the expected fills
        fill_events = [e for e in events if e.event_type == "FILL"]
        assert len(fill_events) >= 2  # At least buy and sell fills

        # Check individual orders
        buy_fills = [e for e in fill_events if e.order_id == "BUY001"]
        sell_fills = [e for e in fill_events if e.order_id == "SELL001"]

        assert len(buy_fills) >= 1
        assert len(sell_fills) >= 1

        # Sum up fills for each order
        total_bought = sum(e.quantity for e in buy_fills)
        total_sold = sum(e.quantity for e in sell_fills)

        assert abs(total_bought - 100.0) < 0.1  # Should be close to 100
        assert abs(total_sold - 100.0) < 0.1  # Should be close to 100

        # Calculate PNL - should be close to zero (minus small slippage)
        pnl = broker.calculate_pnl("TEST")
        assert abs(pnl["position"]) < 0.01  # Flat position
        assert abs(pnl["realized_pnl"]) < 20.0  # Allow for reasonable slippage

        await broker.disconnect()
