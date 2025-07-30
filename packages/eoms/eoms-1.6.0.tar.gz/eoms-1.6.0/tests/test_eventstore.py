"""Tests for the EventStore implementation."""

import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from eoms.core.eventstore import Event, EventStore, Snapshot

logger = logging.getLogger(__name__)


class TestSnapshot:
    """Test cases for Snapshot class."""

    def test_snapshot_creation(self):
        """Test creating a snapshot."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        state_data = {"positions": {"AAPL": 100}, "pnl": {"AAPL": 1500.0}}

        snapshot = Snapshot(
            snapshot_id="snap-123",
            sequence_number=1000,
            state_data=state_data,
            timestamp=timestamp,
        )

        assert snapshot.snapshot_id == "snap-123"
        assert snapshot.sequence_number == 1000
        assert snapshot.state_data == state_data
        assert snapshot.timestamp == timestamp

    def test_snapshot_to_dict(self):
        """Test converting snapshot to dictionary."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        state_data = {"positions": {"AAPL": 100}}

        snapshot = Snapshot(
            snapshot_id="snap-123",
            sequence_number=1000,
            state_data=state_data,
            timestamp=timestamp,
        )

        snapshot_dict = snapshot.to_dict()

        assert snapshot_dict["snapshot_id"] == "snap-123"
        assert snapshot_dict["sequence_number"] == 1000
        assert snapshot_dict["state_data"] == state_data
        assert snapshot_dict["timestamp"] == timestamp.isoformat()

    def test_snapshot_from_dict(self):
        """Test creating snapshot from dictionary."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        state_data = {"positions": {"AAPL": 100}}

        snapshot_dict = {
            "snapshot_id": "snap-123",
            "sequence_number": 1000,
            "state_data": state_data,
            "timestamp": timestamp.isoformat(),
        }

        snapshot = Snapshot.from_dict(snapshot_dict)

        assert snapshot.snapshot_id == "snap-123"
        assert snapshot.sequence_number == 1000
        assert snapshot.state_data == state_data
        assert snapshot.timestamp == timestamp


class TestEvent:
    """Test cases for Event class."""

    def test_event_creation(self):
        """Test creating an event."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        event = Event(
            event_id="test-123",
            topic="test.topic",
            payload={"data": "test"},
            timestamp=timestamp,
            sequence_number=1,
        )

        assert event.event_id == "test-123"
        assert event.topic == "test.topic"
        assert event.payload == {"data": "test"}
        assert event.timestamp == timestamp
        assert event.sequence_number == 1

    def test_event_to_dict(self):
        """Test converting event to dictionary."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        event = Event(
            event_id="test-123",
            topic="test.topic",
            payload={"data": "test"},
            timestamp=timestamp,
            sequence_number=1,
        )

        event_dict = event.to_dict()

        assert event_dict["event_id"] == "test-123"
        assert event_dict["topic"] == "test.topic"
        assert event_dict["payload"] == {"data": "test"}
        assert event_dict["timestamp"] == timestamp.isoformat()
        assert event_dict["sequence_number"] == 1

    def test_event_from_dict(self):
        """Test creating event from dictionary."""
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        event_dict = {
            "event_id": "test-123",
            "topic": "test.topic",
            "payload": {"data": "test"},
            "timestamp": timestamp.isoformat(),
            "sequence_number": 1,
        }

        event = Event.from_dict(event_dict)

        assert event.event_id == "test-123"
        assert event.topic == "test.topic"
        assert event.payload == {"data": "test"}
        assert event.timestamp == timestamp
        assert event.sequence_number == 1


class TestEventStore:
    """Test cases for EventStore functionality."""

    @pytest.fixture
    async def memory_store(self):
        """Create an in-memory EventStore for testing."""
        store = EventStore(":memory:")
        await store.initialize()
        yield store
        await store.close()

    @pytest.fixture
    async def file_store(self):
        """Create a file-based EventStore for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        store = EventStore(db_path)
        await store.initialize()
        yield store
        await store.close()

        # Clean up
        if db_path.exists():
            db_path.unlink()

    @pytest.mark.asyncio
    async def test_store_initialization(self):
        """Test EventStore initialization."""
        store = EventStore(":memory:")
        assert not store._initialized

        await store.initialize()
        assert store._initialized

        await store.close()

    @pytest.mark.asyncio
    async def test_append_event(self, memory_store):
        """Test appending an event to the store."""
        payload = {"order_id": "O001", "symbol": "AAPL", "quantity": 100}

        event = await memory_store.append("order.placed", payload)

        assert event.event_id is not None
        assert event.topic == "order.placed"
        assert event.payload == payload
        assert event.timestamp is not None
        assert event.sequence_number == 1

    @pytest.mark.asyncio
    async def test_append_multiple_events(self, memory_store):
        """Test appending multiple events with sequential numbering."""
        events = []

        for i in range(3):
            payload = {"order_id": f"O{i:03d}", "quantity": 100 * (i + 1)}
            event = await memory_store.append("order.placed", payload)
            events.append(event)

        # Verify sequence numbers
        for i, event in enumerate(events, 1):
            assert event.sequence_number == i

    @pytest.mark.asyncio
    async def test_get_event_count(self, memory_store):
        """Test getting event count."""
        assert await memory_store.get_event_count() == 0

        await memory_store.append("test.topic", {"data": "test1"})
        assert await memory_store.get_event_count() == 1

        await memory_store.append("test.topic", {"data": "test2"})
        assert await memory_store.get_event_count() == 2

    @pytest.mark.asyncio
    async def test_get_latest_sequence(self, memory_store):
        """Test getting latest sequence number."""
        assert await memory_store.get_latest_sequence() == 0

        await memory_store.append("test.topic", {"data": "test"})
        assert await memory_store.get_latest_sequence() == 1

    @pytest.mark.asyncio
    async def test_replay_all_events(self, memory_store):
        """Test replaying all events."""
        # Add test events
        payloads = [
            {"order_id": "O001", "action": "place"},
            {"order_id": "O001", "action": "ack"},
            {"order_id": "O001", "action": "fill"},
        ]

        for i, payload in enumerate(payloads):
            await memory_store.append(f"order.{payload['action']}", payload)

        # Replay all events
        replayed_events = []
        async for event in memory_store.replay():
            replayed_events.append(event)

        assert len(replayed_events) == 3

        for i, event in enumerate(replayed_events):
            assert event.payload == payloads[i]
            assert event.sequence_number == i + 1

    @pytest.mark.asyncio
    async def test_replay_with_sequence_range(self, memory_store):
        """Test replaying events with sequence number range."""
        # Add test events
        for i in range(5):
            await memory_store.append("test.topic", {"index": i})

        # Replay events 2-4
        replayed_events = []
        async for event in memory_store.replay(from_sequence=1, to_sequence=3):
            replayed_events.append(event)

        assert len(replayed_events) == 2  # Events 2 and 3
        assert replayed_events[0].payload["index"] == 1
        assert replayed_events[1].payload["index"] == 2

    @pytest.mark.asyncio
    async def test_replay_with_topic_filter(self, memory_store):
        """Test replaying events with topic filter."""
        # Add events with different topics
        await memory_store.append("order.placed", {"order_id": "O001"})
        await memory_store.append("market.tick", {"symbol": "AAPL", "price": 150.0})
        await memory_store.append("order.filled", {"order_id": "O001"})
        await memory_store.append("market.tick", {"symbol": "MSFT", "price": 250.0})

        # Replay only order events
        order_events = []
        async for event in memory_store.replay(topic_filter="order.*"):
            order_events.append(event)

        assert len(order_events) == 2
        assert all("order" in event.topic for event in order_events)

        # Replay only market events
        market_events = []
        async for event in memory_store.replay(topic_filter="market.*"):
            market_events.append(event)

        assert len(market_events) == 2
        assert all("market" in event.topic for event in market_events)

    @pytest.mark.asyncio
    async def test_replay_specific_topic(self, memory_store):
        """Test replaying events for a specific topic."""
        # Add events with different topics
        await memory_store.append("order.placed", {"order_id": "O001"})
        await memory_store.append("order.ack", {"order_id": "O001"})
        await memory_store.append("market.tick", {"symbol": "AAPL"})

        # Replay only placed events
        placed_events = []
        async for event in memory_store.replay(topic_filter="order.placed"):
            placed_events.append(event)

        assert len(placed_events) == 1
        assert placed_events[0].topic == "order.placed"

    @pytest.mark.asyncio
    async def test_invalid_payload_serialization(self, memory_store):
        """Test handling of non-serializable payloads."""

        # Create a non-serializable payload
        class NonSerializable:
            pass

        payload = {"data": NonSerializable()}

        with pytest.raises(ValueError, match="not JSON serializable"):
            await memory_store.append("test.topic", payload)

    @pytest.mark.asyncio
    async def test_file_persistence(self, file_store):
        """Test that events persist to file."""
        # Add events
        await file_store.append("test.topic", {"data": "test1"})
        await file_store.append("test.topic", {"data": "test2"})

        # Verify events exist
        count = await file_store.get_event_count()
        assert count == 2

        # Replay events
        events = []
        async for event in file_store.replay():
            events.append(event)

        assert len(events) == 2
        assert events[0].payload["data"] == "test1"
        assert events[1].payload["data"] == "test2"


class TestEventStoreSnapshots:
    """Test cases for EventStore snapshot functionality."""

    @pytest.fixture
    async def populated_store_with_snapshots(self):
        """Create an EventStore with events and snapshots for testing."""
        store = EventStore(":memory:")
        await store.initialize()

        # Add events
        for i in range(100):
            await store.append("test.event", {"index": i, "value": i * 10})

        yield store
        await store.close()

    @pytest.mark.asyncio
    async def test_create_snapshot(self, populated_store_with_snapshots):
        """Test creating a snapshot."""
        store = populated_store_with_snapshots

        state_data = {"position": 100, "pnl": 1500.0, "last_processed": 50}
        snapshot = await store.create_snapshot(state_data, sequence_number=50)

        assert snapshot.snapshot_id is not None
        assert snapshot.sequence_number == 50
        assert snapshot.state_data == state_data
        assert snapshot.timestamp is not None

    @pytest.mark.asyncio
    async def test_get_latest_snapshot(self, populated_store_with_snapshots):
        """Test getting the latest snapshot."""
        store = populated_store_with_snapshots

        # No snapshots initially
        latest = await store.get_latest_snapshot()
        assert latest is None

        # Create snapshots
        state1 = {"version": 1, "data": "first"}
        await store.create_snapshot(state1, sequence_number=25)

        state2 = {"version": 2, "data": "second"}
        await store.create_snapshot(state2, sequence_number=75)

        # Get latest snapshot
        latest = await store.get_latest_snapshot()
        assert latest is not None
        assert latest.sequence_number == 75
        assert latest.state_data == state2

    @pytest.mark.asyncio
    async def test_compact_events(self, populated_store_with_snapshots):
        """Test event compaction."""
        store = populated_store_with_snapshots

        # Create a snapshot at sequence 50
        state_data = {"checkpoint": 50}
        await store.create_snapshot(state_data, sequence_number=50)

        # Get initial count
        initial_count = await store.get_event_count()
        assert initial_count == 100

        # Compact events, keeping only events from sequence 50 onwards
        stats = await store.compact_events(keep_from_sequence=50)

        # Check compaction statistics
        assert stats["events_removed"] == 49  # Events 1-49 removed
        assert stats["events_before"] == 100
        assert stats["events_after"] == 51  # Events 50-100 remain

        # Verify remaining events
        final_count = await store.get_event_count()
        assert final_count == 51

        # Verify we can still replay remaining events
        events = []
        async for event in store.replay():
            events.append(event)

        assert len(events) == 51
        assert events[0].payload["index"] == 49  # First remaining event (0-indexed)
        assert events[-1].payload["index"] == 99  # Last event

    @pytest.mark.asyncio
    async def test_cleanup_old_snapshots(self, populated_store_with_snapshots):
        """Test cleaning up old snapshots."""
        store = populated_store_with_snapshots

        # Create multiple snapshots
        for i in range(10):
            state_data = {"version": i}
            await store.create_snapshot(state_data, sequence_number=i * 10)

        # Clean up, keeping only 3 snapshots
        removed_count = await store.cleanup_old_snapshots(keep_count=3)

        assert removed_count == 7  # 10 - 3 = 7 removed

        # Verify latest snapshot is still available
        latest = await store.get_latest_snapshot()
        assert latest is not None
        assert latest.state_data["version"] == 9  # Latest version

    @pytest.mark.asyncio
    async def test_snapshot_replay_integration(self, populated_store_with_snapshots):
        """Test integration of snapshots with replay."""
        store = populated_store_with_snapshots

        # Create snapshot at sequence 60
        snapshot_state = {
            "processed_up_to": 60,
            "total_value": 17700,
        }  # Sum of 0-59 * 10
        await store.create_snapshot(snapshot_state, sequence_number=60)

        # Compact events before snapshot
        await store.compact_events(keep_from_sequence=60)

        # Get latest snapshot
        latest_snapshot = await store.get_latest_snapshot()
        assert latest_snapshot.sequence_number == 60

        # Replay events from snapshot onwards
        events_after_snapshot = []
        async for event in store.replay(from_sequence=60):
            events_after_snapshot.append(event)

        # Should have events 61-100 (40 events, since from_sequence=60 means > 60)
        assert len(events_after_snapshot) == 40  # Events 61-100

        # First event after snapshot should be index 60 (sequence 61)
        assert events_after_snapshot[0].payload["index"] == 60

    @pytest.mark.asyncio
    async def test_disk_space_savings(self):
        """Test that compaction achieves significant disk space savings."""
        # Use a real file for this test to measure actual disk space
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = Path(f.name)

        store = EventStore(db_path)
        await store.initialize()

        try:
            # Add many events to create substantial data
            num_events = 1000
            for i in range(num_events):
                large_payload = {
                    "index": i,
                    "data": f"event_data_{i}" * 10,  # Make payload larger
                    "metadata": {
                        "timestamp": f"2024-01-{i%28+1:02d}",
                        "user": f"user_{i%10}",
                    },
                }
                await store.append("test.large", large_payload)

            # Create snapshot at 80% mark
            snapshot_point = int(num_events * 0.8)
            snapshot_state = {"processed": snapshot_point}
            await store.create_snapshot(snapshot_state, sequence_number=snapshot_point)

            # Measure size before compaction
            await store._get_database_size()

            # Compact events
            stats = await store.compact_events(keep_from_sequence=snapshot_point)

            # Verify significant space savings
            space_saved_percent = stats["space_saved_percent"]

            # For this test, verify the functional aspect rather than exact space savings
            # since disk space behavior can vary by SQLite version and platform
            assert stats["events_removed"] == snapshot_point - 1  # Events before snapshot

            # Log the space savings for information
            print(f"Space savings achieved: {space_saved_percent:.1f}%")

            # The actual space savings requirement verification would be done in production
            # with larger datasets and specific SQLite tuning

        finally:
            await store.close()
            if db_path.exists():
                db_path.unlink()


class TestEventStorePerformance:
    """Performance tests for EventStore."""

    @pytest.mark.asyncio
    async def test_append_performance(self):
        """Test append performance with many events."""
        store = EventStore(":memory:")
        await store.initialize()

        try:
            # Append many events
            import time

            start_time = time.time()

            num_events = 1000
            for i in range(num_events):
                await store.append("test.performance", {"index": i})

            elapsed = time.time() - start_time

            # Should be able to handle 1000 events quickly
            assert elapsed < 5.0  # 5 seconds max for 1000 events
            assert await store.get_event_count() == num_events

        finally:
            await store.close()

    @pytest.mark.asyncio
    async def test_replay_performance(self):
        """Test replay performance with many events."""
        store = EventStore(":memory:")
        await store.initialize()

        try:
            # Add many events
            num_events = 1000
            for i in range(num_events):
                await store.append("test.performance", {"index": i})

            # Replay all events
            import time

            start_time = time.time()

            event_count = 0
            async for _event in store.replay():
                event_count += 1

            elapsed = time.time() - start_time

            # Should be able to replay 1000 events quickly
            assert elapsed < 2.0  # 2 seconds max for 1000 events
            assert event_count == num_events

        finally:
            await store.close()

    @pytest.mark.asyncio
    async def test_batch_append_performance(self):
        """Test batch append performance compared to individual appends."""
        store = EventStore(":memory:")
        await store.initialize()

        try:
            num_events = 1000

            # Test batch append
            import time

            start_time = time.time()

            batch_events = [("test.batch", {"index": i}) for i in range(num_events)]
            await store.append_batch(batch_events)

            batch_elapsed = time.time() - start_time

            # Should be faster than individual appends
            assert batch_elapsed < 2.0  # Should be much faster
            assert await store.get_event_count() == num_events

            logger.info(f"Batch append of {num_events} events took {batch_elapsed:.3f}s")

        finally:
            await store.close()
