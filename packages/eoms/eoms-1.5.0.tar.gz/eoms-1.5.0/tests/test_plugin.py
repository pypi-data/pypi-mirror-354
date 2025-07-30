"""Tests for the plugin system."""

from typing import Any, Dict
from unittest.mock import patch

from eoms.core.plugin import BasePlugin, PluginLoader
from eoms.plugins.sample import SamplePlugin


class MockPlugin(BasePlugin):
    """Mock plugin for testing."""

    def __init__(self, name: str = "mock", version: str = "1.0.0"):
        super().__init__(name, version)
        self.initialized = False
        self.started = False

    def initialize(self, config: Dict[str, Any]) -> None:
        self.initialized = True
        self.config = config

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False


class TestBasePlugin:
    """Test cases for BasePlugin functionality."""

    def test_plugin_creation(self):
        """Test plugin creation and basic properties."""
        plugin = MockPlugin("test-plugin", "2.0.0")

        assert plugin.name == "test-plugin"
        assert plugin.version == "2.0.0"
        assert not plugin.enabled
        assert not plugin.initialized
        assert not plugin.started

    def test_plugin_lifecycle(self):
        """Test plugin enable/disable lifecycle."""
        plugin = MockPlugin()

        # Test enable
        plugin.enable()
        assert plugin.enabled

        # Test disable
        plugin.disable()
        assert not plugin.enabled

    def test_plugin_initialization(self):
        """Test plugin initialization with config."""
        plugin = MockPlugin()
        config = {"setting1": "value1", "setting2": 42}

        plugin.initialize(config)

        assert plugin.initialized
        assert plugin.config == config

    def test_plugin_start_stop(self):
        """Test plugin start/stop functionality."""
        plugin = MockPlugin()
        plugin.initialize({})

        # Test start
        plugin.start()
        assert plugin.started

        # Test stop
        plugin.stop()
        assert not plugin.started

    def test_plugin_info(self):
        """Test plugin information retrieval."""
        plugin = MockPlugin("info-test", "3.0.0")
        plugin.enable()

        info = plugin.get_info()

        assert info["name"] == "info-test"
        assert info["version"] == "3.0.0"
        assert info["enabled"] == "True"


class TestSamplePlugin:
    """Test cases for SamplePlugin."""

    def test_sample_plugin_creation(self):
        """Test SamplePlugin creation."""
        plugin = SamplePlugin()

        assert plugin.name == "sample"
        assert plugin.version == "1.0.0"
        assert plugin._message_count == 0

    def test_sample_plugin_initialization(self):
        """Test SamplePlugin initialization with config."""
        plugin = SamplePlugin()
        config = {"greeting": "Hello Test!", "max_messages": 50}

        plugin.initialize(config)

        assert plugin.greeting == "Hello Test!"
        assert plugin.max_messages == 50

    def test_sample_plugin_message_processing(self):
        """Test SamplePlugin message processing."""
        plugin = SamplePlugin()
        plugin.initialize({"max_messages": 5})
        plugin.enable()
        plugin.start()

        # Test normal message processing
        result = plugin.process_message("test message")
        assert "[SamplePlugin]" in result
        assert "test message" in result
        assert "(count: 1)" in result

        # Test message count increment
        plugin.process_message("another message")
        assert plugin._message_count == 2

    def test_sample_plugin_disabled_processing(self):
        """Test message processing when plugin is disabled."""
        plugin = SamplePlugin()
        plugin.initialize({})
        # Don't enable the plugin

        result = plugin.process_message("test message")
        assert result == "test message"  # Should return unchanged
        assert plugin._message_count == 0

    def test_sample_plugin_message_limit(self):
        """Test message processing limit."""
        plugin = SamplePlugin()
        plugin.initialize({"max_messages": 2})
        plugin.enable()
        plugin.start()

        # Process messages up to limit
        plugin.process_message("msg1")
        plugin.process_message("msg2")

        # This should exceed the limit
        result = plugin.process_message("msg3")
        assert result == "msg3"  # Should process but warn
        assert plugin._message_count == 3

    def test_sample_plugin_info(self):
        """Test SamplePlugin extended info."""
        plugin = SamplePlugin()
        plugin.initialize({"greeting": "Test greeting", "max_messages": 10})
        plugin.enable()

        info = plugin.get_info()

        assert info["name"] == "sample"
        assert info["greeting"] == "Test greeting"
        assert info["max_messages"] == "10"
        assert info["message_count"] == "0"


class TestPluginLoader:
    """Test cases for PluginLoader."""

    def test_plugin_loader_creation(self):
        """Test PluginLoader creation."""
        loader = PluginLoader()

        assert loader.entry_point_group == "eoms.plugins"
        assert len(loader._discovered_plugins) == 0
        assert len(loader._loaded_plugins) == 0

    def test_plugin_loader_custom_group(self):
        """Test PluginLoader with custom entry point group."""
        loader = PluginLoader("custom.plugins")

        assert loader.entry_point_group == "custom.plugins"

    def test_discover_plugins(self):
        """Test plugin discovery functionality."""
        loader = PluginLoader()

        # Manual plugin registration for testing since entry points
        # require proper package installation
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        discovered = loader.get_discovered_plugins()

        # Should find the manually registered sample plugin
        assert "sample" in discovered
        assert issubclass(discovered["sample"], BasePlugin)

    def test_load_plugin(self):
        """Test loading a discovered plugin."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        # Load the sample plugin
        config = {"greeting": "Test loading!", "max_messages": 10}
        plugin = loader.load_plugin("sample", config)

        assert plugin is not None
        assert isinstance(plugin, SamplePlugin)
        assert plugin.greeting == "Test loading!"
        assert plugin.max_messages == 10

    def test_load_nonexistent_plugin(self):
        """Test loading a plugin that doesn't exist."""
        loader = PluginLoader()

        # Don't register any plugins
        plugin = loader.load_plugin("nonexistent")

        assert plugin is None

    def test_load_plugin_twice(self):
        """Test loading the same plugin twice."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        plugin1 = loader.load_plugin("sample")
        plugin2 = loader.load_plugin("sample")

        assert plugin1 is plugin2  # Should return the same instance

    def test_start_stop_plugin(self):
        """Test starting and stopping a plugin."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        # Load and start plugin
        loader.load_plugin("sample")
        result = loader.start_plugin("sample")

        assert result is True

        # Check plugin state
        plugins = loader.get_loaded_plugins()
        assert plugins["sample"].enabled

        # Stop plugin
        result = loader.stop_plugin("sample")

        assert result is True
        assert not plugins["sample"].enabled

    def test_start_nonexistent_plugin(self):
        """Test starting a plugin that isn't loaded."""
        loader = PluginLoader()

        result = loader.start_plugin("nonexistent")

        assert result is False

    def test_unload_plugin(self):
        """Test unloading a plugin."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        # Load plugin
        loader.load_plugin("sample")
        assert "sample" in loader.get_loaded_plugins()

        # Unload plugin
        result = loader.unload_plugin("sample")

        assert result is True
        assert "sample" not in loader.get_loaded_plugins()

    def test_unload_nonexistent_plugin(self):
        """Test unloading a plugin that isn't loaded."""
        loader = PluginLoader()

        result = loader.unload_plugin("nonexistent")

        assert result is False

    def test_get_plugin_info(self):
        """Test getting information about loaded plugins."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        # Load and start a plugin
        loader.load_plugin("sample", {"greeting": "Info test"})
        loader.start_plugin("sample")

        info_list = loader.get_plugin_info()

        assert len(info_list) == 1
        assert info_list[0]["name"] == "sample"
        assert info_list[0]["enabled"] == "True"
        assert info_list[0]["greeting"] == "Info test"

    @patch("eoms.core.plugin.metadata.entry_points")
    def test_discover_plugins_error_handling(self, mock_entry_points):
        """Test error handling during plugin discovery."""
        # Mock a failure in entry point discovery
        mock_entry_points.side_effect = Exception("Discovery failed")

        loader = PluginLoader()
        discovered = loader.discover_plugins()

        # Should handle the error gracefully
        assert discovered == {}

    def test_plugin_lifecycle_integration(self):
        """Test full plugin lifecycle integration."""
        loader = PluginLoader()

        # Manual plugin registration for testing
        from eoms.plugins.sample import SamplePlugin

        loader._discovered_plugins["sample"] = SamplePlugin

        # Load plugin with config
        config = {"greeting": "Integration test", "max_messages": 5}
        plugin = loader.load_plugin("sample", config)
        assert plugin is not None

        # Start plugin
        assert loader.start_plugin("sample")
        assert plugin.enabled

        # Use plugin functionality
        result = plugin.process_message("test")
        assert "[SamplePlugin]" in result

        # Stop plugin
        assert loader.stop_plugin("sample")
        assert not plugin.enabled

        # Unload plugin
        assert loader.unload_plugin("sample")
        assert "sample" not in loader.get_loaded_plugins()
