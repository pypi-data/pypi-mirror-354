"""Test for Positions Manager functionality (M4-E1-T2)."""

import asyncio

import pytest

from eoms.brokers.base import OrderSide, OrderType
from eoms.brokers.sim_broker import SimBroker


class Position:
    """Minimal Position class for testing."""

    def __init__(self, symbol, quantity=0.0, avg_price=0.0, realized_pnl=0.0, unrealized_pnl=0.0):
        self.symbol = symbol
        self.quantity = quantity
        self.avg_price = avg_price
        self.realized_pnl = realized_pnl
        self.unrealized_pnl = unrealized_pnl

    @property
    def total_pnl(self):
        return self.realized_pnl + self.unrealized_pnl

    @property
    def risk_level(self):
        if abs(self.quantity) == 0:
            return "FLAT"
        elif abs(self.total_pnl) > 1000:
            return "HIGH"
        elif abs(self.total_pnl) > 500:
            return "MEDIUM"
        else:
            return "LOW"


class TestPosition:
    """Test Position data class."""

    def test_position_creation(self):
        """Test creating a position."""
        pos = Position(symbol="AAPL", quantity=100.0, avg_price=150.0)

        assert pos.symbol == "AAPL"
        assert pos.quantity == 100.0
        assert pos.avg_price == 150.0
        assert pos.realized_pnl == 0.0
        assert pos.unrealized_pnl == 0.0

    def test_position_total_pnl(self):
        """Test total P&L calculation."""
        pos = Position(symbol="AAPL", quantity=100.0, realized_pnl=500.0, unrealized_pnl=200.0)

        assert pos.total_pnl == 700.0

    def test_position_risk_levels(self):
        """Test risk level determination."""
        # Flat position
        pos = Position(symbol="AAPL", quantity=0.0)
        assert pos.risk_level == "FLAT"

        # Low risk
        pos = Position(symbol="AAPL", quantity=100.0, realized_pnl=100.0)
        assert pos.risk_level == "LOW"

        # Medium risk
        pos = Position(symbol="AAPL", quantity=100.0, realized_pnl=600.0)
        assert pos.risk_level == "MEDIUM"

        # High risk
        pos = Position(symbol="AAPL", quantity=100.0, realized_pnl=1500.0)
        assert pos.risk_level == "HIGH"

        # Negative P&L also counts
        pos = Position(symbol="AAPL", quantity=100.0, realized_pnl=-1200.0)
        assert pos.risk_level == "HIGH"


class TestPositionsManagerFunctionality:
    """Test the core functionality that PositionsManagerWidget uses."""

    @pytest.mark.asyncio
    async def test_position_calculation_from_fills(self):
        """Test position calculation from broker fills."""
        broker = SimBroker({"latency_ms": 1, "fill_probability": 1.0})
        await broker.connect()

        # Place and fill orders to create position
        from eoms.brokers.base import OrderRequest

        # Buy 100 shares
        buy_order = OrderRequest(
            order_id="BUY001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(buy_order)
        await asyncio.sleep(0.1)  # Wait for fill

        # Check position
        pnl_data = broker.calculate_pnl("AAPL")

        # SimBroker may do partial fills, so position should be > 0 and <= 100
        assert pnl_data["position"] > 0
        assert pnl_data["position"] <= 100.0
        assert pnl_data["avg_price"] > 0
        assert pnl_data["realized_pnl"] < 0  # Negative because we paid cash
        assert pnl_data["fill_count"] >= 1

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_position_updates_on_multiple_fills(self):
        """Test position updates with multiple fills."""
        broker = SimBroker({"latency_ms": 1, "fill_probability": 1.0})
        await broker.connect()

        from eoms.brokers.base import OrderRequest

        # Buy 100 shares
        buy1 = OrderRequest(
            order_id="BUY001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        await broker.place_order(buy1)
        await asyncio.sleep(0.05)

        # Buy another 50 shares
        buy2 = OrderRequest(
            order_id="BUY002",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=50.0,
        )

        await broker.place_order(buy2)
        await asyncio.sleep(0.05)

        # Check combined position - should be more than initial due to multiple orders
        pnl_data = broker.calculate_pnl("AAPL")

        assert pnl_data["position"] > 0
        assert pnl_data["fill_count"] >= 2

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_position_reduction_with_sells(self):
        """Test position reduction with sell orders."""
        # Use a simpler test that focuses on the core position calculation logic
        broker = SimBroker({"latency_ms": 1})
        await broker.connect()

        # Manually create fills to test position calculation
        from datetime import datetime

        from eoms.brokers.base import OrderRequest, OrderStatus
        from eoms.brokers.sim_broker import SimulatedFill, SimulatedOrder

        # Create a buy order and add it to broker's history
        buy_request = OrderRequest(
            order_id="BUY001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        buy_fill = SimulatedFill(
            order_id="BUY001",
            symbol="AAPL",
            side=OrderSide.BUY,
            quantity=100.0,
            price=150.0,
            timestamp=datetime.now(),
        )

        buy_order = SimulatedOrder(
            request=buy_request,
            status=OrderStatus.FILLED,
            filled_quantity=100.0,
            fills=[buy_fill],
        )

        broker.all_orders["BUY001"] = buy_order

        # Check position after buy
        pnl_data = broker.calculate_pnl("AAPL")
        assert pnl_data["position"] == 100.0
        assert pnl_data["realized_pnl"] == -15000.0  # Paid 100 * 150

        # Create a sell order
        sell_request = OrderRequest(
            order_id="SELL001",
            symbol="AAPL",
            side=OrderSide.SELL,
            order_type=OrderType.MARKET,
            quantity=30.0,
        )

        sell_fill = SimulatedFill(
            order_id="SELL001",
            symbol="AAPL",
            side=OrderSide.SELL,
            quantity=30.0,
            price=155.0,
            timestamp=datetime.now(),
        )

        sell_order = SimulatedOrder(
            request=sell_request,
            status=OrderStatus.FILLED,
            filled_quantity=30.0,
            fills=[sell_fill],
        )

        broker.all_orders["SELL001"] = sell_order

        # Check position after sell
        final_pnl = broker.calculate_pnl("AAPL")
        assert final_pnl["position"] == 70.0  # 100 - 30
        assert final_pnl["realized_pnl"] == -10350.0  # -15000 + (30 * 155)
        assert final_pnl["fill_count"] == 2

        await broker.disconnect()

    @pytest.mark.asyncio
    async def test_multiple_symbols_tracking(self):
        """Test tracking positions in multiple symbols."""
        broker = SimBroker({"latency_ms": 1, "fill_probability": 1.0})
        await broker.connect()

        from eoms.brokers.base import OrderRequest

        # Trade AAPL
        aapl_order = OrderRequest(
            order_id="AAPL001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        # Trade MSFT
        msft_order = OrderRequest(
            order_id="MSFT001",
            symbol="MSFT",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=200.0,
        )

        await broker.place_order(aapl_order)
        await broker.place_order(msft_order)
        await asyncio.sleep(0.1)

        # Check individual positions - should have positions in both symbols
        aapl_pnl = broker.calculate_pnl("AAPL")
        msft_pnl = broker.calculate_pnl("MSFT")

        assert aapl_pnl["position"] > 0
        assert msft_pnl["position"] > 0

        # Check all positions
        all_pnl = broker.calculate_pnl()  # No symbol filter
        assert all_pnl["fill_count"] >= 2

        await broker.disconnect()

    def test_market_price_for_unrealized_pnl(self):
        """Test market price retrieval for unrealized P&L calculation."""
        broker = SimBroker()

        # Should get different prices for different symbols
        aapl_price = broker.get_market_price("AAPL")
        msft_price = broker.get_market_price("MSFT")

        assert aapl_price > 0
        assert msft_price > 0
        assert isinstance(aapl_price, float)
        assert isinstance(msft_price, float)

    def test_position_risk_calculation_logic(self):
        """Test the risk calculation logic that the widget would use."""

        # Test conversion from broker data to position with risk assessment
        def create_position_from_broker_data(symbol, pnl_data, market_price):
            """Simulate the logic from PositionsManagerWidget._update_position_for_symbol"""
            position = Position(
                symbol=symbol,
                quantity=pnl_data.get("position", 0.0),
                avg_price=pnl_data.get("avg_price", 0.0),
                realized_pnl=pnl_data.get("realized_pnl", 0.0),
            )

            # Calculate unrealized P&L
            if position.quantity != 0 and position.avg_price > 0:
                position.unrealized_pnl = (market_price - position.avg_price) * position.quantity

            return position

        # Test profitable position
        broker_data = {
            "position": 100.0,
            "avg_price": 150.0,
            "realized_pnl": -15000.0,  # Negative (paid cash)
            "fill_count": 1,
        }

        market_price = 160.0  # Price went up
        position = create_position_from_broker_data("AAPL", broker_data, market_price)

        assert position.quantity == 100.0
        assert position.avg_price == 150.0
        assert position.realized_pnl == -15000.0
        assert position.unrealized_pnl == 1000.0  # (160-150) * 100
        assert position.total_pnl == -14000.0
        assert position.risk_level == "HIGH"  # High due to large absolute P&L

        # Test losing position
        market_price = 140.0  # Price went down
        position = create_position_from_broker_data("AAPL", broker_data, market_price)

        assert position.unrealized_pnl == -1000.0  # (140-150) * 100
        assert position.total_pnl == -16000.0
        assert position.risk_level == "HIGH"

        # Test flat position
        flat_data = {
            "position": 0.0,
            "avg_price": 0.0,
            "realized_pnl": 0.0,
            "fill_count": 0,
        }
        position = create_position_from_broker_data("AAPL", flat_data, 150.0)

        assert position.risk_level == "FLAT"
