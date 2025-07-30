"""Tests for the EventBus implementation."""

import asyncio
import time

import pytest

from eoms.core.eventbus import EventBus


class TestEventBus:
    """Test cases for EventBus functionality."""

    @pytest.fixture
    async def event_bus(self):
        """Create an EventBus instance for testing."""
        bus = EventBus()
        await bus.start()
        yield bus
        await bus.stop()

    @pytest.mark.asyncio
    async def test_basic_pub_sub(self, event_bus):
        """Test basic publish/subscribe functionality."""
        received_events = []

        async def handler(topic: str, event):
            received_events.append((topic, event))

        event_bus.subscribe("test.topic", handler)
        await event_bus.publish("test.topic", {"data": "test"})

        # Give time for event processing
        await asyncio.sleep(0.1)

        assert len(received_events) == 1
        assert received_events[0] == ("test.topic", {"data": "test"})

    @pytest.mark.asyncio
    async def test_wildcard_matching(self, event_bus):
        """Test wildcard topic matching."""
        received_events = []

        async def handler(topic: str, event):
            received_events.append((topic, event))

        # Subscribe to wildcard pattern
        event_bus.subscribe("order.*", handler)

        # Publish to matching topics
        await event_bus.publish("order.created", {"id": 1})
        await event_bus.publish("order.filled", {"id": 2})
        # Should not match
        await event_bus.publish("position.updated", {"symbol": "AAPL"})

        await asyncio.sleep(0.1)

        assert len(received_events) == 2
        assert ("order.created", {"id": 1}) in received_events
        assert ("order.filled", {"id": 2}) in received_events

    @pytest.mark.asyncio
    async def test_multiple_subscribers(self, event_bus):
        """Test multiple subscribers to the same topic."""
        handler1_events = []
        handler2_events = []

        async def handler1(topic: str, event):
            handler1_events.append((topic, event))

        async def handler2(topic: str, event):
            handler2_events.append((topic, event))

        event_bus.subscribe("test.topic", handler1)
        event_bus.subscribe("test.topic", handler2)

        await event_bus.publish("test.topic", {"data": "broadcast"})
        await asyncio.sleep(0.1)

        assert len(handler1_events) == 1
        assert len(handler2_events) == 1
        assert handler1_events[0] == ("test.topic", {"data": "broadcast"})
        assert handler2_events[0] == ("test.topic", {"data": "broadcast"})

    @pytest.mark.asyncio
    async def test_unsubscribe(self, event_bus):
        """Test unsubscribing from topics."""
        received_events = []

        async def handler(topic: str, event):
            received_events.append((topic, event))

        event_bus.subscribe("test.topic", handler)
        await event_bus.publish("test.topic", {"data": "before"})
        await asyncio.sleep(0.1)

        event_bus.unsubscribe("test.topic", handler)
        await event_bus.publish("test.topic", {"data": "after"})
        await asyncio.sleep(0.1)

        assert len(received_events) == 1
        assert received_events[0] == ("test.topic", {"data": "before"})

    @pytest.mark.asyncio
    async def test_back_pressure_protection(self):
        """Test back-pressure protection with small queue."""
        bus = EventBus(max_queue_size=5, enable_back_pressure=True)
        await bus.start()

        slow_handler_calls = 0

        async def slow_handler(topic: str, event):
            nonlocal slow_handler_calls
            slow_handler_calls += 1
            await asyncio.sleep(0.1)  # Simulate slow processing

        bus.subscribe("test.topic", slow_handler)

        # Publish more events than queue can handle
        for i in range(20):
            await bus.publish("test.topic", {"id": i})

        await asyncio.sleep(0.5)  # Let some events process
        await bus.stop()

        stats = bus.get_stats()
        assert stats["events_published"] == 20
        assert stats["back_pressure_hits"] > 0
        assert stats["events_dropped"] > 0

    @pytest.mark.asyncio
    async def test_performance_benchmark(self):
        """Test EventBus performance - should handle 100k msg/sec."""
        import os

        bus = EventBus(max_queue_size=50000)
        await bus.start()

        processed_count = 0

        async def fast_handler(topic: str, event):
            nonlocal processed_count
            processed_count += 1

        bus.subscribe("perf.test", fast_handler)

        # Publish 10k events and measure time
        num_events = 10000
        start_time = time.time()

        for i in range(num_events):
            await bus.publish("perf.test", {"id": i})

        # Wait for all events to be processed
        while processed_count < num_events:
            await asyncio.sleep(0.01)

        elapsed_time = time.time() - start_time
        events_per_second = num_events / elapsed_time

        await bus.stop()

        # Adjust performance expectations for CI environments
        # CI environments have resource constraints that affect performance
        is_ci = os.getenv("CI", "").lower() in ("true", "1", "yes")
        min_events_per_sec = 30000 if is_ci else 100000

        # Should handle reasonable throughput for the environment
        assert (
            events_per_second > min_events_per_sec
        ), f"Only achieved {events_per_second:.0f} events/sec"

    @pytest.mark.asyncio
    async def test_stats_collection(self, event_bus):
        """Test statistics collection."""

        async def handler(topic: str, event):
            pass

        event_bus.subscribe("test.topic", handler)

        # Publish some events
        for i in range(5):
            await event_bus.publish("test.topic", {"id": i})

        await asyncio.sleep(0.1)

        stats = event_bus.get_stats()
        assert stats["events_published"] == 5
        assert stats["active_subscribers"] >= 1
        assert "queue_sizes" in stats

    @pytest.mark.asyncio
    async def test_error_handling(self, event_bus):
        """Test error handling in event processing."""

        async def failing_handler(topic: str, event):
            raise ValueError("Handler error")

        async def working_handler(topic: str, event):
            working_handler.called = True

        working_handler.called = False

        event_bus.subscribe("test.topic", failing_handler)
        event_bus.subscribe("test.topic", working_handler)

        await event_bus.publish("test.topic", {"data": "test"})
        await asyncio.sleep(0.1)

        # Working handler should still be called despite failing handler
        assert working_handler.called

    @pytest.mark.asyncio
    async def test_stop_gracefully(self):
        """Test graceful shutdown."""
        bus = EventBus(max_processing_time=2.0)  # Increase timeout
        await bus.start()

        processing_started = False
        processing_completed = False

        async def long_handler(topic: str, event):
            nonlocal processing_started, processing_completed
            processing_started = True
            await asyncio.sleep(0.2)
            processing_completed = True

        bus.subscribe("test.topic", long_handler)
        await bus.publish("test.topic", {"data": "test"})

        # Give handler time to start
        await asyncio.sleep(0.1)
        assert processing_started

        # Stop the bus - this should wait for handler to complete
        await bus.stop()

        # Handler should complete gracefully within the timeout
        assert processing_completed
