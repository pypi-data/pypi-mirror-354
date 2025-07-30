"""Test for Order Manager functionality (M4-E1-T3)."""

from datetime import datetime

from eoms.brokers.base import BrokerEvent, OrderSide, OrderStatus, OrderType


# Define minimal classes for testing without GUI dependencies
class OrderInfo:
    """Minimal OrderInfo class for testing."""

    def __init__(
        self,
        order_id,
        symbol,
        side,
        order_type,
        quantity,
        price=None,
        filled_quantity=0.0,
        remaining_quantity=None,
        status=OrderStatus.NEW,
    ):
        self.order_id = order_id
        self.symbol = symbol
        self.side = side
        self.order_type = order_type
        self.quantity = quantity
        self.price = price
        self.filled_quantity = filled_quantity
        self.remaining_quantity = remaining_quantity if remaining_quantity is not None else quantity
        self.status = status
        self.timestamp = datetime.now()
        self.last_updated = datetime.now()

    @property
    def fill_percentage(self):
        if self.quantity == 0:
            return 0.0
        return (self.filled_quantity / self.quantity) * 100.0

    @property
    def avg_fill_price(self):
        return self.price


class OrderDataManager:
    """Simple order data manager for testing order management logic."""

    def __init__(self):
        self.orders = {}
        self.order_list = []

    def add_order(self, order):
        """Add a new order."""
        self.orders[order.order_id] = order
        self.order_list.append(order.order_id)

    def update_order(self, order_id, order):
        """Update an existing order."""
        if order_id in self.orders:
            self.orders[order_id] = order

    def get_order(self, order_id):
        """Get order by ID."""
        return self.orders.get(order_id)

    def get_order_at_index(self, index):
        """Get order at index."""
        if 0 <= index < len(self.order_list):
            order_id = self.order_list[index]
            return self.orders[order_id]
        return None

    def filter_orders(self, symbol_filter=None, side_filter=None, status_filter=None):
        """Filter orders based on criteria."""
        filtered = []

        for order_id in self.order_list:
            order = self.orders[order_id]

            # Apply filters
            if symbol_filter and symbol_filter.upper() not in order.symbol.upper():
                continue
            if side_filter and side_filter != "All" and order.side.value != side_filter:
                continue
            if status_filter and status_filter != "All" and order.status.value != status_filter:
                continue

            filtered.append(order)

        return filtered

    def clear_orders(self):
        """Clear all orders."""
        self.orders.clear()
        self.order_list.clear()


class TestOrderInfo:
    """Test OrderInfo data class."""

    def test_order_info_creation(self):
        """Test creating order info."""
        order = OrderInfo(
            order_id="TEST001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.0,
        )

        assert order.order_id == "TEST001"
        assert order.symbol == "AAPL"
        assert order.side == OrderSide.BUY
        assert order.order_type == OrderType.LIMIT
        assert order.quantity == 100.0
        assert order.price == 150.0
        assert order.filled_quantity == 0.0
        assert order.remaining_quantity == 100.0
        assert order.status == OrderStatus.NEW

    def test_fill_percentage_calculation(self):
        """Test fill percentage calculation."""
        order = OrderInfo(
            order_id="TEST001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
            filled_quantity=25.0,
        )

        assert order.fill_percentage == 25.0

        # Test fully filled
        order.filled_quantity = 100.0
        assert order.fill_percentage == 100.0

        # Test empty order
        order.quantity = 0.0
        assert order.fill_percentage == 0.0

    def test_market_order_display(self):
        """Test market order without price."""
        order = OrderInfo(
            order_id="TEST001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        assert order.price is None
        assert order.avg_fill_price is None


class TestOrderDataManager:
    """Test OrderDataManager functionality."""

    def test_add_and_retrieve_orders(self):
        """Test adding and retrieving orders."""
        manager = OrderDataManager()

        order1 = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        order2 = OrderInfo("TEST002", "MSFT", OrderSide.SELL, OrderType.LIMIT, 200.0, 250.0)

        manager.add_order(order1)
        manager.add_order(order2)

        assert len(manager.order_list) == 2
        assert manager.get_order("TEST001") == order1
        assert manager.get_order("TEST002") == order2
        assert manager.get_order_at_index(0) == order1
        assert manager.get_order_at_index(1) == order2

    def test_update_order(self):
        """Test updating an existing order."""
        manager = OrderDataManager()

        original_order = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.LIMIT, 100.0, 150.0)
        manager.add_order(original_order)

        # Update with partial fill
        updated_order = OrderInfo(
            "TEST001",
            "AAPL",
            OrderSide.BUY,
            OrderType.LIMIT,
            100.0,
            150.0,
            filled_quantity=25.0,
            remaining_quantity=75.0,
            status=OrderStatus.PARTIALLY_FILLED,
        )

        manager.update_order("TEST001", updated_order)

        retrieved = manager.get_order("TEST001")
        assert retrieved.filled_quantity == 25.0
        assert retrieved.remaining_quantity == 75.0
        assert retrieved.status == OrderStatus.PARTIALLY_FILLED

    def test_filter_by_symbol(self):
        """Test filtering orders by symbol."""
        manager = OrderDataManager()

        order1 = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        order2 = OrderInfo("TEST002", "MSFT", OrderSide.SELL, OrderType.LIMIT, 200.0, 250.0)
        order3 = OrderInfo("TEST003", "AAPL", OrderSide.SELL, OrderType.MARKET, 50.0)

        manager.add_order(order1)
        manager.add_order(order2)
        manager.add_order(order3)

        # Filter by AAPL
        aapl_orders = manager.filter_orders(symbol_filter="AAPL")
        assert len(aapl_orders) == 2
        assert all(order.symbol == "AAPL" for order in aapl_orders)

        # Filter by MSFT
        msft_orders = manager.filter_orders(symbol_filter="MSFT")
        assert len(msft_orders) == 1
        assert msft_orders[0].symbol == "MSFT"

    def test_filter_by_side(self):
        """Test filtering orders by side."""
        manager = OrderDataManager()

        order1 = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        order2 = OrderInfo("TEST002", "MSFT", OrderSide.SELL, OrderType.LIMIT, 200.0, 250.0)
        order3 = OrderInfo("TEST003", "GOOGL", OrderSide.BUY, OrderType.LIMIT, 50.0, 100.0)

        manager.add_order(order1)
        manager.add_order(order2)
        manager.add_order(order3)

        # Filter by BUY
        buy_orders = manager.filter_orders(side_filter="BUY")
        assert len(buy_orders) == 2
        assert all(order.side == OrderSide.BUY for order in buy_orders)

        # Filter by SELL
        sell_orders = manager.filter_orders(side_filter="SELL")
        assert len(sell_orders) == 1
        assert sell_orders[0].side == OrderSide.SELL

    def test_filter_by_status(self):
        """Test filtering orders by status."""
        manager = OrderDataManager()

        order1 = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        order1.status = OrderStatus.FILLED

        order2 = OrderInfo("TEST002", "MSFT", OrderSide.SELL, OrderType.LIMIT, 200.0, 250.0)
        order2.status = OrderStatus.PARTIALLY_FILLED

        order3 = OrderInfo("TEST003", "GOOGL", OrderSide.BUY, OrderType.LIMIT, 50.0, 100.0)
        order3.status = OrderStatus.CANCELLED

        manager.add_order(order1)
        manager.add_order(order2)
        manager.add_order(order3)

        # Filter by FILLED
        filled_orders = manager.filter_orders(status_filter="FILLED")
        assert len(filled_orders) == 1
        assert filled_orders[0].status == OrderStatus.FILLED

        # Filter by PARTIALLY_FILLED
        partial_orders = manager.filter_orders(status_filter="PARTIALLY_FILLED")
        assert len(partial_orders) == 1
        assert partial_orders[0].status == OrderStatus.PARTIALLY_FILLED

    def test_combined_filters(self):
        """Test combining multiple filters."""
        manager = OrderDataManager()

        order1 = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        order1.status = OrderStatus.FILLED

        order2 = OrderInfo("TEST002", "AAPL", OrderSide.SELL, OrderType.LIMIT, 200.0, 250.0)
        order2.status = OrderStatus.FILLED

        order3 = OrderInfo("TEST003", "MSFT", OrderSide.BUY, OrderType.LIMIT, 50.0, 100.0)
        order3.status = OrderStatus.FILLED

        manager.add_order(order1)
        manager.add_order(order2)
        manager.add_order(order3)

        # Filter by AAPL AND BUY AND FILLED
        filtered = manager.filter_orders(
            symbol_filter="AAPL", side_filter="BUY", status_filter="FILLED"
        )
        assert len(filtered) == 1
        assert filtered[0].order_id == "TEST001"


class TestOrderManagerFunctionality:
    """Test the core functionality that OrderManagerWidget uses."""

    def test_order_lifecycle_tracking(self):
        """Test tracking an order through its lifecycle."""
        manager = OrderDataManager()

        # Start with new order
        order = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.LIMIT, 100.0, 150.0)
        manager.add_order(order)

        # Acknowledge
        order.status = OrderStatus.ACKNOWLEDGED
        manager.update_order("TEST001", order)
        assert manager.get_order("TEST001").status == OrderStatus.ACKNOWLEDGED

        # Partial fill
        order.filled_quantity = 30.0
        order.remaining_quantity = 70.0
        order.status = OrderStatus.PARTIALLY_FILLED
        manager.update_order("TEST001", order)

        updated = manager.get_order("TEST001")
        assert updated.filled_quantity == 30.0
        assert updated.fill_percentage == 30.0
        assert updated.status == OrderStatus.PARTIALLY_FILLED

        # Full fill
        order.filled_quantity = 100.0
        order.remaining_quantity = 0.0
        order.status = OrderStatus.FILLED
        manager.update_order("TEST001", order)

        final = manager.get_order("TEST001")
        assert final.filled_quantity == 100.0
        assert final.fill_percentage == 100.0
        assert final.status == OrderStatus.FILLED

    def test_amendment_logic(self):
        """Test order amendment logic."""
        # Create amendable order
        order = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.LIMIT, 100.0, 150.0)
        order.status = OrderStatus.ACKNOWLEDGED

        # Test which orders can be amended
        def can_amend_order(order):
            return order.status in [
                OrderStatus.NEW,
                OrderStatus.ACKNOWLEDGED,
                OrderStatus.PARTIALLY_FILLED,
            ]

        assert can_amend_order(order) is True

        # Test amendment validation
        def validate_amendment(order, new_quantity, new_price):
            errors = []

            if new_quantity <= 0:
                errors.append("Quantity must be positive")
            if new_quantity < order.filled_quantity:
                errors.append("Cannot reduce quantity below filled amount")
            if order.order_type == OrderType.LIMIT and (new_price is None or new_price <= 0):
                errors.append("Price required for limit orders")

            return errors

        # Valid amendment
        errors = validate_amendment(order, 120.0, 155.0)
        assert len(errors) == 0

        # Invalid amendments
        errors = validate_amendment(order, 0, 155.0)  # Zero quantity
        assert "Quantity must be positive" in errors

        errors = validate_amendment(order, 100.0, None)  # No price for limit
        assert "Price required for limit orders" in errors

        # Test with partial fill
        order.filled_quantity = 30.0
        errors = validate_amendment(order, 25.0, 155.0)  # Quantity < filled
        assert "Cannot reduce quantity below filled amount" in errors

    def test_broker_event_integration(self):
        """Test integration with broker events."""
        manager = OrderDataManager()

        # Add initial order
        order = OrderInfo("TEST001", "AAPL", OrderSide.BUY, OrderType.MARKET, 100.0)
        manager.add_order(order)

        # Simulate broker events updating the order
        def process_broker_event(event):
            """Process a broker event and update order."""
            existing_order = manager.get_order(event.order_id)
            if existing_order:
                # Update order from event
                updated_order = OrderInfo(
                    order_id=event.order_id,
                    symbol=event.symbol,
                    side=existing_order.side,
                    order_type=existing_order.order_type,
                    quantity=existing_order.quantity,
                    price=existing_order.price,
                    filled_quantity=event.filled_quantity or existing_order.filled_quantity,
                    remaining_quantity=event.remaining_quantity
                    or existing_order.remaining_quantity,
                    status=event.status or existing_order.status,
                )
                manager.update_order(event.order_id, updated_order)
                return updated_order
            return None

        # ACK event
        ack_event = BrokerEvent(
            event_type="ACK",
            order_id="TEST001",
            symbol="AAPL",
            timestamp=datetime.now(),
            status=OrderStatus.ACKNOWLEDGED,
        )

        updated = process_broker_event(ack_event)
        assert updated.status == OrderStatus.ACKNOWLEDGED

        # FILL event
        fill_event = BrokerEvent(
            event_type="FILL",
            order_id="TEST001",
            symbol="AAPL",
            timestamp=datetime.now(),
            quantity=50.0,
            price=151.0,
            filled_quantity=50.0,
            remaining_quantity=50.0,
            status=OrderStatus.PARTIALLY_FILLED,
        )

        updated = process_broker_event(fill_event)
        assert updated.filled_quantity == 50.0
        assert updated.remaining_quantity == 50.0
        assert updated.status == OrderStatus.PARTIALLY_FILLED
        assert updated.fill_percentage == 50.0
