"""Tests for the ConfigLoader implementation."""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from eoms.core.config import ConfigChangeEvent, ConfigLoader


class TestConfigChangeEvent:
    """Test cases for ConfigChangeEvent."""

    def test_config_change_event_creation(self):
        """Test ConfigChangeEvent creation."""
        old_config = {"key1": "value1", "key2": {"nested": "old"}}
        new_config = {"key1": "value2", "key2": {"nested": "new"}, "key3": "added"}

        event = ConfigChangeEvent(old_config, new_config)

        assert event.old_config == old_config
        assert event.new_config == new_config
        assert isinstance(event.timestamp, float)

    def test_get_changed_keys(self):
        """Test getting changed configuration keys."""
        old_config = {
            "unchanged": "same",
            "modified": "old_value",
            "nested": {"unchanged_nested": "same", "modified_nested": "old"},
            "removed": "will_be_removed",
        }
        new_config = {
            "unchanged": "same",
            "modified": "new_value",
            "nested": {"unchanged_nested": "same", "modified_nested": "new"},
            "added": "new_key",
        }

        event = ConfigChangeEvent(old_config, new_config)
        changed_keys = event.get_changed_keys()

        assert "modified" in changed_keys
        assert "nested.modified_nested" in changed_keys
        assert "added" in changed_keys
        assert "removed" in changed_keys
        assert "unchanged" not in changed_keys
        assert "nested.unchanged_nested" not in changed_keys


class TestConfigLoader:
    """Test cases for ConfigLoader functionality."""

    def create_temp_config(self, config_data: dict) -> Path:
        """Create a temporary configuration file."""
        fd, path = tempfile.mkstemp(suffix=".yaml")
        try:
            with os.fdopen(fd, "w") as f:
                yaml.dump(config_data, f)
        except:
            os.close(fd)
            raise
        return Path(path)

    def test_config_loader_creation_with_existing_file(self):
        """Test ConfigLoader creation with existing config file."""
        config_data = {
            "app": {"name": "EOMS", "debug": True},
            "database": {"host": "localhost", "port": 5432},
        }

        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            assert loader.config_file == config_file
            assert loader.get("app.name") == "EOMS"
            assert loader.get("app.debug") is True
            assert loader.get("database.host") == "localhost"
            assert loader.get("database.port") == 5432

            loader.stop()
        finally:
            config_file.unlink()

    def test_config_loader_creation_with_nonexistent_file(self):
        """Test ConfigLoader creation with non-existent config file."""
        nonexistent_file = Path("/tmp/nonexistent_config.yaml")

        loader = ConfigLoader(nonexistent_file, watch_config=False)

        # Should create empty config
        assert loader.get_all() == {}
        assert loader.get("any.key") is None
        assert loader.get("any.key", "default") == "default"

        loader.stop()

    def test_environment_variable_overrides(self):
        """Test environment variable configuration overrides."""
        config_data = {"app": {"name": "EOMS", "debug": False}}
        config_file = self.create_temp_config(config_data)

        try:
            # Set environment variables
            with patch.dict(
                os.environ,
                {
                    "EOMS_APP__NAME": "EOMS_ENV",
                    "EOMS_APP__DEBUG": "true",
                    "EOMS_DATABASE__HOST": "env-host",
                    "EOMS_DATABASE__PORT": "3306",
                },
            ):
                loader = ConfigLoader(config_file, env_prefix="EOMS_", watch_config=False)

                # Environment variables should override file values
                assert loader.get("app.name") == "EOMS_ENV"
                assert loader.get("app.debug") is True
                assert loader.get("database.host") == "env-host"
                assert loader.get("database.port") == 3306

                loader.stop()
        finally:
            config_file.unlink()

    def test_env_value_parsing(self):
        """Test environment variable value parsing."""
        config_file = self.create_temp_config({})

        try:
            with patch.dict(
                os.environ,
                {
                    "EOMS_STRING": "hello",
                    "EOMS_INT": "42",
                    "EOMS_FLOAT": "3.14",
                    "EOMS_BOOL_TRUE": "true",
                    "EOMS_BOOL_FALSE": "false",
                    "EOMS_LIST": "[1, 2, 3]",
                    "EOMS_NULL": "null",
                },
            ):
                loader = ConfigLoader(config_file, env_prefix="EOMS_", watch_config=False)

                assert loader.get("string") == "hello"
                assert loader.get("int") == 42
                assert loader.get("float") == 3.14
                assert loader.get("bool_true") is True
                assert loader.get("bool_false") is False
                assert loader.get("list") == [1, 2, 3]
                assert loader.get("null") is None

                loader.stop()
        finally:
            config_file.unlink()

    def test_dot_notation_access(self):
        """Test dot notation access to nested configuration."""
        config_data = {
            "level1": {"level2": {"level3": "deep_value"}, "simple": "value"},
            "root": "root_value",
        }

        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            assert loader.get("root") == "root_value"
            assert loader.get("level1.simple") == "value"
            assert loader.get("level1.level2.level3") == "deep_value"
            assert loader.get("nonexistent") is None
            assert loader.get("nonexistent", "default") == "default"
            assert loader.get("level1.nonexistent") is None

            loader.stop()
        finally:
            config_file.unlink()

    def test_dictionary_style_access(self):
        """Test dictionary-style access to configuration."""
        config_data = {"key1": "value1", "nested": {"key2": "value2"}}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            assert loader["key1"] == "value1"
            assert loader["nested.key2"] == "value2"
            assert "key1" in loader
            assert "nested.key2" in loader
            assert "nonexistent" not in loader

            with pytest.raises(KeyError):
                _ = loader["nonexistent"]

            loader.stop()
        finally:
            config_file.unlink()

    def test_config_modification(self):
        """Test runtime configuration modification."""
        config_data = {"original": "value"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            assert loader.get("original") == "value"

            # Modify configuration
            loader.set("original", "modified")
            loader.set("new.nested.key", "new_value")

            assert loader.get("original") == "modified"
            assert loader.get("new.nested.key") == "new_value"

            loader.stop()
        finally:
            config_file.unlink()

    def test_change_callbacks(self):
        """Test configuration change callbacks."""
        config_data = {"test": "initial"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            callback_events = []

            def change_callback(event: ConfigChangeEvent):
                callback_events.append(event)

            loader.add_change_callback(change_callback)

            # Modify configuration to trigger callback
            loader.set("test", "modified")

            assert len(callback_events) == 1
            assert callback_events[0].old_config["test"] == "initial"
            assert callback_events[0].new_config["test"] == "modified"

            # Remove callback
            loader.remove_change_callback(change_callback)
            loader.set("test", "modified_again")

            # Should not trigger additional callback
            assert len(callback_events) == 1

            loader.stop()
        finally:
            config_file.unlink()

    def test_manual_reload(self):
        """Test manual configuration reload."""
        config_data = {"reload_test": "original"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            assert loader.get("reload_test") == "original"

            # Modify the file externally
            new_config = {"reload_test": "reloaded", "new_key": "new_value"}
            with open(config_file, "w") as f:
                yaml.dump(new_config, f)

            # Values should be unchanged until reload
            assert loader.get("reload_test") == "original"
            assert loader.get("new_key") is None

            # Manual reload
            loader.reload()

            # Values should be updated
            assert loader.get("reload_test") == "reloaded"
            assert loader.get("new_key") == "new_value"

            loader.stop()
        finally:
            config_file.unlink()

    def test_hot_reload_functionality(self):
        """Test automatic hot-reload when file changes."""
        config_data = {"hot_reload": "initial"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=True, auto_reload=True)

            # Give the file watcher time to start
            time.sleep(0.1)

            assert loader.get("hot_reload") == "initial"

            callback_events = []

            def change_callback(event: ConfigChangeEvent):
                callback_events.append(event)

            loader.add_change_callback(change_callback)

            # Modify the file externally
            new_config = {"hot_reload": "auto_reloaded", "auto_added": "new"}
            with open(config_file, "w") as f:
                yaml.dump(new_config, f)

            # Wait for file system event and reload
            max_wait = 2.0  # Maximum wait time
            start_time = time.time()

            while time.time() - start_time < max_wait:
                if loader.get("hot_reload") == "auto_reloaded":
                    break
                time.sleep(0.1)

            # Verify auto-reload worked
            assert loader.get("hot_reload") == "auto_reloaded"
            assert loader.get("auto_added") == "new"

            # Verify callback was triggered
            assert len(callback_events) > 0

            loader.stop()
        finally:
            config_file.unlink()

    def test_context_manager(self):
        """Test ConfigLoader as context manager."""
        config_data = {"context": "test"}
        config_file = self.create_temp_config(config_data)

        try:
            with ConfigLoader(config_file, watch_config=False) as loader:
                assert loader.get("context") == "test"
                # Context manager should handle cleanup
        finally:
            config_file.unlink()

    def test_error_handling(self):
        """Test error handling in configuration loading."""
        # Test with invalid YAML
        fd, invalid_yaml_path = tempfile.mkstemp(suffix=".yaml")
        try:
            with os.fdopen(fd, "w") as f:
                f.write("invalid: yaml: content: [")
        except:
            os.close(fd)
            raise

        try:
            loader = ConfigLoader(invalid_yaml_path, watch_config=False)

            # Should handle invalid YAML gracefully
            assert loader.get_all() == {}

            loader.stop()
        finally:
            Path(invalid_yaml_path).unlink()

    def test_repr(self):
        """Test string representation of ConfigLoader."""
        config_data = {"key1": "value1", "key2": "value2"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)
            repr_str = repr(loader)

            assert "ConfigLoader" in repr_str
            assert str(config_file) in repr_str
            assert "key1" in repr_str
            assert "key2" in repr_str

            loader.stop()
        finally:
            config_file.unlink()

    def test_callback_error_handling(self):
        """Test error handling in change callbacks."""
        config_data = {"callback_test": "initial"}
        config_file = self.create_temp_config(config_data)

        try:
            loader = ConfigLoader(config_file, watch_config=False)

            def failing_callback(event: ConfigChangeEvent):
                raise Exception("Callback error")

            def working_callback(event: ConfigChangeEvent):
                working_callback.called = True

            working_callback.called = False

            loader.add_change_callback(failing_callback)
            loader.add_change_callback(working_callback)

            # Modify config - should handle callback error gracefully
            loader.set("callback_test", "modified")

            # Working callback should still be called
            assert working_callback.called

            loader.stop()
        finally:
            config_file.unlink()
