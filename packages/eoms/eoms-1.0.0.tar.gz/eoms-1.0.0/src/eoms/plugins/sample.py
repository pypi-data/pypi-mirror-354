"""
Sample plugin demonstrating the EOMS plugin system.

This plugin serves as an example of how to create plugins for EOMS.
"""

import logging
from typing import Any, Dict

from eoms.core.plugin import BasePlugin

logger = logging.getLogger(__name__)


class SamplePlugin(BasePlugin):
    """
    A sample plugin that demonstrates the plugin interface.

    This plugin doesn't do much - it just logs messages and maintains
    some simple state to show the plugin lifecycle.
    """

    def __init__(self, name: str = "sample", version: str = "1.0.0"):
        """Initialize the sample plugin."""
        super().__init__(name, version)
        self._message_count = 0
        self._config: Dict[str, Any] = {}
        logger.info(f"SamplePlugin {name} v{version} created")

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration.

        Args:
            config: Plugin configuration dictionary
        """
        self._config = config.copy()

        # Example configuration handling
        self.greeting = config.get("greeting", "Hello from SamplePlugin!")
        self.max_messages = config.get("max_messages", 100)

        logger.info(f"SamplePlugin initialized with config: {config}")

    def start(self) -> None:
        """Start the plugin services."""
        if not self.enabled:
            logger.warning("Cannot start disabled plugin")
            return

        logger.info(f"SamplePlugin started: {self.greeting}")
        self._message_count = 0

    def stop(self) -> None:
        """Stop the plugin services."""
        logger.info(f"SamplePlugin stopped. Processed {self._message_count} messages.")
        self._message_count = 0

    def process_message(self, message: str) -> str:
        """
        Process a message (example plugin functionality).

        Args:
            message: Input message to process

        Returns:
            Processed message
        """
        if not self.enabled:
            return message

        self._message_count += 1

        if self._message_count > self.max_messages:
            logger.warning(f"Message limit ({self.max_messages}) exceeded")
            return message

        processed = f"[SamplePlugin] {message} (count: {self._message_count})"
        logger.debug(f"Processed message: {processed}")

        return processed

    def get_info(self) -> Dict[str, str]:
        """Get extended plugin information."""
        info = super().get_info()
        info.update(
            {
                "message_count": str(self._message_count),
                "max_messages": str(self.max_messages),
                "greeting": self.greeting,
            }
        )
        return info


# Plugin factory function (alternative to class-based loading)
def create_plugin() -> SamplePlugin:
    """Create and return a SamplePlugin instance."""
    return SamplePlugin()


# Export the plugin class for entry point discovery
__all__ = ["SamplePlugin", "create_plugin"]
