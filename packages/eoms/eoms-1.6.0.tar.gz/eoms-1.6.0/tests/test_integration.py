"""Integration test demonstrating EventBus + Plugin system working together."""

import asyncio

import pytest

from eoms.core.eventbus import EventBus
from eoms.core.plugin import PluginLoader
from eoms.plugins.sample import SamplePlugin


@pytest.mark.asyncio
async def test_eventbus_plugin_integration():
    """Test EventBus and Plugin system working together."""
    # Create EventBus
    bus = EventBus()
    await bus.start()

    # Create plugin system
    loader = PluginLoader()

    # Manually register sample plugin
    loader._discovered_plugins["sample"] = SamplePlugin

    # Load and start plugin
    plugin = loader.load_plugin("sample", {"greeting": "EventBus Integration!"})
    assert plugin is not None
    loader.start_plugin("sample")

    # Track processed messages
    processed_messages = []

    async def message_handler(topic: str, event):
        """Handler that processes messages with plugin."""
        if plugin.enabled:
            result = plugin.process_message(event.get("message", ""))
            processed_messages.append(result)

    # Subscribe to events
    bus.subscribe("message.process", message_handler)

    # Publish some events
    test_messages = [
        {"message": "Hello EventBus"},
        {"message": "Plugin Integration"},
        {"message": "EOMS System"},
    ]

    for msg in test_messages:
        await bus.publish("message.process", msg)

    # Wait for processing
    await asyncio.sleep(0.1)

    # Verify integration
    assert len(processed_messages) == 3
    assert all("[SamplePlugin]" in msg for msg in processed_messages)
    assert "Hello EventBus" in processed_messages[0]
    assert "Plugin Integration" in processed_messages[1]
    assert "EOMS System" in processed_messages[2]

    # Cleanup
    loader.stop_plugin("sample")
    loader.unload_plugin("sample")
    await bus.stop()


@pytest.mark.asyncio
async def test_multiple_plugins_eventbus():
    """Test multiple plugins working with EventBus."""
    bus = EventBus()
    await bus.start()

    loader = PluginLoader()

    # Register multiple sample plugins with different configs
    loader._discovered_plugins["plugin1"] = SamplePlugin
    loader._discovered_plugins["plugin2"] = SamplePlugin

    # Load plugins with different configs
    plugin1 = loader.load_plugin("plugin1", {"greeting": "Plugin 1", "max_messages": 2})
    plugin2 = loader.load_plugin("plugin2", {"greeting": "Plugin 2", "max_messages": 3})

    loader.start_plugin("plugin1")
    loader.start_plugin("plugin2")

    results = []

    async def multi_plugin_handler(topic: str, event):
        """Handler that uses multiple plugins."""
        message = event.get("message", "")

        # Process with both plugins
        if plugin1.enabled:
            result1 = plugin1.process_message(f"P1: {message}")
            results.append(("plugin1", result1))

        if plugin2.enabled:
            result2 = plugin2.process_message(f"P2: {message}")
            results.append(("plugin2", result2))

    bus.subscribe("multi.process", multi_plugin_handler)

    # Send a message
    await bus.publish("multi.process", {"message": "Test"})
    await asyncio.sleep(0.1)

    # Verify both plugins processed the message
    assert len(results) == 2

    plugin1_result = next(r for r in results if r[0] == "plugin1")
    plugin2_result = next(r for r in results if r[0] == "plugin2")

    assert "[SamplePlugin]" in plugin1_result[1]
    assert "P1: Test" in plugin1_result[1]
    assert "[SamplePlugin]" in plugin2_result[1]
    assert "P2: Test" in plugin2_result[1]

    # Cleanup
    loader.stop_plugin("plugin1")
    loader.stop_plugin("plugin2")
    loader.unload_plugin("plugin1")
    loader.unload_plugin("plugin2")
    await bus.stop()
