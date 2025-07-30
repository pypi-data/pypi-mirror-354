"""Core framework components."""

from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    GlobalCircuitBreakerManager,
    global_circuit_breaker_manager,
)
from .eventbus import BackPressureError, EventBus
from .eventstore import Event, EventStore, Snapshot
from .recovery import RecoveryManager, StateRecoveryHandler
from .resilience import AutoReconnectMixin, ResilientBrokerBase
from .scheduler import SimpleScheduler, SnapshotJob

__all__ = [
    "EventBus",
    "BackPressureError",
    "EventStore",
    "Event",
    "Snapshot",
    "RecoveryManager",
    "StateRecoveryHandler",
    "SimpleScheduler",
    "SnapshotJob",
    "CircuitBreaker",
    "CircuitBreakerError",
    "GlobalCircuitBreakerManager",
    "global_circuit_breaker_manager",
    "AutoReconnectMixin",
    "ResilientBrokerBase",
]
