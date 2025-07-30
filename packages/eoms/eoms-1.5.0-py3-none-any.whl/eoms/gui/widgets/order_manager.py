"""Order Manager widget for displaying and managing orders."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from eoms.brokers.base import BrokerEvent, OrderSide, OrderStatus, OrderType
from eoms.brokers.sim_broker import SimBroker


@dataclass
class OrderInfo:
    """Represents order information for display."""

    order_id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    filled_quantity: float = 0.0
    remaining_quantity: float = 0.0
    status: OrderStatus = OrderStatus.NEW
    timestamp: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def fill_percentage(self) -> float:
        """Calculate fill percentage."""
        if self.quantity == 0:
            return 0.0
        return (self.filled_quantity / self.quantity) * 100.0

    @property
    def avg_fill_price(self) -> Optional[float]:
        """Calculate average fill price (simplified for demo)."""
        return self.price  # Simplified - would calculate from actual fills


class OrderTableModel(QAbstractTableModel):
    """Table model for order data."""

    COLUMNS = [
        "Order ID",
        "Symbol",
        "Side",
        "Type",
        "Quantity",
        "Price",
        "Filled",
        "Remaining",
        "Status",
        "Fill %",
        "Timestamp",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.orders: Dict[str, OrderInfo] = {}
        self.order_list: List[str] = []  # Maintain order for display

    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of orders."""
        return len(self.order_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        """Return number of columns."""
        return len(self.COLUMNS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """Return header data."""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.COLUMNS[section]
        return None

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """Return data for a cell."""
        if not index.isValid() or index.row() >= len(self.order_list):
            return None

        order_id = self.order_list[index.row()]
        order = self.orders[order_id]
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:  # Order ID
                return order.order_id
            elif col == 1:  # Symbol
                return order.symbol
            elif col == 2:  # Side
                return order.side.value
            elif col == 3:  # Type
                return order.order_type.value
            elif col == 4:  # Quantity
                return f"{order.quantity:.0f}"
            elif col == 5:  # Price
                return f"{order.price:.2f}" if order.price else "Market"
            elif col == 6:  # Filled
                return f"{order.filled_quantity:.0f}"
            elif col == 7:  # Remaining
                return f"{order.remaining_quantity:.0f}"
            elif col == 8:  # Status
                return order.status.value
            elif col == 9:  # Fill %
                return f"{order.fill_percentage:.1f}%"
            elif col == 10:  # Timestamp
                return order.timestamp.strftime("%H:%M:%S")

        elif role == Qt.BackgroundRole:
            # Color coding based on status
            if col == 8:  # Status column
                status = order.status
                if status == OrderStatus.FILLED:
                    return QBrush(QColor(200, 255, 200))  # Light green
                elif status == OrderStatus.PARTIALLY_FILLED:
                    return QBrush(QColor(255, 255, 200))  # Light yellow
                elif status == OrderStatus.CANCELLED:
                    return QBrush(QColor(240, 240, 240))  # Light gray
                elif status == OrderStatus.REJECTED:
                    return QBrush(QColor(255, 200, 200))  # Light red

        return None

    def add_order(self, order: OrderInfo):
        """Add a new order."""
        row = len(self.order_list)
        self.beginInsertRows(QModelIndex(), row, row)
        self.orders[order.order_id] = order
        self.order_list.append(order.order_id)
        self.endInsertRows()

    def update_order(self, order_id: str, order: OrderInfo):
        """Update an existing order."""
        if order_id in self.orders:
            row = self.order_list.index(order_id)
            self.orders[order_id] = order

            # Emit data changed for the entire row
            left_index = self.index(row, 0)
            right_index = self.index(row, len(self.COLUMNS) - 1)
            self.dataChanged.emit(left_index, right_index)

    def get_order(self, order_id: str) -> Optional[OrderInfo]:
        """Get order by ID."""
        return self.orders.get(order_id)

    def get_order_at_row(self, row: int) -> Optional[OrderInfo]:
        """Get order at a specific row."""
        if 0 <= row < len(self.order_list):
            order_id = self.order_list[row]
            return self.orders[order_id]
        return None

    def clear_orders(self):
        """Clear all orders."""
        self.beginResetModel()
        self.orders.clear()
        self.order_list.clear()
        self.endResetModel()


class OrderAmendDialog(QDialog):
    """Dialog for amending orders."""

    def __init__(self, order: OrderInfo, parent=None):
        super().__init__(parent)
        self.order = order
        self.amended_order = None

        self.setWindowTitle(f"Amend Order {order.order_id}")
        self.setModal(True)
        self.resize(300, 200)

        self._setup_ui()

    def _setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout(self)

        # Form layout for order fields
        form_layout = QFormLayout()

        # Show current order details (read-only)
        form_layout.addRow("Order ID:", QLabel(self.order.order_id))
        form_layout.addRow("Symbol:", QLabel(self.order.symbol))
        form_layout.addRow("Side:", QLabel(self.order.side.value))
        form_layout.addRow("Type:", QLabel(self.order.order_type.value))

        # Editable fields
        self.quantity_edit = QLineEdit(str(self.order.quantity))
        form_layout.addRow("Quantity:", self.quantity_edit)

        self.price_edit = QLineEdit()
        if self.order.price:
            self.price_edit.setText(f"{self.order.price:.2f}")
        else:
            self.price_edit.setText("")
            self.price_edit.setEnabled(False)
        form_layout.addRow("Price:", self.price_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )
        button_box.accepted.connect(self._accept_changes)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _accept_changes(self):
        """Accept the changes and create amended order."""
        try:
            # Validate quantity
            new_quantity = float(self.quantity_edit.text())
            if new_quantity <= 0:
                raise ValueError("Quantity must be positive")

            # Validate price for limit orders
            new_price = None
            if self.order.order_type == OrderType.LIMIT:
                price_text = self.price_edit.text().strip()
                if price_text:
                    new_price = float(price_text)
                    if new_price <= 0:
                        raise ValueError("Price must be positive")
                else:
                    raise ValueError("Price is required for limit orders")

            # Create amended order
            self.amended_order = OrderInfo(
                order_id=self.order.order_id,
                symbol=self.order.symbol,
                side=self.order.side,
                order_type=self.order.order_type,
                quantity=new_quantity,
                price=new_price,
                filled_quantity=self.order.filled_quantity,
                remaining_quantity=new_quantity - self.order.filled_quantity,
                status=self.order.status,
                timestamp=self.order.timestamp,
                last_updated=datetime.now(),
            )

            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))


class OrderManagerWidget(QWidget):
    """Widget for managing and displaying orders with filtering and sorting."""

    # Signals
    order_amended = Signal(str, dict)  # order_id, amendment_data
    order_selected = Signal(str)  # order_id

    def __init__(self, broker: Optional[SimBroker] = None, parent: Optional[QWidget] = None):
        """Initialize the order manager widget."""
        super().__init__(parent)

        self.broker = broker
        self.order_model = OrderTableModel(self)
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.order_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout(self)

        # Filter controls
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("Filter:"))

        self.symbol_filter = QLineEdit()
        self.symbol_filter.setPlaceholderText("Symbol")
        self.symbol_filter.textChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.symbol_filter)

        self.side_filter = QComboBox()
        self.side_filter.addItems(["All", "BUY", "SELL"])
        self.side_filter.currentTextChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.side_filter)

        self.status_filter = QComboBox()
        self.status_filter.addItems(
            [
                "All",
                "NEW",
                "ACKNOWLEDGED",
                "PARTIALLY_FILLED",
                "FILLED",
                "CANCELLED",
                "REJECTED",
            ]
        )
        self.status_filter.currentTextChanged.connect(self._apply_filters)
        filter_layout.addWidget(self.status_filter)

        clear_filter_btn = QPushButton("Clear Filters")
        clear_filter_btn.clicked.connect(self._clear_filters)
        filter_layout.addWidget(clear_filter_btn)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table view
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.setSortingEnabled(True)

        # Configure column sizing
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(len(OrderTableModel.COLUMNS)):
            if i == 0:  # Order ID
                self.table_view.setColumnWidth(i, 100)
            elif i in [1, 2, 3]:  # Symbol, Side, Type
                self.table_view.setColumnWidth(i, 80)
            elif i in [4, 5, 6, 7]:  # Quantities and Price
                self.table_view.setColumnWidth(i, 70)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        # Double-click to amend
        self.table_view.doubleClicked.connect(self._on_double_click)

        layout.addWidget(self.table_view)

        # Action buttons
        button_layout = QHBoxLayout()

        self.amend_button = QPushButton("Amend Selected")
        self.amend_button.clicked.connect(self._amend_selected_order)
        self.amend_button.setEnabled(False)
        button_layout.addWidget(self.amend_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._refresh_orders)
        button_layout.addWidget(self.refresh_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Connect selection changes
        self.table_view.selectionModel().selectionChanged.connect(self._on_selection_changed)

    def set_broker(self, broker: SimBroker) -> None:
        """Set the broker for order tracking."""
        self.broker = broker

    async def on_broker_event(self, event: BrokerEvent) -> None:
        """Handle broker events to update orders."""
        if event.event_type in ["ACK", "FILL", "CANCEL", "REJECT"]:
            await self._update_order_from_event(event)

    async def _update_order_from_event(self, event: BrokerEvent) -> None:
        """Update order data from broker event."""
        try:
            # Check if this is a new order or update to existing
            existing_order = self.order_model.get_order(event.order_id)

            if existing_order:
                # Update existing order
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
                    timestamp=existing_order.timestamp,
                    last_updated=datetime.now(),
                )

                self.order_model.update_order(event.order_id, updated_order)
            else:
                # This might be a new order we haven't seen yet
                # In a real system, we'd query the broker for full order details
                pass

        except Exception as e:
            print(f"Error updating order from event: {e}")

    def add_order_from_ticket(
        self,
        order_id: str,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: float,
        price: Optional[float] = None,
    ):
        """Add an order from the order ticket (for demo integration)."""
        order = OrderInfo(
            order_id=order_id,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            remaining_quantity=quantity,
            status=OrderStatus.NEW,
        )

        self.order_model.add_order(order)

    def _apply_filters(self):
        """Apply filters to the order view."""
        # Build filter regex
        filters = []

        # Symbol filter
        symbol_text = self.symbol_filter.text().strip()
        if symbol_text:
            filters.append(f".*{symbol_text}.*")

        # Combine all filters
        if filters:
            self.proxy_model.setFilterRegularExpression("|".join(filters))
        else:
            self.proxy_model.setFilterRegularExpression("")

        # Additional filtering by side and status would require custom filter logic
        self.proxy_model.invalidateFilter()

    def _clear_filters(self):
        """Clear all filters."""
        self.symbol_filter.clear()
        self.side_filter.setCurrentIndex(0)  # "All"
        self.status_filter.setCurrentIndex(0)  # "All"
        self.proxy_model.setFilterRegularExpression("")

    def _on_selection_changed(self):
        """Handle selection changes."""
        has_selection = self.table_view.selectionModel().hasSelection()
        self.amend_button.setEnabled(has_selection)

        if has_selection:
            # Get selected order
            selected_indexes = self.table_view.selectionModel().selectedRows()
            if selected_indexes:
                row = self.proxy_model.mapToSource(selected_indexes[0]).row()
                order = self.order_model.get_order_at_row(row)
                if order:
                    self.order_selected.emit(order.order_id)

    def _on_double_click(self, index: QModelIndex):
        """Handle double-click on order row."""
        source_index = self.proxy_model.mapToSource(index)
        row = source_index.row()
        order = self.order_model.get_order_at_row(row)

        if order and order.status in [
            OrderStatus.NEW,
            OrderStatus.ACKNOWLEDGED,
            OrderStatus.PARTIALLY_FILLED,
        ]:
            self._show_amend_dialog(order)
        else:
            QMessageBox.information(
                self,
                "Cannot Amend",
                f"Order {order.order_id} cannot be amended (Status: {order.status.value})",
            )

    def _amend_selected_order(self):
        """Amend the selected order."""
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if selected_indexes:
            source_index = self.proxy_model.mapToSource(selected_indexes[0])
            row = source_index.row()
            order = self.order_model.get_order_at_row(row)
            if order:
                self._show_amend_dialog(order)

    def _show_amend_dialog(self, order: OrderInfo):
        """Show the amend dialog for an order."""
        dialog = OrderAmendDialog(order, self)

        if dialog.exec() == QDialog.Accepted and dialog.amended_order:
            # Update the order in the model
            self.order_model.update_order(order.order_id, dialog.amended_order)

            # Emit signal for actual broker amendment
            amendment_data = {
                "quantity": dialog.amended_order.quantity,
                "price": dialog.amended_order.price,
            }
            self.order_amended.emit(order.order_id, amendment_data)

    def _refresh_orders(self):
        """Refresh orders from broker."""
        if self.broker:
            # In a real implementation, we'd query the broker for all orders
            # For demo, we just update display
            pass

    def clear_orders(self):
        """Clear all orders."""
        self.order_model.clear_orders()
