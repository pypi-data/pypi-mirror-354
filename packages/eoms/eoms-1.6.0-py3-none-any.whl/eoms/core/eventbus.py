"""
Async EventBus implementation with topic-based routing and back-pressure awareness.

Provides high-performance event processing with configurable back-pressure handling
to prevent memory exhaustion during event bursts.
"""

import asyncio
import logging
import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List, Set
from weakref import WeakSet

logger = logging.getLogger(__name__)


class BackPressureError(Exception):
    """Raised when EventBus cannot handle incoming events due to back-pressure."""


EventHandler = Callable[[str, Any], Awaitable[None]]


class EventBus:
    """
    High-performance async EventBus with topic-based routing and back-pressure control.

    Features:
    - Topic-based event routing with wildcard support
    - Configurable back-pressure limits per subscriber
    - Weak references to prevent memory leaks
    - Metrics for monitoring performance
    """

    def __init__(
        self,
        max_queue_size: int = 10000,
        max_processing_time: float = 1.0,
        enable_back_pressure: bool = True,
    ):
        """
        Initialize EventBus.

        Args:
            max_queue_size: Maximum events per subscriber queue before back-pressure
            max_processing_time: Max time to wait for event processing (seconds)
            enable_back_pressure: Whether to enable back-pressure protection
        """
        self._subscribers: Dict[str, WeakSet[EventHandler]] = defaultdict(WeakSet)
        self._subscriber_queues: Dict[EventHandler, asyncio.Queue] = {}
        self._processing_tasks: Set[asyncio.Task] = set()
        self._stats: Dict[str, Any] = {
            "events_published": 0,
            "events_processed": 0,
            "events_dropped": 0,
            "back_pressure_hits": 0,
        }
        self._max_queue_size = max_queue_size
        self._max_processing_time = max_processing_time
        self._enable_back_pressure = enable_back_pressure
        self._running = False

    async def start(self) -> None:
        """Start the EventBus."""
        self._running = True
        logger.info("EventBus started")

    async def stop(self) -> None:
        """Stop the EventBus and wait for pending events to complete."""
        self._running = False

        # Wait for tasks to complete with timeout
        if self._processing_tasks:
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._processing_tasks, return_exceptions=True),
                    timeout=self._max_processing_time,
                )
            except asyncio.TimeoutError:
                # Force cancel remaining tasks
                for task in self._processing_tasks:
                    task.cancel()

        # Clear remaining tasks
        self._processing_tasks.clear()
        self._subscriber_queues.clear()
        logger.info("EventBus stopped")

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        """
        Subscribe a handler to a topic.

        Args:
            topic: Topic to subscribe to (supports wildcards like 'order.*')
            handler: Async function to handle events
        """
        self._subscribers[topic].add(handler)
        self._subscriber_queues[handler] = asyncio.Queue(maxsize=self._max_queue_size)
        logger.debug(f"Subscribed handler to topic: {topic}")

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        """
        Unsubscribe a handler from a topic.

        Args:
            topic: Topic to unsubscribe from
            handler: Handler to remove
        """
        if topic in self._subscribers:
            self._subscribers[topic].discard(handler)
            if not self._subscribers[topic]:
                del self._subscribers[topic]

        if handler in self._subscriber_queues:
            del self._subscriber_queues[handler]

        logger.debug(f"Unsubscribed handler from topic: {topic}")

    async def publish(self, topic: str, event: Any) -> None:
        """
        Publish an event to a topic.

        Args:
            topic: Topic to publish to
            event: Event data to publish

        Raises:
            BackPressureError: If back-pressure limits are exceeded
        """
        if not self._running:
            return

        self._stats["events_published"] += 1
        matching_handlers = self._get_matching_handlers(topic)

        if not matching_handlers:
            return

        # Queue events for handlers
        for handler in matching_handlers:
            await self._queue_event_for_handler(handler, topic, event)

    def _get_matching_handlers(self, topic: str) -> List[EventHandler]:
        """Get all handlers that match the given topic."""
        handlers: List[EventHandler] = []

        for subscribed_topic, topic_handlers in self._subscribers.items():
            if self._topic_matches(topic, subscribed_topic):
                handlers.extend(topic_handlers)

        return handlers

    def _topic_matches(self, published_topic: str, subscribed_topic: str) -> bool:
        """Check if published topic matches subscribed topic pattern."""
        if subscribed_topic == published_topic:
            return True

        if "*" in subscribed_topic:
            # Simple wildcard matching
            if subscribed_topic.endswith(".*"):
                prefix = subscribed_topic[:-2]
                return published_topic.startswith(prefix + ".")
            elif subscribed_topic.startswith("*."):
                suffix = subscribed_topic[2:]
                return published_topic.endswith("." + suffix)

        return False

    async def _queue_event_for_handler(self, handler: EventHandler, topic: str, event: Any) -> None:
        """Queue an event for a specific handler with back-pressure handling."""
        queue = self._subscriber_queues.get(handler)
        if not queue:
            return

        try:
            if self._enable_back_pressure and queue.qsize() >= self._max_queue_size:
                self._stats["back_pressure_hits"] += 1
                self._stats["events_dropped"] += 1
                logger.warning(
                    f"Back-pressure: dropping event for topic {topic}, "
                    f"queue size: {queue.qsize()}"
                )
                return

            # Queue the event
            await queue.put((topic, event))

            # Start processing task if not already running
            self._start_handler_task(handler)

        except Exception as e:
            logger.error(f"Error queuing event for handler: {e}")
            self._stats["events_dropped"] += 1

    def _start_handler_task(self, handler: EventHandler) -> None:
        """Start a processing task for a handler if not already running."""
        # Check if handler already has a running task
        handler_tasks = [
            task for task in self._processing_tasks if task.get_name() == f"handler-{id(handler)}"
        ]

        if not handler_tasks:
            task = asyncio.create_task(
                self._process_handler_queue(handler), name=f"handler-{id(handler)}"
            )
            self._processing_tasks.add(task)
            task.add_done_callback(self._processing_tasks.discard)

    async def _process_handler_queue(self, handler: EventHandler) -> None:
        """Process events in a handler's queue."""
        queue = self._subscriber_queues.get(handler)
        if not queue:
            return

        while self._running:
            try:
                # Wait for an event with timeout
                topic, event = await asyncio.wait_for(
                    queue.get(), timeout=0.1  # Short timeout for running flag
                )

                # Process the event
                start_time = time.time()
                await handler(topic, event)
                processing_time = time.time() - start_time

                self._stats["events_processed"] += 1

                if processing_time > self._max_processing_time:
                    logger.warning(
                        f"Slow event processing: {processing_time:.3f}s " f"for topic {topic}"
                    )

            except asyncio.TimeoutError:
                # Check if there are any remaining items to process
                if queue.empty():
                    break
            except Exception as e:
                logger.error(f"Error processing event: {e}")

        # Process any remaining events in the queue when shutting down
        while not queue.empty() and self._running is False:
            try:
                topic, event = queue.get_nowait()
                await handler(topic, event)
                self._stats["events_processed"] += 1
            except asyncio.QueueEmpty:
                break
            except Exception as e:
                logger.error(f"Error processing final event: {e}")
                break

    def get_stats(self) -> Dict[str, Any]:
        """Get EventBus statistics."""
        stats = self._stats.copy()
        queue_sizes = {
            id(handler): queue.qsize() for handler, queue in self._subscriber_queues.items()
        }
        stats.update(
            {
                "active_subscribers": sum(len(handlers) for handlers in self._subscribers.values()),
                "active_queues": len(self._subscriber_queues),
                "active_tasks": len(self._processing_tasks),
                "queue_sizes": queue_sizes,
            }
        )
        return stats
