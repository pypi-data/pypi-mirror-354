"""EOMS Market Data Feed Infrastructure.

This module provides the base classes and implementations for market data feeds
that handle real-time and historical market data streaming.
"""

from .base import FeedBase, MarketDataEvent, SubscriptionRequest
from .random_feed import RandomFeed
from .websocket_adapter import BinanceFeed, WebSocketFeedAdapter

__all__ = [
    "FeedBase",
    "MarketDataEvent",
    "SubscriptionRequest",
    "RandomFeed",
    "WebSocketFeedAdapter",
    "BinanceFeed",
]
