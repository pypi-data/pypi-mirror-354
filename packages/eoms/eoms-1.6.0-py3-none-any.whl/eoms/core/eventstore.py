"""
Event Store implementation for EOMS.

Provides append-only event persistence to SQLite with replay capabilities
for event sourcing and state reconstruction. Includes snapshot and compaction
features for efficient storage management.
"""

import asyncio
import json
import logging
import sqlite3
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, AsyncIterator, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class Snapshot:
    """Represents a state snapshot for compaction."""

    def __init__(
        self,
        snapshot_id: str,
        sequence_number: int,
        state_data: Dict[str, Any],
        timestamp: datetime,
    ):
        self.snapshot_id = snapshot_id
        self.sequence_number = sequence_number
        self.state_data = state_data
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary for serialization."""
        return {
            "snapshot_id": self.snapshot_id,
            "sequence_number": self.sequence_number,
            "state_data": self.state_data,
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Snapshot":
        """Create snapshot from dictionary."""
        return cls(
            snapshot_id=data["snapshot_id"],
            sequence_number=data["sequence_number"],
            state_data=data["state_data"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class Event:
    """Represents a stored event in the event store."""

    def __init__(
        self,
        event_id: str,
        topic: str,
        payload: Any,
        timestamp: datetime,
        sequence_number: int = 0,
    ):
        self.event_id = event_id
        self.topic = topic
        self.payload = payload
        self.timestamp = timestamp
        self.sequence_number = sequence_number

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "topic": self.topic,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "sequence_number": self.sequence_number,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """Create event from dictionary."""
        return cls(
            event_id=data["event_id"],
            topic=data["topic"],
            payload=data["payload"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            sequence_number=data.get("sequence_number", 0),
        )


class EventStore:
    """
    Append-only event store using SQLite.

    Features:
    - Append-only storage for event sourcing
    - Sequential event IDs for ordering
    - JSON payload serialization
    - Replay capabilities for state reconstruction
    - Snapshot and compaction for disk space optimization
    - Thread-safe operations
    """

    def __init__(self, db_path: Union[str, Path] = ":memory:"):
        """
        Initialize EventStore.

        Args:
            db_path: Path to SQLite database file. Use ":memory:" for in-memory store.
        """
        self.db_path = str(db_path)
        self._sequence_counter = 0
        self._connection: Optional[sqlite3.Connection] = None
        self._lock = asyncio.Lock()
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the event store and create tables."""
        async with self._lock:
            if self._initialized:
                return

            # Run in thread pool to avoid blocking
            await asyncio.get_event_loop().run_in_executor(None, self._init_db)
            self._initialized = True
            logger.info(f"EventStore initialized with database: {self.db_path}")

    def _init_db(self) -> None:
        """Initialize database schema."""
        self._connection = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            isolation_level="IMMEDIATE",  # Better concurrency
        )

        # Enable WAL mode for better concurrent read/write performance
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=NORMAL")
        self._connection.execute("PRAGMA cache_size=10000")
        self._connection.execute("PRAGMA temp_store=MEMORY")

        # Create events table
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                sequence_number INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                topic TEXT NOT NULL,
                payload TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """
        )

        # Create indices for performance
        self._connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_events_timestamp
            ON events(timestamp)
        """
        )
        self._connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_events_topic
            ON events(topic)
        """
        )
        self._connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_events_created_at
            ON events(created_at)
        """
        )

        # Create snapshots table
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY,
                sequence_number INTEGER NOT NULL,
                state_data TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at REAL NOT NULL
            )
        """
        )

        # Create index for snapshots
        self._connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_snapshots_sequence
            ON snapshots(sequence_number DESC)
        """
        )

        self._connection.commit()

        # Get current sequence number
        cursor = self._connection.execute("SELECT MAX(sequence_number) FROM events")
        result = cursor.fetchone()
        self._sequence_counter = result[0] if result[0] is not None else 0

    async def append(self, topic: str, payload: Any) -> Event:
        """
        Append an event to the store.

        Args:
            topic: Event topic
            payload: Event payload (must be JSON serializable)

        Returns:
            The created Event object

        Raises:
            ValueError: If payload is not JSON serializable
        """
        if not self._initialized:
            await self.initialize()

        # Create event
        event_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

        # Serialize payload
        try:
            payload_json = json.dumps(payload)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Payload is not JSON serializable: {e}")

        # Store in database
        async with self._lock:
            await asyncio.get_event_loop().run_in_executor(
                None, self._insert_event, event_id, topic, payload_json, timestamp
            )

            # Increment sequence counter
            self._sequence_counter += 1

        event = Event(
            event_id=event_id,
            topic=topic,
            payload=payload,
            timestamp=timestamp,
            sequence_number=self._sequence_counter,
        )

        logger.debug(f"Appended event {event_id} to topic {topic}")
        return event

    async def append_batch(self, events: List[tuple[str, Any]]) -> List[Event]:
        """
        Append multiple events in a single transaction for better performance.

        Args:
            events: List of (topic, payload) tuples

        Returns:
            List of created Event objects

        Raises:
            ValueError: If any payload is not JSON serializable
        """
        if not events:
            return []

        if not self._initialized:
            await self.initialize()

        # Prepare all events
        prepared_events = []
        result_events = []

        for topic, payload in events:
            event_id = str(uuid.uuid4())
            timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

            # Serialize payload
            try:
                payload_json = json.dumps(payload)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Payload is not JSON serializable: {e}")

            prepared_events.append((event_id, topic, payload_json, timestamp))
            result_events.append(
                Event(
                    event_id=event_id,
                    topic=topic,
                    payload=payload,
                    timestamp=timestamp,
                    sequence_number=0,  # Will be set after insertion
                )
            )

        # Insert all events in a single transaction
        async with self._lock:
            await asyncio.get_event_loop().run_in_executor(
                None, self._insert_events_batch, prepared_events
            )

            # Update sequence numbers
            for event in result_events:
                self._sequence_counter += 1
                event.sequence_number = self._sequence_counter

        logger.debug(f"Appended batch of {len(events)} events")
        return result_events

    def _insert_events_batch(self, events: List[tuple]) -> None:
        """Insert multiple events in a single transaction."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        current_time = time.time()

        # Prepare data for batch insert
        batch_data = [
            (event_id, topic, payload_json, timestamp.isoformat(), current_time)
            for event_id, topic, payload_json, timestamp in events
        ]

        self._connection.executemany(
            """
            INSERT INTO events (event_id, topic, payload, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            batch_data,
        )
        self._connection.commit()

    def _insert_event(
        self, event_id: str, topic: str, payload_json: str, timestamp: datetime
    ) -> None:
        """Insert event into database."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        self._connection.execute(
            """
            INSERT INTO events (event_id, topic, payload, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (event_id, topic, payload_json, timestamp.isoformat(), time.time()),
        )
        self._connection.commit()

    async def replay(
        self,
        from_sequence: int = 0,
        to_sequence: Optional[int] = None,
        topic_filter: Optional[str] = None,
    ) -> AsyncIterator[Event]:
        """
        Replay events from the store.

        Args:
            from_sequence: Starting sequence number (inclusive)
            to_sequence: Ending sequence number (inclusive). None for all events.
            topic_filter: Optional topic filter (supports wildcards like 'order.*')

        Yields:
            Event objects in sequence order
        """
        if not self._initialized:
            await self.initialize()

        # Build query
        query = """
            SELECT sequence_number, event_id, topic, payload, timestamp
            FROM events
            WHERE sequence_number > ?
        """
        params = [from_sequence]

        if to_sequence is not None:
            query += " AND sequence_number <= ?"
            params.append(to_sequence)

        if topic_filter:
            if "*" in topic_filter:
                # Convert wildcard to SQL LIKE pattern
                like_pattern = topic_filter.replace("*", "%")
                query += " AND topic LIKE ?"
                params.append(like_pattern)
            else:
                query += " AND topic = ?"
                params.append(topic_filter)

        query += " ORDER BY sequence_number"

        # Execute query in thread pool
        rows = await asyncio.get_event_loop().run_in_executor(
            None, self._execute_replay_query, query, params
        )

        # Yield events
        for row in rows:
            sequence_number, event_id, topic, payload_json, timestamp_str = row

            try:
                payload = json.loads(payload_json)
                timestamp = datetime.fromisoformat(timestamp_str)

                yield Event(
                    event_id=event_id,
                    topic=topic,
                    payload=payload,
                    timestamp=timestamp,
                    sequence_number=sequence_number,
                )
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error deserializing event {event_id}: {e}")
                continue

    def _execute_replay_query(self, query: str, params: List[Any]) -> List[tuple]:
        """Execute replay query and return results."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        cursor = self._connection.execute(query, params)
        return cursor.fetchall()

    async def get_event_count(self) -> int:
        """Get total number of events in store."""
        if not self._initialized:
            await self.initialize()

        count = await asyncio.get_event_loop().run_in_executor(None, self._get_count)
        return count

    def _get_count(self) -> int:
        """Get event count from database."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        cursor = self._connection.execute("SELECT COUNT(*) FROM events")
        return cursor.fetchone()[0]

    async def get_latest_sequence(self) -> int:
        """Get the latest sequence number."""
        if not self._initialized:
            await self.initialize()

        return self._sequence_counter

    async def close(self) -> None:
        """Close the event store."""
        async with self._lock:
            if self._connection:
                await asyncio.get_event_loop().run_in_executor(None, self._connection.close)
                self._connection = None

        self._initialized = False
        logger.info("EventStore closed")

    async def create_snapshot(
        self, state_data: Dict[str, Any], sequence_number: Optional[int] = None
    ) -> Snapshot:
        """
        Create a snapshot of the current state.

        Args:
            state_data: Current state data to snapshot
            sequence_number: Sequence number to snapshot at. If None, uses latest.

        Returns:
            Created Snapshot object
        """
        if not self._initialized:
            await self.initialize()

        if sequence_number is None:
            sequence_number = self._sequence_counter

        snapshot_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)

        # Serialize state data
        try:
            state_json = json.dumps(state_data)
        except (TypeError, ValueError) as e:
            raise ValueError(f"State data is not JSON serializable: {e}")

        # Store snapshot in database
        async with self._lock:
            await asyncio.get_event_loop().run_in_executor(
                None,
                self._insert_snapshot,
                snapshot_id,
                sequence_number,
                state_json,
                timestamp,
            )

        snapshot = Snapshot(
            snapshot_id=snapshot_id,
            sequence_number=sequence_number,
            state_data=state_data,
            timestamp=timestamp,
        )

        logger.info(f"Created snapshot {snapshot_id} at sequence {sequence_number}")
        return snapshot

    def _insert_snapshot(
        self,
        snapshot_id: str,
        sequence_number: int,
        state_json: str,
        timestamp: datetime,
    ) -> None:
        """Insert snapshot into database."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        self._connection.execute(
            """
            INSERT OR REPLACE INTO snapshots
            (snapshot_id, sequence_number, state_data, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                snapshot_id,
                sequence_number,
                state_json,
                timestamp.isoformat(),
                time.time(),
            ),
        )
        self._connection.commit()

    async def get_latest_snapshot(self) -> Optional[Snapshot]:
        """
        Get the latest snapshot.

        Returns:
            Latest Snapshot object or None if no snapshots exist
        """
        if not self._initialized:
            await self.initialize()

        row = await asyncio.get_event_loop().run_in_executor(None, self._get_latest_snapshot_row)

        if not row:
            return None

        snapshot_id, sequence_number, state_json, timestamp_str = row

        try:
            state_data = json.loads(state_json)
            timestamp = datetime.fromisoformat(timestamp_str)

            return Snapshot(
                snapshot_id=snapshot_id,
                sequence_number=sequence_number,
                state_data=state_data,
                timestamp=timestamp,
            )
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Error deserializing snapshot {snapshot_id}: {e}")
            return None

    def _get_latest_snapshot_row(self) -> Optional[tuple]:
        """Get the latest snapshot row from database."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        cursor = self._connection.execute(
            """
            SELECT snapshot_id, sequence_number, state_data, timestamp
            FROM snapshots
            ORDER BY sequence_number DESC
            LIMIT 1
            """
        )
        return cursor.fetchone()

    async def compact_events(self, keep_from_sequence: int) -> Dict[str, Any]:
        """
        Compact events by removing events older than the specified sequence number.

        This should typically be called after creating a snapshot to remove
        events that are no longer needed for replay.

        Args:
            keep_from_sequence: Keep events from this sequence number onwards

        Returns:
            Dictionary with compaction statistics
        """
        if not self._initialized:
            await self.initialize()

        # Get counts before compaction
        total_events_before = await self.get_event_count()

        # Perform compaction
        async with self._lock:
            (
                events_removed,
                db_size_before,
                db_size_after,
            ) = await asyncio.get_event_loop().run_in_executor(
                None, self._delete_old_events_with_size, keep_from_sequence
            )

        # Get counts after compaction
        total_events_after = await self.get_event_count()

        # Calculate space savings
        space_saved_bytes = db_size_before - db_size_after
        space_saved_percent = (
            (space_saved_bytes / db_size_before * 100) if db_size_before > 0 else 0
        )

        stats = {
            "events_removed": events_removed,
            "events_before": total_events_before,
            "events_after": total_events_after,
            "db_size_before_bytes": db_size_before,
            "db_size_after_bytes": db_size_after,
            "space_saved_bytes": space_saved_bytes,
            "space_saved_percent": space_saved_percent,
        }

        logger.info(
            f"Compaction completed: removed {events_removed} events, "
            f"saved {space_saved_bytes} bytes ({space_saved_percent:.1f}%)"
        )

        return stats

    def _delete_old_events_with_size(self, keep_from_sequence: int) -> tuple[int, int, int]:
        """Delete events older than the specified sequence number and return size info."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        # Get size before deletion
        db_size_before = self._get_database_file_size()

        # Delete events in a transaction
        cursor = self._connection.execute(
            "DELETE FROM events WHERE sequence_number < ?", (keep_from_sequence,)
        )

        events_removed = cursor.rowcount
        self._connection.commit()

        # Run VACUUM outside of transaction
        self._connection.isolation_level = None  # autocommit mode
        try:
            self._connection.execute("VACUUM")
        finally:
            self._connection.isolation_level = "IMMEDIATE"  # restore transaction mode

        # Get size after vacuum
        db_size_after = self._get_database_file_size()

        return events_removed, db_size_before, db_size_after

    def _get_database_file_size(self) -> int:
        """Get the current database file size in bytes."""
        if self.db_path == ":memory:":
            # For in-memory databases, return 0 as size calculation isn't meaningful
            return 0

        try:
            db_path = Path(self.db_path)
            if db_path.exists():
                return db_path.stat().st_size
        except Exception as e:
            logger.warning(f"Could not get database size: {e}")

        return 0

    async def _get_database_size(self) -> int:
        """Get the current database size in bytes."""
        return self._get_database_file_size()

    async def cleanup_old_snapshots(self, keep_count: int = 5) -> int:
        """
        Clean up old snapshots, keeping only the most recent ones.

        Args:
            keep_count: Number of recent snapshots to keep

        Returns:
            Number of snapshots removed
        """
        if not self._initialized:
            await self.initialize()

        async with self._lock:
            removed_count = await asyncio.get_event_loop().run_in_executor(
                None, self._delete_old_snapshots, keep_count
            )

        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old snapshots")

        return removed_count

    def _delete_old_snapshots(self, keep_count: int) -> int:
        """Delete old snapshots, keeping only the most recent ones."""
        if not self._connection:
            raise RuntimeError("EventStore not initialized")

        # Get snapshots to delete (all except the most recent keep_count)
        cursor = self._connection.execute(
            """
            SELECT snapshot_id FROM snapshots
            ORDER BY sequence_number DESC
            LIMIT -1 OFFSET ?
            """,
            (keep_count,),
        )

        snapshots_to_delete = [row[0] for row in cursor.fetchall()]

        if not snapshots_to_delete:
            return 0

        # Delete old snapshots
        placeholders = ",".join("?" * len(snapshots_to_delete))
        cursor = self._connection.execute(
            f"DELETE FROM snapshots WHERE snapshot_id IN ({placeholders})",
            snapshots_to_delete,
        )

        removed_count = cursor.rowcount
        self._connection.commit()

        return removed_count
