"""Prometheus metrics exporter for EOMS.

This module provides comprehensive metrics collection and Prometheus endpoint
for monitoring trading system performance, latency, and P&L in real-time.
"""

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from threading import Lock
from typing import Optional

try:
    from prometheus_client import (
        CollectorRegistry,
        Counter,
        Gauge,
        Histogram,
        Info,
        generate_latest,
        start_http_server,
    )

    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

__all__ = [
    "MetricsConfig",
    "EOSMetricsCollector",
    "get_metrics_collector",
    "MetricsServer",
    "latency_timer",
]


@dataclass
class MetricsConfig:
    """Configuration for EOMS metrics collection."""

    enabled: bool = True
    port: int = 9090
    host: str = "0.0.0.0"
    service_name: str = "eoms"
    environment: str = "development"
    export_interval: float = 15.0  # seconds

    # Histogram buckets for latency measurements (in seconds)
    latency_buckets: tuple = field(
        default_factory=lambda: (
            0.001,
            0.005,
            0.01,
            0.025,
            0.05,
            0.1,
            0.25,
            0.5,
            1.0,
            2.5,
            5.0,
            float("inf"),
        )
    )


class EOSMetricsCollector:
    """Central metrics collector for EOMS trading system."""

    def __init__(self, config: Optional[MetricsConfig] = None):
        """Initialize metrics collector.

        Args:
            config: Metrics configuration. Uses defaults if None.
        """
        self.config = config or MetricsConfig()
        self.logger = logging.getLogger(__name__)
        self._lock = Lock()

        if not PROMETHEUS_AVAILABLE:
            self.logger.warning("Prometheus client not available - metrics disabled")
            self.config.enabled = False
            return

        if not self.config.enabled:
            self.logger.info("Metrics collection disabled")
            return

        # Create custom registry
        self.registry = CollectorRegistry()

        # System info
        self.system_info = Info(
            "eoms_system_info", "EOMS system information", registry=self.registry
        )
        self.system_info.info(
            {
                "service": self.config.service_name,
                "environment": self.config.environment,
                "version": "1.0.0",  # TODO: Get from package
            }
        )

        # Order metrics
        self.orders_total = Counter(
            "eoms_orders_total",
            "Total number of orders by status",
            ["status", "symbol", "side"],
            registry=self.registry,
        )

        self.order_latency = Histogram(
            "eoms_order_latency_seconds",
            "Order processing latency from request to acknowledgment",
            ["operation", "symbol"],
            buckets=self.config.latency_buckets,
            registry=self.registry,
        )

        # Fill metrics
        self.fills_total = Counter(
            "eoms_fills_total",
            "Total number of fills",
            ["symbol", "side"],
            registry=self.registry,
        )

        self.fill_volume = Counter(
            "eoms_fill_volume_total",
            "Total fill volume",
            ["symbol", "side"],
            registry=self.registry,
        )

        # P&L metrics
        self.pnl_realized = Gauge(
            "eoms_pnl_realized_total",
            "Realized P&L by symbol",
            ["symbol"],
            registry=self.registry,
        )

        self.pnl_unrealized = Gauge(
            "eoms_pnl_unrealized_total",
            "Unrealized P&L by symbol",
            ["symbol"],
            registry=self.registry,
        )

        self.positions = Gauge(
            "eoms_positions_current",
            "Current positions by symbol",
            ["symbol"],
            registry=self.registry,
        )

        # System performance metrics
        self.event_bus_messages = Counter(
            "eoms_event_bus_messages_total",
            "Total messages processed by event bus",
            ["topic", "status"],
            registry=self.registry,
        )

        self.event_bus_latency = Histogram(
            "eoms_event_bus_latency_seconds",
            "Event bus message processing latency",
            ["topic"],
            buckets=self.config.latency_buckets,
            registry=self.registry,
        )

        # Strategy metrics
        self.strategies_active = Gauge(
            "eoms_strategies_active",
            "Number of active strategies",
            registry=self.registry,
        )

        self.strategy_pnl = Gauge(
            "eoms_strategy_pnl_total",
            "P&L by strategy",
            ["strategy_id", "symbol"],
            registry=self.registry,
        )

        # Connection metrics
        self.connections_active = Gauge(
            "eoms_connections_active",
            "Active connections to external services",
            ["service_type", "endpoint"],
            registry=self.registry,
        )

        self.connection_errors = Counter(
            "eoms_connection_errors_total",
            "Connection errors by service",
            ["service_type", "endpoint", "error_type"],
            registry=self.registry,
        )

        # Risk metrics
        self.risk_breaches = Counter(
            "eoms_risk_breaches_total",
            "Risk limit breaches",
            ["breach_type", "symbol"],
            registry=self.registry,
        )

        self.logger.info(f"Metrics collector initialized for {self.config.service_name}")

    def record_order(self, status: str, symbol: str, side: str) -> None:
        """Record order metric.

        Args:
            status: Order status (NEW, ACK, FILL, CANCEL, REJECT)
            symbol: Trading symbol
            side: Order side (BUY, SELL)
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.orders_total.labels(
                status=status.upper(), symbol=symbol.upper(), side=side.upper()
            ).inc()

    def record_order_latency(self, operation: str, symbol: str, latency_seconds: float) -> None:
        """Record order processing latency.

        Args:
            operation: Operation type (place, cancel, amend)
            symbol: Trading symbol
            latency_seconds: Latency in seconds
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.order_latency.labels(operation=operation.lower(), symbol=symbol.upper()).observe(
                latency_seconds
            )

    def record_fill(self, symbol: str, side: str, quantity: float) -> None:
        """Record fill event.

        Args:
            symbol: Trading symbol
            side: Fill side (BUY, SELL)
            quantity: Fill quantity
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.fills_total.labels(symbol=symbol.upper(), side=side.upper()).inc()

            self.fill_volume.labels(symbol=symbol.upper(), side=side.upper()).inc(abs(quantity))

    def update_pnl(self, symbol: str, realized_pnl: float, unrealized_pnl: float) -> None:
        """Update P&L metrics.

        Args:
            symbol: Trading symbol
            realized_pnl: Realized P&L
            unrealized_pnl: Unrealized P&L
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.pnl_realized.labels(symbol=symbol.upper()).set(realized_pnl)
            self.pnl_unrealized.labels(symbol=symbol.upper()).set(unrealized_pnl)

    def update_position(self, symbol: str, position: float) -> None:
        """Update position metric.

        Args:
            symbol: Trading symbol
            position: Current position (positive for long, negative for short)
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.positions.labels(symbol=symbol.upper()).set(position)

    def record_event_bus_message(self, topic: str, status: str = "processed") -> None:
        """Record event bus message.

        Args:
            topic: Message topic
            status: Processing status (processed, failed)
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.event_bus_messages.labels(topic=topic, status=status).inc()

    def record_event_bus_latency(self, topic: str, latency_seconds: float) -> None:
        """Record event bus processing latency.

        Args:
            topic: Message topic
            latency_seconds: Processing latency in seconds
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.event_bus_latency.labels(topic=topic).observe(latency_seconds)

    def update_active_strategies(self, count: int) -> None:
        """Update active strategies count.

        Args:
            count: Number of active strategies
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.strategies_active.set(count)

    def update_strategy_pnl(self, strategy_id: str, symbol: str, pnl: float) -> None:
        """Update strategy P&L.

        Args:
            strategy_id: Strategy identifier
            symbol: Trading symbol
            pnl: Strategy P&L for symbol
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.strategy_pnl.labels(strategy_id=strategy_id, symbol=symbol.upper()).set(pnl)

    def update_connection_status(self, service_type: str, endpoint: str, active: bool) -> None:
        """Update connection status.

        Args:
            service_type: Type of service (broker, feed, etc.)
            endpoint: Service endpoint
            active: Whether connection is active
        """
        if not self.config.enabled:
            return

        with self._lock:
            current_value = 1 if active else 0
            self.connections_active.labels(service_type=service_type, endpoint=endpoint).set(
                current_value
            )

    def record_connection_error(self, service_type: str, endpoint: str, error_type: str) -> None:
        """Record connection error.

        Args:
            service_type: Type of service (broker, feed, etc.)
            endpoint: Service endpoint
            error_type: Type of error (timeout, auth, network, etc.)
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.connection_errors.labels(
                service_type=service_type, endpoint=endpoint, error_type=error_type
            ).inc()

    def record_risk_breach(self, breach_type: str, symbol: str) -> None:
        """Record risk limit breach.

        Args:
            breach_type: Type of breach (position_limit, loss_limit, etc.)
            symbol: Trading symbol
        """
        if not self.config.enabled:
            return

        with self._lock:
            self.risk_breaches.labels(breach_type=breach_type, symbol=symbol.upper()).inc()

    def get_metrics(self) -> str:
        """Get metrics in Prometheus format.

        Returns:
            Metrics data in Prometheus format
        """
        if not self.config.enabled:
            return ""

        return generate_latest(self.registry).decode("utf-8")

    @contextmanager
    def timer(self, metric_name: str, **labels):
        """Context manager for timing operations.

        Args:
            metric_name: Name of the metric to update
            **labels: Metric labels

        Example:
            with metrics.timer('order_latency', operation='place', symbol='AAPL'):
                # Order placement code here
                pass
        """
        if not self.config.enabled:
            yield
            return

        start_time = time.time()
        try:
            yield
        finally:
            duration = time.time() - start_time

            # Find the appropriate metric
            if metric_name == "order_latency":
                self.record_order_latency(
                    labels.get("operation", "unknown"),
                    labels.get("symbol", "UNKNOWN"),
                    duration,
                )
            elif metric_name == "event_bus_latency":
                self.record_event_bus_latency(labels.get("topic", "unknown"), duration)


class MetricsServer:
    """HTTP server for Prometheus metrics endpoint."""

    def __init__(self, collector: EOSMetricsCollector):
        """Initialize metrics server.

        Args:
            collector: Metrics collector instance
        """
        self.collector = collector
        self.config = collector.config
        self.logger = logging.getLogger(__name__)
        self.server = None

    def start(self) -> bool:
        """Start the metrics HTTP server.

        Returns:
            True if server started successfully, False otherwise
        """
        if not self.config.enabled or not PROMETHEUS_AVAILABLE:
            self.logger.info("Metrics server disabled")
            return False

        try:
            # Start HTTP server with custom registry
            self.server = start_http_server(
                port=self.config.port,
                addr=self.config.host,
                registry=self.collector.registry,
            )

            self.logger.info(f"Metrics server started on {self.config.host}:{self.config.port}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start metrics server: {e}")
            return False

    def stop(self) -> None:
        """Stop the metrics server."""
        if self.server:
            try:
                self.server.shutdown()
                self.logger.info("Metrics server stopped")
            except Exception as e:
                self.logger.error(f"Error stopping metrics server: {e}")


# Global metrics collector instance
_metrics_collector: Optional[EOSMetricsCollector] = None


def get_metrics_collector(
    config: Optional[MetricsConfig] = None,
) -> EOSMetricsCollector:
    """Get the global metrics collector instance.

    Args:
        config: Metrics configuration (only used on first call)

    Returns:
        Global metrics collector instance
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = EOSMetricsCollector(config)

    return _metrics_collector


def latency_timer(operation: str, symbol: str = "UNKNOWN"):
    """Convenient timer decorator for measuring operation latency.

    Args:
        operation: Operation name
        symbol: Trading symbol

    Example:
        @latency_timer('order_placement', 'AAPL')
        def place_order():
            # Order placement code
            pass
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            metrics = get_metrics_collector()
            with metrics.timer("order_latency", operation=operation, symbol=symbol):
                return func(*args, **kwargs)

        return wrapper

    return decorator
