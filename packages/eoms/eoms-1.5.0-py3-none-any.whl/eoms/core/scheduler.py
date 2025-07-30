"""
Nightly job scheduler for EventStore maintenance.

Provides automated snapshot creation and compaction for disk space optimization.
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from eoms.core.eventstore import EventStore
from eoms.core.recovery import RecoveryManager

logger = logging.getLogger(__name__)


class SnapshotJob:
    """
    Automated job for creating snapshots and compacting events.

    This job should be run nightly to maintain optimal disk space usage
    and ensure fast recovery times.
    """

    def __init__(
        self,
        event_store: EventStore,
        recovery_manager: RecoveryManager,
        state_provider: Optional[Callable[[], Dict[str, Any]]] = None,
        min_events_for_snapshot: int = 10000,
        keep_snapshots: int = 7,
    ):
        """
        Initialize SnapshotJob.

        Args:
            event_store: EventStore to maintain
            recovery_manager: RecoveryManager for state reconstruction
            state_provider: Function to get current state for snapshot. If None,
                          uses recovery manager to rebuild state.
            min_events_for_snapshot: Minimum events before creating snapshot
            keep_snapshots: Number of recent snapshots to keep
        """
        self.event_store = event_store
        self.recovery_manager = recovery_manager
        self.state_provider = state_provider
        self.min_events_for_snapshot = min_events_for_snapshot
        self.keep_snapshots = keep_snapshots

        # Job statistics
        self.last_run: Optional[datetime] = None
        self.last_snapshot_sequence: Optional[int] = None
        self.total_runs = 0
        self.total_space_saved = 0

    async def run(self) -> Dict[str, Any]:
        """
        Run the snapshot and compaction job.

        Returns:
            Dictionary with job execution results
        """
        start_time = time.time()
        job_timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

        logger.info("Starting nightly snapshot job")

        try:
            # Get current state of the event store
            total_events = await self.event_store.get_event_count()
            latest_sequence = await self.event_store.get_latest_sequence()

            if total_events < self.min_events_for_snapshot:
                logger.info(
                    f"Not enough events for snapshot "
                    f"({total_events} < {self.min_events_for_snapshot})"
                )
                return {
                    "success": True,
                    "action": "skipped",
                    "reason": "insufficient_events",
                    "total_events": total_events,
                    "execution_time": time.time() - start_time,
                }

            # Check if we need a new snapshot
            latest_snapshot = await self.event_store.get_latest_snapshot()

            events_since_snapshot = latest_sequence
            if latest_snapshot:
                events_since_snapshot = latest_sequence - latest_snapshot.sequence_number

            # Create snapshot if enough new events
            snapshot_created = False
            compaction_performed = False
            space_saved = 0

            if events_since_snapshot >= self.min_events_for_snapshot // 2:
                # Get current state for snapshot
                current_state = await self._get_current_state(latest_sequence)

                # Create snapshot
                snapshot = await self.event_store.create_snapshot(
                    current_state, sequence_number=latest_sequence
                )
                snapshot_created = True
                self.last_snapshot_sequence = latest_sequence

                logger.info(
                    f"Created snapshot {snapshot.snapshot_id} at sequence {latest_sequence}"
                )

                # Compact events older than the snapshot
                if latest_snapshot:
                    # Keep events from the previous snapshot onwards initially
                    compact_from = latest_snapshot.sequence_number

                    # But if we have many events, we can be more aggressive
                    if events_since_snapshot > self.min_events_for_snapshot:
                        # Keep only recent half of events
                        compact_from = latest_sequence - (events_since_snapshot // 2)

                    compaction_stats = await self.event_store.compact_events(compact_from)
                    compaction_performed = True
                    space_saved = compaction_stats["space_saved_bytes"]
                    self.total_space_saved += space_saved

                    logger.info(
                        f"Compacted {compaction_stats['events_removed']} events, "
                        f"saved {space_saved} bytes"
                    )

            # Clean up old snapshots
            removed_snapshots = await self.event_store.cleanup_old_snapshots(
                keep_count=self.keep_snapshots
            )

            # Update job statistics
            execution_time = time.time() - start_time
            self.last_run = job_timestamp
            self.total_runs += 1

            result = {
                "success": True,
                "action": "completed",
                "snapshot_created": snapshot_created,
                "compaction_performed": compaction_performed,
                "space_saved_bytes": space_saved,
                "removed_snapshots": removed_snapshots,
                "total_events": total_events,
                "events_since_last_snapshot": events_since_snapshot,
                "execution_time": execution_time,
                "timestamp": job_timestamp.isoformat(),
            }

            logger.info(f"Snapshot job completed in {execution_time:.2f}s")
            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Snapshot job failed after {execution_time:.2f}s: {e}")

            return {
                "success": False,
                "action": "failed",
                "error": str(e),
                "execution_time": execution_time,
                "timestamp": job_timestamp.isoformat(),
            }

    async def _get_current_state(self, up_to_sequence: int) -> Dict[str, Any]:
        """
        Get current state for snapshot creation.

        Args:
            up_to_sequence: Sequence number to capture state up to

        Returns:
            Current state dictionary
        """
        if self.state_provider:
            # Use provided state function
            return self.state_provider()

        # Use recovery manager to rebuild state
        # This is a simplified approach - in production you'd want more sophisticated state capture
        recovery_result = await self.recovery_manager.recover_state(
            to_sequence=up_to_sequence,
            republish_events=False,
        )

        return {
            "recovery_stats": recovery_result.get("metrics", {}),
            "snapshot_sequence": up_to_sequence,
            "snapshot_timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
            "total_events": await self.event_store.get_event_count(),
        }

    def get_job_statistics(self) -> Dict[str, Any]:
        """Get job execution statistics."""
        return {
            "total_runs": self.total_runs,
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "last_snapshot_sequence": self.last_snapshot_sequence,
            "total_space_saved_bytes": self.total_space_saved,
        }


class SimpleScheduler:
    """
    Simple scheduler for running maintenance jobs.

    In production, you might want to use a more sophisticated scheduler
    like APScheduler or integrate with existing job scheduling systems.
    """

    def __init__(self):
        self.jobs: Dict[str, SnapshotJob] = {}
        self.running = False
        self._task: Optional[asyncio.Task] = None

    def add_job(self, name: str, job: SnapshotJob) -> None:
        """Add a job to the scheduler."""
        self.jobs[name] = job
        logger.info(f"Added job '{name}' to scheduler")

    def remove_job(self, name: str) -> None:
        """Remove a job from the scheduler."""
        if name in self.jobs:
            del self.jobs[name]
            logger.info(f"Removed job '{name}' from scheduler")

    async def start(self, check_interval: int = 3600) -> None:
        """
        Start the scheduler.

        Args:
            check_interval: How often to check for jobs to run (seconds)
        """
        if self.running:
            return

        self.running = True
        self._task = asyncio.create_task(self._run_loop(check_interval))
        logger.info(f"Scheduler started with {check_interval}s check interval")

    async def stop(self) -> None:
        """Stop the scheduler."""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler stopped")

    async def _run_loop(self, check_interval: int) -> None:
        """Main scheduler loop."""
        while self.running:
            try:
                # For this simple scheduler, run all jobs each time
                # In production, you'd have more sophisticated scheduling logic
                for name, job in self.jobs.items():
                    try:
                        logger.debug(f"Running job '{name}'")
                        result = await job.run()

                        if not result["success"]:
                            logger.warning(
                                f"Job '{name}' failed: {result.get('error', 'Unknown error')}"
                            )

                    except Exception as e:
                        logger.error(f"Error running job '{name}': {e}")

                # Wait for next check
                await asyncio.sleep(check_interval)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)  # Wait a minute before retrying

    async def run_job_now(self, name: str) -> Dict[str, Any]:
        """Run a specific job immediately."""
        if name not in self.jobs:
            raise ValueError(f"Job '{name}' not found")

        logger.info(f"Running job '{name}' on demand")
        return await self.jobs[name].run()
