"""
Rapid - High-performance web framework for Python

A FastAPI-compatible framework optimized for speed and developer experience.
"""

__version__ = "0.1.0"
__author__ = "Wesley Ellis"
__email__ = "your.email@example.com"

from .json_utils import dumps, dumps_bytes, loads
from .main import Rapid
from .request import Request, UploadFile
from .responses import JSONResponse
from .routing import Route, Router

__all__ = [
    "Rapid",
    "Route",
    "Router",
    "JSONResponse",
    "Request",
    "UploadFile",
    "dumps",
    "loads",
    "dumps_bytes",
]
