"""
HTTP response classes for Rapid
"""

import json
import mimetypes
import os
from typing import Any, Dict, Optional, Union

from ..utils.json import cached_json_response, dumps_bytes


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

        # Use cached response if enabled and content is cacheable
        if self.use_cache and self.cache_key:
            try:
                return cached_json_response(self.content, self.cache_key)
            except (TypeError, ValueError):
                pass

        # Auto-enable caching for simple static responses
        elif isinstance(self.content, dict) and len(str(self.content)) < 1000:
            # Cache small dictionary responses automatically
            cache_key = f"auto_{hash(str(self.content))}"
            try:
                return cached_json_response(self.content, cache_key)
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


class FileResponse(Response):
    """File response for serving static files"""

    def __init__(
        self,
        path: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        filename: Optional[str] = None,
    ):
        self.path = path
        self.filename = filename

        headers = headers or {}

        # Determine media type if not provided
        if media_type is None:
            media_type, _ = mimetypes.guess_type(path)
            if media_type is None:
                media_type = "application/octet-stream"

        headers.setdefault("content-type", media_type)

        # Set content-disposition if filename provided
        if filename:
            headers["content-disposition"] = f'attachment; filename="{filename}"'

        super().__init__(
            content=None,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
        )

    async def __call__(self, scope: dict, receive: callable, send: callable):
        """ASGI callable for file streaming"""
        # Check if file exists
        if not os.path.exists(self.path):
            # File not found - return 404
            await send(
                {
                    "type": "http.response.start",
                    "status": 404,
                    "headers": [[b"content-type", b"application/json"]],
                }
            )
            await send(
                {
                    "type": "http.response.body",
                    "body": b'{"detail": "File not found"}',
                }
            )
            return

        # Get file size for content-length header
        file_size = os.path.getsize(self.path)
        headers = list(self.headers.items())
        headers.append(("content-length", str(file_size)))

        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": [[key.encode(), value.encode()] for key, value in headers],
            }
        )

        # Stream file content in chunks
        chunk_size = 64 * 1024  # 64KB chunks
        with open(self.path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                await send(
                    {
                        "type": "http.response.body",
                        "body": chunk,
                        "more_body": True,
                    }
                )

        # Send final empty chunk to indicate end
        await send(
            {
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            }
        )
