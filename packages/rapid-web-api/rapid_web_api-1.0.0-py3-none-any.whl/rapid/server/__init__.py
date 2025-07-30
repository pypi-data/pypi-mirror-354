"""
Server implementations for Rapid
"""

from .dev_server import RapidServer

try:
    from .websocket import (
        MessageType,
        WebSocketManager,
        WebSocketMessage,
        WebSocketServer,
        create_gaming_websocket,
        create_trading_websocket,
    )

    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    WebSocketServer = None
    WebSocketManager = None
    WebSocketMessage = None
    MessageType = None
    create_gaming_websocket = None
    create_trading_websocket = None

__all__ = [
    "RapidServer",
    "WebSocketServer",
    "WebSocketManager",
    "WebSocketMessage",
    "MessageType",
    "create_gaming_websocket",
    "create_trading_websocket",
    "WEBSOCKET_AVAILABLE",
]
