"""Random market data feed for testing and simulation."""

import asyncio
import random
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import (
    BookData,
    BookLevel,
    FeedBase,
    MarketDataEvent,
    MarketDataType,
    QuoteData,
    SubscriptionRequest,
    TradeData,
)


class RandomFeed(FeedBase):
    """Random market data feed that generates synthetic market data.

    This feed is useful for testing, simulation, and development when
    you don't have access to real market data. It generates realistic
    random price movements, quotes, trades, and order book data.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the random feed.

        Args:
            config: Configuration dictionary
        """
        super().__init__("RandomFeed", config)

        # Configuration parameters
        self.tick_interval = self.config.get("tick_interval", 0.1)  # seconds
        self.volatility = self.config.get("volatility", 0.01)  # 1% volatility
        self.spread_bps = self.config.get("spread_bps", 5)  # 5 basis points spread
        self.book_depth = self.config.get("book_depth", 5)  # 5 levels

        # Initial prices for symbols
        self.prices = {
            "AAPL": 150.0,
            "MSFT": 300.0,
            "GOOGL": 2500.0,
            "TSLA": 200.0,
            "SPY": 400.0,
        }
        self.prices.update(self.config.get("initial_prices", {}))

        # Feed state
        self._running = False
        self._feed_task: Optional[asyncio.Task] = None

    async def connect(self) -> bool:
        """Connect to the random feed.

        Returns:
            Always returns True
        """
        await asyncio.sleep(0.01)  # Simulate connection delay
        self.connected = True
        self._running = True

        # Start the data generation loop
        self._feed_task = asyncio.create_task(self._data_loop())

        return True

    async def disconnect(self) -> None:
        """Disconnect from the random feed."""
        self._running = False

        if self._feed_task:
            self._feed_task.cancel()
            try:
                await self._feed_task
            except asyncio.CancelledError:
                pass

        self.connected = False

    async def subscribe(self, request: SubscriptionRequest) -> bool:
        """Subscribe to market data.

        Args:
            request: The subscription request

        Returns:
            True if subscription was successful
        """
        if not self.connected:
            return False

        # Initialize price if not present
        if request.symbol not in self.prices:
            self.prices[request.symbol] = random.uniform(10.0, 1000.0)

        # Store subscription
        self.subscriptions[request.symbol] = request

        return True

    async def unsubscribe(self, symbol: str) -> bool:
        """Unsubscribe from market data.

        Args:
            symbol: Symbol to unsubscribe from

        Returns:
            True if unsubscription was successful
        """
        if symbol in self.subscriptions:
            del self.subscriptions[symbol]

        return True

    async def snapshot(
        self, symbol: str, data_types: List[MarketDataType]
    ) -> Optional[Dict[str, Any]]:
        """Get a snapshot of current market data.

        Args:
            symbol: Symbol to get snapshot for
            data_types: Types of data to include in snapshot

        Returns:
            Dictionary containing snapshot data
        """
        if not self.connected or symbol not in self.prices:
            return None

        snapshot = {}
        current_price = self.prices[symbol]

        for data_type in data_types:
            if data_type == MarketDataType.QUOTE:
                quote_data = self._generate_quote_data(current_price)
                snapshot["quote"] = {
                    "bid_price": quote_data.bid_price,
                    "ask_price": quote_data.ask_price,
                    "bid_size": quote_data.bid_size,
                    "ask_size": quote_data.ask_size,
                    "bid_exchange": quote_data.bid_exchange,
                    "ask_exchange": quote_data.ask_exchange,
                }
            elif data_type == MarketDataType.TRADE:
                trade_data = self._generate_trade_data(current_price)
                snapshot["trade"] = {
                    "price": trade_data.price,
                    "size": trade_data.size,
                    "exchange": trade_data.exchange,
                    "trade_id": trade_data.trade_id,
                }
            elif data_type == MarketDataType.BOOK:
                book_data = self._generate_book_data(current_price)
                snapshot["book"] = {
                    "bids": [
                        {
                            "price": level.price,
                            "size": level.size,
                            "order_count": level.order_count,
                        }
                        for level in book_data.bids
                    ],
                    "asks": [
                        {
                            "price": level.price,
                            "size": level.size,
                            "order_count": level.order_count,
                        }
                        for level in book_data.asks
                    ],
                    "exchange": book_data.exchange,
                }

        return snapshot

    async def _data_loop(self) -> None:
        """Main data generation loop."""
        while self._running:
            try:
                await self._generate_data()
                await asyncio.sleep(self.tick_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error in random feed data loop: {e}")
                await asyncio.sleep(1.0)  # Back off on error

    async def _generate_data(self) -> None:
        """Generate random market data for all subscribed symbols."""
        for symbol, request in self.subscriptions.items():
            # Update price with random walk
            current_price = self.prices[symbol]
            price_change = current_price * random.gauss(0, self.volatility)
            new_price = max(0.01, current_price + price_change)
            self.prices[symbol] = new_price

            # Generate data for each requested type
            for data_type in request.data_types:
                event = None

                if data_type == MarketDataType.TICK:
                    event = self._create_tick_event(symbol, new_price)
                elif data_type == MarketDataType.QUOTE:
                    event = self._create_quote_event(symbol, new_price)
                elif (
                    data_type == MarketDataType.TRADE and random.random() < 0.3
                ):  # 30% chance of trade
                    event = self._create_trade_event(symbol, new_price)
                elif (
                    data_type == MarketDataType.BOOK and random.random() < 0.1
                ):  # 10% chance of book update
                    event = self._create_book_event(symbol, new_price)

                if event:
                    await self._emit_data(event)

    def _create_tick_event(self, symbol: str, price: float) -> MarketDataEvent:
        """Create a tick event."""
        return MarketDataEvent(
            event_type=MarketDataType.TICK,
            symbol=symbol,
            timestamp=datetime.now(),
            data={"price": price},
            feed_name=self.name,
            sequence_number=self._next_sequence_number(),
        )

    def _create_quote_event(self, symbol: str, mid_price: float) -> MarketDataEvent:
        """Create a quote event."""
        quote_data = self._generate_quote_data(mid_price)

        return MarketDataEvent(
            event_type=MarketDataType.QUOTE,
            symbol=symbol,
            timestamp=datetime.now(),
            data={
                "bid_price": quote_data.bid_price,
                "ask_price": quote_data.ask_price,
                "bid_size": quote_data.bid_size,
                "ask_size": quote_data.ask_size,
                "bid_exchange": quote_data.bid_exchange,
                "ask_exchange": quote_data.ask_exchange,
            },
            feed_name=self.name,
            sequence_number=self._next_sequence_number(),
        )

    def _create_trade_event(self, symbol: str, base_price: float) -> MarketDataEvent:
        """Create a trade event."""
        trade_data = self._generate_trade_data(base_price)

        return MarketDataEvent(
            event_type=MarketDataType.TRADE,
            symbol=symbol,
            timestamp=datetime.now(),
            data={
                "price": trade_data.price,
                "size": trade_data.size,
                "exchange": trade_data.exchange,
                "trade_id": trade_data.trade_id,
            },
            feed_name=self.name,
            sequence_number=self._next_sequence_number(),
        )

    def _create_book_event(self, symbol: str, mid_price: float) -> MarketDataEvent:
        """Create a book event."""
        book_data = self._generate_book_data(mid_price)

        return MarketDataEvent(
            event_type=MarketDataType.BOOK,
            symbol=symbol,
            timestamp=datetime.now(),
            data={
                "bids": [
                    {
                        "price": level.price,
                        "size": level.size,
                        "order_count": level.order_count,
                    }
                    for level in book_data.bids
                ],
                "asks": [
                    {
                        "price": level.price,
                        "size": level.size,
                        "order_count": level.order_count,
                    }
                    for level in book_data.asks
                ],
                "exchange": book_data.exchange,
            },
            feed_name=self.name,
            sequence_number=self._next_sequence_number(),
        )

    def _generate_quote_data(self, mid_price: float) -> QuoteData:
        """Generate random quote data."""
        spread = mid_price * (self.spread_bps / 10000.0)

        bid_price = mid_price - spread / 2
        ask_price = mid_price + spread / 2

        # Add some randomness to spread
        spread_noise = spread * random.uniform(-0.5, 0.5)
        bid_price += spread_noise
        ask_price -= spread_noise

        return QuoteData(
            bid_price=round(bid_price, 2),
            ask_price=round(ask_price, 2),
            bid_size=random.randint(100, 10000),
            ask_size=random.randint(100, 10000),
            bid_exchange="NASDAQ",
            ask_exchange="NASDAQ",
        )

    def _generate_trade_data(self, base_price: float) -> TradeData:
        """Generate random trade data."""
        # Trade price with some noise around current price
        price_noise = base_price * random.gauss(0, 0.001)  # 0.1% noise
        trade_price = base_price + price_noise

        return TradeData(
            price=round(trade_price, 2),
            size=random.randint(100, 5000),
            exchange="NASDAQ",
            trade_id=f"T{random.randint(100000, 999999)}",
        )

    def _generate_book_data(self, mid_price: float) -> BookData:
        """Generate random order book data."""
        spread = mid_price * (self.spread_bps / 10000.0)

        bids = []
        asks = []

        # Generate bid levels (decreasing prices)
        for i in range(self.book_depth):
            level_offset = spread * (1 + i * 0.5)
            price = round(mid_price - level_offset, 2)
            size = random.randint(100, 2000) * (self.book_depth - i)  # More size at better prices
            bids.append(BookLevel(price=price, size=size, order_count=random.randint(1, 10)))

        # Generate ask levels (increasing prices)
        for i in range(self.book_depth):
            level_offset = spread * (1 + i * 0.5)
            price = round(mid_price + level_offset, 2)
            size = random.randint(100, 2000) * (self.book_depth - i)  # More size at better prices
            asks.append(BookLevel(price=price, size=size, order_count=random.randint(1, 10)))

        return BookData(bids=bids, asks=asks, exchange="NASDAQ")

    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol.

        Args:
            symbol: Symbol to get price for

        Returns:
            Current price or None if not available
        """
        return self.prices.get(symbol)

    def set_price(self, symbol: str, price: float) -> None:
        """Set the current price for a symbol.

        Args:
            symbol: Symbol to set price for
            price: Price to set
        """
        self.prices[symbol] = price
