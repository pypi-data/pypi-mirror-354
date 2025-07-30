"""High-performance table view with virtual scrolling for EOMS GUI."""

from typing import Any, Callable, Dict, List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt, QTimer
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableView


class VirtualTableModel(QAbstractTableModel):
    """High-performance table model supporting virtual scrolling for large datasets."""

    def __init__(self, parent: Optional[QObject] = None):
        """Initialize virtual table model.

        Args:
            parent: Parent QObject
        """
        super().__init__(parent)

        # Data source - can be a function that returns data for a given range
        self._data_source: Optional[Callable[[int, int], List[List[Any]]]] = None
        self._total_rows = 0
        self._column_count = 0
        self._headers: List[str] = []

        # Cache for performance
        self._cache: Dict[int, List[Any]] = {}
        self._cache_size = 1000  # Number of rows to cache
        self._cache_start = 0
        self._cache_end = 0

        # Update batching
        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self._flush_updates)
        self._pending_updates: set = set()

    def set_data_source(
        self,
        data_source: Callable[[int, int], List[List[Any]]],
        total_rows: int,
        column_count: int,
        headers: List[str] = None,
    ) -> None:
        """Set the data source for virtual scrolling.

        Args:
            data_source: Function that returns data for a range (start_row, end_row)
            total_rows: Total number of rows in the dataset
            column_count: Number of columns
            headers: Optional column headers
        """
        self.beginResetModel()

        self._data_source = data_source
        self._total_rows = total_rows
        self._column_count = column_count
        self._headers = headers or [f"Column {i+1}" for i in range(column_count)]

        # Clear cache
        self._cache.clear()
        self._cache_start = 0
        self._cache_end = 0

        self.endResetModel()

    def _ensure_cached(self, row: int) -> None:
        """Ensure the specified row is in cache.

        Args:
            row: Row index to ensure is cached
        """
        if not self._data_source:
            return

        # Check if row is in cache
        if self._cache_start <= row < self._cache_end:
            return

        # Calculate new cache range centered on the requested row
        cache_half = self._cache_size // 2
        new_start = max(0, row - cache_half)
        new_end = min(self._total_rows, new_start + self._cache_size)

        # Adjust start if we're near the end
        if new_end - new_start < self._cache_size:
            new_start = max(0, new_end - self._cache_size)

        # Load new cache data
        try:
            cache_data = self._data_source(new_start, new_end)

            # Update cache
            self._cache.clear()
            for i, row_data in enumerate(cache_data):
                self._cache[new_start + i] = row_data

            self._cache_start = new_start
            self._cache_end = new_end

        except Exception:
            # If data loading fails, clear cache
            self._cache.clear()
            self._cache_start = 0
            self._cache_end = 0

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get total number of rows.

        Args:
            parent: Parent index (unused)

        Returns:
            Total number of rows
        """
        return self._total_rows

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get number of columns.

        Args:
            parent: Parent index (unused)

        Returns:
            Number of columns
        """
        return self._column_count

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        """Get data for a cell.

        Args:
            index: Model index
            role: Data role

        Returns:
            Cell data
        """
        if not index.isValid() or not self._data_source:
            return None

        row, col = index.row(), index.column()

        if row < 0 or row >= self._total_rows or col < 0 or col >= self._column_count:
            return None

        if role == Qt.DisplayRole:
            # Ensure row is cached
            self._ensure_cached(row)

            # Get data from cache
            if row in self._cache and col < len(self._cache[row]):
                value = self._cache[row][col]
                return str(value) if value is not None else ""

        elif role == Qt.TextAlignmentRole:
            # Right-align numbers
            self._ensure_cached(row)
            if row in self._cache and col < len(self._cache[row]):
                value = self._cache[row][col]
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
            Header data
        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if 0 <= section < len(self._headers):
                return self._headers[section]
        elif orientation == Qt.Vertical:
            return str(section + 1)

        return None

    def invalidate_cache(self) -> None:
        """Invalidate the entire cache, forcing a reload."""
        self._cache.clear()
        self._cache_start = 0
        self._cache_end = 0

    def refresh_range(self, start_row: int, end_row: int) -> None:
        """Refresh a specific range of rows.

        Args:
            start_row: Start row index
            end_row: End row index (exclusive)
        """
        if not self._data_source:
            return

        # Check if range overlaps with cache
        if (
            self._cache_start <= start_row < self._cache_end
            or self._cache_start < end_row <= self._cache_end
        ):

            # Invalidate overlapping cache entries
            for row in range(max(start_row, self._cache_start), min(end_row, self._cache_end)):
                if row in self._cache:
                    del self._cache[row]

        # Emit data changed
        top_left = self.index(start_row, 0)
        bottom_right = self.index(end_row - 1, self._column_count - 1)
        self.dataChanged.emit(top_left, bottom_right)


class HighPerformanceTableView(QTableView):
    """High-performance table view optimized for large datasets."""

    def __init__(self, parent: Optional[QObject] = None):
        """Initialize high-performance table view.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Performance optimizations
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Enable sorting
        self.setSortingEnabled(True)

        # Optimize headers
        horizontal_header = self.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
        horizontal_header.setSectionResizeMode(QHeaderView.Interactive)

        vertical_header = self.verticalHeader()
        vertical_header.setDefaultSectionSize(20)  # Compact row height
        vertical_header.setMinimumSectionSize(16)

        # Set up virtual model
        self._virtual_model = VirtualTableModel(self)
        self.setModel(self._virtual_model)

    def set_data_source(
        self,
        data_source: Callable[[int, int], List[List[Any]]],
        total_rows: int,
        column_count: int,
        headers: List[str] = None,
    ) -> None:
        """Set the data source for the table.

        Args:
            data_source: Function that returns data for a range
            total_rows: Total number of rows
            column_count: Number of columns
            headers: Column headers
        """
        self._virtual_model.set_data_source(data_source, total_rows, column_count, headers)

    def refresh_visible_data(self) -> None:
        """Refresh only the currently visible data."""
        if not self.model():
            return

        # Get visible row range
        viewport_rect = self.viewport().rect()
        top_index = self.indexAt(viewport_rect.topLeft())
        bottom_index = self.indexAt(viewport_rect.bottomLeft())

        if top_index.isValid() and bottom_index.isValid():
            start_row = top_index.row()
            end_row = bottom_index.row() + 1

            # Add some buffer
            buffer = 10
            start_row = max(0, start_row - buffer)
            end_row = min(self.model().rowCount(), end_row + buffer)

            self._virtual_model.refresh_range(start_row, end_row)

    def scrollTo(
        self,
        index: QModelIndex,
        hint: QAbstractItemView.ScrollHint = QAbstractItemView.EnsureVisible,
    ) -> None:
        """Optimized scrolling for large datasets.

        Args:
            index: Index to scroll to
            hint: Scroll hint
        """
        # Pre-cache data around the target index
        if index.isValid() and isinstance(self.model(), VirtualTableModel):
            row = index.row()
            buffer = 50  # Cache 50 rows around target
            start = max(0, row - buffer)
            end = min(self.model().rowCount(), row + buffer)

            # This will trigger caching when data() is called
            for r in range(start, min(start + 10, end)):  # Cache first 10 rows immediately
                self.model().index(r, 0)

        super().scrollTo(index, hint)


def create_sample_data_source(num_rows: int) -> Callable[[int, int], List[List[Any]]]:
    """Create a sample data source for testing.

    Args:
        num_rows: Total number of rows to generate

    Returns:
        Data source function
    """

    def data_source(start_row: int, end_row: int) -> List[List[Any]]:
        """Generate sample data for the specified range.

        Args:
            start_row: Start row index
            end_row: End row index (exclusive)

        Returns:
            List of rows, each containing column data
        """
        import random

        data = []
        for row in range(start_row, end_row):
            row_data = [
                f"Row {row + 1}",  # ID column
                f"Item_{row + 1:06d}",  # Name column
                random.randint(1, 1000),  # Quantity
                round(random.uniform(10.0, 500.0), 2),  # Price
                random.choice(["Active", "Inactive", "Pending"]),  # Status
            ]
            data.append(row_data)

        return data

    return data_source


def create_market_data_source(
    symbols: List[str],
) -> Callable[[int, int], List[List[Any]]]:
    """Create a market data source for testing.

    Args:
        symbols: List of trading symbols

    Returns:
        Data source function that generates market data
    """
    import random
    import time

    # Base prices for each symbol
    base_prices = {symbol: random.uniform(50.0, 200.0) for symbol in symbols}

    def data_source(start_row: int, end_row: int) -> List[List[Any]]:
        """Generate market data for the specified range.

        Args:
            start_row: Start row index
            end_row: End row index (exclusive)

        Returns:
            Market data rows
        """
        data = []
        for row in range(start_row, end_row):
            symbol = symbols[row % len(symbols)]
            base_price = base_prices[symbol]

            # Add some random variation
            price = base_price + random.uniform(-5.0, 5.0)
            change = random.uniform(-2.0, 2.0)
            volume = random.randint(1000, 100000)

            row_data = [
                symbol,
                f"{price:.2f}",
                f"{change:+.2f}",
                f"{(change/price)*100:+.2f}%",
                f"{volume:,}",
                time.strftime("%H:%M:%S"),
            ]
            data.append(row_data)

        return data

    return data_source
