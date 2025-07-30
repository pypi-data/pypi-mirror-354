"""Tests for the nightly job scheduler."""

import asyncio
from datetime import datetime

import pytest

from eoms.core.eventstore import EventStore
from eoms.core.recovery import RecoveryManager
from eoms.core.scheduler import SimpleScheduler, SnapshotJob


class MockStateHandler:
    """Mock state recovery handler for testing."""

    def __init__(self, name: str, topics: list[str]):
        self.name = name
        self.topics = topics
        self.recovered_events = []

    async def recover_from_event(self, event) -> None:
        """Recover state from event."""
        self.recovered_events.append(event)

    def get_recovery_topics(self) -> list[str]:
        """Get recovery topics."""
        return self.topics

    def get_component_name(self) -> str:
        """Get component name."""
        return self.name


class TestSnapshotJob:
    """Test cases for SnapshotJob functionality."""

    @pytest.fixture
    async def setup(self):
        """Create test setup with EventStore and RecoveryManager."""
        store = EventStore(":memory:")
        await store.initialize()

        recovery_manager = RecoveryManager(store)
        handler = MockStateHandler("test", ["*"])
        recovery_manager.register_handler(handler)

        yield store, recovery_manager

        await store.close()

    @pytest.mark.asyncio
    async def test_job_creation(self, setup):
        """Test creating a SnapshotJob."""
        store, recovery_manager = setup

        job = SnapshotJob(store, recovery_manager)

        assert job.event_store == store
        assert job.recovery_manager == recovery_manager
        assert job.min_events_for_snapshot == 10000
        assert job.keep_snapshots == 7
        assert job.total_runs == 0

    @pytest.mark.asyncio
    async def test_job_skips_when_insufficient_events(self, setup):
        """Test that job skips when there are not enough events."""
        store, recovery_manager = setup

        # Add only a few events
        for i in range(100):
            await store.append("test.event", {"index": i})

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=1000)
        result = await job.run()

        assert result["success"] is True
        assert result["action"] == "skipped"
        assert result["reason"] == "insufficient_events"
        assert result["total_events"] == 100

    @pytest.mark.asyncio
    async def test_job_creates_first_snapshot(self, setup):
        """Test job creates first snapshot when conditions are met."""
        store, recovery_manager = setup

        # Add enough events
        for i in range(1000):
            await store.append("test.event", {"index": i})

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=500)
        result = await job.run()

        assert result["success"] is True
        assert result["action"] == "completed"
        assert result["snapshot_created"] is True
        assert result["compaction_performed"] is False  # No previous snapshot to compact from
        assert result["total_events"] == 1000

        # Verify snapshot was created
        snapshot = await store.get_latest_snapshot()
        assert snapshot is not None
        assert snapshot.sequence_number == 1000

    @pytest.mark.asyncio
    async def test_job_with_custom_state_provider(self, setup):
        """Test job with custom state provider function."""
        store, recovery_manager = setup

        # Add events
        for i in range(1000):
            await store.append("test.event", {"index": i})

        def custom_state_provider():
            return {"custom_state": "test_value", "timestamp": "2024-01-01"}

        job = SnapshotJob(
            store,
            recovery_manager,
            state_provider=custom_state_provider,
            min_events_for_snapshot=500,
        )
        result = await job.run()

        assert result["success"] is True
        assert result["snapshot_created"] is True

        # Verify snapshot contains custom state
        snapshot = await store.get_latest_snapshot()
        assert snapshot.state_data["custom_state"] == "test_value"

    @pytest.mark.asyncio
    async def test_job_compaction_with_existing_snapshot(self, setup):
        """Test job performs compaction when there's an existing snapshot."""
        store, recovery_manager = setup

        # Add initial events
        for i in range(1000):
            await store.append("test.event", {"index": i})

        # Create initial snapshot manually
        await store.create_snapshot({"initial": True}, sequence_number=500)

        # Add more events
        for i in range(1000, 2000):
            await store.append("test.event", {"index": i})

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=500)
        result = await job.run()

        assert result["success"] is True
        assert result["action"] == "completed"
        assert result["snapshot_created"] is True
        assert result["compaction_performed"] is True
        assert result["space_saved_bytes"] >= 0  # Might be 0 in memory

        # Verify events were compacted
        final_count = await store.get_event_count()
        assert final_count < 2000  # Some events should have been removed

    @pytest.mark.asyncio
    async def test_job_statistics(self, setup):
        """Test job statistics tracking."""
        store, recovery_manager = setup

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=100)

        # Initial statistics
        stats = job.get_job_statistics()
        assert stats["total_runs"] == 0
        assert stats["last_run"] is None

        # Add events and run job
        for i in range(200):
            await store.append("test.event", {"index": i})

        result = await job.run()
        assert result["success"] is True

        # Check updated statistics
        stats = job.get_job_statistics()
        assert stats["total_runs"] == 1
        assert stats["last_run"] is not None
        assert stats["last_snapshot_sequence"] == 200

    @pytest.mark.asyncio
    async def test_job_cleanup_old_snapshots(self, setup):
        """Test that job cleans up old snapshots."""
        store, recovery_manager = setup

        # Create multiple snapshots
        for i in range(10):
            await store.create_snapshot({"version": i}, sequence_number=i * 100)

        job = SnapshotJob(store, recovery_manager, keep_snapshots=3, min_events_for_snapshot=100)

        # Add some events and run job
        for i in range(200):
            await store.append("test.event", {"index": i})

        result = await job.run()

        assert result["success"] is True
        assert result["removed_snapshots"] > 0  # Should have removed old snapshots


class TestSimpleScheduler:
    """Test cases for SimpleScheduler functionality."""

    @pytest.fixture
    async def scheduler_setup(self):
        """Create test setup with scheduler and jobs."""
        store = EventStore(":memory:")
        await store.initialize()

        recovery_manager = RecoveryManager(store)
        handler = MockStateHandler("test", ["*"])
        recovery_manager.register_handler(handler)

        scheduler = SimpleScheduler()

        yield scheduler, store, recovery_manager

        await scheduler.stop()
        await store.close()

    @pytest.mark.asyncio
    async def test_scheduler_creation(self, scheduler_setup):
        """Test creating a scheduler."""
        scheduler, store, recovery_manager = scheduler_setup

        assert len(scheduler.jobs) == 0
        assert not scheduler.running

    @pytest.mark.asyncio
    async def test_add_remove_job(self, scheduler_setup):
        """Test adding and removing jobs."""
        scheduler, store, recovery_manager = scheduler_setup

        job = SnapshotJob(store, recovery_manager)

        # Add job
        scheduler.add_job("test_job", job)
        assert len(scheduler.jobs) == 1
        assert "test_job" in scheduler.jobs

        # Remove job
        scheduler.remove_job("test_job")
        assert len(scheduler.jobs) == 0
        assert "test_job" not in scheduler.jobs

    @pytest.mark.asyncio
    async def test_run_job_now(self, scheduler_setup):
        """Test running a job on demand."""
        scheduler, store, recovery_manager = scheduler_setup

        # Add events
        for i in range(200):
            await store.append("test.event", {"index": i})

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=100)
        scheduler.add_job("test_job", job)

        # Run job immediately
        result = await scheduler.run_job_now("test_job")

        assert result["success"] is True
        assert result["action"] == "completed"
        assert result["snapshot_created"] is True

    @pytest.mark.asyncio
    async def test_run_nonexistent_job(self, scheduler_setup):
        """Test running a job that doesn't exist."""
        scheduler, store, recovery_manager = scheduler_setup

        with pytest.raises(ValueError, match="Job 'nonexistent' not found"):
            await scheduler.run_job_now("nonexistent")

    @pytest.mark.asyncio
    async def test_scheduler_start_stop(self, scheduler_setup):
        """Test starting and stopping the scheduler."""
        scheduler, store, recovery_manager = scheduler_setup

        # Start scheduler
        await scheduler.start(check_interval=1)  # 1 second for testing
        assert scheduler.running is True
        assert scheduler._task is not None

        # Stop scheduler
        await scheduler.stop()
        assert scheduler.running is False

    @pytest.mark.asyncio
    async def test_scheduler_runs_jobs_periodically(self, scheduler_setup):
        """Test that scheduler runs jobs periodically."""
        scheduler, store, recovery_manager = scheduler_setup

        # Add events
        for i in range(200):
            await store.append("test.event", {"index": i})

        job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=100)
        scheduler.add_job("test_job", job)

        # Start scheduler with very short interval
        await scheduler.start(check_interval=0.1)  # 100ms for testing

        # Wait a short time
        await asyncio.sleep(0.5)

        # Stop scheduler
        await scheduler.stop()

        # Job should have run at least once
        stats = job.get_job_statistics()
        assert stats["total_runs"] >= 1


class TestSchedulerIntegration:
    """Integration tests for the complete scheduler system."""

    @pytest.mark.asyncio
    async def test_full_snapshot_workflow(self):
        """Test complete workflow from events to snapshot to compaction."""
        # Setup
        store = EventStore(":memory:")
        await store.initialize()

        recovery_manager = RecoveryManager(store)
        handler = MockStateHandler("test", ["*"])
        recovery_manager.register_handler(handler)

        scheduler = SimpleScheduler()

        try:
            # Add many events over time
            for batch in range(5):
                for i in range(500):
                    await store.append(
                        "test.event",
                        {
                            "batch": batch,
                            "index": i,
                            "timestamp": datetime.now().isoformat(),
                        },
                    )

                # Run snapshot job after each batch
                job = SnapshotJob(store, recovery_manager, min_events_for_snapshot=400)
                result = await job.run()

                if batch == 0:
                    # First run should create snapshot
                    assert result["snapshot_created"] is True
                    assert result["compaction_performed"] is False
                else:
                    # Subsequent runs should create snapshot and compact
                    assert result["snapshot_created"] is True
                    assert result["compaction_performed"] is True

            # Verify final state
            total_events = await store.get_event_count()
            latest_snapshot = await store.get_latest_snapshot()

            assert total_events < 2500  # Should be less than total due to compaction
            assert latest_snapshot is not None
            assert latest_snapshot.sequence_number > 2000  # Latest snapshot should be recent

        finally:
            await scheduler.stop()
            await store.close()
