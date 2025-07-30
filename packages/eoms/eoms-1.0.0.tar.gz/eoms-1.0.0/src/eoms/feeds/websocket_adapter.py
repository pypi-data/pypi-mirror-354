"""WebSocket feed adapter template."""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base import (
    FeedBase,
    MarketDataEvent,
    MarketDataType,
    SubscriptionRequest,
)

# Try to import websockets, but handle gracefully if not available
try:
    import websockets

    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    websockets = None

logger = logging.getLogger(__name__)


class WebSocketFeedAdapter(FeedBase):
    """WebSocket feed adapter template.

    This is a template implementation that demonstrates how to create
    a WebSocket-based market data feed. It includes connection management,
    subscription handling, and message parsing.

    This template can be customized for specific exchanges or data providers
    by overriding the message parsing and subscription methods.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the WebSocket feed adapter.

        Args:
            config: Configuration dictionary
        """
        super().__init__("WebSocketFeed", config)

        if not WEBSOCKETS_AVAILABLE:
            logger.warning("websockets library not available. Install with: pip install websockets")

        # Configuration
        self.ws_url = self.config.get("ws_url", "wss://stream.binance.com:9443/ws")
        self.ping_interval = self.config.get("ping_interval", 30)
        self.reconnect_delay = self.config.get("reconnect_delay", 5)
        self.max_reconnect_attempts = self.config.get("max_reconnect_attempts", 10)

        # WebSocket state
        self.websocket: Optional[Any] = None
        self.reconnect_attempts = 0
        self._running = False
        self._message_task: Optional[asyncio.Task] = None

    async def connect(self) -> bool:
        """Connect to the WebSocket feed.

        Returns:
            True if connection successful, False otherwise
        """
        if not WEBSOCKETS_AVAILABLE:
            logger.error("websockets library not available")
            return False

        try:
            logger.info(f"Connecting to WebSocket feed at {self.ws_url}")

            # Connect to WebSocket
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=self.ping_interval,
                ping_timeout=10,
                close_timeout=10,
            )

            self.connected = True
            self._running = True
            self.reconnect_attempts = 0

            # Start message handling task
            self._message_task = asyncio.create_task(self._message_loop())

            logger.info("WebSocket feed connected successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to WebSocket feed: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from the WebSocket feed."""
        self._running = False

        if self._message_task:
            self._message_task.cancel()
            try:
                await self._message_task
            except asyncio.CancelledError:
                pass

        if self.websocket:
            try:
                await self.websocket.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket: {e}")

        self.connected = False
        self.websocket = None
        logger.info("WebSocket feed disconnected")

    async def subscribe(self, request: SubscriptionRequest) -> bool:
        """Subscribe to market data.

        Args:
            request: The subscription request

        Returns:
            True if subscription was successful
        """
        if not self.connected or not self.websocket:
            return False

        try:
            # Convert subscription request to WebSocket message
            # This is a template - customize for specific exchange
            subscription_message = self._create_subscription_message(request)

            # Send subscription message
            await self.websocket.send(json.dumps(subscription_message))

            # Store subscription
            self.subscriptions[request.symbol] = request

            logger.info(f"Subscribed to {request.symbol}")
            return True

        except Exception as e:
            logger.error(f"Failed to subscribe to {request.symbol}: {e}")
            return False

    async def unsubscribe(self, symbol: str) -> bool:
        """Unsubscribe from market data.

        Args:
            symbol: Symbol to unsubscribe from

        Returns:
            True if unsubscription was successful
        """
        if not self.connected or not self.websocket:
            return False

        try:
            # Convert unsubscribe request to WebSocket message
            unsubscribe_message = self._create_unsubscribe_message(symbol)

            # Send unsubscribe message
            await self.websocket.send(json.dumps(unsubscribe_message))

            # Remove subscription
            if symbol in self.subscriptions:
                del self.subscriptions[symbol]

            logger.info(f"Unsubscribed from {symbol}")
            return True

        except Exception as e:
            logger.error(f"Failed to unsubscribe from {symbol}: {e}")
            return False

    async def snapshot(
        self, symbol: str, data_types: List[MarketDataType]
    ) -> Optional[Dict[str, Any]]:
        """Get a snapshot of current market data.

        Args:
            symbol: Symbol to get snapshot for
            data_types: Types of data to include in snapshot

        Returns:
            Dictionary containing snapshot data, or None if not available
        """
        # WebSocket feeds typically don't support snapshots directly
        # This would require a separate REST API call
        logger.warning("Snapshot not implemented for WebSocket feed template")
        return None

    async def _message_loop(self) -> None:
        """Main message processing loop."""
        while self._running:
            try:
                if self.websocket:
                    # Receive message with timeout
                    message = await asyncio.wait_for(
                        self.websocket.recv(), timeout=60.0  # 60 second timeout
                    )

                    # Process the message
                    await self._process_message(message)
                else:
                    await asyncio.sleep(1.0)

            except asyncio.TimeoutError:
                logger.warning("WebSocket message timeout - checking connection")
                if not await self._check_connection():
                    await self._reconnect()

            except asyncio.CancelledError:
                break

            except Exception as e:
                logger.error(f"Error in message loop: {e}")
                await self._reconnect()

    async def _process_message(self, message: str) -> None:
        """Process a WebSocket message.

        Args:
            message: Raw message string
        """
        try:
            # Parse JSON message
            data = json.loads(message)

            # Convert to market data event
            event = self._parse_message(data)

            if event:
                await self._emit_data(event)

        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON message: {message}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _parse_message(self, data: Dict[str, Any]) -> Optional[MarketDataEvent]:
        """Parse a message into a market data event.

        This is a template method that should be overridden for specific exchanges.

        Args:
            data: Parsed JSON data

        Returns:
            MarketDataEvent or None if not a data message
        """
        # Template implementation for Binance-style messages
        if "stream" in data and "data" in data:
            stream = data["stream"]
            message_data = data["data"]

            # Extract symbol from stream name (e.g., "btcusdt@ticker")
            if "@" in stream:
                symbol_part = stream.split("@")[0]
                symbol = symbol_part.upper()

                # Parse ticker data
                if "@ticker" in stream:
                    return MarketDataEvent(
                        event_type=MarketDataType.QUOTE,
                        symbol=symbol,
                        timestamp=datetime.now(),
                        data={
                            "bid_price": float(message_data.get("b", 0)),
                            "ask_price": float(message_data.get("a", 0)),
                            "bid_size": float(message_data.get("B", 0)),
                            "ask_size": float(message_data.get("A", 0)),
                        },
                        feed_name=self.name,
                        sequence_number=self._next_sequence_number(),
                    )

                # Parse trade data
                elif "@trade" in stream:
                    return MarketDataEvent(
                        event_type=MarketDataType.TRADE,
                        symbol=symbol,
                        timestamp=datetime.now(),
                        data={
                            "price": float(message_data.get("p", 0)),
                            "size": float(message_data.get("q", 0)),
                            "trade_id": message_data.get("t"),
                        },
                        feed_name=self.name,
                        sequence_number=self._next_sequence_number(),
                    )

        return None

    def _create_subscription_message(self, request: SubscriptionRequest) -> Dict[str, Any]:
        """Create a subscription message for the WebSocket.

        This is a template method that should be customized for specific exchanges.

        Args:
            request: Subscription request

        Returns:
            Dictionary representing the subscription message
        """
        # Template implementation for Binance-style subscriptions
        symbol = request.symbol.lower()

        # Map data types to stream names
        streams = []
        for data_type in request.data_types:
            if data_type == MarketDataType.QUOTE:
                streams.append(f"{symbol}@ticker")
            elif data_type == MarketDataType.TRADE:
                streams.append(f"{symbol}@trade")
            elif data_type == MarketDataType.BOOK:
                streams.append(f"{symbol}@depth")

        return {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": request.subscription_id or 1,
        }

    def _create_unsubscribe_message(self, symbol: str) -> Dict[str, Any]:
        """Create an unsubscribe message for the WebSocket.

        Args:
            symbol: Symbol to unsubscribe from

        Returns:
            Dictionary representing the unsubscribe message
        """
        symbol = symbol.lower()

        # Get all streams for this symbol
        streams = [f"{symbol}@ticker", f"{symbol}@trade", f"{symbol}@depth"]

        return {"method": "UNSUBSCRIBE", "params": streams, "id": 2}

    async def _check_connection(self) -> bool:
        """Check if WebSocket connection is still alive.

        Returns:
            True if connection is alive, False otherwise
        """
        if not self.websocket:
            return False

        try:
            # Send a ping to check connection
            await self.websocket.ping()
            return True
        except Exception:
            return False

    async def _reconnect(self) -> None:
        """Attempt to reconnect to the WebSocket."""
        if self.reconnect_attempts >= self.max_reconnect_attempts:
            logger.error("Max reconnect attempts reached, giving up")
            self._running = False
            return

        self.reconnect_attempts += 1
        logger.info(
            f"Attempting to reconnect ({self.reconnect_attempts}/{self.max_reconnect_attempts})"
        )

        # Close existing connection
        if self.websocket:
            try:
                await self.websocket.close()
            except Exception:
                pass

        self.connected = False
        self.websocket = None

        # Wait before reconnecting
        await asyncio.sleep(self.reconnect_delay)

        # Attempt to reconnect
        if await self.connect():
            # Re-subscribe to all symbols
            subscriptions = list(self.subscriptions.values())
            self.subscriptions.clear()

            for subscription in subscriptions:
                await self.subscribe(subscription)

    @staticmethod
    def is_available() -> bool:
        """Check if websockets library is available.

        Returns:
            True if websockets is available, False otherwise
        """
        return WEBSOCKETS_AVAILABLE


class BinanceFeed(WebSocketFeedAdapter):
    """Binance WebSocket feed implementation.

    This is a concrete implementation of the WebSocket adapter template
    specifically for Binance market data.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize Binance feed.

        Args:
            config: Configuration dictionary
        """
        default_config = {
            "ws_url": "wss://stream.binance.com:9443/ws",
        }

        if config:
            default_config.update(config)

        super().__init__(default_config)
        self.name = "BinanceFeed"


# Demo function to show how to use the WebSocket feed
async def demo_binance_feed():
    """Demo function showing how to use the Binance WebSocket feed."""
    if not WebSocketFeedAdapter.is_available():
        print("websockets library not available. Install with: pip install websockets")
        return

    feed = BinanceFeed()

    # Set up data callback
    async def data_callback(event):
        print(f"Received {event.event_type.value} for {event.symbol}: {event.data}")

    feed.set_data_callback(data_callback)

    try:
        # Connect to feed
        if await feed.connect():
            print("Connected to Binance feed")

            # Subscribe to BTC/USDT ticker and trades
            request = SubscriptionRequest(
                symbol="BTCUSDT",
                data_types=[MarketDataType.QUOTE, MarketDataType.TRADE],
                subscription_id="demo_sub_1",
            )

            if await feed.subscribe(request):
                print("Subscribed to BTCUSDT")

                # Let it run for a few seconds
                await asyncio.sleep(10)

                # Unsubscribe
                await feed.unsubscribe("BTCUSDT")
                print("Unsubscribed from BTCUSDT")

        else:
            print("Failed to connect to Binance feed")

    finally:
        await feed.disconnect()
        print("Disconnected from Binance feed")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_binance_feed())
