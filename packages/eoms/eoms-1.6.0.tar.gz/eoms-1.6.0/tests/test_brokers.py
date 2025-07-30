"""Tests for broker infrastructure."""

from datetime import datetime

import pytest

from eoms.brokers import BrokerEvent, NullBroker, OrderRequest
from eoms.brokers.base import OrderSide, OrderStatus, OrderType


class TestOrderRequest:
    """Test OrderRequest data class."""

    def test_order_request_creation(self):
        """Test creating an order request."""
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )

        assert order.order_id == "O001"
        assert order.symbol == "AAPL"
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.LIMIT
        assert order.quantity == 100.0
        assert order.price == 150.50
        assert order.time_in_force == "DAY"

    def test_order_request_to_dict(self):
        """Test converting order request to dictionary."""
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )

        order_dict = order.to_dict()

        assert order_dict["order_id"] == "O001"
        assert order_dict["symbol"] == "AAPL"
        assert order_dict["side"] == "BUY"
        assert order_dict["order_type"] == "LIMIT"
        assert order_dict["quantity"] == 100.0
        assert order_dict["price"] == 150.50


class TestBrokerEvent:
    """Test BrokerEvent data class."""

    def test_broker_event_creation(self):
        """Test creating a broker event."""
        timestamp = datetime.now()
        event = BrokerEvent(
            event_type="ACK",
            order_id="O001",
            symbol="AAPL",
            timestamp=timestamp,
            status=OrderStatus.ACKNOWLEDGED,
        )

        assert event.event_type == "ACK"
        assert event.order_id == "O001"
        assert event.symbol == "AAPL"
        assert event.timestamp == timestamp
        assert event.status == OrderStatus.ACKNOWLEDGED

    def test_broker_event_to_dict(self):
        """Test converting broker event to dictionary."""
        timestamp = datetime.now()
        event = BrokerEvent(
            event_type="FILL",
            order_id="O001",
            symbol="AAPL",
            timestamp=timestamp,
            quantity=100.0,
            price=150.50,
            status=OrderStatus.FILLED,
        )

        event_dict = event.to_dict()

        assert event_dict["event_type"] == "FILL"
        assert event_dict["order_id"] == "O001"
        assert event_dict["symbol"] == "AAPL"
        assert event_dict["timestamp"] == timestamp.isoformat()
        assert event_dict["quantity"] == 100.0
        assert event_dict["price"] == 150.50
        assert event_dict["status"] == "FILLED"


class TestNullBroker:
    """Test NullBroker implementation."""

    def test_null_broker_creation(self):
        """Test creating a null broker."""
        broker = NullBroker()

        assert broker.get_name() == "NullBroker"
        assert not broker.is_connected()
        assert broker.config == {}

    def test_null_broker_with_config(self):
        """Test creating a null broker with config."""
        config = {"setting1": "value1"}
        broker = NullBroker(config)

        assert broker.config == config

    @pytest.mark.asyncio
    async def test_connect_disconnect(self):
        """Test broker connection and disconnection."""
        broker = NullBroker()

        # Initially not connected
        assert not broker.is_connected()

        # Connect
        result = await broker.connect()
        assert result is True
        assert broker.is_connected()

        # Disconnect
        await broker.disconnect()
        assert not broker.is_connected()

    @pytest.mark.asyncio
    async def test_place_order_success(self):
        """Test successful order placement."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event: BrokerEvent):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )

        result = await broker.place_order(order)
        assert result is True

        # Check that order was stored
        orders = broker.get_orders()
        assert "O001" in orders
        assert orders["O001"] == order

        # Check that acknowledgment event was emitted
        assert len(events) == 1
        event = events[0]
        assert event.event_type == "ACK"
        assert event.order_id == "O001"
        assert event.symbol == "AAPL"
        assert event.status == OrderStatus.ACKNOWLEDGED

    @pytest.mark.asyncio
    async def test_place_order_disconnected(self):
        """Test order placement when disconnected."""
        broker = NullBroker()

        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )

        result = await broker.place_order(order)
        assert result is False

    @pytest.mark.asyncio
    async def test_amend_order_success(self):
        """Test successful order amendment."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event: BrokerEvent):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order first
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )
        await broker.place_order(order)

        # Clear events from placement
        events.clear()

        # Amend order
        result = await broker.amend_order("O001", price=151.00, quantity=200.0)
        assert result is True

        # Check that order was updated
        orders = broker.get_orders()
        amended_order = orders["O001"]
        assert amended_order.price == 151.00
        assert amended_order.quantity == 200.0

        # Check that acknowledgment event was emitted
        assert len(events) == 1
        event = events[0]
        assert event.event_type == "ACK"
        assert event.order_id == "O001"
        assert "amendment acknowledged" in event.message

    @pytest.mark.asyncio
    async def test_amend_order_not_found(self):
        """Test amending non-existent order."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event: BrokerEvent):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Amend non-existent order
        result = await broker.amend_order("O999", price=151.00)
        assert result is False

        # Check that reject event was emitted
        assert len(events) == 1
        event = events[0]
        assert event.event_type == "REJECT"
        assert event.order_id == "O999"
        assert event.status == OrderStatus.REJECTED
        assert "not found" in event.message

    @pytest.mark.asyncio
    async def test_cancel_order_success(self):
        """Test successful order cancellation."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event: BrokerEvent):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Place order first
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )
        await broker.place_order(order)

        # Clear events from placement
        events.clear()

        # Cancel order
        result = await broker.cancel_order("O001")
        assert result is True

        # Check that order was removed
        orders = broker.get_orders()
        assert "O001" not in orders

        # Check that cancellation event was emitted
        assert len(events) == 1
        event = events[0]
        assert event.event_type == "CANCEL"
        assert event.order_id == "O001"
        assert event.status == OrderStatus.CANCELLED

    @pytest.mark.asyncio
    async def test_cancel_order_not_found(self):
        """Test cancelling non-existent order."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback
        events = []

        async def event_callback(event: BrokerEvent):
            events.append(event)

        broker.set_event_callback(event_callback)

        # Cancel non-existent order
        result = await broker.cancel_order("O999")
        assert result is False

        # Check that reject event was emitted
        assert len(events) == 1
        event = events[0]
        assert event.event_type == "REJECT"
        assert event.order_id == "O999"
        assert event.status == OrderStatus.REJECTED
        assert "not found" in event.message

    @pytest.mark.asyncio
    async def test_event_callback_error_handling(self):
        """Test that errors in event callbacks don't crash the broker."""
        broker = NullBroker()
        await broker.connect()

        # Set up event callback that raises an exception
        async def failing_callback(event: BrokerEvent):
            raise ValueError("Test error")

        broker.set_event_callback(failing_callback)

        # Place order - should not raise exception despite callback error
        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.50,
        )

        # This should not raise an exception
        result = await broker.place_order(order)
        assert result is True

    def test_clear_orders(self):
        """Test clearing all orders."""
        broker = NullBroker()

        # Add some orders manually
        order1 = OrderRequest("O001", "AAPL", OrderSide.BUY, OrderType.LIMIT, 100.0)
        order2 = OrderRequest("O002", "MSFT", OrderSide.SELL, OrderType.MARKET, 50.0)
        broker._orders["O001"] = order1
        broker._orders["O002"] = order2

        # Verify orders exist
        assert len(broker.get_orders()) == 2

        # Clear orders
        broker.clear_orders()

        # Verify orders are cleared
        assert len(broker.get_orders()) == 0
