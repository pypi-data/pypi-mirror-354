"""Window layout management for EOMS GUI application."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from PySide6.QtCore import QByteArray, QObject, QSettings, Signal
from PySide6.QtWidgets import QMainWindow


class WindowManager(QObject):
    """Manages window layouts and persistence."""

    layout_saved = Signal(str)  # Emitted when layout is saved
    layout_restored = Signal(str)  # Emitted when layout is restored

    def __init__(self, main_window: QMainWindow, parent: Optional[QObject] = None):
        """Initialize window manager.

        Args:
            main_window: The main window to manage
            parent: Parent QObject
        """
        super().__init__(parent)

        self.main_window = main_window
        self.settings = QSettings("AtwaterFinancial", "EOMS")

        # Layout storage
        self._layouts: Dict[str, Dict[str, Any]] = {}
        self._current_layout_name: Optional[str] = None

        # Load saved layouts
        self._load_layouts_from_settings()

    def save_current_layout(self, name: str = "default") -> bool:
        """Save the current window layout.

        Args:
            name: Name for the layout

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Get window geometry and state
            geometry = self.main_window.saveGeometry()
            state = self.main_window.saveState()

            # Convert QByteArray to base64 for JSON storage
            layout_data = {
                "geometry": geometry.toBase64().data().decode("utf-8"),
                "state": state.toBase64().data().decode("utf-8"),
                "window_title": self.main_window.windowTitle(),
            }

            # Store layout
            self._layouts[name] = layout_data
            self._current_layout_name = name

            # Save to settings
            self._save_layouts_to_settings()

            # Emit signal
            self.layout_saved.emit(name)

            return True

        except Exception:
            return False

    def restore_layout(self, name: str = "default") -> bool:
        """Restore a saved window layout.

        Args:
            name: Name of the layout to restore

        Returns:
            True if restored successfully, False otherwise
        """
        if name not in self._layouts:
            return False

        try:
            layout_data = self._layouts[name]

            # Restore geometry
            geometry_bytes = QByteArray.fromBase64(layout_data["geometry"].encode("utf-8"))
            self.main_window.restoreGeometry(geometry_bytes)

            # Restore dock widget state
            state_bytes = QByteArray.fromBase64(layout_data["state"].encode("utf-8"))
            self.main_window.restoreState(state_bytes)

            # Update current layout
            self._current_layout_name = name

            # Emit signal
            self.layout_restored.emit(name)

            return True

        except Exception:
            return False

    def delete_layout(self, name: str) -> bool:
        """Delete a saved layout.

        Args:
            name: Name of the layout to delete

        Returns:
            True if deleted successfully, False if not found
        """
        if name not in self._layouts:
            return False

        del self._layouts[name]

        # Clear current layout if it was deleted
        if self._current_layout_name == name:
            self._current_layout_name = None

        # Save to settings
        self._save_layouts_to_settings()

        return True

    def get_layout_names(self) -> list[str]:
        """Get list of all saved layout names.

        Returns:
            List of layout names
        """
        return list(self._layouts.keys())

    def has_layout(self, name: str) -> bool:
        """Check if a layout exists.

        Args:
            name: Name of the layout

        Returns:
            True if layout exists, False otherwise
        """
        return name in self._layouts

    def get_current_layout_name(self) -> Optional[str]:
        """Get the name of the currently active layout.

        Returns:
            Name of current layout or None if no layout is active
        """
        return self._current_layout_name

    def export_layout(self, name: str, file_path: str) -> bool:
        """Export a layout to a file.

        Args:
            name: Name of the layout to export
            file_path: Path to save the layout file

        Returns:
            True if exported successfully, False otherwise
        """
        if name not in self._layouts:
            return False

        try:
            layout_data = {
                "version": "1.0",
                "layout_name": name,
                "layout": self._layouts[name],
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(layout_data, f, indent=2)

            return True

        except Exception:
            return False

    def import_layout(self, file_path: str, name: Optional[str] = None) -> Optional[str]:
        """Import a layout from a file.

        Args:
            file_path: Path to the layout file
            name: Name to use for the imported layout (uses file name if None)

        Returns:
            Name of the imported layout or None if import failed
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                layout_data = json.load(f)

            # Validate format
            if "layout" not in layout_data:
                return None

            # Determine layout name
            if name is None:
                name = layout_data.get("layout_name", Path(file_path).stem)

            # Store layout
            self._layouts[name] = layout_data["layout"]

            # Save to settings
            self._save_layouts_to_settings()

            return name

        except Exception:
            return None

    def auto_save_layout(self) -> None:
        """Automatically save the current layout to 'auto_save'."""
        self.save_current_layout("auto_save")

    def restore_default_layout(self) -> bool:
        """Restore the default layout if it exists.

        Returns:
            True if default layout was restored, False otherwise
        """
        return self.restore_layout("default")

    def restore_last_layout(self) -> bool:
        """Restore the last saved layout.

        Returns:
            True if layout was restored, False otherwise
        """
        # Try auto_save first, then default
        if self.has_layout("auto_save"):
            return self.restore_layout("auto_save")
        elif self.has_layout("default"):
            return self.restore_layout("default")
        return False

    def save_layout_on_exit(self) -> None:
        """Save current layout as auto_save for restoration on next startup."""
        self.auto_save_layout()

    def _load_layouts_from_settings(self) -> None:
        """Load saved layouts from settings."""
        layouts_json = self.settings.value("window_layouts", "{}")
        try:
            if isinstance(layouts_json, str):
                self._layouts = json.loads(layouts_json)
            else:
                self._layouts = {}
        except (json.JSONDecodeError, TypeError):
            self._layouts = {}

        # Load current layout name
        self._current_layout_name = self.settings.value("current_layout", None)

    def _save_layouts_to_settings(self) -> None:
        """Save layouts to settings."""
        layouts_json = json.dumps(self._layouts)
        self.settings.setValue("window_layouts", layouts_json)

        if self._current_layout_name:
            self.settings.setValue("current_layout", self._current_layout_name)
        else:
            self.settings.remove("current_layout")

    def clear_all_layouts(self) -> None:
        """Clear all saved layouts."""
        self._layouts.clear()
        self._current_layout_name = None
        self._save_layouts_to_settings()

    def setup_auto_save(self) -> None:
        """Setup automatic layout saving when the window is closed."""
        # Connect to the main window's closeEvent (requires subclassing or event filter)
        # For now, this is a placeholder - actual implementation would need
        # the main window to call save_layout_on_exit() in its closeEvent
        pass
