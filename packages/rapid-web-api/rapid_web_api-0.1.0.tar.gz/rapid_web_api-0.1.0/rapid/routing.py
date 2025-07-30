"""
High-performance routing system for Rapid
"""

import re
from typing import Any, Callable, Dict, Optional, Tuple


class Route:
    """Represents a single route in the application"""

    def __init__(self, method: str, path: str, handler: Callable, **kwargs):
        self.method = method
        self.path = path
        self.handler = handler
        self.kwargs = kwargs

        # Compile path pattern for fast matching
        self.pattern, self.param_names = self._compile_path(path)

    def _compile_path(self, path: str) -> Tuple[re.Pattern, list]:
        """
        Compile path pattern to regex for fast matching.

        Converts FastAPI-style paths like "/items/{item_id}"
        to regex patterns.
        """
        param_names = []
        pattern_parts = []

        # Split path into segments
        segments = path.split("/")

        for segment in segments:
            if not segment:
                continue

            if segment.startswith("{") and segment.endswith("}"):
                # Path parameter
                param_name = segment[1:-1]
                param_names.append(param_name)

                # Check for type hints (basic support)
                if ":" in param_name:
                    param_name, param_type = param_name.split(":", 1)
                    param_names[-1] = param_name

                    if param_type == "int":
                        pattern_parts.append(r"(\d+)")
                    elif param_type == "float":
                        pattern_parts.append(r"(\d+\.?\d*)")
                    else:
                        pattern_parts.append(r"([^/]+)")
                else:
                    pattern_parts.append(r"([^/]+)")
            else:
                # Static segment
                pattern_parts.append(re.escape(segment))

        # Construct full pattern
        if pattern_parts:
            full_pattern = "^/" + "/".join(pattern_parts) + "$"
        else:
            full_pattern = "^/$"

        return re.compile(full_pattern), param_names

    def match(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Check if this route matches the given path.

        Returns path parameters if match, None otherwise.
        """
        match = self.pattern.match(path)
        if not match:
            return None

        # Extract path parameters
        params = {}
        for i, param_name in enumerate(self.param_names):
            value = match.group(i + 1)

            # Basic type conversion
            try:
                # Try int first
                if value.isdigit():
                    params[param_name] = int(value)
                # Try float
                elif "." in value and value.replace(".", "").isdigit():
                    params[param_name] = float(value)
                else:
                    params[param_name] = value
            except ValueError:
                params[param_name] = value

        return params


class Router:
    """
    High-performance router for Rapid applications.

    Optimized for fast route matching and minimal overhead.
    """

    def __init__(self):
        self.routes: Dict[str, list] = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "DELETE": [],
            "PATCH": [],
            "HEAD": [],
            "OPTIONS": [],
        }

        # Cache for compiled routes (future optimization)
        self._route_cache = {}

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

        if method not in self.routes:
            self.routes[method] = []

        self.routes[method].append(route)

        # Clear cache when routes change
        self._route_cache.clear()

    def match(
        self, method: str, path: str
    ) -> Tuple[Optional[Callable], Dict[str, Any]]:
        """
        Find matching route for the given method and path.

        Returns (handler, path_params) tuple.
        """
        if method not in self.routes:
            return None, {}

        # Try to match against each route for this method
        for route in self.routes[method]:
            params = route.match(path)
            if params is not None:
                return route.handler, params

        return None, {}

    def get_routes(self) -> Dict[str, list]:
        """Get all registered routes"""
        return self.routes.copy()
