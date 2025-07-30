"""Base agent classes for EOMS autonomous components."""

import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from eoms.core.eventbus import EventBus

logger = logging.getLogger(__name__)


@dataclass
class AgentStatus:
    """Agent status information."""

    name: str
    status: str
    last_heartbeat: datetime
    message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base class for all EOMS agents.

    Agents are autonomous components that:
    - Subscribe to specific event topics
    - Process events asynchronously
    - Emit heartbeats for health monitoring
    - Handle graceful startup/shutdown
    """

    def __init__(self, name: str, event_bus: EventBus, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the agent.

        Args:
            name: Agent name
            event_bus: Shared event bus
            config: Agent configuration
        """
        self.name = name
        self.event_bus = event_bus
        self.config = config or {}
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._status = "stopped"
        self._last_heartbeat = datetime.now()

    async def start(self) -> bool:
        """
        Start the agent.

        Returns:
            True if started successfully
        """
        if self._running:
            logger.warning(f"Agent {self.name} is already running")
            return False

        try:
            logger.info(f"Starting agent {self.name}")
            self._running = True
            self._status = "starting"

            # Subscribe to topics
            await self._subscribe_to_topics()

            # Initialize agent-specific components
            await self.initialize()

            # Start main loop
            self._task = asyncio.create_task(self._main_loop())

            # Start heartbeat
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

            self._status = "running"
            logger.info(f"Agent {self.name} started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start agent {self.name}: {e}")
            self._status = "error"
            self._running = False
            return False

    async def stop(self) -> bool:
        """
        Stop the agent.

        Returns:
            True if stopped successfully
        """
        if not self._running:
            logger.warning(f"Agent {self.name} is not running")
            return False

        try:
            logger.info(f"Stopping agent {self.name}")
            self._running = False
            self._status = "stopping"

            # Cancel tasks
            if self._task and not self._task.done():
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass

            if self._heartbeat_task and not self._heartbeat_task.done():
                self._heartbeat_task.cancel()
                try:
                    await self._heartbeat_task
                except asyncio.CancelledError:
                    pass

            # Agent-specific cleanup
            await self.cleanup()

            self._status = "stopped"
            logger.info(f"Agent {self.name} stopped successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to stop agent {self.name}: {e}")
            self._status = "error"
            return False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize agent-specific components."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup agent-specific components."""
        pass

    @abstractmethod
    async def process_event(self, topic: str, event: Any) -> None:
        """
        Process an event.

        Args:
            topic: Event topic
            event: Event data
        """
        pass

    @abstractmethod
    def get_subscribed_topics(self) -> list[str]:
        """Get list of topics this agent subscribes to."""
        pass

    async def _subscribe_to_topics(self) -> None:
        """Subscribe to event topics."""
        topics = self.get_subscribed_topics()
        for topic in topics:
            self.event_bus.subscribe(topic, self._event_handler)
            logger.debug(f"Agent {self.name} subscribed to topic: {topic}")

    async def _event_handler(self, topic: str, event: Any) -> None:
        """Handle incoming events."""
        try:
            await self.process_event(topic, event)
        except Exception as e:
            logger.error(f"Agent {self.name} error processing event on topic {topic}: {e}")

    async def _main_loop(self) -> None:
        """Main agent loop."""
        try:
            while self._running:
                await self.main_loop_iteration()
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
        except asyncio.CancelledError:
            logger.debug(f"Agent {self.name} main loop cancelled")
        except Exception as e:
            logger.error(f"Agent {self.name} main loop error: {e}")
            self._status = "error"

    async def _heartbeat_loop(self) -> None:
        """Heartbeat loop for health monitoring."""
        try:
            while self._running:
                await self.emit_heartbeat()
                await asyncio.sleep(5.0)  # Heartbeat every 5 seconds
        except asyncio.CancelledError:
            logger.debug(f"Agent {self.name} heartbeat loop cancelled")
        except Exception as e:
            logger.error(f"Agent {self.name} heartbeat error: {e}")

    async def emit_heartbeat(self) -> None:
        """Emit heartbeat event."""
        self._last_heartbeat = datetime.now()

        status = AgentStatus(
            name=self.name,
            status=self._status,
            last_heartbeat=self._last_heartbeat,
            message=f"Agent {self.name} heartbeat",
            metrics=await self.get_metrics(),
        )

        try:
            await self.event_bus.publish("agent.heartbeat", status)
        except Exception as e:
            logger.error(f"Agent {self.name} failed to emit heartbeat: {e}")

    async def main_loop_iteration(self) -> None:
        """Override this for custom main loop behavior."""
        pass

    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics for monitoring."""
        return {
            "status": self._status,
            "uptime": (datetime.now() - self._last_heartbeat).total_seconds(),
        }

    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        return AgentStatus(name=self.name, status=self._status, last_heartbeat=self._last_heartbeat)

    @property
    def is_running(self) -> bool:
        """Check if agent is running."""
        return self._running
