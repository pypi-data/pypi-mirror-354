"""PNL Window widget for displaying profit/loss charts and statistics."""

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QRect, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from eoms.brokers.base import OrderSide

logger = logging.getLogger(__name__)


@dataclass
class PnlSnapshot:
    """Snapshot of P&L at a point in time."""

    timestamp: datetime
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    positions: Dict[str, float] = field(default_factory=dict)
    market_values: Dict[str, float] = field(default_factory=dict)


@dataclass
class PnlStats:
    """P&L statistics."""

    total_realized: float = 0.0
    total_unrealized: float = 0.0
    total_pnl: float = 0.0
    max_drawdown: float = 0.0
    max_profit: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0


class SimpleChart(QWidget):
    """Simple chart widget for displaying P&L over time."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_points: List[Tuple[datetime, float]] = []
        self.setMinimumHeight(200)

    def add_data_point(self, timestamp: datetime, value: float):
        """Add a data point to the chart."""
        self.data_points.append((timestamp, value))

        # Keep only last 100 points for performance
        if len(self.data_points) > 100:
            self.data_points = self.data_points[-100:]

        self.update()

    def clear_data(self):
        """Clear all data points."""
        self.data_points.clear()
        self.update()

    def paintEvent(self, event):
        """Paint the chart."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        painter.fillRect(self.rect(), QColor(250, 250, 250))

        if len(self.data_points) < 2:
            # Draw "No Data" message
            painter.setPen(QPen(QColor(128, 128, 128)))
            painter.drawText(self.rect(), Qt.AlignCenter, "No P&L data available")
            return

        # Calculate chart bounds
        margin = 20
        chart_rect = QRect(margin, margin, self.width() - 2 * margin, self.height() - 2 * margin)

        # Find data bounds
        values = [point[1] for point in self.data_points]
        min_value = min(values)
        max_value = max(values)

        if max_value == min_value:
            max_value += 1  # Avoid division by zero

        # Draw axes
        painter.setPen(QPen(QColor(64, 64, 64), 1))
        painter.drawRect(chart_rect)

        # Draw zero line
        zero_y = chart_rect.bottom() - int(
            (0 - min_value) / (max_value - min_value) * chart_rect.height()
        )
        if chart_rect.top() <= zero_y <= chart_rect.bottom():
            painter.setPen(QPen(QColor(128, 128, 128), 1, Qt.DashLine))
            painter.drawLine(chart_rect.left(), zero_y, chart_rect.right(), zero_y)

        # Draw data line
        if len(self.data_points) > 1:
            # Determine line color based on final value
            final_pnl = self.data_points[-1][1]
            line_color = (
                QColor(34, 139, 34) if final_pnl >= 0 else QColor(220, 20, 60)
            )  # Green or Red
            painter.setPen(QPen(line_color, 2))

            # Convert data points to screen coordinates
            points = []
            for i, (_timestamp, value) in enumerate(self.data_points):
                x = chart_rect.left() + int(i / (len(self.data_points) - 1) * chart_rect.width())
                y = chart_rect.bottom() - int(
                    (value - min_value) / (max_value - min_value) * chart_rect.height()
                )
                points.append((x, y))

            # Draw lines between points
            for i in range(len(points) - 1):
                painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

        # Draw value labels
        painter.setPen(QPen(QColor(64, 64, 64)))
        painter.drawText(chart_rect.left() - 15, chart_rect.top() + 5, f"${max_value:.2f}")
        painter.drawText(chart_rect.left() - 15, chart_rect.bottom() + 5, f"${min_value:.2f}")


class PnlSummaryModel(QAbstractTableModel):
    """Table model for P&L summary by symbol."""

    COLUMNS = [
        "Symbol",
        "Position",
        "Avg Price",
        "Market Price",
        "Market Value",
        "Realized P&L",
        "Unrealized P&L",
        "Total P&L",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pnl_data: Dict[str, Dict] = {}

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.pnl_data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid() or index.row() >= len(self.pnl_data):
            return None

        symbol = list(self.pnl_data.keys())[index.row()]
        data = self.pnl_data[symbol]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:  # Symbol
                return symbol
            elif column == 1:  # Position
                return f"{data.get('position', 0.0):.2f}"
            elif column == 2:  # Avg Price
                return f"${data.get('avg_price', 0.0):.2f}"
            elif column == 3:  # Market Price
                return f"${data.get('market_price', 0.0):.2f}"
            elif column == 4:  # Market Value
                return f"${data.get('market_value', 0.0):.2f}"
            elif column == 5:  # Realized P&L
                return f"${data.get('realized_pnl', 0.0):.2f}"
            elif column == 6:  # Unrealized P&L
                return f"${data.get('unrealized_pnl', 0.0):.2f}"
            elif column == 7:  # Total P&L
                total = data.get("realized_pnl", 0.0) + data.get("unrealized_pnl", 0.0)
                return f"${total:.2f}"

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight | Qt.AlignVCenter

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.COLUMNS[section]
        return None

    def update_symbol_pnl(self, symbol: str, data: Dict):
        """Update P&L data for a symbol."""
        if symbol not in self.pnl_data:
            # Add new symbol
            self.beginInsertRows(QModelIndex(), len(self.pnl_data), len(self.pnl_data))
            self.pnl_data[symbol] = data
            self.endInsertRows()
        else:
            # Update existing symbol
            self.pnl_data[symbol].update(data)
            row = list(self.pnl_data.keys()).index(symbol)
            top_left = self.index(row, 0)
            bottom_right = self.index(row, len(self.COLUMNS) - 1)
            self.dataChanged.emit(top_left, bottom_right)

    def clear_data(self):
        """Clear all P&L data."""
        self.beginResetModel()
        self.pnl_data.clear()
        self.endResetModel()


class PNLWindowWidget(QWidget):
    """Widget for displaying P&L charts and statistics."""

    pnl_updated = Signal(float)  # Emits total P&L updates

    def __init__(self, broker=None, parent=None):
        super().__init__(parent)
        self.broker = broker
        self.pnl_history: List[PnlSnapshot] = []
        self.current_stats = PnlStats()
        self.positions: Dict[str, float] = defaultdict(float)  # symbol -> quantity
        self.avg_prices: Dict[str, float] = {}  # symbol -> avg price
        self.realized_pnl: Dict[str, float] = defaultdict(float)  # symbol -> realized P&L

        self.setup_ui()
        self.setup_connections()

        # Timer for periodic updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_pnl)
        self.update_timer.start(1000)  # Update every second

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("P&L Monitor")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title)

        # Create splitter for chart and table
        splitter = QSplitter(Qt.Vertical)

        # Chart section
        chart_frame = QFrame()
        chart_frame.setFrameStyle(QFrame.StyledPanel)
        chart_layout = QVBoxLayout(chart_frame)

        # Chart controls
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Time Range:"))

        self.time_range_combo = QComboBox()
        self.time_range_combo.addItems(["1 Hour", "4 Hours", "1 Day", "All"])
        self.time_range_combo.setCurrentText("1 Hour")
        controls_layout.addWidget(self.time_range_combo)

        controls_layout.addStretch()

        self.reset_button = QPushButton("Reset")
        controls_layout.addWidget(self.reset_button)

        chart_layout.addLayout(controls_layout)

        # P&L Chart
        self.pnl_chart = SimpleChart()
        chart_layout.addWidget(self.pnl_chart)

        splitter.addWidget(chart_frame)

        # Statistics section
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.StyledPanel)
        stats_layout = QVBoxLayout(stats_frame)

        # Summary statistics
        summary_grid = QGridLayout()

        self.total_pnl_label = QLabel("$0.00")
        self.total_pnl_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        summary_grid.addWidget(QLabel("Total P&L:"), 0, 0)
        summary_grid.addWidget(self.total_pnl_label, 0, 1)

        self.realized_pnl_label = QLabel("$0.00")
        summary_grid.addWidget(QLabel("Realized:"), 0, 2)
        summary_grid.addWidget(self.realized_pnl_label, 0, 3)

        self.unrealized_pnl_label = QLabel("$0.00")
        summary_grid.addWidget(QLabel("Unrealized:"), 0, 4)
        summary_grid.addWidget(self.unrealized_pnl_label, 0, 5)

        self.max_profit_label = QLabel("$0.00")
        summary_grid.addWidget(QLabel("Max Profit:"), 1, 0)
        summary_grid.addWidget(self.max_profit_label, 1, 1)

        self.max_drawdown_label = QLabel("$0.00")
        summary_grid.addWidget(QLabel("Max Drawdown:"), 1, 2)
        summary_grid.addWidget(self.max_drawdown_label, 1, 3)

        self.win_rate_label = QLabel("0.0%")
        summary_grid.addWidget(QLabel("Win Rate:"), 1, 4)
        summary_grid.addWidget(self.win_rate_label, 1, 5)

        stats_layout.addLayout(summary_grid)

        # P&L by symbol table
        self.pnl_model = PnlSummaryModel()
        self.pnl_table = QTableView()
        self.pnl_table.setModel(self.pnl_model)
        self.pnl_table.setAlternatingRowColors(True)

        # Auto-resize columns
        header = self.pnl_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i in range(len(PnlSummaryModel.COLUMNS)):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        stats_layout.addWidget(QLabel("P&L by Symbol:"))
        stats_layout.addWidget(self.pnl_table)

        splitter.addWidget(stats_frame)

        # Set splitter proportions
        splitter.setSizes([300, 400])
        layout.addWidget(splitter)

        # Status
        self.status_label = QLabel("Ready - No broker connected")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def setup_connections(self):
        """Setup signal connections."""
        self.reset_button.clicked.connect(self.reset_pnl)
        self.time_range_combo.currentTextChanged.connect(self.update_chart_range)

    def set_broker(self, broker):
        """Set the broker for P&L calculation."""
        self.broker = broker
        if broker:
            self.status_label.setText("Connected to broker")
        else:
            self.status_label.setText("No broker connected")

    def update_pnl(self):
        """Update P&L calculations and display."""
        if not self.broker:
            return

        try:
            # Get fill history from broker
            fills = self.broker.get_fill_history()

            # Process fills to calculate positions and P&L
            self.process_fills(fills)

            # Calculate current P&L
            current_pnl = self.calculate_current_pnl()

            # Update statistics
            self.update_statistics(current_pnl)

            # Update chart
            self.pnl_chart.add_data_point(datetime.now(), current_pnl.total_pnl)

            # Update summary by symbol
            self.update_symbol_summary()

            # Update labels
            self.update_summary_labels(current_pnl)

            # Emit signal
            self.pnl_updated.emit(current_pnl.total_pnl)

        except Exception as e:
            logger.error(f"Error updating P&L: {e}")
            self.status_label.setText(f"Error: {e}")

    def process_fills(self, fills: List):
        """Process broker fills to update positions and realized P&L."""
        self.positions.clear()
        self.avg_prices.clear()
        self.realized_pnl.clear()

        symbol_costs = defaultdict(float)  # Total cost per symbol
        symbol_quantities = defaultdict(float)  # Total quantity per symbol

        for fill in fills:
            if (
                hasattr(fill, "symbol")
                and hasattr(fill, "side")
                and hasattr(fill, "quantity")
                and hasattr(fill, "price")
            ):
                symbol = fill.symbol
                quantity = fill.quantity
                price = fill.price

                if fill.side == OrderSide.BUY:
                    self.positions[symbol] += quantity
                    symbol_costs[symbol] += quantity * price
                    symbol_quantities[symbol] += quantity
                else:  # SELL
                    # Calculate realized P&L for this sell
                    if symbol in self.avg_prices and self.avg_prices[symbol] > 0:
                        avg_cost = self.avg_prices[symbol]
                        realized = quantity * (price - avg_cost)
                        self.realized_pnl[symbol] += realized

                    self.positions[symbol] -= quantity
                    symbol_costs[symbol] -= quantity * price  # Reduce cost basis

        # Calculate average prices
        for symbol in self.positions:
            if symbol_quantities[symbol] > 0:
                self.avg_prices[symbol] = symbol_costs[symbol] / symbol_quantities[symbol]

    def calculate_current_pnl(self) -> PnlSnapshot:
        """Calculate current P&L snapshot."""
        total_realized = sum(self.realized_pnl.values())
        total_unrealized = 0.0
        market_values = {}

        # Calculate unrealized P&L based on current market prices
        for symbol, position in self.positions.items():
            if position != 0 and symbol in self.avg_prices:
                # Get current market price
                market_price = self.get_market_price(symbol)
                market_value = position * market_price
                market_values[symbol] = market_value

                # Calculate unrealized P&L
                cost_basis = position * self.avg_prices[symbol]
                unrealized = market_value - cost_basis
                total_unrealized += unrealized

        return PnlSnapshot(
            timestamp=datetime.now(),
            realized_pnl=total_realized,
            unrealized_pnl=total_unrealized,
            total_pnl=total_realized + total_unrealized,
            positions=dict(self.positions),
            market_values=market_values,
        )

    def get_market_price(self, symbol: str) -> float:
        """Get current market price for a symbol."""
        if self.broker and hasattr(self.broker, "get_market_price"):
            return self.broker.get_market_price(symbol)
        return self.avg_prices.get(symbol, 0.0)  # Fallback to avg price

    def update_statistics(self, current_pnl: PnlSnapshot):
        """Update P&L statistics."""
        self.current_stats.total_realized = current_pnl.realized_pnl
        self.current_stats.total_unrealized = current_pnl.unrealized_pnl
        self.current_stats.total_pnl = current_pnl.total_pnl

        # Track max profit and drawdown
        if current_pnl.total_pnl > self.current_stats.max_profit:
            self.current_stats.max_profit = current_pnl.total_pnl

        drawdown = self.current_stats.max_profit - current_pnl.total_pnl
        if drawdown > self.current_stats.max_drawdown:
            self.current_stats.max_drawdown = drawdown

        # Calculate win rate (simplified)
        total_trades = len([pnl for pnl in self.realized_pnl.values() if pnl != 0])
        winning_trades = len([pnl for pnl in self.realized_pnl.values() if pnl > 0])

        self.current_stats.total_trades = total_trades
        self.current_stats.winning_trades = winning_trades
        self.current_stats.losing_trades = total_trades - winning_trades

        if total_trades > 0:
            self.current_stats.win_rate = (winning_trades / total_trades) * 100
        else:
            self.current_stats.win_rate = 0.0

    def update_symbol_summary(self):
        """Update the P&L summary table by symbol."""
        for symbol in set(list(self.positions.keys()) + list(self.realized_pnl.keys())):
            position = self.positions.get(symbol, 0.0)
            avg_price = self.avg_prices.get(symbol, 0.0)
            market_price = self.get_market_price(symbol)
            market_value = position * market_price
            realized = self.realized_pnl.get(symbol, 0.0)

            # Calculate unrealized P&L
            if position != 0 and avg_price > 0:
                cost_basis = position * avg_price
                unrealized = market_value - cost_basis
            else:
                unrealized = 0.0

            data = {
                "position": position,
                "avg_price": avg_price,
                "market_price": market_price,
                "market_value": market_value,
                "realized_pnl": realized,
                "unrealized_pnl": unrealized,
            }

            self.pnl_model.update_symbol_pnl(symbol, data)

    def update_summary_labels(self, current_pnl: PnlSnapshot):
        """Update the summary labels."""
        # Set color based on P&L
        color = "green" if current_pnl.total_pnl >= 0 else "red"
        self.total_pnl_label.setText(f"${current_pnl.total_pnl:.2f}")
        self.total_pnl_label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")

        self.realized_pnl_label.setText(f"${current_pnl.realized_pnl:.2f}")
        self.unrealized_pnl_label.setText(f"${current_pnl.unrealized_pnl:.2f}")
        self.max_profit_label.setText(f"${self.current_stats.max_profit:.2f}")
        self.max_drawdown_label.setText(f"${self.current_stats.max_drawdown:.2f}")
        self.win_rate_label.setText(f"{self.current_stats.win_rate:.1f}%")

    def update_chart_range(self):
        """Update chart time range."""
        # For now, this is a placeholder
        # In a full implementation, you would filter the data points based on the selected range
        pass

    def reset_pnl(self):
        """Reset P&L calculations."""
        self.pnl_history.clear()
        self.current_stats = PnlStats()
        self.positions.clear()
        self.avg_prices.clear()
        self.realized_pnl.clear()

        self.pnl_chart.clear_data()
        self.pnl_model.clear_data()

        # Reset labels
        self.total_pnl_label.setText("$0.00")
        self.total_pnl_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.realized_pnl_label.setText("$0.00")
        self.unrealized_pnl_label.setText("$0.00")
        self.max_profit_label.setText("$0.00")
        self.max_drawdown_label.setText("$0.00")
        self.win_rate_label.setText("0.0%")

        self.status_label.setText("P&L reset")

    def get_current_pnl_stats(self) -> PnlStats:
        """Get current P&L statistics."""
        return self.current_stats
