"""
High-performance router for Rapid applications
"""

from typing import Any, Callable, Dict, List, Optional, Tuple

from .matcher import RouteMatcher
from .route import Route


class Router:
    """
    High-performance router for Rapid applications.

    Optimized for fast route matching and minimal overhead.
    """

    def __init__(self):
        self.matcher = RouteMatcher()

        # Middleware support
        self._middleware: List[Callable] = []
        self._route_middleware: Dict[str, List[Callable]] = {}

    def route(self, method: str, path: str, **kwargs):
        """
        Decorator to register route handlers.

        Usage:
            @router.route("GET", "/users/{user_id}")
            def get_user(user_id: int):
                return {"user_id": user_id}
        """

        def decorator(handler: Callable):
            self.add_route(method, path, handler, **kwargs)
            return handler

        return decorator

    def add_route(self, method: str, path: str, handler: Callable, **kwargs):
        """Add a route to the router"""
        route = Route(method, path, handler, **kwargs)
        self.matcher.add_route(route)

        # Store route-specific middleware
        middleware = kwargs.get("middleware", [])
        if middleware:
            route_key = f"{method}:{path}"
            self._route_middleware[route_key] = middleware

    def match(self, method: str, path: str) -> Tuple[Optional[Route], Dict[str, Any]]:
        """
        Find matching route for the given method and path.

        Returns (route, path_params) tuple.
        """
        return self.matcher.match(method, path)

    def add_middleware(self, middleware: Callable):
        """Add global middleware"""
        self._middleware.append(middleware)

    def get_middleware_for_route(self, method: str, path: str) -> List[Callable]:
        """Get middleware for a specific route"""
        route_key = f"{method}:{path}"
        global_middleware = self._middleware.copy()
        route_middleware = self._route_middleware.get(route_key, [])
        return global_middleware + route_middleware

    def get_routes(self) -> List[Route]:
        """Get all registered routes"""
        return self.matcher.get_all_routes()

    def get_stats(self) -> Dict[str, Any]:
        """Get router performance statistics"""
        return self.matcher.get_stats()

    def clear_cache(self):
        """Clear route matching cache"""
        self.matcher.clear_cache()
