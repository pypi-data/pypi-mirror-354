"""Reactive data model bridges for EOMS GUI application."""

from typing import Any, Callable, Dict, List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt, QTimer, Signal


class Observable(QObject):
    """A reactive data container that emits signals when data changes."""

    data_changed = Signal(object)  # Emitted when data changes

    def __init__(self, initial_value: Any = None, parent: Optional[QObject] = None):
        """Initialize observable with optional initial value.

        Args:
            initial_value: Initial value for the observable
            parent: Parent QObject
        """
        super().__init__(parent)
        self._value = initial_value
        self._subscribers: List[Callable[[Any], None]] = []

    def get_value(self) -> Any:
        """Get the current value.

        Returns:
            Current value
        """
        return self._value

    def set_value(self, value: Any) -> None:
        """Set a new value and notify subscribers.

        Args:
            value: New value to set
        """
        if self._value != value:
            self._value = value
            self.data_changed.emit(value)

            # Notify subscribers
            for subscriber in self._subscribers:
                try:
                    subscriber(value)
                except Exception:
                    pass  # Don't let subscriber errors break the observable

    def subscribe(self, callback: Callable[[Any], None]) -> None:
        """Subscribe to value changes.

        Args:
            callback: Function to call when value changes
        """
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Any], None]) -> None:
        """Unsubscribe from value changes.

        Args:
            callback: Function to remove from subscribers
        """
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def map(self, transform: Callable[[Any], Any]) -> "Observable":
        """Create a new observable that applies a transformation.

        Args:
            transform: Function to transform the value

        Returns:
            New observable with transformed values
        """
        mapped = Observable(transform(self._value) if self._value is not None else None)

        def update_mapped(value):
            mapped.set_value(transform(value))

        self.subscribe(update_mapped)
        return mapped

    def filter(self, predicate: Callable[[Any], bool]) -> "Observable":
        """Create a new observable that only emits values passing the predicate.

        Args:
            predicate: Function to test values

        Returns:
            New observable with filtered values
        """
        filtered = Observable(
            self._value if self._value is not None and predicate(self._value) else None
        )

        def update_filtered(value):
            if predicate(value):
                filtered.set_value(value)

        self.subscribe(update_filtered)
        return filtered


class ReactiveTableModel(QAbstractTableModel):
    """A table model that reactively updates from Observable data sources."""

    def __init__(self, parent: Optional[QObject] = None):
        """Initialize reactive table model.

        Args:
            parent: Parent QObject
        """
        super().__init__(parent)

        self._data: List[List[Any]] = []
        self._headers: List[str] = []
        self._observables: Dict[tuple, Observable] = {}  # (row, col) -> Observable

        # Performance optimization
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._process_pending_updates)
        self._pending_updates: set = set()

    def set_headers(self, headers: List[str]) -> None:
        """Set column headers.

        Args:
            headers: List of header names
        """
        self.beginResetModel()
        self._headers = headers.copy()
        self.endResetModel()

    def set_data_size(self, rows: int, cols: int) -> None:
        """Set the size of the data model.

        Args:
            rows: Number of rows
            cols: Number of columns
        """
        self.beginResetModel()
        self._data = [[None for _ in range(cols)] for _ in range(rows)]
        self.endResetModel()

    def bind_cell(self, row: int, col: int, observable: Observable) -> None:
        """Bind a cell to an observable data source.

        Args:
            row: Row index
            col: Column index
            observable: Observable to bind to this cell
        """
        # Store observable reference
        self._observables[(row, col)] = observable

        # Set initial value
        if len(self._data) > row and len(self._data[row]) > col:
            self._data[row][col] = observable.get_value()

        # Connect to updates
        observable.data_changed.connect(
            lambda value, r=row, c=col: self._schedule_cell_update(r, c, value)
        )

    def _schedule_cell_update(self, row: int, col: int, value: Any) -> None:
        """Schedule a cell update for batch processing.

        Args:
            row: Row index
            col: Column index
            value: New value
        """
        # Update data immediately
        if len(self._data) > row and len(self._data[row]) > col:
            self._data[row][col] = value

        # Schedule UI update
        self._pending_updates.add((row, col))

        # Batch updates for performance (50ms delay)
        if not self._update_timer.isActive():
            self._update_timer.start(50)

    def _process_pending_updates(self) -> None:
        """Process all pending cell updates."""
        if not self._pending_updates:
            return

        # Find the bounding rectangle of all updates
        min_row = min(row for row, col in self._pending_updates)
        max_row = max(row for row, col in self._pending_updates)
        min_col = min(col for row, col in self._pending_updates)
        max_col = max(col for row, col in self._pending_updates)

        # Emit data changed for the bounding rectangle
        top_left = self.index(min_row, min_col)
        bottom_right = self.index(max_row, max_col)
        self.dataChanged.emit(top_left, bottom_right, [Qt.DisplayRole])

        # Clear pending updates
        self._pending_updates.clear()

    def bind_row(self, row: int, observables: "List[Observable]") -> None:
        """Bind an entire row to a list of observables.

        Args:
            row: Row index
            observables: List of observables for each column
        """
        for col, observable in enumerate(observables):
            if observable is not None:
                self.bind_cell(row, col, observable)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get number of rows.

        Args:
            parent: Parent index (unused for table model)

        Returns:
            Number of rows
        """
        return len(self._data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get number of columns.

        Args:
            parent: Parent index (unused for table model)

        Returns:
            Number of columns
        """
        return len(self._headers) if self._headers else (len(self._data[0]) if self._data else 0)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """Get data for a cell.

        Args:
            index: Model index
            role: Data role

        Returns:
            Cell data or None
        """
        if not index.isValid():
            return None

        row, col = index.row(), index.column()

        if row >= len(self._data) or col >= len(self._data[row]) or row < 0 or col < 0:
            return None

        if role == Qt.DisplayRole:
            value = self._data[row][col]
            return str(value) if value is not None else ""
        elif role == Qt.TextAlignmentRole:
            # Right-align numbers
            value = self._data[row][col]
            if isinstance(value, (int, float)):
                return Qt.AlignRight | Qt.AlignVCenter

        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole
    ) -> Any:
        """Get header data.

        Args:
            section: Section index
            orientation: Horizontal or vertical
            role: Data role

        Returns:
            Header data or None
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if 0 <= section < len(self._headers):
                return self._headers[section]
        elif orientation == Qt.Vertical:
            return str(section + 1)

        return None

    def get_observable(self, row: int, col: int) -> "Optional[Observable]":
        """Get the observable bound to a specific cell.

        Args:
            row: Row index
            col: Column index

        Returns:
            Observable if bound, None otherwise
        """
        return self._observables.get((row, col))


class MarketDataObservable(Observable):
    """Specialized observable for market data with price formatting."""

    def __init__(self, symbol: str, initial_price: float = 0.0, parent: Optional[QObject] = None):
        """Initialize market data observable.

        Args:
            symbol: Trading symbol
            initial_price: Initial price
            parent: Parent QObject
        """
        super().__init__(initial_price, parent)
        self.symbol = symbol
        self._last_price = initial_price

    def update_price(self, price: float) -> None:
        """Update the price and calculate change.

        Args:
            price: New price
        """
        old_price = self._last_price
        self._last_price = price

        # Create price update data
        price_data = {
            "symbol": self.symbol,
            "price": price,
            "change": price - old_price if old_price > 0 else 0.0,
            "change_pct": (((price - old_price) / old_price * 100) if old_price > 0 else 0.0),
        }

        self.set_value(price_data)

    def get_formatted_price(self) -> str:
        """Get formatted price string.

        Returns:
            Formatted price
        """
        data = self.get_value()
        if isinstance(data, dict) and "price" in data:
            return f"{data['price']:.2f}"
        return "0.00"

    def get_formatted_change(self) -> str:
        """Get formatted change string.

        Returns:
            Formatted change with +/- sign
        """
        data = self.get_value()
        if isinstance(data, dict) and "change" in data:
            change = data["change"]
            sign = "+" if change >= 0 else ""
            return f"{sign}{change:.2f}"
        return "+0.00"
