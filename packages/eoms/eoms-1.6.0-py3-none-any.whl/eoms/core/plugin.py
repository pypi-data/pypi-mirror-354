"""
Plugin system for EOMS with automatic discovery via entry points.

Provides a base plugin interface and loader for extending EOMS functionality.
"""

import logging
from abc import ABC, abstractmethod
from importlib import metadata
from typing import Any, Dict, List, Optional, Type

logger = logging.getLogger(__name__)


class BasePlugin(ABC):
    """
    Abstract base class for EOMS plugins.

    All plugins must inherit from this class and implement the required methods.
    """

    def __init__(self, name: str, version: str = "1.0.0"):
        """
        Initialize the plugin.

        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self._enabled = False

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.

        Args:
            config: Plugin configuration dictionary
        """
        pass

    @abstractmethod
    def start(self) -> None:
        """Start the plugin services."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop the plugin services."""
        pass

    def enable(self) -> None:
        """Enable the plugin."""
        self._enabled = True
        logger.info(f"Plugin {self.name} enabled")

    def disable(self) -> None:
        """Disable the plugin."""
        self._enabled = False
        logger.info(f"Plugin {self.name} disabled")

    @property
    def enabled(self) -> bool:
        """Check if plugin is enabled."""
        return self._enabled

    def get_info(self) -> Dict[str, str]:
        """Get plugin information."""
        return {
            "name": self.name,
            "version": self.version,
            "enabled": str(self._enabled),
        }


class PluginLoader:
    """
    Plugin loader that discovers and manages plugins via entry points.

    Automatically discovers plugins registered in entry points and provides
    methods to load, configure, and manage them.
    """

    def __init__(self, entry_point_group: str = "eoms.plugins"):
        """
        Initialize the plugin loader.

        Args:
            entry_point_group: Entry point group name to search for plugins
        """
        self.entry_point_group = entry_point_group
        self._discovered_plugins: Dict[str, Type[BasePlugin]] = {}
        self._loaded_plugins: Dict[str, BasePlugin] = {}

    def discover_plugins(self) -> Dict[str, Type[BasePlugin]]:
        """
        Discover all available plugins through entry points.

        Returns:
            Dictionary mapping plugin names to plugin classes
        """
        self._discovered_plugins.clear()

        try:
            # Use importlib.metadata to find entry points
            entry_points = metadata.entry_points()

            # Get entry points for our group
            if hasattr(entry_points, "select"):
                # Python 3.10+ API
                plugin_entries = entry_points.select(group=self.entry_point_group)
            else:
                # Python 3.9 API - handle deprecated dict interface
                plugin_entries = entry_points.get(self.entry_point_group) or []

            for entry_point in plugin_entries:
                try:
                    plugin_class = entry_point.load()

                    # Verify it's a BasePlugin subclass
                    if not issubclass(plugin_class, BasePlugin):
                        logger.warning(
                            f"Plugin {entry_point.name} does not inherit " f"from BasePlugin"
                        )
                        continue

                    self._discovered_plugins[entry_point.name] = plugin_class
                    logger.info(f"Discovered plugin: {entry_point.name}")

                except Exception as e:
                    logger.error(f"Failed to load plugin {entry_point.name}: {e}")

        except Exception as e:
            logger.error(f"Failed to discover plugins: {e}")

        return self._discovered_plugins.copy()

    def load_plugin(
        self, plugin_name: str, config: Optional[Dict[str, Any]] = None
    ) -> Optional[BasePlugin]:
        """
        Load and initialize a specific plugin.

        Args:
            plugin_name: Name of the plugin to load
            config: Optional configuration for the plugin

        Returns:
            Loaded plugin instance or None if failed
        """
        if plugin_name in self._loaded_plugins:
            logger.warning(f"Plugin {plugin_name} is already loaded")
            return self._loaded_plugins[plugin_name]

        if plugin_name not in self._discovered_plugins:
            logger.error(f"Plugin {plugin_name} not found in discovered plugins")
            return None

        try:
            plugin_class = self._discovered_plugins[plugin_name]
            plugin_instance = plugin_class(name=plugin_name)

            # Initialize with config
            plugin_instance.initialize(config or {})

            self._loaded_plugins[plugin_name] = plugin_instance
            logger.info(f"Loaded plugin: {plugin_name}")

            return plugin_instance

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return None

    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin.

        Args:
            plugin_name: Name of the plugin to unload

        Returns:
            True if successfully unloaded, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.warning(f"Plugin {plugin_name} is not loaded")
            return False

        try:
            plugin = self._loaded_plugins[plugin_name]

            if plugin.enabled:
                plugin.stop()
                plugin.disable()

            del self._loaded_plugins[plugin_name]
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_name}: {e}")
            return False

    def start_plugin(self, plugin_name: str) -> bool:
        """
        Start a loaded plugin.

        Args:
            plugin_name: Name of the plugin to start

        Returns:
            True if successfully started, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.error(f"Plugin {plugin_name} is not loaded")
            return False

        try:
            plugin = self._loaded_plugins[plugin_name]
            plugin.enable()
            plugin.start()
            logger.info(f"Started plugin: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to start plugin {plugin_name}: {e}")
            return False

    def stop_plugin(self, plugin_name: str) -> bool:
        """
        Stop a running plugin.

        Args:
            plugin_name: Name of the plugin to stop

        Returns:
            True if successfully stopped, False otherwise
        """
        if plugin_name not in self._loaded_plugins:
            logger.error(f"Plugin {plugin_name} is not loaded")
            return False

        try:
            plugin = self._loaded_plugins[plugin_name]
            plugin.stop()
            plugin.disable()
            logger.info(f"Stopped plugin: {plugin_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to stop plugin {plugin_name}: {e}")
            return False

    def get_loaded_plugins(self) -> Dict[str, BasePlugin]:
        """Get all loaded plugins."""
        return self._loaded_plugins.copy()

    def get_discovered_plugins(self) -> Dict[str, Type[BasePlugin]]:
        """Get all discovered plugin classes."""
        return self._discovered_plugins.copy()

    def get_plugin_info(self) -> List[Dict[str, str]]:
        """Get information about all loaded plugins."""
        return [plugin.get_info() for plugin in self._loaded_plugins.values()]
