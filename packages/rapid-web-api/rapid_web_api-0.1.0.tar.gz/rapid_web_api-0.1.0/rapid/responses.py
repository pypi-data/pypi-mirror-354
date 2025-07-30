"""
HTTP response classes for Rapid
"""

import json
from typing import Any, Dict, Optional, Union

from .json_utils import cached_json_response, dumps_bytes


class Response:
    """Base response class"""

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
    ):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.media_type = media_type

    async def __call__(self, scope: dict, receive: callable, send: callable):
        """ASGI callable"""
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [
                    [key.encode(), value.encode()]
                    for key, value in self.headers.items()
                ],
            }
        )

        body = self.render()
        await send({"type": "http.response.body", "body": body})

    def render(self) -> bytes:
        """Render response content to bytes"""
        if self.content is None:
            return b""

        if isinstance(self.content, bytes):
            return self.content

        if isinstance(self.content, str):
            return self.content.encode("utf-8")

        return str(self.content).encode("utf-8")


class JSONResponse(Response):
    """JSON response with automatic serialization and caching"""

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        cache_key: Optional[str] = None,
        use_cache: bool = False,
    ):
        headers = headers or {}
        headers.setdefault("content-type", "application/json")

        self.cache_key = cache_key
        self.use_cache = use_cache

        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="application/json",
        )

    def render(self) -> bytes:
        """Render content as JSON using optimized serialization with caching"""
        if self.content is None:
            return b"null"

        # Use cached response if enabled
        if self.use_cache and self.cache_key:
            try:
                return cached_json_response(self.content, self.cache_key)
            except (TypeError, ValueError):
                pass

        # Use optimized JSON serialization
        try:
            return dumps_bytes(self.content)
        except (TypeError, ValueError) as e:
            # Fallback for complex objects
            return dumps_bytes({"error": "Serialization failed", "detail": str(e)})


class HTMLResponse(Response):
    """HTML response"""

    def __init__(
        self,
        content: str = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ):
        headers = headers or {}
        headers.setdefault("content-type", "text/html; charset=utf-8")

        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/html",
        )


class PlainTextResponse(Response):
    """Plain text response"""

    def __init__(
        self,
        content: str = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
    ):
        headers = headers or {}
        headers.setdefault("content-type", "text/plain; charset=utf-8")

        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/plain",
        )


class RedirectResponse(Response):
    """HTTP redirect response"""

    def __init__(
        self, url: str, status_code: int = 307, headers: Optional[Dict[str, str]] = None
    ):
        headers = headers or {}
        headers["location"] = url

        super().__init__(content=None, status_code=status_code, headers=headers)
