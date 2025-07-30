"""
Configuration loader with YAML/ENV support and hot-reload functionality.

Provides unified configuration management with automatic file watching
and environment variable override support.
"""

import logging
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

import yaml
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)


class ConfigChangeEvent:
    """Event emitted when configuration changes."""

    def __init__(self, old_config: Dict[str, Any], new_config: Dict[str, Any]):
        self.old_config = old_config
        self.new_config = new_config
        self.timestamp = time.time()

    def get_changed_keys(self) -> List[str]:
        """Get list of configuration keys that changed."""
        changed = []

        def find_changes(old: Dict, new: Dict, prefix: str = ""):
            for key in set(old.keys()) | set(new.keys()):
                full_key = f"{prefix}.{key}" if prefix else key

                if key not in old:
                    changed.append(full_key)
                elif key not in new:
                    changed.append(full_key)
                elif isinstance(old[key], dict) and isinstance(new[key], dict):
                    find_changes(old[key], new[key], full_key)
                elif old[key] != new[key]:
                    changed.append(full_key)

        find_changes(self.old_config, self.new_config)
        return changed


class ConfigFileHandler(FileSystemEventHandler):
    """File system event handler for configuration file changes."""

    def __init__(self, config_loader: "ConfigLoader"):
        self.config_loader = config_loader
        self._last_modified = {}

    def on_modified(self, event):
        """Handle file modification events."""
        if isinstance(event, FileModifiedEvent) and not event.is_directory:
            file_path = Path(event.src_path)

            # Check if this is our config file
            if file_path.name == self.config_loader.config_file.name:
                # Debounce rapid file changes
                current_time = time.time()
                last_time = self._last_modified.get(str(file_path), 0)

                if current_time - last_time > 0.5:  # 500ms debounce
                    self._last_modified[str(file_path)] = current_time
                    logger.info(f"Config file changed: {file_path}")
                    self.config_loader._reload_config()


class ConfigLoader:
    """
    Configuration loader with YAML file and environment variable support.

    Features:
    - Load configuration from YAML files
    - Environment variable overrides with prefix support
    - Hot-reload with file system watching
    - Dot notation access to nested values
    - Change event notifications
    """

    def __init__(
        self,
        config_file: Union[str, Path],
        env_prefix: str = "EOMS_",
        watch_config: bool = True,
        auto_reload: bool = True,
    ):
        """
        Initialize ConfigLoader.

        Args:
            config_file: Path to YAML configuration file
            env_prefix: Prefix for environment variables
            watch_config: Whether to watch config file for changes
            auto_reload: Whether to automatically reload on changes
        """
        self.config_file = Path(config_file)
        self.env_prefix = env_prefix
        self.watch_config = watch_config
        self.auto_reload = auto_reload

        self._config: Dict[str, Any] = {}
        self._observer: Optional[Observer] = None
        self._change_callbacks: List[Callable[[ConfigChangeEvent], None]] = []
        self._lock = threading.RLock()

        # Load initial configuration
        self._load_config()

        # Start file watching if enabled
        if self.watch_config and self.auto_reload:
            self._start_watching()

    def _load_config(self) -> None:
        """Load configuration from file and environment variables."""
        with self._lock:
            old_config = self._config.copy()

            # Load from YAML file
            yaml_config = self._load_yaml_config()

            # Apply environment variable overrides
            env_config = self._load_env_config()
            self._config = self._merge_configs(yaml_config, env_config)

            logger.info(f"Loaded configuration from {self.config_file}")
            logger.debug(f"Configuration keys: {list(self._config.keys())}")

            # Notify of changes if this is a reload
            if old_config and old_config != self._config:
                change_event = ConfigChangeEvent(old_config, self._config)
                self._notify_change(change_event)

    def _load_yaml_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_file.exists():
            logger.warning(f"Config file does not exist: {self.config_file}")
            return {}

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                logger.debug(f"Loaded YAML config: {config}")
                return config
        except Exception as e:
            logger.error(f"Failed to load YAML config from {self.config_file}: {e}")
            return {}

    def _load_env_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        env_config = {}

        for key, value in os.environ.items():
            if key.startswith(self.env_prefix):
                # Remove prefix and convert to nested dict
                config_key = key[len(self.env_prefix) :].lower()

                # Convert double underscore to dot notation
                config_key = config_key.replace("__", ".")

                # Set nested value
                self._set_nested_value(env_config, config_key, self._parse_env_value(value))

        if env_config:
            logger.debug(f"Loaded env config: {env_config}")

        return env_config

    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        # Handle special case for empty string
        if value == "":
            return value

        # Try to parse as YAML to handle booleans, numbers, lists, etc.
        try:
            parsed = yaml.safe_load(value)
            # Return the parsed value, handling None properly
            return parsed
        except Exception:
            return value

    def _set_nested_value(self, config: Dict[str, Any], key: str, value: Any) -> None:
        """Set a nested configuration value using dot notation."""
        keys = key.split(".")
        current = config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two configuration dictionaries, with override taking precedence."""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def _start_watching(self) -> None:
        """Start file system watching for configuration changes."""
        if not self.config_file.exists():
            logger.warning("Cannot watch non-existent config file")
            return

        try:
            self._observer = Observer()
            handler = ConfigFileHandler(self)

            # Watch the directory containing the config file
            watch_dir = self.config_file.parent
            self._observer.schedule(handler, str(watch_dir), recursive=False)
            self._observer.start()

            logger.info(f"Started watching config file: {self.config_file}")
        except Exception as e:
            logger.error(f"Failed to start config file watching: {e}")

    def _stop_watching(self) -> None:
        """Stop file system watching."""
        if self._observer and self._observer.is_alive():
            self._observer.stop()
            self._observer.join()
            logger.info("Stopped config file watching")

    def _reload_config(self) -> None:
        """Reload configuration from file (called by file watcher)."""
        try:
            self._load_config()
            logger.info("Configuration reloaded successfully")
        except Exception as e:
            logger.error(f"Failed to reload configuration: {e}")

    def _notify_change(self, event: ConfigChangeEvent) -> None:
        """Notify all registered callbacks of configuration changes."""
        changed_keys = event.get_changed_keys()
        logger.info(f"Configuration changed: {changed_keys}")

        for callback in self._change_callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in config change callback: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation like 'database.host')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        with self._lock:
            keys = key.split(".")
            current = self._config

            try:
                for k in keys:
                    current = current[k]
                return current
            except (KeyError, TypeError):
                return default

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value using dot notation.

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        with self._lock:
            old_config = self._config.copy()
            self._set_nested_value(self._config, key, value)

            # Notify of change
            change_event = ConfigChangeEvent(old_config, self._config)
            self._notify_change(change_event)

    def get_all(self) -> Dict[str, Any]:
        """Get a copy of the entire configuration dictionary."""
        with self._lock:
            return self._config.copy()

    def reload(self) -> None:
        """Manually reload configuration from file."""
        self._reload_config()

    def add_change_callback(self, callback: Callable[[ConfigChangeEvent], None]) -> None:
        """
        Add a callback to be called when configuration changes.

        Args:
            callback: Function that takes a ConfigChangeEvent
        """
        self._change_callbacks.append(callback)
        logger.debug(f"Added config change callback: {callback.__name__}")

    def remove_change_callback(self, callback: Callable[[ConfigChangeEvent], None]) -> None:
        """
        Remove a configuration change callback.

        Args:
            callback: Function to remove
        """
        if callback in self._change_callbacks:
            self._change_callbacks.remove(callback)
            logger.debug(f"Removed config change callback: {callback.__name__}")

    def stop(self) -> None:
        """Stop the configuration loader and cleanup resources."""
        self._stop_watching()
        self._change_callbacks.clear()
        logger.info("ConfigLoader stopped")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()

    def __getitem__(self, key: str) -> Any:
        """Dictionary-style access to configuration."""
        value = self.get(key)
        if value is None:
            raise KeyError(f"Configuration key not found: {key}")
        return value

    def __contains__(self, key: str) -> bool:
        """Check if configuration key exists."""
        return self.get(key) is not None

    def __repr__(self) -> str:
        """String representation of ConfigLoader."""
        return f"ConfigLoader(config_file={self.config_file}, " f"keys={list(self._config.keys())})"
