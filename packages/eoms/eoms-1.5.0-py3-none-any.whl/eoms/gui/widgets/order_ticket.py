"""Order Ticket widget for placing and managing orders."""

import asyncio
import uuid
from typing import Optional

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from eoms.brokers.base import OrderRequest, OrderSide, OrderType
from eoms.brokers.sim_broker import SimBroker


class OrderTicketWidget(QWidget):
    """Widget for placing and canceling orders."""

    # Signals
    order_placed = Signal(str)  # order_id
    order_cancelled = Signal(str)  # order_id
    status_updated = Signal(str)  # status message

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the order ticket widget."""
        super().__init__(parent)

        # Create broker instance
        self.broker = SimBroker({"latency_ms": 10})
        self.broker_connected = False

        # Track placed orders
        self.placed_orders = {}

        self._setup_ui()
        self._setup_broker()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout(self)

        # Create form layout for order inputs
        form_layout = QFormLayout()

        # Symbol input
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("e.g. AAPL")
        self.symbol_input.setText("AAPL")  # Default for demo
        form_layout.addRow("Symbol:", self.symbol_input)

        # Side selection
        self.side_combo = QComboBox()
        self.side_combo.addItems(["BUY", "SELL"])
        form_layout.addRow("Side:", self.side_combo)

        # Order type selection
        self.type_combo = QComboBox()
        self.type_combo.addItems(["MARKET", "LIMIT"])
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        form_layout.addRow("Type:", self.type_combo)

        # Quantity input
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("100")
        self.quantity_input.setText("100")  # Default for demo
        form_layout.addRow("Quantity:", self.quantity_input)

        # Price input (for limit orders)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("0.00")
        self.price_input.setEnabled(False)  # Disabled for market orders initially
        form_layout.addRow("Price:", self.price_input)

        # Route selection (placeholder for now)
        self.route_combo = QComboBox()
        self.route_combo.addItems(["SimBroker", "AUTO"])
        form_layout.addRow("Route:", self.route_combo)

        layout.addLayout(form_layout)

        # Buttons layout
        button_layout = QHBoxLayout()

        self.place_button = QPushButton("Place Order")
        self.place_button.clicked.connect(self._place_order)
        self.place_button.setEnabled(False)  # Disabled until broker connects
        button_layout.addWidget(self.place_button)

        self.cancel_button = QPushButton("Cancel Last")
        self.cancel_button.clicked.connect(self._cancel_last_order)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Connecting to broker...")
        layout.addWidget(self.status_label)

    def _setup_broker(self) -> None:
        """Setup broker connection and callbacks."""
        # Setup event callback for broker events
        self.broker.set_event_callback(self._on_broker_event)

        # Use a timer to connect broker asynchronously
        self.connect_timer = QTimer()
        self.connect_timer.timeout.connect(self._connect_broker)
        self.connect_timer.setSingleShot(True)
        self.connect_timer.start(100)  # Connect after 100ms

    def _connect_broker(self) -> None:
        """Connect to the broker."""

        async def do_connect():
            connected = await self.broker.connect()
            if connected:
                self.broker_connected = True
                self.place_button.setEnabled(True)
                self.status_label.setText("Connected to SimBroker - Ready to trade")
                self.status_updated.emit("Broker connected")
            else:
                self.status_label.setText("Failed to connect to broker")
                self.status_updated.emit("Broker connection failed")

        # Run async connection in event loop
        asyncio.create_task(do_connect())

    def _on_type_changed(self, order_type: str) -> None:
        """Handle order type change."""
        if order_type == "LIMIT":
            self.price_input.setEnabled(True)
            # Set a default price near current market price
            if not self.price_input.text():
                try:
                    market_price = self.broker.get_market_price(self.symbol_input.text() or "AAPL")
                    self.price_input.setText(f"{market_price:.2f}")
                except Exception:
                    self.price_input.setText("100.00")
        else:
            self.price_input.setEnabled(False)
            self.price_input.clear()

    def _place_order(self) -> None:
        """Place an order."""
        if not self.broker_connected:
            self.status_label.setText("Not connected to broker")
            return

        try:
            # Generate order ID
            order_id = f"O{uuid.uuid4().hex[:8].upper()}"

            # Get form values
            symbol = self.symbol_input.text().strip().upper()
            if not symbol:
                self.status_label.setText("Symbol is required")
                return

            side = OrderSide(self.side_combo.currentText())
            order_type = OrderType(self.type_combo.currentText())

            try:
                quantity = float(self.quantity_input.text())
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
            except ValueError:
                self.status_label.setText("Invalid quantity")
                return

            price = None
            if order_type == OrderType.LIMIT:
                try:
                    price = float(self.price_input.text())
                    if price <= 0:
                        raise ValueError("Price must be positive")
                except ValueError:
                    self.status_label.setText("Invalid price for limit order")
                    return

            # Create order request
            order = OrderRequest(
                order_id=order_id,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )

            # Place order asynchronously
            async def do_place():
                success = await self.broker.place_order(order)
                if success:
                    self.placed_orders[order_id] = order
                    self.cancel_button.setEnabled(True)
                    self.status_label.setText(f"Order {order_id} placed")
                    self.order_placed.emit(order_id)
                else:
                    self.status_label.setText(f"Failed to place order {order_id}")

            asyncio.create_task(do_place())

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def _cancel_last_order(self) -> None:
        """Cancel the last placed order."""
        if not self.placed_orders:
            self.status_label.setText("No orders to cancel")
            return

        # Get last order ID
        order_id = list(self.placed_orders.keys())[-1]

        async def do_cancel():
            success = await self.broker.cancel_order(order_id)
            if success:
                self.status_label.setText(f"Cancellation sent for {order_id}")
                self.order_cancelled.emit(order_id)
            else:
                self.status_label.setText(f"Failed to cancel {order_id}")

        asyncio.create_task(do_cancel())

    async def _on_broker_event(self, event) -> None:
        """Handle broker events."""
        # Update status based on event type
        if event.event_type == "ACK":
            self.status_label.setText(f"Order {event.order_id} acknowledged")
        elif event.event_type == "FILL":
            filled_qty = event.filled_quantity or 0
            remaining_qty = event.remaining_quantity or 0
            self.status_label.setText(
                f"Fill: {event.order_id} - {filled_qty:.0f}@{event.price:.2f} "
                f"({remaining_qty:.0f} remaining)"
            )
        elif event.event_type == "CANCEL":
            self.status_label.setText(f"Order {event.order_id} cancelled")
            # Remove from tracking
            if event.order_id in self.placed_orders:
                del self.placed_orders[event.order_id]
            if not self.placed_orders:
                self.cancel_button.setEnabled(False)
        elif event.event_type == "REJECT":
            self.status_label.setText(f"Order {event.order_id} rejected: {event.message}")

        self.status_updated.emit(f"{event.event_type}: {event.order_id}")

    def closeEvent(self, event) -> None:
        """Handle widget close event."""
        if self.broker_connected:

            async def do_disconnect():
                await self.broker.disconnect()

            asyncio.create_task(do_disconnect())
        super().closeEvent(event)
