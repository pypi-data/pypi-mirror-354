"""Tests for trading strategies."""

from datetime import datetime

from eoms.strategies.base import (
    BaseStrategy,
    PriceUpdate,
    SampleStrategy,
    StrategyEvent,
    StrategyStatus,
)


class TestStrategyStatus:
    """Test StrategyStatus enum."""

    def test_strategy_status_values(self):
        """Test strategy status enum values."""
        assert StrategyStatus.STOPPED.value == "stopped"
        assert StrategyStatus.STARTING.value == "starting"
        assert StrategyStatus.RUNNING.value == "running"
        assert StrategyStatus.STOPPING.value == "stopping"
        assert StrategyStatus.ERROR.value == "error"


class TestStrategyEvent:
    """Test StrategyEvent dataclass."""

    def test_strategy_event_creation(self):
        """Test strategy event creation."""
        timestamp = datetime.now()
        event = StrategyEvent(
            strategy_name="TestStrategy",
            status=StrategyStatus.RUNNING,
            timestamp=timestamp,
            message="Test message",
        )

        assert event.strategy_name == "TestStrategy"
        assert event.status == StrategyStatus.RUNNING
        assert event.timestamp == timestamp
        assert event.message == "Test message"
        assert event.data is None


class TestPriceUpdate:
    """Test PriceUpdate dataclass."""

    def test_price_update_creation(self):
        """Test price update creation."""
        timestamp = datetime.now()
        update = PriceUpdate(symbol="AAPL", price=150.25, timestamp=timestamp, volume=1000.0)

        assert update.symbol == "AAPL"
        assert update.price == 150.25
        assert update.timestamp == timestamp
        assert update.volume == 1000.0


class TestSampleStrategy:
    """Test SampleStrategy implementation."""

    def test_sample_strategy_creation(self):
        """Test sample strategy creation."""
        strategy = SampleStrategy()

        assert strategy.name == "SampleStrategy"
        assert strategy.status == StrategyStatus.STOPPED
        assert strategy.config == {}
        assert strategy.last_price is None
        assert strategy.signal_count == 0

    def test_sample_strategy_with_config(self):
        """Test sample strategy with custom config."""
        config = {"param1": "value1", "param2": 42}
        strategy = SampleStrategy("CustomSample", config)

        assert strategy.name == "CustomSample"
        assert strategy.config == config

    def test_strategy_initialization(self):
        """Test strategy initialization."""
        strategy = SampleStrategy()

        result = strategy.initialize()

        assert result is True
        assert strategy.status == StrategyStatus.STOPPED

    def test_strategy_start_stop_cycle(self):
        """Test strategy start/stop cycle."""
        strategy = SampleStrategy()
        strategy.initialize()

        # Test start
        result = strategy.start()
        assert result is True
        assert strategy.status == StrategyStatus.RUNNING

        # Test stop
        result = strategy.stop()
        assert result is True
        assert strategy.status == StrategyStatus.STOPPED

    def test_strategy_event_callback(self):
        """Test strategy event callback mechanism."""
        strategy = SampleStrategy()
        events = []

        def event_callback(event):
            events.append(event)

        strategy.set_event_callback(event_callback)
        strategy.initialize()

        # Should have received initialization event
        assert len(events) == 1
        assert events[0].strategy_name == "SampleStrategy"
        assert events[0].status == StrategyStatus.STOPPED
        assert "initialized" in events[0].message.lower()

    def test_strategy_price_update_handling(self):
        """Test strategy price update handling."""
        strategy = SampleStrategy()
        strategy.initialize()
        strategy.start()

        events = []
        strategy.set_event_callback(lambda e: events.append(e))

        # Send price updates
        for i in range(15):  # Should trigger signal on 10th update
            price_update = PriceUpdate(symbol="AAPL", price=150.0 + i, timestamp=datetime.now())
            strategy.on_price_update(price_update)

        assert strategy.signal_count == 15
        assert strategy.last_price == 164.0  # 150 + 14

        # Should have generated signal on 10th update
        signal_events = [e for e in events if e.message and "signal" in e.message.lower()]
        assert len(signal_events) >= 1

    def test_strategy_get_info(self):
        """Test strategy info retrieval."""
        config = {"test": "value"}
        strategy = SampleStrategy("TestStrategy", config)
        strategy.initialize()
        strategy.start()

        info = strategy.get_info()

        assert info["name"] == "TestStrategy"
        assert info["status"] == "running"
        assert info["config"] == config

    def test_strategy_error_handling_in_callback(self):
        """Test strategy handles callback errors gracefully."""
        strategy = SampleStrategy()

        def failing_callback(event):
            raise Exception("Callback error")

        strategy.set_event_callback(failing_callback)

        # This should not raise an exception
        strategy.initialize()
        assert strategy.status == StrategyStatus.STOPPED


class ConcreteStrategy(BaseStrategy):
    """Concrete strategy for testing BaseStrategy."""

    def __init__(self, name="TestStrategy", config=None):
        super().__init__(name, config)
        self.initialized = False
        self.started = False

    def initialize(self) -> bool:
        self.initialized = True
        return True

    def start(self) -> bool:
        if not self.initialized:
            return False
        self.started = True
        self.status = StrategyStatus.RUNNING
        return True

    def stop(self) -> bool:
        self.started = False
        self.status = StrategyStatus.STOPPED
        return True

    def on_price_update(self, price_update: PriceUpdate) -> None:
        pass


class TestBaseStrategy:
    """Test BaseStrategy abstract class."""

    def test_base_strategy_creation(self):
        """Test base strategy creation."""
        strategy = ConcreteStrategy("TestStrategy", {"param": "value"})

        assert strategy.name == "TestStrategy"
        assert strategy.config == {"param": "value"}
        assert strategy.status == StrategyStatus.STOPPED

    def test_base_strategy_event_emission(self):
        """Test base strategy event emission."""
        strategy = ConcreteStrategy()
        events = []

        strategy.set_event_callback(lambda e: events.append(e))
        strategy._emit_event(StrategyStatus.RUNNING, "Test message", {"key": "value"})

        assert len(events) == 1
        event = events[0]
        assert event.strategy_name == "TestStrategy"
        assert event.status == StrategyStatus.RUNNING
        assert event.message == "Test message"
        assert event.data == {"key": "value"}

    def test_base_strategy_lifecycle(self):
        """Test base strategy lifecycle."""
        strategy = ConcreteStrategy()

        # Initial state
        assert not strategy.initialized
        assert not strategy.started
        assert strategy.status == StrategyStatus.STOPPED

        # Initialize
        result = strategy.initialize()
        assert result is True
        assert strategy.initialized

        # Start
        result = strategy.start()
        assert result is True
        assert strategy.started
        assert strategy.status == StrategyStatus.RUNNING

        # Stop
        result = strategy.stop()
        assert result is True
        assert not strategy.started
        assert strategy.status == StrategyStatus.STOPPED
