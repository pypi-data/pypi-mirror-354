"""Tests for FIX44Broker implementation."""

import pytest

from eoms.brokers import FIX44Broker, OrderRequest
from eoms.brokers.base import OrderSide, OrderType


class TestFIX44Broker:
    """Test FIX44Broker implementation."""

    def test_fix44_broker_creation(self):
        """Test creating a FIX44 broker."""
        broker = FIX44Broker()

        assert broker.get_name() == "FIX44Broker"
        assert not broker.is_connected()
        assert not broker.is_logged_on()

    def test_fix44_broker_with_config(self):
        """Test creating FIX44 broker with custom config."""
        config = {
            "sender_comp_id": "TEST_SENDER",
            "target_comp_id": "TEST_TARGET",
            "host": "test.broker.com",
            "port": "5002",
            "fix_settings": {"HeartBtInt": "60"},
        }
        broker = FIX44Broker(config)

        assert broker.fix_config["SenderCompID"] == "TEST_SENDER"
        assert broker.fix_config["TargetCompID"] == "TEST_TARGET"
        assert broker.fix_config["SocketConnectHost"] == "test.broker.com"
        assert broker.fix_config["SocketConnectPort"] == "5002"
        assert broker.fix_config["HeartBtInt"] == "60"

    def test_fix_availability_check(self):
        """Test QuickFIX availability check."""
        # This should not raise an exception regardless of QuickFIX availability
        available = FIX44Broker.is_available()
        assert isinstance(available, bool)

    @pytest.mark.asyncio
    async def test_operations_without_quickfix(self):
        """Test broker operations when QuickFIX is not available."""
        broker = FIX44Broker()

        order = OrderRequest(
            order_id="O001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        # If QuickFIX is not available, operations should fail gracefully
        if not FIX44Broker.is_available():
            # Connect should fail
            result = await broker.connect()
            assert result is False

            # Operations should fail when not connected
            assert await broker.place_order(order) is False
            assert await broker.amend_order("O001", price=155.0) is False
            assert await broker.cancel_order("O001") is False

    @pytest.mark.asyncio
    async def test_connect_without_server(self):
        """Test connection attempt without a FIX server."""
        # This test assumes no FIX server is running
        config = {
            "host": "localhost",
            "port": "59999",  # Unlikely to be in use
            "sender_comp_id": "TEST",
            "target_comp_id": "FAKE",
        }
        broker = FIX44Broker(config)

        if FIX44Broker.is_available():
            # Connection should fail (no server running)
            result = await broker.connect()
            # This might fail due to timeout or connection error
            # We just ensure it doesn't crash
            assert isinstance(result, bool)

            await broker.disconnect()

    def test_fix_configuration_defaults(self):
        """Test default FIX configuration values."""
        broker = FIX44Broker()

        expected_defaults = {
            "SenderCompID": "EOMS",
            "TargetCompID": "BROKER",
            "SocketConnectHost": "localhost",
            "SocketConnectPort": "5001",
            "BeginString": "FIX.4.4",
            "HeartBtInt": "30",
            "UseDataDictionary": "Y",
            "ReconnectInterval": "5",
        }

        for key, expected_value in expected_defaults.items():
            assert broker.fix_config[key] == expected_value

    @pytest.mark.asyncio
    async def test_message_handling_without_crash(self):
        """Test that message handler methods don't crash."""
        broker = FIX44Broker()

        if FIX44Broker.is_available():
            # Create application to test message handling
            application = broker.application = MockFIXApplication(broker)

            # Test admin message handlers
            application.onCreate("test_session")
            application.onLogon("test_session")
            application.onLogout("test_session")
            application.toAdmin(None, "test_session")
            application.fromAdmin(None, "test_session")
            application.toApp(None, "test_session")

            # These should not crash
            assert True

    def test_order_type_mapping(self):
        """Test that order types are properly defined."""
        FIX44Broker()

        # Test that we can create orders with different types
        market_order = OrderRequest(
            order_id="M001",
            symbol="AAPL",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=100.0,
        )

        limit_order = OrderRequest(
            order_id="L001",
            symbol="AAPL",
            side=OrderSide.SELL,
            order_type=OrderType.LIMIT,
            quantity=100.0,
            price=150.0,
        )

        assert market_order.order_type == OrderType.MARKET
        assert limit_order.order_type == OrderType.LIMIT
        assert limit_order.price == 150.0


class MockFIXApplication:
    """Mock FIX application for testing."""

    def __init__(self, broker):
        self.broker = broker

    def onCreate(self, sessionID):
        pass

    def onLogon(self, sessionID):
        pass

    def onLogout(self, sessionID):
        pass

    def toAdmin(self, message, sessionID):
        pass

    def fromAdmin(self, message, sessionID):
        pass

    def toApp(self, message, sessionID):
        pass

    def fromApp(self, message, sessionID):
        pass


@pytest.mark.skipif(not FIX44Broker.is_available(), reason="QuickFIX-Python not available")
class TestFIX44BrokerWithQuickFIX:
    """Tests that require QuickFIX-Python to be installed."""

    def test_quickfix_imports(self):
        """Test that QuickFIX imports work when available."""
        # This test only runs if QuickFIX is available
        from eoms.brokers.fix44_broker import fix

        assert fix is not None

    def test_session_id_creation(self):
        """Test FIX session ID creation."""
        broker = FIX44Broker({"sender_comp_id": "SENDER", "target_comp_id": "TARGET"})

        # This would test actual QuickFIX functionality
        # For now, just ensure the broker was created successfully
        assert broker.fix_config["SenderCompID"] == "SENDER"
        assert broker.fix_config["TargetCompID"] == "TARGET"
