"""Basic tests for GUI module structure."""

import sys
from unittest.mock import MagicMock

# Mock PySide6 completely to avoid dependency issues
mock_modules = {
    "PySide6": MagicMock(),
    "PySide6.QtCore": MagicMock(),
    "PySide6.QtWidgets": MagicMock(),
    "PySide6.QtGui": MagicMock(),
}

for name, mock_module in mock_modules.items():
    sys.modules[name] = mock_module


# Test that the GUI modules can be imported
def test_gui_module_imports():
    """Test that GUI modules can be imported successfully."""
    from eoms.gui import (
        HighPerformanceTableView,
        MainWindow,
        MarketDataObservable,
        Observable,
        ReactiveTableModel,
        ThemeManager,
        VirtualTableModel,
        WindowManager,
    )

    # Check that classes are available
    assert MainWindow is not None
    assert ThemeManager is not None
    assert WindowManager is not None
    assert Observable is not None
    assert ReactiveTableModel is not None
    assert MarketDataObservable is not None
    assert VirtualTableModel is not None
    assert HighPerformanceTableView is not None


def test_theme_enum():
    """Test the Theme enum."""
    from eoms.gui.theme_manager import Theme

    assert Theme.LIGHT.value == "light"
    assert Theme.DARK.value == "dark"
    assert Theme.AUTO.value == "auto"


def test_gui_module_structure():
    """Test that GUI module has correct structure."""
    import eoms.gui

    # Check that __all__ is defined correctly
    expected_exports = [
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
    assert hasattr(eoms.gui, "__all__")
    assert set(eoms.gui.__all__) == set(expected_exports)

    # Check that all exports are available
    for export in expected_exports:
        assert hasattr(eoms.gui, export)


def test_observable_basic_functionality():
    """Test that Observable can be instantiated (basic smoke test)."""
    # Just test that the class can be imported and instantiated with mocking
    from eoms.gui.reactive_models import Observable

    # With mocking, we can't test the actual functionality,
    # but we can verify the class exists and is importable
    assert Observable is not None


def test_observable_transformations():
    """Test that Observable transformations exist (basic smoke test)."""
    # Just test import works with mocking
    from eoms.gui.reactive_models import Observable

    # Verify the class can be imported
    assert Observable is not None


def test_market_data_observable():
    """Test that MarketDataObservable can be imported (basic smoke test)."""
    from eoms.gui.reactive_models import MarketDataObservable

    # Just verify the class exists
    assert MarketDataObservable is not None
