"""Tests for market data feed infrastructure."""

import asyncio
from datetime import datetime

import pytest

from eoms.feeds import MarketDataEvent, RandomFeed, SubscriptionRequest
from eoms.feeds.base import BookData, BookLevel, MarketDataType, QuoteData, TradeData


class TestMarketDataTypes:
    """Test market data type definitions."""

    def test_subscription_request_creation(self):
        """Test creating a subscription request."""
        request = SubscriptionRequest(
            symbol="AAPL",
            data_types=[MarketDataType.QUOTE, MarketDataType.TRADE],
            subscription_id="SUB001",
        )

        assert request.symbol == "AAPL"
        assert MarketDataType.QUOTE in request.data_types
        assert MarketDataType.TRADE in request.data_types
        assert request.subscription_id == "SUB001"

    def test_subscription_request_to_dict(self):
        """Test converting subscription request to dictionary."""
        request = SubscriptionRequest(
            symbol="AAPL",
            data_types=[MarketDataType.QUOTE],
            params={"param1": "value1"},
        )

        request_dict = request.to_dict()

        assert request_dict["symbol"] == "AAPL"
        assert request_dict["data_types"] == ["QUOTE"]
        assert request_dict["params"]["param1"] == "value1"

    def test_market_data_event_creation(self):
        """Test creating a market data event."""
        timestamp = datetime.now()
        event = MarketDataEvent(
            event_type=MarketDataType.QUOTE,
            symbol="AAPL",
            timestamp=timestamp,
            data={"bid": 150.0, "ask": 150.05},
            feed_name="TestFeed",
        )

        assert event.event_type == MarketDataType.QUOTE
        assert event.symbol == "AAPL"
        assert event.timestamp == timestamp
        assert event.data["bid"] == 150.0
        assert event.feed_name == "TestFeed"

    def test_market_data_event_to_dict(self):
        """Test converting market data event to dictionary."""
        timestamp = datetime.now()
        event = MarketDataEvent(
            event_type=MarketDataType.TRADE,
            symbol="AAPL",
            timestamp=timestamp,
            data={"price": 150.0, "size": 100},
            sequence_number=123,
        )

        event_dict = event.to_dict()

        assert event_dict["event_type"] == "TRADE"
        assert event_dict["symbol"] == "AAPL"
        assert event_dict["timestamp"] == timestamp.isoformat()
        assert event_dict["data"]["price"] == 150.0
        assert event_dict["sequence_number"] == 123


class TestDataStructures:
    """Test market data structures."""

    def test_quote_data(self):
        """Test QuoteData structure."""
        quote = QuoteData(
            bid_price=150.0,
            ask_price=150.05,
            bid_size=1000,
            ask_size=500,
            bid_exchange="NYSE",
            ask_exchange="NASDAQ",
        )

        assert quote.bid_price == 150.0
        assert quote.ask_price == 150.05
        assert quote.bid_size == 1000
        assert quote.ask_size == 500
        assert quote.bid_exchange == "NYSE"
        assert quote.ask_exchange == "NASDAQ"

    def test_trade_data(self):
        """Test TradeData structure."""
        trade = TradeData(price=150.0, size=100, exchange="NYSE", trade_id="T123456")

        assert trade.price == 150.0
        assert trade.size == 100
        assert trade.exchange == "NYSE"
        assert trade.trade_id == "T123456"

    def test_book_data(self):
        """Test BookData structure."""
        bids = [
            BookLevel(price=149.99, size=1000, order_count=5),
            BookLevel(price=149.98, size=2000, order_count=10),
        ]
        asks = [
            BookLevel(price=150.01, size=800, order_count=3),
            BookLevel(price=150.02, size=1500, order_count=7),
        ]

        book = BookData(bids=bids, asks=asks, exchange="NYSE")

        assert len(book.bids) == 2
        assert len(book.asks) == 2
        assert book.bids[0].price == 149.99
        assert book.asks[0].price == 150.01
        assert book.exchange == "NYSE"


class TestRandomFeed:
    """Test RandomFeed implementation."""

    def test_random_feed_creation(self):
        """Test creating a random feed."""
        feed = RandomFeed()

        assert feed.get_name() == "RandomFeed"
        assert not feed.is_connected()
        assert "AAPL" in feed.prices

    def test_random_feed_with_config(self):
        """Test creating random feed with custom config."""
        config = {
            "tick_interval": 0.05,
            "volatility": 0.02,
            "initial_prices": {"CUSTOM": 500.0},
        }
        feed = RandomFeed(config)

        assert feed.tick_interval == 0.05
        assert feed.volatility == 0.02
        assert feed.prices["CUSTOM"] == 500.0

    @pytest.mark.asyncio
    async def test_connect_disconnect(self):
        """Test feed connection and disconnection."""
        feed = RandomFeed()

        # Initially not connected
        assert not feed.is_connected()

        # Connect
        result = await feed.connect()
        assert result is True
        assert feed.is_connected()
        assert feed._running is True
        assert feed._feed_task is not None

        # Disconnect
        await feed.disconnect()
        assert not feed.is_connected()
        assert feed._running is False

    @pytest.mark.asyncio
    async def test_subscribe_unsubscribe(self):
        """Test subscription management."""
        feed = RandomFeed()
        await feed.connect()

        # Subscribe to AAPL quotes
        request = SubscriptionRequest(
            symbol="AAPL", data_types=[MarketDataType.QUOTE], subscription_id="SUB001"
        )

        result = await feed.subscribe(request)
        assert result is True
        assert feed.is_subscribed("AAPL")

        subscriptions = feed.get_subscriptions()
        assert "AAPL" in subscriptions
        assert subscriptions["AAPL"] == request

        # Unsubscribe
        result = await feed.unsubscribe("AAPL")
        assert result is True
        assert not feed.is_subscribed("AAPL")

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_subscribe_new_symbol(self):
        """Test subscribing to a new symbol initializes its price."""
        feed = RandomFeed()
        await feed.connect()

        # NEW_SYMBOL should not exist initially
        assert "NEW_SYMBOL" not in feed.prices

        request = SubscriptionRequest(symbol="NEW_SYMBOL", data_types=[MarketDataType.QUOTE])

        result = await feed.subscribe(request)
        assert result is True

        # Price should now be initialized
        assert "NEW_SYMBOL" in feed.prices
        assert feed.prices["NEW_SYMBOL"] > 0

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_subscription_fails_when_disconnected(self):
        """Test that subscription fails when disconnected."""
        feed = RandomFeed()

        request = SubscriptionRequest(symbol="AAPL", data_types=[MarketDataType.QUOTE])

        result = await feed.subscribe(request)
        assert result is False

    @pytest.mark.asyncio
    async def test_snapshot(self):
        """Test getting market data snapshot."""
        feed = RandomFeed()
        await feed.connect()

        # Test snapshot with quote data
        snapshot = await feed.snapshot("AAPL", [MarketDataType.QUOTE])
        assert snapshot is not None
        assert "quote" in snapshot

        quote_data = snapshot["quote"]
        assert "bid_price" in quote_data
        assert "ask_price" in quote_data
        assert "bid_size" in quote_data
        assert "ask_size" in quote_data

        # Test snapshot with multiple data types
        snapshot = await feed.snapshot(
            "AAPL", [MarketDataType.QUOTE, MarketDataType.TRADE, MarketDataType.BOOK]
        )
        assert "quote" in snapshot
        assert "trade" in snapshot
        assert "book" in snapshot

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_snapshot_returns_none_when_disconnected(self):
        """Test that snapshot returns None when disconnected."""
        feed = RandomFeed()

        snapshot = await feed.snapshot("AAPL", [MarketDataType.QUOTE])
        assert snapshot is None

    @pytest.mark.asyncio
    async def test_data_generation(self):
        """Test that feed generates market data events."""
        config = {"tick_interval": 0.01}  # Fast ticks for testing
        feed = RandomFeed(config)
        await feed.connect()

        # Set up data callback
        events = []

        async def data_callback(event: MarketDataEvent):
            events.append(event)

        feed.set_data_callback(data_callback)

        # Subscribe to data
        request = SubscriptionRequest(
            symbol="AAPL",
            data_types=[MarketDataType.TICK, MarketDataType.QUOTE],
            subscription_id="TEST",
        )

        await feed.subscribe(request)

        # Wait for some data to be generated
        await asyncio.sleep(0.1)

        # Should have received some events
        assert len(events) > 0

        # Check event properties
        tick_events = [e for e in events if e.event_type == MarketDataType.TICK]
        quote_events = [e for e in events if e.event_type == MarketDataType.QUOTE]

        assert len(tick_events) > 0
        assert len(quote_events) > 0

        # Check tick event
        tick_event = tick_events[0]
        assert tick_event.symbol == "AAPL"
        assert tick_event.feed_name == "RandomFeed"
        assert "price" in tick_event.data
        assert tick_event.sequence_number > 0

        # Check quote event
        quote_event = quote_events[0]
        assert quote_event.symbol == "AAPL"
        assert "bid_price" in quote_event.data
        assert "ask_price" in quote_event.data

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_trade_and_book_events(self):
        """Test generation of trade and book events."""
        config = {"tick_interval": 0.001}  # Very fast for testing
        feed = RandomFeed(config)
        await feed.connect()

        events = []

        async def data_callback(event: MarketDataEvent):
            events.append(event)

        feed.set_data_callback(data_callback)

        # Subscribe to all data types
        request = SubscriptionRequest(
            symbol="AAPL", data_types=[MarketDataType.TRADE, MarketDataType.BOOK]
        )

        await feed.subscribe(request)

        # Wait for events (trades and books are less frequent)
        await asyncio.sleep(0.5)

        # Should eventually get trade and book events
        trade_events = [e for e in events if e.event_type == MarketDataType.TRADE]
        book_events = [e for e in events if e.event_type == MarketDataType.BOOK]

        # Note: These are probabilistic, so we might not always get them
        # But the structure should be correct when we do

        if trade_events:
            trade_event = trade_events[0]
            assert trade_event.symbol == "AAPL"
            assert "price" in trade_event.data
            assert "size" in trade_event.data
            assert "trade_id" in trade_event.data

        if book_events:
            book_event = book_events[0]
            assert book_event.symbol == "AAPL"
            assert "bids" in book_event.data
            assert "asks" in book_event.data
            assert len(book_event.data["bids"]) > 0
            assert len(book_event.data["asks"]) > 0

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_data_callback_error_handling(self):
        """Test that errors in data callbacks don't crash the feed."""
        feed = RandomFeed({"tick_interval": 0.01})
        await feed.connect()

        # Set up event callback that raises an exception
        async def failing_callback(event: MarketDataEvent):
            raise ValueError("Test error")

        feed.set_data_callback(failing_callback)

        # Subscribe to data
        request = SubscriptionRequest(symbol="AAPL", data_types=[MarketDataType.TICK])

        await feed.subscribe(request)

        # Wait a bit - should not crash despite callback errors
        await asyncio.sleep(0.05)

        # Feed should still be connected and running
        assert feed.is_connected()
        assert feed._running

        await feed.disconnect()

    def test_price_management(self):
        """Test price management functionality."""
        feed = RandomFeed()

        # Test getting current price
        price = feed.get_current_price("AAPL")
        assert price == 150.0

        # Test setting price
        feed.set_price("AAPL", 155.0)
        assert feed.get_current_price("AAPL") == 155.0

        # Test unknown symbol
        price = feed.get_current_price("UNKNOWN")
        assert price is None

    @pytest.mark.asyncio
    async def test_multiple_symbol_subscriptions(self):
        """Test subscribing to multiple symbols."""
        feed = RandomFeed({"tick_interval": 0.01})
        await feed.connect()

        events = []

        async def data_callback(event: MarketDataEvent):
            events.append(event)

        feed.set_data_callback(data_callback)

        # Subscribe to multiple symbols
        symbols = ["AAPL", "MSFT", "GOOGL"]
        for symbol in symbols:
            request = SubscriptionRequest(symbol=symbol, data_types=[MarketDataType.TICK])
            await feed.subscribe(request)

        # Wait for data
        await asyncio.sleep(0.1)

        # Should have events for all symbols
        event_symbols = {event.symbol for event in events}
        for symbol in symbols:
            assert symbol in event_symbols

        await feed.disconnect()

    @pytest.mark.asyncio
    async def test_price_evolution(self):
        """Test that prices evolve over time with volatility."""
        feed = RandomFeed({"volatility": 0.1, "tick_interval": 0.01})  # High volatility
        await feed.connect()

        initial_price = feed.get_current_price("AAPL")

        # Subscribe to ticks to trigger price updates
        request = SubscriptionRequest(symbol="AAPL", data_types=[MarketDataType.TICK])
        await feed.subscribe(request)

        # Wait for price to evolve
        await asyncio.sleep(0.1)

        final_price = feed.get_current_price("AAPL")

        # Price should have changed (very high probability with 0.1 volatility)
        assert abs(final_price - initial_price) / initial_price > 0.001  # At least 0.1% change

        await feed.disconnect()
