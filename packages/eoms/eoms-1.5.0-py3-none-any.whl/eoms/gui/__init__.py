"""GUI components for EOMS."""

from .main_window import MainWindow
from .reactive_models import MarketDataObservable, Observable, ReactiveTableModel
from .theme_manager import ThemeManager
from .virtual_table import HighPerformanceTableView, VirtualTableModel
from .widgets import (
    AlgoManagerWidget,
    OrderManagerWidget,
    OrderTicketWidget,
    PNLWindowWidget,
    PositionsManagerWidget,
)
from .window_manager import WindowManager

__all__ = [
    "MainWindow",
    "ThemeManager",
    "WindowManager",
    "Observable",
    "ReactiveTableModel",
    "MarketDataObservable",
    "VirtualTableModel",
    "HighPerformanceTableView",
    "OrderTicketWidget",
    "PositionsManagerWidget",
    "OrderManagerWidget",
    "AlgoManagerWidget",
    "PNLWindowWidget",
]
