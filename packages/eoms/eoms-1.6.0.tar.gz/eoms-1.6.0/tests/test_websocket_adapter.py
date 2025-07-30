"""Tests for WebSocket feed adapter."""

import json

import pytest

from eoms.feeds import BinanceFeed, SubscriptionRequest, WebSocketFeedAdapter
from eoms.feeds.base import MarketDataType


class TestWebSocketFeedAdapter:
    """Test WebSocket feed adapter template."""

    def test_websocket_adapter_creation(self):
        """Test creating a WebSocket adapter."""
        adapter = WebSocketFeedAdapter()

        assert adapter.get_name() == "WebSocketFeed"
        assert not adapter.is_connected()
        assert adapter.ws_url == "wss://stream.binance.com:9443/ws"

    def test_websocket_adapter_with_config(self):
        """Test creating WebSocket adapter with custom config."""
        config = {
            "ws_url": "wss://custom.exchange.com/ws",
            "ping_interval": 60,
            "reconnect_delay": 10,
            "max_reconnect_attempts": 5,
        }
        adapter = WebSocketFeedAdapter(config)

        assert adapter.ws_url == "wss://custom.exchange.com/ws"
        assert adapter.ping_interval == 60
        assert adapter.reconnect_delay == 10
        assert adapter.max_reconnect_attempts == 5

    def test_websockets_availability_check(self):
        """Test websockets availability check."""
        # This should not raise an exception regardless of websockets availability
        available = WebSocketFeedAdapter.is_available()
        assert isinstance(available, bool)

    @pytest.mark.asyncio
    async def test_operations_without_websockets(self):
        """Test adapter operations when websockets is not available."""
        adapter = WebSocketFeedAdapter()

        request = SubscriptionRequest(symbol="BTCUSDT", data_types=[MarketDataType.QUOTE])

        # If websockets is not available, operations should fail gracefully
        if not WebSocketFeedAdapter.is_available():
            # Connect should fail
            result = await adapter.connect()
            assert result is False

            # Operations should fail when not connected
            assert await adapter.subscribe(request) is False
            assert await adapter.unsubscribe("BTCUSDT") is False

    def test_subscription_message_creation(self):
        """Test creating subscription messages."""
        adapter = WebSocketFeedAdapter()

        request = SubscriptionRequest(
            symbol="BTCUSDT",
            data_types=[MarketDataType.QUOTE, MarketDataType.TRADE],
            subscription_id="test_sub",
        )

        message = adapter._create_subscription_message(request)

        assert message["method"] == "SUBSCRIBE"
        assert "btcusdt@ticker" in message["params"]
        assert "btcusdt@trade" in message["params"]
        assert message["id"] == "test_sub"

    def test_unsubscribe_message_creation(self):
        """Test creating unsubscribe messages."""
        adapter = WebSocketFeedAdapter()

        message = adapter._create_unsubscribe_message("BTCUSDT")

        assert message["method"] == "UNSUBSCRIBE"
        assert "btcusdt@ticker" in message["params"]
        assert "btcusdt@trade" in message["params"]
        assert "btcusdt@depth" in message["params"]

    def test_message_parsing_ticker(self):
        """Test parsing ticker messages."""
        adapter = WebSocketFeedAdapter()

        # Simulate Binance ticker message
        data = {
            "stream": "btcusdt@ticker",
            "data": {
                "b": "50000.00",  # bid price
                "a": "50001.00",  # ask price
                "B": "1.5",  # bid quantity
                "A": "2.0",  # ask quantity
            },
        }

        event = adapter._parse_message(data)

        assert event is not None
        assert event.event_type == MarketDataType.QUOTE
        assert event.symbol == "BTCUSDT"
        assert event.data["bid_price"] == 50000.0
        assert event.data["ask_price"] == 50001.0
        assert event.data["bid_size"] == 1.5
        assert event.data["ask_size"] == 2.0
        assert event.feed_name == "WebSocketFeed"

    def test_message_parsing_trade(self):
        """Test parsing trade messages."""
        adapter = WebSocketFeedAdapter()

        # Simulate Binance trade message
        data = {
            "stream": "btcusdt@trade",
            "data": {
                "p": "50000.50",  # price
                "q": "0.1",  # quantity
                "t": 123456,  # trade ID
            },
        }

        event = adapter._parse_message(data)

        assert event is not None
        assert event.event_type == MarketDataType.TRADE
        assert event.symbol == "BTCUSDT"
        assert event.data["price"] == 50000.5
        assert event.data["size"] == 0.1
        assert event.data["trade_id"] == 123456

    def test_message_parsing_invalid(self):
        """Test parsing invalid messages."""
        adapter = WebSocketFeedAdapter()

        # Invalid message format
        data = {"invalid": "message"}
        event = adapter._parse_message(data)
        assert event is None

        # Unknown stream
        data = {"stream": "unknown@stream", "data": {}}
        event = adapter._parse_message(data)
        assert event is None

    @pytest.mark.asyncio
    async def test_snapshot_not_implemented(self):
        """Test that snapshot returns None (not implemented)."""
        adapter = WebSocketFeedAdapter()

        snapshot = await adapter.snapshot("BTCUSDT", [MarketDataType.QUOTE])
        assert snapshot is None


class TestBinanceFeed:
    """Test Binance feed implementation."""

    def test_binance_feed_creation(self):
        """Test creating a Binance feed."""
        feed = BinanceFeed()

        assert feed.get_name() == "BinanceFeed"
        assert feed.ws_url == "wss://stream.binance.com:9443/ws"

    def test_binance_feed_with_config(self):
        """Test creating Binance feed with custom config."""
        config = {"ping_interval": 45}
        feed = BinanceFeed(config)

        # Should use Binance URL by default but allow config overrides
        assert feed.ws_url == "wss://stream.binance.com:9443/ws"
        assert feed.ping_interval == 45


@pytest.mark.skipif(
    not WebSocketFeedAdapter.is_available(), reason="websockets library not available"
)
class TestWebSocketAdapterWithWebSockets:
    """Tests that require websockets library to be installed."""

    @pytest.mark.asyncio
    async def test_connect_to_invalid_url(self):
        """Test connection to invalid WebSocket URL."""
        config = {"ws_url": "wss://invalid.url.that.does.not.exist/ws"}
        adapter = WebSocketFeedAdapter(config)

        # Should fail to connect to invalid URL
        result = await adapter.connect()
        assert result is False
        assert not adapter.is_connected()

    def test_websockets_imports(self):
        """Test that websockets imports work when available."""
        # This test only runs if websockets is available
        from eoms.feeds.websocket_adapter import websockets

        assert websockets is not None


class MockWebSocket:
    """Mock WebSocket for testing."""

    def __init__(self):
        self.messages = []
        self.closed = False
        self.ping_responses = []

    async def send(self, message):
        """Mock send method."""
        self.messages.append(message)

    async def recv(self):
        """Mock recv method."""
        # Simulate receiving a test message
        return json.dumps(
            {
                "stream": "btcusdt@ticker",
                "data": {"b": "50000.00", "a": "50001.00", "B": "1.0", "A": "1.0"},
            }
        )

    async def close(self):
        """Mock close method."""
        self.closed = True

    async def ping(self):
        """Mock ping method."""
        if self.ping_responses:
            response = self.ping_responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return response
        return True


class TestWebSocketAdapterMocked:
    """Test WebSocket adapter with mocked WebSocket."""

    @pytest.mark.asyncio
    async def test_message_processing(self):
        """Test message processing with mocked WebSocket."""
        if not WebSocketFeedAdapter.is_available():
            pytest.skip("websockets not available")

        adapter = WebSocketFeedAdapter()

        # Mock the WebSocket
        mock_ws = MockWebSocket()
        adapter.websocket = mock_ws
        adapter.connected = True

        # Test message processing
        test_message = json.dumps(
            {
                "stream": "btcusdt@ticker",
                "data": {"b": "50000.00", "a": "50001.00", "B": "1.0", "A": "1.0"},
            }
        )

        # Set up event callback
        events = []

        async def data_callback(event):
            events.append(event)

        adapter.set_data_callback(data_callback)

        # Process the message
        await adapter._process_message(test_message)

        # Should have received an event
        assert len(events) == 1
        event = events[0]
        assert event.event_type == MarketDataType.QUOTE
        assert event.symbol == "BTCUSDT"

    @pytest.mark.asyncio
    async def test_subscription_with_mock(self):
        """Test subscription with mocked WebSocket."""
        if not WebSocketFeedAdapter.is_available():
            pytest.skip("websockets not available")

        adapter = WebSocketFeedAdapter()

        # Mock the WebSocket
        mock_ws = MockWebSocket()
        adapter.websocket = mock_ws
        adapter.connected = True

        # Test subscription
        request = SubscriptionRequest(symbol="BTCUSDT", data_types=[MarketDataType.QUOTE])

        result = await adapter.subscribe(request)
        assert result is True

        # Check that subscription message was sent
        assert len(mock_ws.messages) == 1
        message = json.loads(mock_ws.messages[0])
        assert message["method"] == "SUBSCRIBE"
        assert "btcusdt@ticker" in message["params"]

        # Check that subscription is stored
        assert adapter.is_subscribed("BTCUSDT")

    @pytest.mark.asyncio
    async def test_connection_check(self):
        """Test connection check with mocked WebSocket."""
        if not WebSocketFeedAdapter.is_available():
            pytest.skip("websockets not available")

        adapter = WebSocketFeedAdapter()

        # Test with no WebSocket
        result = await adapter._check_connection()
        assert result is False

        # Test with working WebSocket
        mock_ws = MockWebSocket()
        adapter.websocket = mock_ws

        result = await adapter._check_connection()
        assert result is True

        # Test with failing WebSocket
        mock_ws.ping_responses = [Exception("Connection lost")]
        result = await adapter._check_connection()
        assert result is False
