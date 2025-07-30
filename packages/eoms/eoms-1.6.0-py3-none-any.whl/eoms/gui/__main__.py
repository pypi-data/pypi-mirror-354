#!/usr/bin/env python3
"""
Entry point for EOMS GUI application.

This module allows running the EOMS GUI using:
    python -m eoms.gui
"""

import sys

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from eoms.gui import MainWindow, ThemeManager, WindowManager
    from eoms.gui.widgets import (
        AlgoManagerWidget,
        OrderManagerWidget,
        OrderTicketWidget,
        PNLWindowWidget,
        PositionsManagerWidget,
    )

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available. Install with: pip install -e '.[gui]'")


def setup_default_widgets(main_window: MainWindow) -> None:
    """Setup default trading widgets in the main window.
    
    Args:
        main_window: The main window to add widgets to
    """
    # Create and add Order Ticket widget
    order_ticket = OrderTicketWidget()
    main_window.add_dockable_module(
        "order_ticket",
        "Order Ticket", 
        order_ticket,
        Qt.LeftDockWidgetArea
    )
    
    # Create and add Positions Manager widget
    positions_manager = PositionsManagerWidget()
    main_window.add_dockable_module(
        "positions",
        "Positions Manager",
        positions_manager,
        Qt.LeftDockWidgetArea
    )
    
    # Create and add Order Manager widget
    order_manager = OrderManagerWidget()
    main_window.add_dockable_module(
        "orders",
        "Order Manager",
        order_manager,
        Qt.RightDockWidgetArea
    )
    
    # Create and add P&L Window widget
    pnl_window = PNLWindowWidget()
    main_window.add_dockable_module(
        "pnl",
        "P&L Window",
        pnl_window,
        Qt.RightDockWidgetArea
    )
    
    # Create and add Algorithm Manager widget
    algo_manager = AlgoManagerWidget()
    main_window.add_dockable_module(
        "algos",
        "Algorithm Manager",
        algo_manager,
        Qt.BottomDockWidgetArea
    )


def main():
    """Main GUI application entry point."""
    if not PYSIDE6_AVAILABLE:
        print("Error: PySide6 is required to run the GUI.")
        print("Install with: pip install -e '.[gui]'")
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName("EOMS")
    app.setApplicationDisplayName("EOMS - Execution & Order Management System")

    # Create main window
    main_window = MainWindow()

    # Setup theme manager and window manager
    # Note: These are created for proper initialization but not stored
    # as they're used internally by the GUI framework
    ThemeManager()
    WindowManager(main_window)
    
    # Setup default trading widgets
    setup_default_widgets(main_window)

    # Show the window
    main_window.show()

    # Add status message
    main_window.status_bar.showMessage("EOMS ready")

    print("EOMS GUI application started")
    print("Close window to exit")

    # Run the application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
