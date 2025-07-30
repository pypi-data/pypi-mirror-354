"""Main window for EOMS GUI application."""

from typing import Dict, List, Optional

from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QMainWindow,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class DockableModule(QDockWidget):
    """A dockable module that can be undocked and redocked."""

    undocked = Signal(str)  # Emitted when module is undocked
    redocked = Signal(str)  # Emitted when module is redocked

    def __init__(self, name: str, title: str, parent: Optional[QWidget] = None):
        """Initialize dockable module.

        Args:
            name: Internal name for the module
            title: Display title for the dock widget
            parent: Parent widget
        """
        super().__init__(title, parent)
        self.module_name = name

        # Allow the widget to be moved, floated, and closed
        self.setFeatures(
            QDockWidget.DockWidgetMovable
            | QDockWidget.DockWidgetFloatable
            | QDockWidget.DockWidgetClosable
        )

        # Connect signals to track docking state
        self.topLevelChanged.connect(self._on_top_level_changed)

    def _on_top_level_changed(self, top_level: bool) -> None:
        """Handle when the dock widget becomes floating or docked.

        Args:
            top_level: True if widget is floating, False if docked
        """
        if top_level:
            self.undocked.emit(self.module_name)
        else:
            self.redocked.emit(self.module_name)


class MainWindow(QMainWindow):
    """Main application window with dockable modules."""

    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize main window."""
        super().__init__(parent)

        self.setWindowTitle("EOMS - Execution & Order Management System")
        self.setMinimumSize(1200, 800)

        # Store dockable modules
        self._modules: Dict[str, DockableModule] = {}

        # Setup UI components
        self._setup_ui()

        # Setup window settings
        self.settings = QSettings("AtwaterFinancial", "EOMS")

    def _setup_ui(self) -> None:
        """Setup the main window UI."""
        # Create central widget
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

        # Create menu bar
        self._setup_menu_bar()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _setup_menu_bar(self) -> None:
        """Setup the application menu bar."""
        menu_bar = self.menuBar()

        # View menu for showing/hiding dock widgets
        view_menu = menu_bar.addMenu("&View")
        self.view_menu = view_menu

        # Window menu for layout management
        window_menu = menu_bar.addMenu("&Window")
        self.window_menu = window_menu

    def add_dockable_module(
        self, name: str, title: str, widget: QWidget, area: int = None
    ) -> "DockableModule":
        """Add a dockable module to the main window.

        Args:
            name: Internal name for the module
            title: Display title for the module
            widget: The widget to dock
            area: Qt dock area (defaults to LeftDockWidgetArea)

        Returns:
            The created DockableModule
        """
        if area is None:
            from PySide6.QtCore import Qt

            area = Qt.LeftDockWidgetArea

        # Create the dockable module
        dock_module = DockableModule(name, title, self)
        dock_module.setWidget(widget)

        # Connect signals
        dock_module.undocked.connect(self._on_module_undocked)
        dock_module.redocked.connect(self._on_module_redocked)

        # Add to main window
        self.addDockWidget(area, dock_module)

        # Store reference
        self._modules[name] = dock_module

        # Add to view menu
        toggle_action = dock_module.toggleViewAction()
        self.view_menu.addAction(toggle_action)

        return dock_module

    def remove_dockable_module(self, name: str) -> bool:
        """Remove a dockable module from the main window.

        Args:
            name: Name of the module to remove

        Returns:
            True if module was removed, False if not found
        """
        if name not in self._modules:
            return False

        dock_module = self._modules[name]

        # Remove from view menu
        toggle_action = dock_module.toggleViewAction()
        self.view_menu.removeAction(toggle_action)

        # Remove from main window
        self.removeDockWidget(dock_module)

        # Clean up
        dock_module.deleteLater()
        del self._modules[name]

        return True

    def get_module(self, name: str) -> "Optional[DockableModule]":
        """Get a dockable module by name.

        Args:
            name: Name of the module

        Returns:
            The module if found, None otherwise
        """
        return self._modules.get(name)

    def get_module_names(self) -> List[str]:
        """Get list of all module names.

        Returns:
            List of module names
        """
        return list(self._modules.keys())

    def is_module_docked(self, name: str) -> bool:
        """Check if a module is currently docked.

        Args:
            name: Name of the module

        Returns:
            True if module is docked, False if floating or not found
        """
        module = self._modules.get(name)
        if module is None:
            return False
        return not module.isFloating()

    def _on_module_undocked(self, name: str) -> None:
        """Handle when a module is undocked (becomes floating).

        Args:
            name: Name of the undocked module
        """
        self.status_bar.showMessage(f"Module '{name}' undocked")

    def _on_module_redocked(self, name: str) -> None:
        """Handle when a module is redocked.

        Args:
            name: Name of the redocked module
        """
        self.status_bar.showMessage(f"Module '{name}' redocked")


def create_application() -> QApplication:
    """Create and configure the Qt application.

    Returns:
        Configured QApplication instance
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    app.setApplicationName("EOMS")
    app.setApplicationDisplayName("Execution & Order Management System")
    app.setOrganizationName("Atwater Financial")
    app.setOrganizationDomain("atwaterfinancial.com")

    return app
