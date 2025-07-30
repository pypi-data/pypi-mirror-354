"""
Rapid - High-performance web framework for Python

A FastAPI-compatible framework optimized for speed and developer experience.
Offers specialized modules for different use cases:

- Web APIs (default): Traditional REST APIs with 3.6x FastAPI performance
- Gaming: Ultra-low latency real-time applications (<5ms response times)
- Video: High-throughput video streaming and delivery
- Enterprise: Advanced security, monitoring, and clustering
- Government: High-security applications with FIPS compliance
"""

__version__ = "1.0.0"
__author__ = "Wesley Ellis"
__email__ = "wes@wesellis.com"

# Core imports
from .core.app import Rapid
from .http.request import Request, UploadFile
from .http.response import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
)
from .routing.route import Route
from .routing.router import Router
from .utils.json import dumps, dumps_bytes, get_performance_stats, loads

# Specialized modules with graceful fallbacks
try:
    from .gaming import GameServer

    GAMING_SUPPORT = True
except ImportError:
    GAMING_SUPPORT = False
    GameServer = None  # type: ignore

try:
    from .financial import TradingServer

    FINANCIAL_SUPPORT = True
except ImportError:
    FINANCIAL_SUPPORT = False
    TradingServer = None  # type: ignore

try:
    from .video import StreamingServer as VideoServer  # Use correct class name

    VIDEO_SUPPORT = True
except ImportError:
    VIDEO_SUPPORT = False
    VideoServer = None  # type: ignore

try:
    from .enterprise import EnterpriseServer

    ENTERPRISE_SUPPORT = True
except ImportError:
    ENTERPRISE_SUPPORT = False
    EnterpriseServer = None  # type: ignore

try:
    from .government import GovernmentServer

    GOVERNMENT_SUPPORT = True
except ImportError:
    GOVERNMENT_SUPPORT = False
    GovernmentServer = None  # type: ignore

# Optional WebSocket support
try:
    from .server.websocket import MessageType, WebSocketServer

    WEBSOCKET_SUPPORT = True
except ImportError:
    WEBSOCKET_SUPPORT = False
    WebSocketServer = None  # type: ignore
    MessageType = None  # type: ignore

# Optional CLI support
try:
    from .cli import RapidCLI

    CLI_SUPPORT = True
except ImportError:
    CLI_SUPPORT = False
    RapidCLI = None  # type: ignore

__all__ = [
    "Rapid",
    "Route",
    "Router",
    "JSONResponse",
    "PlainTextResponse",
    "HTMLResponse",
    "FileResponse",
    "RedirectResponse",
    "Request",
    "UploadFile",
    "dumps",
    "loads",
    "dumps_bytes",
    "get_performance_stats",
    # Specialized modules
    "GameServer",
    "GAMING_SUPPORT",
    "TradingServer",
    "FINANCIAL_SUPPORT",
    "VideoServer",
    "VIDEO_SUPPORT",
    "EnterpriseServer",
    "ENTERPRISE_SUPPORT",
    "GovernmentServer",
    "GOVERNMENT_SUPPORT",
    # Optional features
    "WebSocketServer",
    "MessageType",
    "WEBSOCKET_SUPPORT",
    "RapidCLI",
    "CLI_SUPPORT",
]
