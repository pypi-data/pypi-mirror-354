"""Algo Agent for managing trading strategies."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from eoms.agents.base import BaseAgent
from eoms.core.eventbus import EventBus
from eoms.strategies.base import (
    BaseStrategy,
    PriceUpdate,
    StrategyEvent,
    StrategyStatus,
)

logger = logging.getLogger(__name__)


class AlgoAgent(BaseAgent):
    """
    Algorithm Agent for managing trading strategies.

    Responsibilities:
    - Load/unload user strategies
    - Schedule strategy execution on price updates
    - Orchestrate child orders from strategies
    - Monitor strategy health and performance
    """

    def __init__(self, event_bus: EventBus, config: Optional[Dict[str, Any]] = None):
        super().__init__("ALGO", event_bus, config)
        self.strategies: Dict[str, BaseStrategy] = {}
        self.strategy_metrics: Dict[str, Dict[str, Any]] = {}

    async def initialize(self) -> None:
        """Initialize the algo agent."""
        logger.info("Initializing Algo Agent")
        # Could load strategies from config here

    async def cleanup(self) -> None:
        """Cleanup the algo agent."""
        logger.info("Cleaning up Algo Agent")
        # Stop all strategies
        for strategy in self.strategies.values():
            if strategy.status == StrategyStatus.RUNNING:
                strategy.stop()

    def get_subscribed_topics(self) -> List[str]:
        """Get subscribed topics."""
        return ["price.update", "algo.command", "strategy.event"]

    async def process_event(self, topic: str, event: Any) -> None:
        """Process incoming events."""
        try:
            if topic == "price.update":
                await self._handle_price_update(event)
            elif topic == "algo.command":
                await self._handle_algo_command(event)
            elif topic == "strategy.event":
                await self._handle_strategy_event(event)
        except Exception as e:
            logger.error(f"Algo Agent error processing {topic}: {e}")

    async def _handle_price_update(self, price_update: PriceUpdate) -> None:
        """Handle price updates by forwarding to running strategies."""
        for strategy_name, strategy in self.strategies.items():
            if strategy.status == StrategyStatus.RUNNING:
                try:
                    strategy.on_price_update(price_update)

                    # Update metrics
                    if strategy_name not in self.strategy_metrics:
                        self.strategy_metrics[strategy_name] = {
                            "price_updates_processed": 0,
                            "last_update": None,
                        }

                    self.strategy_metrics[strategy_name]["price_updates_processed"] += 1
                    self.strategy_metrics[strategy_name]["last_update"] = datetime.now()

                except Exception as e:
                    logger.error(f"Error sending price update to strategy {strategy_name}: {e}")

    async def _handle_algo_command(self, command: Dict[str, Any]) -> None:
        """Handle algorithm management commands."""
        action = command.get("action")
        strategy_name = command.get("strategy_name")

        if action == "start" and strategy_name:
            await self._start_strategy(strategy_name)
        elif action == "stop" and strategy_name:
            await self._stop_strategy(strategy_name)
        elif action == "load" and strategy_name:
            strategy_class = command.get("strategy_class")
            config = command.get("config", {})
            await self._load_strategy(strategy_name, strategy_class, config)
        elif action == "unload" and strategy_name:
            await self._unload_strategy(strategy_name)
        else:
            logger.warning(f"Unknown algo command: {command}")

    async def _handle_strategy_event(self, event: StrategyEvent) -> None:
        """Handle strategy events."""
        # Forward strategy events to the event bus
        await self.event_bus.publish("algo.status", event)

        # Update strategy metrics
        strategy_name = event.strategy_name
        if strategy_name not in self.strategy_metrics:
            self.strategy_metrics[strategy_name] = {}

        self.strategy_metrics[strategy_name].update(
            {
                "last_event": event.message,
                "last_event_time": event.timestamp,
                "status": event.status.value,
            }
        )

    async def _start_strategy(self, strategy_name: str) -> None:
        """Start a loaded strategy."""
        if strategy_name not in self.strategies:
            logger.error(f"Strategy {strategy_name} not loaded")
            return

        strategy = self.strategies[strategy_name]
        if strategy.start():
            logger.info(f"Started strategy: {strategy_name}")
            await self.event_bus.publish(
                "algo.status",
                StrategyEvent(
                    strategy_name=strategy_name,
                    status=StrategyStatus.RUNNING,
                    timestamp=datetime.now(),
                    message="Strategy started by Algo Agent",
                ),
            )
        else:
            logger.error(f"Failed to start strategy: {strategy_name}")

    async def _stop_strategy(self, strategy_name: str) -> None:
        """Stop a running strategy."""
        if strategy_name not in self.strategies:
            logger.error(f"Strategy {strategy_name} not loaded")
            return

        strategy = self.strategies[strategy_name]
        if strategy.stop():
            logger.info(f"Stopped strategy: {strategy_name}")
            await self.event_bus.publish(
                "algo.status",
                StrategyEvent(
                    strategy_name=strategy_name,
                    status=StrategyStatus.STOPPED,
                    timestamp=datetime.now(),
                    message="Strategy stopped by Algo Agent",
                ),
            )
        else:
            logger.error(f"Failed to stop strategy: {strategy_name}")

    async def _load_strategy(
        self, strategy_name: str, strategy_class, config: Dict[str, Any]
    ) -> None:
        """Load a new strategy."""
        try:
            if strategy_name in self.strategies:
                logger.warning(f"Strategy {strategy_name} already loaded")
                return

            # Create strategy instance
            strategy = strategy_class(strategy_name, config)

            # Set event callback to handle strategy events
            strategy.set_event_callback(self._on_strategy_event)

            # Initialize strategy
            if strategy.initialize():
                self.strategies[strategy_name] = strategy
                self.strategy_metrics[strategy_name] = {
                    "loaded_time": datetime.now(),
                    "status": strategy.status.value,
                    "price_updates_processed": 0,
                    "last_update": None,
                }

                logger.info(f"Loaded strategy: {strategy_name}")
                await self.event_bus.publish(
                    "algo.status",
                    StrategyEvent(
                        strategy_name=strategy_name,
                        status=StrategyStatus.STOPPED,
                        timestamp=datetime.now(),
                        message="Strategy loaded by Algo Agent",
                    ),
                )
            else:
                logger.error(f"Failed to initialize strategy: {strategy_name}")

        except Exception as e:
            logger.error(f"Error loading strategy {strategy_name}: {e}")

    async def _unload_strategy(self, strategy_name: str) -> None:
        """Unload a strategy."""
        if strategy_name not in self.strategies:
            logger.error(f"Strategy {strategy_name} not loaded")
            return

        strategy = self.strategies[strategy_name]

        # Stop if running
        if strategy.status == StrategyStatus.RUNNING:
            strategy.stop()

        # Remove from loaded strategies
        del self.strategies[strategy_name]
        if strategy_name in self.strategy_metrics:
            del self.strategy_metrics[strategy_name]

        logger.info(f"Unloaded strategy: {strategy_name}")
        await self.event_bus.publish(
            "algo.status",
            StrategyEvent(
                strategy_name=strategy_name,
                status=StrategyStatus.STOPPED,
                timestamp=datetime.now(),
                message="Strategy unloaded by Algo Agent",
            ),
        )

    def _on_strategy_event(self, event: StrategyEvent) -> None:
        """Handle strategy events from strategies."""
        # Create a task to handle the event asynchronously
        asyncio.create_task(self._handle_strategy_event(event))

    async def main_loop_iteration(self) -> None:
        """Main loop iteration for periodic tasks."""
        # Could add periodic health checks, performance monitoring, etc.
        pass

    async def get_metrics(self) -> Dict[str, Any]:
        """Get agent metrics."""
        base_metrics = await super().get_metrics()

        algo_metrics = {
            "strategies_loaded": len(self.strategies),
            "strategies_running": len(
                [s for s in self.strategies.values() if s.status == StrategyStatus.RUNNING]
            ),
            "strategy_details": self.strategy_metrics.copy(),
        }

        base_metrics.update(algo_metrics)
        return base_metrics

    def get_loaded_strategies(self) -> Dict[str, BaseStrategy]:
        """Get all loaded strategies."""
        return self.strategies.copy()

    def get_running_strategies(self) -> List[str]:
        """Get names of running strategies."""
        return [
            name
            for name, strategy in self.strategies.items()
            if strategy.status == StrategyStatus.RUNNING
        ]
