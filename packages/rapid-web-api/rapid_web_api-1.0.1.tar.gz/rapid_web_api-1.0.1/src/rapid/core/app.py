"""
Main Rapid application class - FastAPI-compatible interface
"""

import inspect
import json
from typing import Any, Callable, Dict, Optional, Union

from ..http.request import Request
from ..http.response import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from ..routing.router import Router
from ..server.dev_server import RapidServer


class Rapid:
    """
    The main Rapid application class.

    Provides FastAPI-compatible interface with superior performance.
    """

    def __init__(
        self,
        title: str = "Rapid API",
        description: str = "",
        version: str = "0.1.0",
        debug: bool = False,
    ):
        self.title = title
        self.description = description
        self.version = version
        self.debug = debug
        self.router = Router()
        self._startup_handlers = []
        self._shutdown_handlers = []
        self._middleware = []
        self._exception_handlers = {}

    def get(self, path: str, **kwargs):
        """Register a GET route handler"""
        return self.router.route("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        """Register a POST route handler"""
        return self.router.route("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        """Register a PUT route handler"""
        return self.router.route("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        """Register a DELETE route handler"""
        return self.router.route("DELETE", path, **kwargs)

    def patch(self, path: str, **kwargs):
        """Register a PATCH route handler"""
        return self.router.route("PATCH", path, **kwargs)

    def head(self, path: str, **kwargs):
        """Register a HEAD route handler"""
        return self.router.route("HEAD", path, **kwargs)

    def options(self, path: str, **kwargs):
        """Register a OPTIONS route handler"""
        return self.router.route("OPTIONS", path, **kwargs)

    def on_event(self, event_type: str):
        """Register startup/shutdown event handlers"""

        def decorator(func: Callable):
            if event_type == "startup":
                self._startup_handlers.append(func)
            elif event_type == "shutdown":
                self._shutdown_handlers.append(func)
            return func

        return decorator

    def middleware(self, middleware_type: str):
        """Register middleware (FastAPI compatible)"""

        def decorator(func: Callable):
            self._middleware.append((middleware_type, func))
            return func

        return decorator

    def exception_handler(self, exc_class_or_status_code: Union[int, type]):
        """Register custom exception handlers (FastAPI compatible)"""

        def decorator(func: Callable):
            self._exception_handlers[exc_class_or_status_code] = func
            return func

        return decorator

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        """ASGI application interface"""
        if scope["type"] == "http":
            await self._handle_http(scope, receive, send)
        elif scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)

    async def _handle_http(self, scope: dict, receive: Callable, send: Callable):
        """Handle HTTP requests"""
        method = scope["method"]
        path = scope["path"]

        # Find matching route
        route, path_params = self.router.match(method, path)

        if route is None:
            # 404 Not Found
            response = JSONResponse(content={"detail": "Not Found"}, status_code=404)
            await response(scope, receive, send)
            return

        try:
            # Parse request body if needed
            body = b""
            while True:
                message = await receive()
                if message["type"] == "http.request":
                    body += message.get("body", b"")
                    if not message.get("more_body", False):
                        break

            # Create Request object
            headers = {k.decode(): v.decode() for k, v in scope.get("headers", [])}
            # Note: request object created but not used in current handler interface
            # This will be enhanced in future versions for middleware support
            Request(
                method=method,
                path=path,
                query_string=scope.get("query_string", b""),
                headers=headers,
                body=body,
                path_params=path_params,
            )

            # Call handler
            handler = route.handler
            if inspect.iscoroutinefunction(handler):
                result = await handler(**path_params)
            else:
                result = handler(**path_params)

            # Create response
            if isinstance(result, dict):
                response = JSONResponse(content=result)
            else:
                response = JSONResponse(content={"result": result})

            await response(scope, receive, send)

        except Exception as e:
            # 500 Internal Server Error
            if self.debug:
                error_detail = {"detail": str(e), "type": type(e).__name__}
            else:
                error_detail = {"detail": "Internal Server Error"}

            response = JSONResponse(content=error_detail, status_code=500)
            await response(scope, receive, send)

    async def _handle_lifespan(self, scope: dict, receive: Callable, send: Callable):
        """Handle application lifespan events"""
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                try:
                    for handler in self._startup_handlers:
                        if inspect.iscoroutinefunction(handler):
                            await handler()
                        else:
                            handler()
                    await send({"type": "lifespan.startup.complete"})
                except Exception as e:
                    await send({"type": "lifespan.startup.failed", "message": str(e)})
            elif message["type"] == "lifespan.shutdown":
                try:
                    for handler in self._shutdown_handlers:
                        if inspect.iscoroutinefunction(handler):
                            await handler()
                        else:
                            handler()
                    await send({"type": "lifespan.shutdown.complete"})
                except Exception as e:
                    await send({"type": "lifespan.shutdown.failed", "message": str(e)})
                break

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 8000,
        workers: int = 1,
        reload: bool = False,
    ):
        """Run the Rapid application"""
        server = RapidServer(self)
        server.run(host=host, port=port, workers=workers, reload=reload)
