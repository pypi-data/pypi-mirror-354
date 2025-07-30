"""Algo Manager widget for loading and managing trading strategies."""

import importlib.util
import logging
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from eoms.core.eventbus import EventBus
from eoms.strategies.base import (
    BaseStrategy,
    SampleStrategy,
    StrategyEvent,
    StrategyStatus,
)

logger = logging.getLogger(__name__)


class StrategyTableModel(QAbstractTableModel):
    """Table model for loaded strategies."""

    COLUMNS = ["Name", "Status", "File", "Last Event"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.strategies: List[BaseStrategy] = []
        self.strategy_files: Dict[str, str] = {}
        self.last_events: Dict[str, str] = {}

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.strategies)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid() or index.row() >= len(self.strategies):
            return None

        strategy = self.strategies[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == 0:  # Name
                return strategy.name
            elif column == 1:  # Status
                return strategy.status.value.upper()
            elif column == 2:  # File
                return self.strategy_files.get(strategy.name, "Built-in")
            elif column == 3:  # Last Event
                return self.last_events.get(strategy.name, "None")

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.COLUMNS[section]
        return None

    def add_strategy(self, strategy: BaseStrategy, file_path: str = ""):
        """Add a strategy to the model."""
        self.beginInsertRows(QModelIndex(), len(self.strategies), len(self.strategies))
        self.strategies.append(strategy)
        self.strategy_files[strategy.name] = file_path
        self.last_events[strategy.name] = "Loaded"
        self.endInsertRows()

    def remove_strategy(self, row: int):
        """Remove a strategy from the model."""
        if 0 <= row < len(self.strategies):
            strategy = self.strategies[row]
            self.beginRemoveRows(QModelIndex(), row, row)
            self.strategies.pop(row)
            self.strategy_files.pop(strategy.name, None)
            self.last_events.pop(strategy.name, None)
            self.endRemoveRows()

    def get_strategy(self, row: int) -> Optional[BaseStrategy]:
        """Get strategy at row."""
        if 0 <= row < len(self.strategies):
            return self.strategies[row]
        return None

    def update_strategy_event(self, strategy_name: str, event_message: str):
        """Update the last event for a strategy."""
        self.last_events[strategy_name] = event_message
        # Find the row and emit data changed
        for i, strategy in enumerate(self.strategies):
            if strategy.name == strategy_name:
                index = self.index(i, 3)  # Last Event column
                self.dataChanged.emit(index, index)
                break


class AlgoManagerWidget(QWidget):
    """Widget for managing trading algorithms/strategies."""

    strategy_event = Signal(object)  # Emits StrategyEvent objects

    def __init__(self, event_bus: Optional[EventBus] = None, parent=None):
        super().__init__(parent)
        self.event_bus = event_bus
        self.strategy_model = StrategyTableModel()
        self.loaded_strategies: Dict[str, BaseStrategy] = {}

        self.setup_ui()
        self.setup_connections()

        # Add sample strategy by default
        self.load_sample_strategy()

        # Timer for periodic status updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_strategy_status)
        self.update_timer.start(1000)  # Update every second

    def setup_ui(self):
        """Setup the user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Algorithm Manager")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        layout.addWidget(title)

        # Create splitter for table and log
        splitter = QSplitter(Qt.Vertical)

        # Strategy table
        self.strategy_table = QTableView()
        self.strategy_table.setModel(self.strategy_model)
        self.strategy_table.setSelectionBehavior(QTableView.SelectRows)

        # Auto-resize columns
        header = self.strategy_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        splitter.addWidget(self.strategy_table)

        # Event log
        self.event_log = QTextEdit()
        self.event_log.setMaximumHeight(150)
        self.event_log.setReadOnly(True)
        self.event_log.setPlaceholderText("Strategy events will appear here...")
        splitter.addWidget(self.event_log)

        layout.addWidget(splitter)

        # Control buttons
        button_layout = QHBoxLayout()

        self.load_button = QPushButton("Load Strategy")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.remove_button = QPushButton("Remove")
        self.clear_log_button = QPushButton("Clear Log")

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_log_button)

        layout.addLayout(button_layout)

        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def setup_connections(self):
        """Setup signal connections."""
        self.load_button.clicked.connect(self.load_strategy_file)
        self.start_button.clicked.connect(self.start_selected_strategy)
        self.stop_button.clicked.connect(self.stop_selected_strategy)
        self.remove_button.clicked.connect(self.remove_selected_strategy)
        self.clear_log_button.clicked.connect(self.clear_event_log)

        # Enable/disable buttons based on selection
        self.strategy_table.selectionModel().currentChanged.connect(self.update_button_states)

    def load_sample_strategy(self):
        """Load the built-in sample strategy."""
        try:
            sample_strategy = SampleStrategy()
            sample_strategy.set_event_callback(self.on_strategy_event)
            sample_strategy.initialize()

            self.strategy_model.add_strategy(sample_strategy, "Built-in")
            self.loaded_strategies[sample_strategy.name] = sample_strategy

            self.log_event(f"Loaded sample strategy: {sample_strategy.name}")

        except Exception as e:
            logger.error(f"Failed to load sample strategy: {e}")
            self.log_event(f"Error loading sample strategy: {e}")

    def load_strategy_file(self):
        """Load a strategy from a Python file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Strategy File", "", "Python Files (*.py)"
        )

        if not file_path:
            return

        try:
            # Load the Python module
            spec = importlib.util.spec_from_file_location("strategy_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find strategy classes in the module
            strategy_classes = []
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and issubclass(obj, BaseStrategy) and obj != BaseStrategy:
                    strategy_classes.append(obj)

            if not strategy_classes:
                QMessageBox.warning(
                    self,
                    "No Strategies Found",
                    "No valid strategy classes found in the file.",
                )
                return

            # If multiple strategies, could add selection dialog
            # For now, use the first one found
            strategy_class = strategy_classes[0]

            # Create and initialize strategy instance
            strategy = strategy_class()
            strategy.set_event_callback(self.on_strategy_event)

            if strategy.initialize():
                self.strategy_model.add_strategy(strategy, file_path)
                self.loaded_strategies[strategy.name] = strategy

                self.log_event(f"Loaded strategy: {strategy.name} from {Path(file_path).name}")
                self.status_label.setText(f"Loaded: {strategy.name}")
            else:
                QMessageBox.critical(
                    self,
                    "Strategy Initialization Failed",
                    f"Failed to initialize strategy: {strategy.name}",
                )

        except Exception as e:
            logger.error(f"Failed to load strategy from {file_path}: {e}")
            QMessageBox.critical(self, "Load Error", f"Failed to load strategy:\n{str(e)}")

    def start_selected_strategy(self):
        """Start the selected strategy."""
        current_index = self.strategy_table.currentIndex()
        if not current_index.isValid():
            QMessageBox.information(self, "No Selection", "Please select a strategy to start.")
            return

        strategy = self.strategy_model.get_strategy(current_index.row())
        if strategy:
            if strategy.status == StrategyStatus.RUNNING:
                QMessageBox.information(
                    self,
                    "Already Running",
                    f"Strategy {strategy.name} is already running.",
                )
                return

            if strategy.start():
                self.log_event(f"Started strategy: {strategy.name}")
                self.status_label.setText(f"Started: {strategy.name}")
            else:
                QMessageBox.critical(
                    self, "Start Failed", f"Failed to start strategy: {strategy.name}"
                )

    def stop_selected_strategy(self):
        """Stop the selected strategy."""
        current_index = self.strategy_table.currentIndex()
        if not current_index.isValid():
            QMessageBox.information(self, "No Selection", "Please select a strategy to stop.")
            return

        strategy = self.strategy_model.get_strategy(current_index.row())
        if strategy:
            if strategy.status == StrategyStatus.STOPPED:
                QMessageBox.information(
                    self,
                    "Already Stopped",
                    f"Strategy {strategy.name} is already stopped.",
                )
                return

            if strategy.stop():
                self.log_event(f"Stopped strategy: {strategy.name}")
                self.status_label.setText(f"Stopped: {strategy.name}")
            else:
                QMessageBox.critical(
                    self, "Stop Failed", f"Failed to stop strategy: {strategy.name}"
                )

    def remove_selected_strategy(self):
        """Remove the selected strategy."""
        current_index = self.strategy_table.currentIndex()
        if not current_index.isValid():
            QMessageBox.information(self, "No Selection", "Please select a strategy to remove.")
            return

        strategy = self.strategy_model.get_strategy(current_index.row())
        if strategy:
            # Stop strategy if running
            if strategy.status == StrategyStatus.RUNNING:
                strategy.stop()

            # Remove from model and loaded strategies
            self.strategy_model.remove_strategy(current_index.row())
            self.loaded_strategies.pop(strategy.name, None)

            self.log_event(f"Removed strategy: {strategy.name}")
            self.status_label.setText(f"Removed: {strategy.name}")

    def clear_event_log(self):
        """Clear the event log."""
        self.event_log.clear()

    def update_button_states(self):
        """Update button enabled/disabled states based on selection."""
        has_selection = self.strategy_table.currentIndex().isValid()

        self.start_button.setEnabled(has_selection)
        self.stop_button.setEnabled(has_selection)
        self.remove_button.setEnabled(has_selection)

    def update_strategy_status(self):
        """Update strategy status display."""
        # Refresh the table to show current status
        if self.strategy_model.rowCount() > 0:
            top_left = self.strategy_model.index(0, 1)  # Status column
            bottom_right = self.strategy_model.index(self.strategy_model.rowCount() - 1, 1)
            self.strategy_model.dataChanged.emit(top_left, bottom_right)

    def on_strategy_event(self, event: StrategyEvent):
        """Handle strategy events."""
        try:
            # Log the event
            timestamp = event.timestamp.strftime("%H:%M:%S")
            message = f"[{timestamp}] {event.strategy_name}: {event.status.value}"
            if event.message:
                message += f" - {event.message}"

            self.log_event(message)

            # Update the model
            self.strategy_model.update_strategy_event(
                event.strategy_name, event.message or event.status.value
            )

            # Emit signal if event bus is available
            if self.event_bus:
                self.event_bus.publish("algo.status", event)

            # Also emit Qt signal
            self.strategy_event.emit(event)

        except Exception as e:
            logger.error(f"Error handling strategy event: {e}")

    def log_event(self, message: str):
        """Log an event to the event log."""
        self.event_log.append(message)

        # Auto-scroll to bottom
        scrollbar = self.event_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def get_running_strategies(self) -> List[BaseStrategy]:
        """Get list of currently running strategies."""
        return [s for s in self.loaded_strategies.values() if s.status == StrategyStatus.RUNNING]

    def stop_all_strategies(self):
        """Stop all running strategies."""
        for strategy in self.get_running_strategies():
            strategy.stop()
        self.log_event("Stopped all strategies")
