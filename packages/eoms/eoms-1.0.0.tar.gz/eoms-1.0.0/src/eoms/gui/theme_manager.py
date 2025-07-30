"""Theme management for EOMS GUI application."""

from enum import Enum
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QSettings, Signal
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


class Theme(Enum):
    """Available themes."""

    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # Follow system theme


class ThemeManager(QObject):
    """Manages application themes and custom CSS styling."""

    theme_changed = Signal(str)  # Emitted when theme changes

    def __init__(self, parent: Optional[QObject] = None):
        """Initialize theme manager."""
        super().__init__(parent)

        self.settings = QSettings("AtwaterFinancial", "EOMS")
        self._current_theme = Theme.LIGHT
        self._custom_css: Optional[str] = None

        # Load saved theme
        self._load_theme_from_settings()

    def _load_theme_from_settings(self) -> None:
        """Load theme setting from persistent storage."""
        theme_name = self.settings.value("theme", Theme.LIGHT.value)
        try:
            self._current_theme = Theme(theme_name)
        except ValueError:
            self._current_theme = Theme.LIGHT

        # Load custom CSS
        custom_css = self.settings.value("custom_css", "")
        if custom_css:
            self._custom_css = custom_css

    def get_current_theme(self) -> Theme:
        """Get the currently active theme.

        Returns:
            The current theme
        """
        return self._current_theme

    def set_theme(self, theme: Theme) -> None:
        """Set the application theme.

        Args:
            theme: The theme to apply
        """
        if theme == self._current_theme:
            return

        self._current_theme = theme

        # Save to settings
        self.settings.setValue("theme", theme.value)

        # Apply the theme
        self._apply_theme()

        # Emit signal
        self.theme_changed.emit(theme.value)

    def get_custom_css(self) -> Optional[str]:
        """Get the current custom CSS.

        Returns:
            Custom CSS string or None if not set
        """
        return self._custom_css

    def set_custom_css(self, css: str) -> None:
        """Set custom CSS for the application.

        Args:
            css: CSS string to apply
        """
        self._custom_css = css

        # Save to settings
        self.settings.setValue("custom_css", css)

        # Apply the CSS
        self._apply_theme()

    def clear_custom_css(self) -> None:
        """Clear custom CSS."""
        self._custom_css = None
        self.settings.remove("custom_css")
        self._apply_theme()

    def load_css_from_file(self, file_path: str) -> bool:
        """Load custom CSS from a file.

        Args:
            file_path: Path to the CSS file

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False

            with open(path, "r", encoding="utf-8") as f:
                css_content = f.read()

            self.set_custom_css(css_content)
            return True

        except Exception:
            return False

    def _apply_theme(self) -> None:
        """Apply the current theme to the application."""
        app = QApplication.instance()
        if app is None:
            return

        # Get base theme CSS
        theme_css = self._get_theme_css()

        # Combine with custom CSS
        full_css = theme_css
        if self._custom_css:
            full_css += "\n\n/* Custom CSS */\n" + self._custom_css

        # Apply to application
        app.setStyleSheet(full_css)

        # Set palette for consistency
        palette = self._get_theme_palette()
        if palette:
            app.setPalette(palette)

    def _get_theme_css(self) -> str:
        """Get CSS for the current theme.

        Returns:
            CSS string for the theme
        """
        if self._current_theme == Theme.DARK:
            return self._get_dark_theme_css()
        elif self._current_theme == Theme.AUTO:
            # For now, use light theme. In the future, detect system theme
            return self._get_light_theme_css()
        else:  # LIGHT
            return self._get_light_theme_css()

    def _get_light_theme_css(self) -> str:
        """Get CSS for light theme.

        Returns:
            Light theme CSS
        """
        return """
        /* Light Theme */
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }

        QDockWidget {
            background-color: #f5f5f5;
            color: #000000;
            titlebar-close-icon: url(close.png);
            titlebar-normal-icon: url(undock.png);
        }

        QDockWidget::title {
            background-color: #e0e0e0;
            border: 1px solid #c0c0c0;
            padding: 4px;
            text-align: center;
        }

        QMenuBar {
            background-color: #f0f0f0;
            color: #000000;
            border-bottom: 1px solid #d0d0d0;
        }

        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }

        QMenuBar::item:selected {
            background-color: #d0d0d0;
        }

        QStatusBar {
            background-color: #f0f0f0;
            color: #000000;
            border-top: 1px solid #d0d0d0;
        }

        QTableView {
            background-color: #ffffff;
            alternate-background-color: #f9f9f9;
            gridline-color: #e0e0e0;
        }

        QTableView::item:selected {
            background-color: #0078d4;
            color: #ffffff;
        }
        """

    def _get_dark_theme_css(self) -> str:
        """Get CSS for dark theme.

        Returns:
            Dark theme CSS
        """
        return """
        /* Dark Theme */
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }

        QDockWidget {
            background-color: #3c3c3c;
            color: #ffffff;
        }

        QDockWidget::title {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 4px;
            text-align: center;
            color: #ffffff;
        }

        QMenuBar {
            background-color: #353535;
            color: #ffffff;
            border-bottom: 1px solid #555555;
        }

        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }

        QMenuBar::item:selected {
            background-color: #555555;
        }

        QStatusBar {
            background-color: #353535;
            color: #ffffff;
            border-top: 1px solid #555555;
        }

        QTableView {
            background-color: #2b2b2b;
            alternate-background-color: #353535;
            gridline-color: #555555;
            color: #ffffff;
        }

        QTableView::item:selected {
            background-color: #0078d4;
            color: #ffffff;
        }

        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        """

    def _get_theme_palette(self) -> Optional[QPalette]:
        """Get color palette for the current theme.

        Returns:
            QPalette for the theme or None
        """
        if self._current_theme == Theme.DARK:
            palette = QPalette()

            # Window colors
            palette.setColor(QPalette.Window, QColor(43, 43, 43))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))

            # Base colors (input fields)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))

            # Text colors
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))

            # Button colors
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))

            # Highlight colors
            palette.setColor(QPalette.Highlight, QColor(0, 120, 212))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

            return palette

        return None  # Use default palette for light theme

    def apply_theme(self) -> None:
        """Apply the current theme immediately."""
        self._apply_theme()

    def reset_to_default(self) -> None:
        """Reset theme to default (light theme, no custom CSS)."""
        self.set_theme(Theme.LIGHT)
        self.clear_custom_css()
