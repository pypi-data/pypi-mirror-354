"""Positions Manager widget for tracking and displaying positions."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QHeaderView, QTableView, QVBoxLayout, QWidget

from eoms.brokers.base import BrokerEvent
from eoms.brokers.sim_broker import SimBroker


@dataclass
class Position:
    """Represents a position in a symbol."""

    symbol: str
    quantity: float = 0.0
    avg_price: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    market_value: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def total_pnl(self) -> float:
        """Get total P&L (realized + unrealized)."""
        return self.realized_pnl + self.unrealized_pnl

    @property
    def risk_level(self) -> str:
        """Determine risk level based on position size and P&L."""
        if abs(self.quantity) == 0:
            return "FLAT"
        elif abs(self.total_pnl) > 1000:  # High P&L threshold
            return "HIGH"
        elif abs(self.total_pnl) > 500:  # Medium P&L threshold
            return "MEDIUM"
        else:
            return "LOW"


class PositionsTableModel(QAbstractTableModel):
    """Table model for positions data."""

    COLUMNS = [
        "Symbol",
        "Quantity",
        "Avg Price",
        "Market Price",
        "Market Value",
        "Realized P&L",
        "Unrealized P&L",
        "Total P&L",
        "Risk",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.positions: Dict[str, Position] = {}

    def rowCount(self, parent=QModelIndex()) -> int:
        """Return number of positions."""
        return len(self.positions)

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
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if row >= len(self.positions):
            return None

        position = list(self.positions.values())[row]

        if role == Qt.DisplayRole:
            if col == 0:  # Symbol
                return position.symbol
            elif col == 1:  # Quantity
                return f"{position.quantity:.0f}"
            elif col == 2:  # Avg Price
                return f"{position.avg_price:.2f}" if position.avg_price > 0 else "0.00"
            elif col == 3:  # Market Price
                # This will be updated by the widget
                return "0.00"
            elif col == 4:  # Market Value
                return f"{position.market_value:.2f}"
            elif col == 5:  # Realized P&L
                return f"{position.realized_pnl:.2f}"
            elif col == 6:  # Unrealized P&L
                return f"{position.unrealized_pnl:.2f}"
            elif col == 7:  # Total P&L
                return f"{position.total_pnl:.2f}"
            elif col == 8:  # Risk
                return position.risk_level

        elif role == Qt.BackgroundRole:
            # Color coding based on risk level
            if col == 8:  # Risk column
                risk = position.risk_level
                if risk == "HIGH":
                    return QBrush(QColor(255, 200, 200))  # Light red
                elif risk == "MEDIUM":
                    return QBrush(QColor(255, 255, 200))  # Light yellow
                elif risk == "LOW":
                    return QBrush(QColor(200, 255, 200))  # Light green
                else:  # FLAT
                    return QBrush(QColor(240, 240, 240))  # Light gray

            # P&L color coding
            elif col in [5, 6, 7]:  # P&L columns
                pnl = 0.0
                if col == 5:
                    pnl = position.realized_pnl
                elif col == 6:
                    pnl = position.unrealized_pnl
                elif col == 7:
                    pnl = position.total_pnl

                if pnl > 0:
                    return QBrush(QColor(220, 255, 220))  # Light green for profit
                elif pnl < 0:
                    return QBrush(QColor(255, 220, 220))  # Light red for loss

        return None

    def update_position(self, symbol: str, position: Position):
        """Update or add a position."""
        if symbol in self.positions:
            # Find row and update
            symbols = list(self.positions.keys())
            row = symbols.index(symbol)
            self.positions[symbol] = position

            # Emit data changed for the entire row
            left_index = self.index(row, 0)
            right_index = self.index(row, len(self.COLUMNS) - 1)
            self.dataChanged.emit(left_index, right_index)
        else:
            # Add new position
            row = len(self.positions)
            self.beginInsertRows(QModelIndex(), row, row)
            self.positions[symbol] = position
            self.endInsertRows()

    def get_position(self, symbol: str) -> Optional[Position]:
        """Get position for a symbol."""
        return self.positions.get(symbol)

    def clear_positions(self):
        """Clear all positions."""
        self.beginResetModel()
        self.positions.clear()
        self.endResetModel()


class PositionsManagerWidget(QWidget):
    """Widget for managing and displaying positions with risk color-coding."""

    # Signals
    position_updated = Signal(str, float)  # symbol, quantity
    risk_alert = Signal(str, str)  # symbol, risk_level

    def __init__(self, broker: Optional[SimBroker] = None, parent: Optional[QWidget] = None):
        """Initialize the positions manager widget."""
        super().__init__(parent)

        self.broker = broker
        self.positions_model = PositionsTableModel(self)

        self._setup_ui()

        # Setup periodic market price updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_market_prices)
        self.update_timer.start(1000)  # Update every second

    def _setup_ui(self) -> None:
        """Setup the user interface."""
        layout = QVBoxLayout(self)

        # Create table view
        self.table_view = QTableView()
        self.table_view.setModel(self.positions_model)
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        # Configure column sizing
        header = self.table_view.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(len(PositionsTableModel.COLUMNS)):
            if i == 0:  # Symbol column
                header.setSectionResizeMode(i, QHeaderView.Fixed)
                self.table_view.setColumnWidth(i, 80)
            elif i in [1, 2, 3]:  # Quantity, Avg Price, Market Price
                header.setSectionResizeMode(i, QHeaderView.Fixed)
                self.table_view.setColumnWidth(i, 90)
            else:  # Other columns
                header.setSectionResizeMode(i, QHeaderView.Stretch)

        layout.addWidget(self.table_view)

    def set_broker(self, broker: SimBroker) -> None:
        """Set the broker for position tracking."""
        self.broker = broker

    async def on_broker_event(self, event: BrokerEvent) -> None:
        """Handle broker events to update positions."""
        if event.event_type == "FILL" and self.broker:
            # Update position for this symbol
            await self._update_position_for_symbol(event.symbol)

    async def _update_position_for_symbol(self, symbol: str) -> None:
        """Update position data for a specific symbol."""
        if not self.broker:
            return

        try:
            # Get position data from broker
            pnl_data = self.broker.calculate_pnl(symbol)

            # Create or update position
            position = Position(
                symbol=symbol,
                quantity=pnl_data.get("position", 0.0),
                avg_price=pnl_data.get("avg_price", 0.0),
                realized_pnl=pnl_data.get("realized_pnl", 0.0),
                last_updated=datetime.now(),
            )

            # Calculate market value and unrealized P&L
            if position.quantity != 0:
                try:
                    market_price = self.broker.get_market_price(symbol)
                    position.market_value = position.quantity * market_price

                    # Unrealized P&L = (market_price - avg_price) * quantity
                    if position.avg_price > 0:
                        position.unrealized_pnl = (
                            market_price - position.avg_price
                        ) * position.quantity
                except Exception:
                    # If we can't get market price, keep at 0
                    pass

            # Update the model
            self.positions_model.update_position(symbol, position)

            # Emit signals
            self.position_updated.emit(symbol, position.quantity)

            # Check for risk alerts
            if position.risk_level in ["HIGH", "MEDIUM"]:
                self.risk_alert.emit(symbol, position.risk_level)

        except Exception as e:
            print(f"Error updating position for {symbol}: {e}")

    def _update_market_prices(self) -> None:
        """Update market prices for all positions."""
        if not self.broker:
            return

        for symbol in self.positions_model.positions.keys():
            asyncio.create_task(self._update_position_for_symbol(symbol))

    def refresh_all_positions(self) -> None:
        """Refresh all positions from broker data."""
        if not self.broker:
            return

        # Get all symbols that have fills
        fills = self.broker.get_fill_history()
        symbols = set(fill.symbol for fill in fills)

        for symbol in symbols:
            asyncio.create_task(self._update_position_for_symbol(symbol))

    def clear_positions(self) -> None:
        """Clear all positions."""
        self.positions_model.clear_positions()
