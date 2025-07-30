"""Tests for Prometheus metrics exporter."""

import time
from unittest.mock import MagicMock, patch

import pytest

from eoms.core.metrics import (
    PROMETHEUS_AVAILABLE,
    EOSMetricsCollector,
    MetricsConfig,
    MetricsServer,
    get_metrics_collector,
    latency_timer,
)


@pytest.fixture
def metrics_config():
    """Create test metrics configuration."""
    return MetricsConfig(
        enabled=True,
        port=9091,  # Use different port for testing
        host="127.0.0.1",
        service_name="test_eoms",
        environment="test",
        export_interval=1.0,
    )


class TestMetricsConfig:
    """Test metrics configuration."""

    def test_default_config(self):
        """Test default configuration values."""
        config = MetricsConfig()

        assert config.enabled is True
        assert config.port == 9090
        assert config.host == "0.0.0.0"
        assert config.service_name == "eoms"
        assert config.environment == "development"
        assert config.export_interval == 15.0
        assert len(config.latency_buckets) > 0

    def test_custom_config(self):
        """Test custom configuration."""
        config = MetricsConfig(
            enabled=False,
            port=8080,
            host="localhost",
            service_name="custom_service",
            environment="production",
            export_interval=30.0,
        )

        assert config.enabled is False
        assert config.port == 8080
        assert config.host == "localhost"
        assert config.service_name == "custom_service"
        assert config.environment == "production"
        assert config.export_interval == 30.0


@pytest.mark.skipif(not PROMETHEUS_AVAILABLE, reason="Prometheus client not available")
class TestEOSMetricsCollector:
    """Test metrics collector."""

    def test_collector_initialization(self, metrics_config):
        """Test collector initialization."""
        collector = EOSMetricsCollector(metrics_config)

        assert collector.config == metrics_config
        assert collector.registry is not None

        # Check that metrics are initialized
        assert collector.orders_total is not None
        assert collector.order_latency is not None
        assert collector.pnl_realized is not None

    def test_collector_disabled(self):
        """Test collector with disabled metrics."""
        config = MetricsConfig(enabled=False)
        collector = EOSMetricsCollector(config)

        # Should work without errors even when disabled
        collector.record_order("NEW", "AAPL", "BUY")
        collector.record_fill("AAPL", "BUY", 100)
        collector.update_pnl("AAPL", 100.0, 50.0)

    def test_record_order(self, metrics_config):
        """Test order recording."""
        collector = EOSMetricsCollector(metrics_config)

        # Record some orders
        collector.record_order("NEW", "AAPL", "BUY")
        collector.record_order("ACK", "AAPL", "BUY")
        collector.record_order("FILL", "MSFT", "SELL")

        # Get metrics
        metrics_output = collector.get_metrics()

        assert "eoms_orders_total" in metrics_output
        assert 'status="NEW"' in metrics_output
        assert 'symbol="AAPL"' in metrics_output
        assert 'side="BUY"' in metrics_output

    def test_record_order_latency(self, metrics_config):
        """Test order latency recording."""
        collector = EOSMetricsCollector(metrics_config)

        collector.record_order_latency("place", "AAPL", 0.025)
        collector.record_order_latency("cancel", "MSFT", 0.010)

        metrics_output = collector.get_metrics()

        assert "eoms_order_latency_seconds" in metrics_output
        assert 'operation="place"' in metrics_output
        assert 'symbol="AAPL"' in metrics_output

    def test_record_fill(self, metrics_config):
        """Test fill recording."""
        collector = EOSMetricsCollector(metrics_config)

        collector.record_fill("AAPL", "BUY", 100)
        collector.record_fill("AAPL", "SELL", 50)

        metrics_output = collector.get_metrics()

        assert "eoms_fills_total" in metrics_output
        assert "eoms_fill_volume_total" in metrics_output
        assert 'symbol="AAPL"' in metrics_output
        assert 'side="BUY"' in metrics_output

    def test_update_pnl(self, metrics_config):
        """Test P&L updates."""
        collector = EOSMetricsCollector(metrics_config)

        collector.update_pnl("AAPL", 100.0, 50.0)
        collector.update_pnl("MSFT", -25.0, 75.0)

        metrics_output = collector.get_metrics()

        assert "eoms_pnl_realized_total" in metrics_output
        assert "eoms_pnl_unrealized_total" in metrics_output
        assert 'symbol="AAPL"' in metrics_output
        assert 'symbol="MSFT"' in metrics_output

    def test_update_position(self, metrics_config):
        """Test position updates."""
        collector = EOSMetricsCollector(metrics_config)

        collector.update_position("AAPL", 100)
        collector.update_position("MSFT", -50)

        metrics_output = collector.get_metrics()

        assert "eoms_positions_current" in metrics_output
        assert 'symbol="AAPL"' in metrics_output
        assert 'symbol="MSFT"' in metrics_output

    def test_event_bus_metrics(self, metrics_config):
        """Test event bus metrics."""
        collector = EOSMetricsCollector(metrics_config)

        collector.record_event_bus_message("orders", "processed")
        collector.record_event_bus_message("fills", "failed")
        collector.record_event_bus_latency("orders", 0.001)

        metrics_output = collector.get_metrics()

        assert "eoms_event_bus_messages_total" in metrics_output
        assert "eoms_event_bus_latency_seconds" in metrics_output
        assert 'topic="orders"' in metrics_output
        assert 'status="processed"' in metrics_output

    def test_strategy_metrics(self, metrics_config):
        """Test strategy metrics."""
        collector = EOSMetricsCollector(metrics_config)

        collector.update_active_strategies(3)
        collector.update_strategy_pnl("strategy1", "AAPL", 150.0)
        collector.update_strategy_pnl("strategy2", "MSFT", -25.0)

        metrics_output = collector.get_metrics()

        assert "eoms_strategies_active" in metrics_output
        assert "eoms_strategy_pnl_total" in metrics_output
        assert 'strategy_id="strategy1"' in metrics_output

    def test_connection_metrics(self, metrics_config):
        """Test connection metrics."""
        collector = EOSMetricsCollector(metrics_config)

        collector.update_connection_status("broker", "fix.example.com", True)
        collector.update_connection_status("feed", "ws.example.com", False)
        collector.record_connection_error("broker", "fix.example.com", "timeout")

        metrics_output = collector.get_metrics()

        assert "eoms_connections_active" in metrics_output
        assert "eoms_connection_errors_total" in metrics_output
        assert 'service_type="broker"' in metrics_output
        assert 'error_type="timeout"' in metrics_output

    def test_risk_metrics(self, metrics_config):
        """Test risk metrics."""
        collector = EOSMetricsCollector(metrics_config)

        collector.record_risk_breach("position_limit", "AAPL")
        collector.record_risk_breach("loss_limit", "MSFT")

        metrics_output = collector.get_metrics()

        assert "eoms_risk_breaches_total" in metrics_output
        assert 'breach_type="position_limit"' in metrics_output
        assert 'symbol="AAPL"' in metrics_output

    def test_timer_context_manager(self, metrics_config):
        """Test timer context manager."""
        collector = EOSMetricsCollector(metrics_config)

        with collector.timer("order_latency", operation="place", symbol="AAPL"):
            time.sleep(0.01)  # Simulate work

        metrics_output = collector.get_metrics()

        assert "eoms_order_latency_seconds" in metrics_output
        assert 'operation="place"' in metrics_output
        assert 'symbol="AAPL"' in metrics_output

    def test_timer_with_disabled_metrics(self):
        """Test timer works when metrics are disabled."""
        config = MetricsConfig(enabled=False)
        collector = EOSMetricsCollector(config)

        # Should not raise any errors
        with collector.timer("order_latency", operation="place", symbol="AAPL"):
            time.sleep(0.001)


@pytest.mark.skipif(not PROMETHEUS_AVAILABLE, reason="Prometheus client not available")
class TestMetricsServer:
    """Test metrics HTTP server."""

    def test_server_initialization(self, metrics_config):
        """Test server initialization."""
        collector = EOSMetricsCollector(metrics_config)
        server = MetricsServer(collector)

        assert server.collector == collector
        assert server.config == metrics_config

    @patch("eoms.core.metrics.start_http_server")
    def test_server_start(self, mock_start_server, metrics_config):
        """Test server start."""
        collector = EOSMetricsCollector(metrics_config)
        server = MetricsServer(collector)

        mock_start_server.return_value = MagicMock()

        result = server.start()

        assert result is True
        mock_start_server.assert_called_once_with(
            port=9091, addr="127.0.0.1", registry=collector.registry
        )

    @patch("eoms.core.metrics.start_http_server")
    def test_server_start_failure(self, mock_start_server, metrics_config):
        """Test server start failure."""
        collector = EOSMetricsCollector(metrics_config)
        server = MetricsServer(collector)

        mock_start_server.side_effect = Exception("Port in use")

        result = server.start()

        assert result is False

    def test_server_disabled(self):
        """Test server with disabled metrics."""
        config = MetricsConfig(enabled=False)
        collector = EOSMetricsCollector(config)
        server = MetricsServer(collector)

        result = server.start()

        assert result is False


class TestGlobalCollector:
    """Test global metrics collector functions."""

    def test_get_metrics_collector(self, metrics_config):
        """Test get_metrics_collector function."""
        # Reset global collector
        import eoms.core.metrics

        eoms.core.metrics._metrics_collector = None

        collector = get_metrics_collector(metrics_config)

        assert isinstance(collector, EOSMetricsCollector)
        assert collector.config.service_name == "test_eoms"

        # Should return same instance on subsequent calls
        collector2 = get_metrics_collector()
        assert collector is collector2

    @pytest.mark.skipif(not PROMETHEUS_AVAILABLE, reason="Prometheus client not available")
    def test_latency_timer_decorator(self, metrics_config):
        """Test latency timer decorator."""
        import eoms.core.metrics

        eoms.core.metrics._metrics_collector = EOSMetricsCollector(metrics_config)

        @latency_timer("order_placement", "AAPL")
        def mock_order_function():
            time.sleep(0.01)
            return "order_placed"

        result = mock_order_function()

        assert result == "order_placed"

        # Check that metrics were recorded
        collector = get_metrics_collector()
        metrics_output = collector.get_metrics()

        assert "eoms_order_latency_seconds" in metrics_output


class TestMetricsWithoutPrometheus:
    """Test metrics behavior when Prometheus is not available."""

    @patch("eoms.core.metrics.PROMETHEUS_AVAILABLE", False)
    def test_collector_without_prometheus(self):
        """Test collector when Prometheus is not available."""
        config = MetricsConfig()
        collector = EOSMetricsCollector(config)

        # Should be disabled
        assert not collector.config.enabled

        # Should work without errors
        collector.record_order("NEW", "AAPL", "BUY")
        collector.update_pnl("AAPL", 100.0, 50.0)

        # Should return empty metrics
        assert collector.get_metrics() == ""

    @patch("eoms.core.metrics.PROMETHEUS_AVAILABLE", False)
    def test_server_without_prometheus(self):
        """Test server when Prometheus is not available."""
        config = MetricsConfig()
        collector = EOSMetricsCollector(config)
        server = MetricsServer(collector)

        result = server.start()

        assert result is False
