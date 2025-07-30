#!/usr/bin/env python3
"""
Entry point for EOMS GUI application.

This module allows running the EOMS GUI using:
    python -m eoms.gui
"""

import sys

try:
    from PySide6.QtWidgets import QApplication

    from eoms.gui import MainWindow, ThemeManager, WindowManager

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False
    print("PySide6 not available. Install with: pip install -e '.[gui]'")


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
