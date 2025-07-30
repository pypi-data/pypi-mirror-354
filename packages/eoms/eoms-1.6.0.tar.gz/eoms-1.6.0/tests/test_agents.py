"""Tests for EOMS agents."""

from datetime import datetime
from unittest.mock import Mock

import pytest

from eoms.agents.algo_agent import AlgoAgent
from eoms.agents.base import AgentStatus, BaseAgent
from eoms.agents.pnl_agent import PnlAgent, PnlSnapshot
from eoms.brokers.base import OrderSide
from eoms.core.eventbus import EventBus
from eoms.strategies.base import (
    PriceUpdate,
    SampleStrategy,
    StrategyStatus,
)


class ConcreteAgent(BaseAgent):
    """Concrete agent for testing BaseAgent."""

    def __init__(self, name: str, event_bus: EventBus, config=None):
        super().__init__(name, event_bus, config)
        self.events_processed = 0
        self.initialized = False
        self.cleaned_up = False

    async def initialize(self):
        self.initialized = True

    async def cleanup(self):
        self.cleaned_up = True

    async def process_event(self, topic: str, event):
        self.events_processed += 1

    def get_subscribed_topics(self):
        return ["test.topic"]


class TestBaseAgent:
    """Test BaseAgent functionality."""

    @pytest.fixture
    async def event_bus(self):
        """Create event bus for testing."""
        bus = EventBus()
        await bus.start()
        yield bus
        await bus.stop()

    @pytest.fixture
    def agent(self, event_bus):
        """Create test agent."""
        return ConcreteAgent("TestAgent", event_bus)

    @pytest.mark.asyncio
    async def test_agent_creation(self, agent):
        """Test agent creation."""
        assert agent.name == "TestAgent"
        assert not agent.is_running
        assert agent._status == "stopped"

    @pytest.mark.asyncio
    async def test_agent_start_stop(self, agent):
        """Test agent start/stop cycle."""
        # Start agent
        result = await agent.start()
        assert result is True
        assert agent.is_running
        assert agent._status == "running"
        assert agent.initialized

        # Stop agent
        result = await agent.stop()
        assert result is True
        assert not agent.is_running
        assert agent._status == "stopped"
        assert agent.cleaned_up

    @pytest.mark.asyncio
    async def test_agent_double_start(self, agent):
        """Test starting agent twice."""
        await agent.start()
        result = await agent.start()  # Second start should return False
        assert result is False
        await agent.stop()

    @pytest.mark.asyncio
    async def test_agent_stop_without_start(self, agent):
        """Test stopping agent without starting."""
        result = await agent.stop()
        assert result is False

    @pytest.mark.asyncio
    async def test_agent_status(self, agent):
        """Test agent status."""
        status = agent.get_status()
        assert isinstance(status, AgentStatus)
        assert status.name == "TestAgent"
        assert status.status == "stopped"

    @pytest.mark.asyncio
    async def test_agent_metrics(self, agent):
        """Test agent metrics."""
        metrics = await agent.get_metrics()
        assert "status" in metrics
        assert "uptime" in metrics


class TestAlgoAgent:
    """Test AlgoAgent functionality."""

    @pytest.fixture
    async def event_bus(self):
        """Create event bus for testing."""
        bus = EventBus()
        await bus.start()
        yield bus
        await bus.stop()

    @pytest.fixture
    def algo_agent(self, event_bus):
        """Create algo agent."""
        return AlgoAgent(event_bus)

    @pytest.mark.asyncio
    async def test_algo_agent_creation(self, algo_agent):
        """Test algo agent creation."""
        assert algo_agent.name == "ALGO"
        assert len(algo_agent.strategies) == 0
        assert len(algo_agent.strategy_metrics) == 0

    @pytest.mark.asyncio
    async def test_algo_agent_subscribed_topics(self, algo_agent):
        """Test subscribed topics."""
        topics = algo_agent.get_subscribed_topics()
        assert "price.update" in topics
        assert "algo.command" in topics
        assert "strategy.event" in topics

    @pytest.mark.asyncio
    async def test_algo_agent_start_stop(self, algo_agent):
        """Test algo agent start/stop."""
        result = await algo_agent.start()
        assert result is True
        assert algo_agent.is_running

        result = await algo_agent.stop()
        assert result is True
        assert not algo_agent.is_running

    @pytest.mark.asyncio
    async def test_price_update_handling(self, algo_agent):
        """Test price update handling."""
        await algo_agent.start()

        # Load a strategy
        await algo_agent._load_strategy("TestStrategy", SampleStrategy, {})
        await algo_agent._start_strategy("TestStrategy")

        # Send price update
        price_update = PriceUpdate(symbol="AAPL", price=150.0, timestamp=datetime.now())

        await algo_agent._handle_price_update(price_update)

        # Check metrics
        assert "TestStrategy" in algo_agent.strategy_metrics
        assert algo_agent.strategy_metrics["TestStrategy"]["price_updates_processed"] == 1

        await algo_agent.stop()

    @pytest.mark.asyncio
    async def test_algo_command_handling(self, algo_agent):
        """Test algorithm command handling."""
        await algo_agent.start()

        # Load strategy command
        load_command = {
            "action": "load",
            "strategy_name": "TestStrategy",
            "strategy_class": SampleStrategy,
            "config": {},
        }

        await algo_agent._handle_algo_command(load_command)
        assert "TestStrategy" in algo_agent.strategies

        # Start strategy command
        start_command = {"action": "start", "strategy_name": "TestStrategy"}

        await algo_agent._handle_algo_command(start_command)
        strategy = algo_agent.strategies["TestStrategy"]
        assert strategy.status == StrategyStatus.RUNNING

        # Stop strategy command
        stop_command = {"action": "stop", "strategy_name": "TestStrategy"}

        await algo_agent._handle_algo_command(stop_command)
        assert strategy.status == StrategyStatus.STOPPED

        await algo_agent.stop()

    @pytest.mark.asyncio
    async def test_get_loaded_strategies(self, algo_agent):
        """Test getting loaded strategies."""
        await algo_agent.start()

        # Initially empty
        strategies = algo_agent.get_loaded_strategies()
        assert len(strategies) == 0

        # Load a strategy
        await algo_agent._load_strategy("TestStrategy", SampleStrategy, {})
        strategies = algo_agent.get_loaded_strategies()
        assert len(strategies) == 1
        assert "TestStrategy" in strategies

        await algo_agent.stop()

    @pytest.mark.asyncio
    async def test_get_running_strategies(self, algo_agent):
        """Test getting running strategies."""
        await algo_agent.start()

        # Load and start strategy
        await algo_agent._load_strategy("TestStrategy", SampleStrategy, {})
        await algo_agent._start_strategy("TestStrategy")

        running = algo_agent.get_running_strategies()
        assert len(running) == 1
        assert "TestStrategy" in running

        await algo_agent.stop()


class TestPnlAgent:
    """Test PnlAgent functionality."""

    @pytest.fixture
    async def event_bus(self):
        """Create event bus for testing."""
        bus = EventBus()
        await bus.start()
        yield bus
        await bus.stop()

    @pytest.fixture
    def pnl_agent(self, event_bus):
        """Create PNL agent."""
        return PnlAgent(event_bus)

    @pytest.mark.asyncio
    async def test_pnl_agent_creation(self, pnl_agent):
        """Test PNL agent creation."""
        assert pnl_agent.name == "PNL"
        assert len(pnl_agent.positions) == 0
        assert len(pnl_agent.avg_prices) == 0
        assert len(pnl_agent.realized_pnl) == 0

    @pytest.mark.asyncio
    async def test_pnl_agent_subscribed_topics(self, pnl_agent):
        """Test subscribed topics."""
        topics = pnl_agent.get_subscribed_topics()
        assert "order.fill" in topics
        assert "price.update" in topics
        assert "position.snapshot" in topics

    @pytest.mark.asyncio
    async def test_position_update_from_fill(self, pnl_agent):
        """Test position update from fill."""
        # Buy 100 shares at $150
        pnl_agent._update_position_from_fill("AAPL", OrderSide.BUY, 100.0, 150.0)

        assert pnl_agent.positions["AAPL"] == 100.0
        assert pnl_agent.avg_prices["AAPL"] == 150.0
        assert pnl_agent.realized_pnl["AAPL"] == 0.0  # No realized P&L yet

    @pytest.mark.asyncio
    async def test_realized_pnl_calculation(self, pnl_agent):
        """Test realized P&L calculation."""
        # Buy 100 shares at $150
        pnl_agent._update_position_from_fill("AAPL", OrderSide.BUY, 100.0, 150.0)

        # Sell 50 shares at $160
        pnl_agent._update_position_from_fill("AAPL", OrderSide.SELL, 50.0, 160.0)

        assert pnl_agent.positions["AAPL"] == 50.0  # 50 shares left
        assert pnl_agent.realized_pnl["AAPL"] == 500.0  # 50 * (160 - 150) = $500

    @pytest.mark.asyncio
    async def test_unrealized_pnl_calculation(self, pnl_agent):
        """Test unrealized P&L calculation."""
        # Buy 100 shares at $150
        pnl_agent._update_position_from_fill("AAPL", OrderSide.BUY, 100.0, 150.0)

        # Update market price to $155
        pnl_agent.market_prices["AAPL"] = 155.0

        unrealized = pnl_agent._calculate_unrealized_pnl("AAPL")
        assert unrealized == 500.0  # 100 * (155 - 150) = $500

    @pytest.mark.asyncio
    async def test_price_update_handling(self, pnl_agent):
        """Test price update handling."""
        await pnl_agent.start()

        # Create mock price update
        price_update = Mock()
        price_update.symbol = "AAPL"
        price_update.price = 155.0

        await pnl_agent._handle_price_update(price_update)

        assert pnl_agent.market_prices["AAPL"] == 155.0
        assert pnl_agent.total_price_updates == 1

        await pnl_agent.stop()

    @pytest.mark.asyncio
    async def test_order_fill_handling(self, pnl_agent):
        """Test order fill handling."""
        await pnl_agent.start()

        # Create mock fill event
        fill_event = Mock()
        fill_event.symbol = "AAPL"
        fill_event.side = OrderSide.BUY
        fill_event.quantity = 100.0
        fill_event.price = 150.0

        await pnl_agent._handle_order_fill(fill_event)

        assert pnl_agent.positions["AAPL"] == 100.0
        assert pnl_agent.total_fills_processed == 1

        await pnl_agent.stop()

    @pytest.mark.asyncio
    async def test_pnl_summary(self, pnl_agent):
        """Test P&L summary."""
        # Add some positions
        pnl_agent._update_position_from_fill("AAPL", OrderSide.BUY, 100.0, 150.0)
        pnl_agent._update_position_from_fill("AAPL", OrderSide.SELL, 50.0, 160.0)
        pnl_agent.market_prices["AAPL"] = 155.0

        summary = pnl_agent.get_pnl_summary()

        assert summary["total_realized"] == 500.0  # From the sell
        assert summary["total_unrealized"] == 250.0  # 50 * (155 - 150)
        assert summary["total_pnl"] == 750.0
        assert "AAPL" in summary["positions"]

    @pytest.mark.asyncio
    async def test_metrics(self, pnl_agent):
        """Test agent metrics."""
        await pnl_agent.start()

        # Add some activity
        pnl_agent.total_fills_processed = 5
        pnl_agent.total_price_updates = 10
        pnl_agent._update_position_from_fill("AAPL", OrderSide.BUY, 100.0, 150.0)

        metrics = await pnl_agent.get_metrics()

        assert metrics["total_fills_processed"] == 5
        assert metrics["total_price_updates"] == 10
        assert metrics["symbols_tracked"] == 1
        assert "total_pnl" in metrics

        await pnl_agent.stop()


class TestPnlSnapshot:
    """Test PnlSnapshot data class."""

    def test_pnl_snapshot_creation(self):
        """Test PNL snapshot creation."""
        timestamp = datetime.now()
        snapshot = PnlSnapshot(
            timestamp=timestamp,
            symbol="AAPL",
            realized_pnl=500.0,
            unrealized_pnl=250.0,
            position=100.0,
            avg_price=150.0,
            market_price=152.5,
        )

        assert snapshot.timestamp == timestamp
        assert snapshot.symbol == "AAPL"
        assert snapshot.realized_pnl == 500.0
        assert snapshot.unrealized_pnl == 250.0
        assert snapshot.total_pnl == 750.0  # realized + unrealized
        assert snapshot.position == 100.0
        assert snapshot.avg_price == 150.0
        assert snapshot.market_price == 152.5
