"""Tests for Algo Manager and PNL Window widgets."""

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

# Skip all tests if PySide6 is not available
pytest_plugins = []

try:
    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication

    from eoms.brokers.sim_broker import SimBroker
    from eoms.gui.widgets.algo_manager import AlgoManagerWidget, StrategyTableModel
    from eoms.gui.widgets.pnl_window import (
        PnlSummaryModel,
        PNLWindowWidget,
        SimpleChart,
    )
    from eoms.strategies.base import SampleStrategy, StrategyEvent, StrategyStatus

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False


@pytest.mark.skipif(not PYSIDE6_AVAILABLE, reason="PySide6 not available")
class TestStrategyTableModel:
    """Test StrategyTableModel functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def model(self, app):
        """Create StrategyTableModel for testing."""
        return StrategyTableModel()

    def test_model_creation(self, model):
        """Test model creation."""
        assert model.rowCount() == 0
        assert model.columnCount() == 4

    def test_add_strategy(self, model):
        """Test adding strategy to model."""
        strategy = SampleStrategy("TestStrategy")
        model.add_strategy(strategy, "test.py")

        assert model.rowCount() == 1
        assert model.strategies[0] == strategy
        assert model.strategy_files["TestStrategy"] == "test.py"

    def test_remove_strategy(self, model):
        """Test removing strategy from model."""
        strategy = SampleStrategy("TestStrategy")
        model.add_strategy(strategy, "test.py")
        model.remove_strategy(0)

        assert model.rowCount() == 0
        assert "TestStrategy" not in model.strategy_files

    def test_update_strategy_event(self, model):
        """Test updating strategy event."""
        strategy = SampleStrategy("TestStrategy")
        model.add_strategy(strategy, "test.py")
        model.update_strategy_event("TestStrategy", "New event")

        assert model.last_events["TestStrategy"] == "New event"


@pytest.mark.skipif(not PYSIDE6_AVAILABLE, reason="PySide6 not available")
class TestAlgoManagerWidget:
    """Test AlgoManagerWidget functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def widget(self, app):
        """Create AlgoManagerWidget for testing."""
        with patch.object(QTimer, "start"):  # Prevent timer from starting
            widget = AlgoManagerWidget()
        return widget

    def test_widget_creation(self, widget):
        """Test widget creation."""
        assert widget.strategy_model is not None
        assert isinstance(widget.loaded_strategies, dict)
        assert len(widget.loaded_strategies) == 1  # Sample strategy

    def test_load_sample_strategy(self, widget):
        """Test loading sample strategy."""
        # Sample strategy should be loaded by default
        assert "SampleStrategy" in widget.loaded_strategies
        strategy = widget.loaded_strategies["SampleStrategy"]
        assert isinstance(strategy, SampleStrategy)
        assert strategy.status == StrategyStatus.STOPPED

    def test_strategy_event_handling(self, widget):
        """Test strategy event handling."""
        event = StrategyEvent(
            strategy_name="TestStrategy",
            status=StrategyStatus.RUNNING,
            timestamp=datetime.now(),
            message="Test message",
        )

        widget.on_strategy_event(event)

        # Check if event was logged
        log_text = widget.event_log.toPlainText()
        assert "TestStrategy" in log_text
        assert "running" in log_text.lower()

    def test_get_running_strategies(self, widget):
        """Test getting running strategies."""
        # Initially no running strategies
        running = widget.get_running_strategies()
        assert len(running) == 0

        # Start sample strategy
        strategy = widget.loaded_strategies["SampleStrategy"]
        strategy.start()

        running = widget.get_running_strategies()
        assert len(running) == 1
        assert running[0] == strategy

    def test_stop_all_strategies(self, widget):
        """Test stopping all strategies."""
        # Start sample strategy
        strategy = widget.loaded_strategies["SampleStrategy"]
        strategy.start()
        assert strategy.status == StrategyStatus.RUNNING

        # Stop all
        widget.stop_all_strategies()
        assert strategy.status == StrategyStatus.STOPPED


@pytest.mark.skipif(not PYSIDE6_AVAILABLE, reason="PySide6 not available")
class TestPnlSummaryModel:
    """Test PnlSummaryModel functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def model(self, app):
        """Create PnlSummaryModel for testing."""
        return PnlSummaryModel()

    def test_model_creation(self, model):
        """Test model creation."""
        assert model.rowCount() == 0
        assert model.columnCount() == 8

    def test_update_symbol_pnl(self, model):
        """Test updating symbol P&L data."""
        data = {
            "position": 100.0,
            "avg_price": 150.0,
            "market_price": 155.0,
            "market_value": 15500.0,
            "realized_pnl": 250.0,
            "unrealized_pnl": 500.0,
        }

        model.update_symbol_pnl("AAPL", data)

        assert model.rowCount() == 1
        assert "AAPL" in model.pnl_data
        assert model.pnl_data["AAPL"] == data

    def test_clear_data(self, model):
        """Test clearing P&L data."""
        data = {"position": 100.0, "realized_pnl": 250.0}
        model.update_symbol_pnl("AAPL", data)

        model.clear_data()

        assert model.rowCount() == 0
        assert len(model.pnl_data) == 0


@pytest.mark.skipif(not PYSIDE6_AVAILABLE, reason="PySide6 not available")
class TestPNLWindowWidget:
    """Test PNLWindowWidget functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def broker(self):
        """Create mock broker."""
        broker = Mock(spec=SimBroker)
        broker.get_fill_history.return_value = []
        broker.get_market_price.return_value = 150.0
        return broker

    @pytest.fixture
    def widget(self, app, broker):
        """Create PNLWindowWidget for testing."""
        with patch.object(QTimer, "start"):  # Prevent timer from starting
            widget = PNLWindowWidget(broker)
        return widget

    def test_widget_creation(self, widget):
        """Test widget creation."""
        assert widget.broker is not None
        assert isinstance(widget.pnl_history, list)
        assert isinstance(widget.positions, dict)
        assert isinstance(widget.avg_prices, dict)
        assert isinstance(widget.realized_pnl, dict)

    def test_set_broker(self, widget):
        """Test setting broker."""
        new_broker = Mock()
        widget.set_broker(new_broker)
        assert widget.broker == new_broker

    def test_reset_pnl(self, widget):
        """Test resetting P&L calculations."""
        # Add some test data
        widget.positions["AAPL"] = 100.0
        widget.avg_prices["AAPL"] = 150.0
        widget.realized_pnl["AAPL"] = 250.0

        widget.reset_pnl()

        assert len(widget.positions) == 0
        assert len(widget.avg_prices) == 0
        assert len(widget.realized_pnl) == 0
        assert len(widget.pnl_history) == 0

    def test_get_market_price(self, widget):
        """Test getting market price."""
        price = widget.get_market_price("AAPL")
        assert price == 150.0

        # Test fallback to avg price when broker not available
        widget.avg_prices["MSFT"] = 300.0
        widget.broker = None
        price = widget.get_market_price("MSFT")
        assert price == 300.0

    def test_process_fills_empty(self, widget):
        """Test processing empty fills list."""
        widget.process_fills([])

        assert len(widget.positions) == 0
        assert len(widget.avg_prices) == 0
        assert len(widget.realized_pnl) == 0


@pytest.mark.skipif(not PYSIDE6_AVAILABLE, reason="PySide6 not available")
class TestSimpleChart:
    """Test SimpleChart functionality."""

    @pytest.fixture
    def app(self):
        """Create QApplication for testing."""
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        return app

    @pytest.fixture
    def chart(self, app):
        """Create SimpleChart for testing."""
        return SimpleChart()

    def test_chart_creation(self, chart):
        """Test chart creation."""
        assert len(chart.data_points) == 0

    def test_add_data_point(self, chart):
        """Test adding data points."""
        timestamp = datetime.now()
        chart.add_data_point(timestamp, 100.0)

        assert len(chart.data_points) == 1
        assert chart.data_points[0] == (timestamp, 100.0)

    def test_clear_data(self, chart):
        """Test clearing chart data."""
        chart.add_data_point(datetime.now(), 100.0)
        chart.clear_data()

        assert len(chart.data_points) == 0

    def test_data_point_limit(self, chart):
        """Test data point limit."""
        # Add more than 100 points
        for i in range(150):
            chart.add_data_point(datetime.now(), float(i))

        # Should only keep last 100
        assert len(chart.data_points) == 100
        assert chart.data_points[-1][1] == 149.0


# Test module-level functionality without GUI dependencies
class TestModuleFunctionality:
    """Test functionality that doesn't require GUI."""

    def test_strategy_imports(self):
        """Test strategy module imports work."""
        from eoms.strategies.base import BaseStrategy, SampleStrategy, StrategyStatus

        assert BaseStrategy is not None
        assert SampleStrategy is not None
        assert StrategyStatus is not None

    def test_sample_strategy_creation_no_gui(self):
        """Test sample strategy creation without GUI."""
        from eoms.strategies.base import SampleStrategy, StrategyStatus

        strategy = SampleStrategy()
        assert strategy.name == "SampleStrategy"
        assert strategy.status == StrategyStatus.STOPPED

        # Test basic lifecycle
        assert strategy.initialize() is True
        assert strategy.start() is True
        assert strategy.status == StrategyStatus.RUNNING
        assert strategy.stop() is True
        assert strategy.status == StrategyStatus.STOPPED
