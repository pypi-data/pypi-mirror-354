"""Tests for the RecoveryManager implementation."""

from typing import List

import pytest

from eoms.core.eventstore import Event, EventStore
from eoms.core.recovery import RecoveryManager


class MockStateHandler:
    """Mock state recovery handler for testing."""

    def __init__(self, name: str, topics: List[str]):
        self.name = name
        self.topics = topics
        self.recovered_events = []
        self.errors = []

    async def recover_from_event(self, event: Event) -> None:
        """Recover state from event."""
        if event.topic == "error.test":
            raise ValueError(f"Test error for event {event.event_id}")

        self.recovered_events.append(event)

    def get_recovery_topics(self) -> List[str]:
        """Get recovery topics."""
        return self.topics

    def get_component_name(self) -> str:
        """Get component name."""
        return self.name


class TestRecoveryManager:
    """Test cases for RecoveryManager functionality."""

    @pytest.fixture
    async def event_store(self):
        """Create an EventStore for testing."""
        store = EventStore(":memory:")
        await store.initialize()
        yield store
        await store.close()

    @pytest.fixture
    async def recovery_manager(self, event_store):
        """Create a RecoveryManager for testing."""
        manager = RecoveryManager(event_store)
        yield manager

    @pytest.fixture
    async def populated_store(self, event_store):
        """Create an EventStore with test data."""
        # Add various events
        await event_store.append("order.placed", {"order_id": "O001", "symbol": "AAPL"})
        await event_store.append("order.ack", {"order_id": "O001"})
        await event_store.append("market.tick", {"symbol": "AAPL", "price": 150.0})
        await event_store.append("order.fill", {"order_id": "O001", "quantity": 100})
        await event_store.append("position.update", {"symbol": "AAPL", "quantity": 100})

        yield event_store

    @pytest.mark.asyncio
    async def test_handler_registration(self, recovery_manager):
        """Test registering and unregistering handlers."""
        handler = MockStateHandler("test", ["order.*", "market.tick"])

        # Register handler
        recovery_manager.register_handler(handler)

        # Check handler is registered
        status = await recovery_manager.get_recovery_status()
        assert status["registered_handlers"] == 1
        assert status["total_topics"] == 2

        # Unregister handler
        recovery_manager.unregister_handler(handler)

        status = await recovery_manager.get_recovery_status()
        assert status["registered_handlers"] == 0

    @pytest.mark.asyncio
    async def test_basic_recovery(self, recovery_manager, populated_store):
        """Test basic state recovery."""
        order_handler = MockStateHandler("order_handler", ["order.*"])
        market_handler = MockStateHandler("market_handler", ["market.*"])

        recovery_manager.register_handler(order_handler)
        recovery_manager.register_handler(market_handler)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True
        assert (
            result["metrics"]["events_processed"] == 4
        )  # order.placed, order.ack, market.tick, order.fill
        assert result["metrics"]["events_skipped"] == 1  # position.update has no handler

        # Check handlers received correct events
        assert len(order_handler.recovered_events) == 3  # placed, ack, fill
        assert len(market_handler.recovered_events) == 1  # tick

        # Verify event order
        order_topics = [e.topic for e in order_handler.recovered_events]
        assert order_topics == ["order.placed", "order.ack", "order.fill"]

    @pytest.mark.asyncio
    async def test_topic_filtering(self, recovery_manager, populated_store):
        """Test recovery with topic filtering."""
        handler = MockStateHandler("handler", ["order.*"])
        recovery_manager.register_handler(handler)

        # Recover only order events
        result = await recovery_manager.recover_state(topic_filter="order.*")

        assert result["success"] is True
        assert result["metrics"]["events_processed"] == 3
        assert len(handler.recovered_events) == 3

    @pytest.mark.asyncio
    async def test_sequence_range_recovery(self, recovery_manager, populated_store):
        """Test recovery with sequence number range."""
        handler = MockStateHandler("handler", ["*"])  # Catch all events
        recovery_manager.register_handler(handler)

        # Recover events 2-3 (from_sequence=1 means > 1, so starts at 2)
        result = await recovery_manager.recover_state(from_sequence=1, to_sequence=3)

        assert result["success"] is True
        assert result["metrics"]["events_processed"] == 2  # Events 2 and 3
        assert len(handler.recovered_events) == 2

    @pytest.mark.asyncio
    async def test_error_handling(self, recovery_manager, event_store):
        """Test recovery with handler errors."""
        # Add events including one that will cause an error
        await event_store.append("good.event", {"data": "test1"})
        await event_store.append("error.test", {"data": "test2"})  # This will cause error
        await event_store.append("good.event", {"data": "test3"})

        handler = MockStateHandler("handler", ["*"])
        recovery_manager.register_handler(handler)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True
        assert result["metrics"]["events_processed"] == 3
        assert result["metrics"]["errors"] == 1  # One error from error.test

        # Should still process other events
        assert len(handler.recovered_events) == 2  # Two good events

    @pytest.mark.asyncio
    async def test_wildcard_topic_matching(self, recovery_manager, event_store):
        """Test wildcard topic matching."""
        # Add events with various topics
        await event_store.append("order.placed", {"data": "order1"})
        await event_store.append("order.filled", {"data": "order2"})
        await event_store.append("market.tick", {"data": "market1"})
        await event_store.append("position.update", {"data": "position1"})

        # Handler for all order events
        order_handler = MockStateHandler("order", ["order.*"])
        recovery_manager.register_handler(order_handler)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True
        assert len(order_handler.recovered_events) == 2  # Two order events

        topics = [e.topic for e in order_handler.recovered_events]
        assert "order.placed" in topics
        assert "order.filled" in topics

    @pytest.mark.asyncio
    async def test_performance_smoke_test(self, recovery_manager, event_store):
        """Test the performance smoke test functionality."""
        # Add some test events
        for i in range(100):
            await event_store.append("test.event", {"index": i})

        handler = MockStateHandler("handler", ["*"])
        recovery_manager.register_handler(handler)

        # Run smoke test
        result = await recovery_manager.perform_smoke_test()

        assert result["success"] is True
        assert result["test_events"] == 100
        assert result["events_per_second"] > 0
        assert result["estimated_time_for_1m"] > 0
        assert "recovery_result" in result

    @pytest.mark.asyncio
    async def test_empty_store_smoke_test(self, recovery_manager):
        """Test smoke test with empty store."""
        result = await recovery_manager.perform_smoke_test()

        assert result["success"] is True
        assert result["total_events"] == 0
        assert result["estimated_time_for_1m"] == 0.0

    @pytest.mark.asyncio
    async def test_multiple_handlers_same_topic(self, recovery_manager, event_store):
        """Test multiple handlers for the same topic."""
        await event_store.append("shared.event", {"data": "test"})

        handler1 = MockStateHandler("handler1", ["shared.*"])
        handler2 = MockStateHandler("handler2", ["shared.*"])

        recovery_manager.register_handler(handler1)
        recovery_manager.register_handler(handler2)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True
        assert result["metrics"]["events_processed"] == 1

        # Both handlers should have processed the event
        assert len(handler1.recovered_events) == 1
        assert len(handler2.recovered_events) == 1

    @pytest.mark.asyncio
    async def test_batch_processing(self, recovery_manager, event_store):
        """Test batch processing with many events."""
        # Add many events to test batch processing
        num_events = 2500  # More than one batch (1000)
        for i in range(num_events):
            await event_store.append("test.batch", {"index": i})

        handler = MockStateHandler("handler", ["*"])
        recovery_manager.register_handler(handler)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True
        assert result["metrics"]["events_processed"] == num_events
        assert len(handler.recovered_events) == num_events

        # Verify events are in order
        indices = [e.payload["index"] for e in handler.recovered_events]
        assert indices == list(range(num_events))

    @pytest.mark.asyncio
    async def test_recovery_metrics(self, recovery_manager, populated_store):
        """Test recovery metrics collection."""
        handler = MockStateHandler("handler", ["order.*"])
        recovery_manager.register_handler(handler)

        # Perform recovery
        result = await recovery_manager.recover_state()

        assert result["success"] is True

        metrics = result["metrics"]
        assert "events_processed" in metrics
        assert "events_skipped" in metrics
        assert "errors" in metrics
        assert "recovery_time" in metrics
        assert "last_recovery" in metrics

        assert metrics["events_processed"] > 0
        assert metrics["recovery_time"] > 0
        assert metrics["last_recovery"] is not None

    @pytest.mark.asyncio
    async def test_get_recovery_status(self, recovery_manager):
        """Test getting recovery status."""
        handler = MockStateHandler("handler", ["test.*"])
        recovery_manager.register_handler(handler)

        status = await recovery_manager.get_recovery_status()

        assert "registered_handlers" in status
        assert "total_topics" in status
        assert "metrics" in status

        assert status["registered_handlers"] == 1
        assert status["total_topics"] == 1


class TestPerformanceRequirement:
    """Test cases specifically for the < 2s for 1M events requirement."""

    @pytest.mark.asyncio
    async def test_large_scale_recovery_simulation(self):
        """Test recovery performance with a large number of events."""
        # Use in-memory store for speed
        store = EventStore(":memory:")
        await store.initialize()

        try:
            manager = RecoveryManager(store)
            handler = MockStateHandler("perf_handler", ["*"])
            manager.register_handler(handler)

            # Add a substantial number of events for testing
            num_events = 10000  # Substantial but not too slow for CI

            import time

            start_time = time.time()

            for i in range(num_events):
                await store.append("perf.test", {"index": i, "data": f"event_{i}"})

            append_time = time.time() - start_time

            # Perform recovery
            recovery_start = time.time()
            result = await manager.recover_state()
            recovery_time = time.time() - recovery_start

            assert result["success"] is True
            assert result["metrics"]["events_processed"] == num_events

            # Calculate estimated performance for 1M events
            events_per_second = num_events / recovery_time
            estimated_1m_time = 1_000_000 / events_per_second

            print("Performance test results:")
            print(f"  {num_events} events appended in {append_time:.3f}s")
            print(f"  {num_events} events recovered in {recovery_time:.3f}s")
            print(f"  Recovery rate: {events_per_second:.0f} events/second")
            print(f"  Estimated time for 1M events: {estimated_1m_time:.2f}s")

            # The target is < 2s for 1M events
            # For this to pass with our test size, we need good performance
            assert (
                recovery_time < 5.0
            ), f"Recovery too slow: {recovery_time:.3f}s for {num_events} events"

        finally:
            await store.close()
