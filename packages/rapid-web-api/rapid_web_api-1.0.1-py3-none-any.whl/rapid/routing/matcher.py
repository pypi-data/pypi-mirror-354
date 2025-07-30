"""
Route matching utilities for high-performance routing
"""

from typing import Any, Callable, Dict, List, Optional, Tuple

from .route import Route


class RouteMatcher:
    """
    High-performance route matcher with optimization strategies.

    Uses prefix trees and caching for fast route resolution.
    """

    def __init__(self):
        # Routes organized by method
        self.routes_by_method: Dict[str, List[Route]] = {}

        # Optimization caches
        self._static_routes: Dict[str, Dict[str, Route]] = {}  # method -> path -> route
        self._pattern_cache: Dict[str, Tuple[Route, Dict[str, Any]]] = {}

        # Pre-compiled static route lookup for maximum speed
        self._static_lookup: Dict[str, Route] = {}  # "METHOD:path" -> route

        # Route statistics for optimization
        self._match_stats: Dict[str, int] = {}

    def add_route(self, route: Route):
        """Add a route to the matcher"""
        method = route.method.upper()

        if method not in self.routes_by_method:
            self.routes_by_method[method] = []

        self.routes_by_method[method].append(route)

        # Check if this is a static route (no parameters)
        if not route.param_names:
            if method not in self._static_routes:
                self._static_routes[method] = {}
            self._static_routes[method][route.path] = route

            # Add to fast lookup table
            lookup_key = f"{method}:{route.path}"
            self._static_lookup[lookup_key] = route

        # Clear pattern cache when routes change
        self._pattern_cache.clear()

        # Sort routes by complexity (static first, then by parameter count)
        self._optimize_route_order(method)

    def _optimize_route_order(self, method: str):
        """Optimize route order for faster matching"""
        if method not in self.routes_by_method:
            return

        routes = self.routes_by_method[method]

        # Sort by:
        # 1. Static routes first (no parameters)
        # 2. Routes with fewer parameters
        # 3. Routes with more specific patterns (longer static parts)
        def route_priority(route: Route) -> Tuple[int, int, int]:
            param_count = len(route.param_names)
            static_length = len(
                [
                    p
                    for p in route.path.split("/")
                    if not (p.startswith("{") and p.endswith("}"))
                ]
            )
            return (param_count, -static_length, route.path.count("/"))

        routes.sort(key=route_priority)

    def match(self, method: str, path: str) -> Tuple[Optional[Route], Dict[str, Any]]:
        """
        Find matching route for the given method and path.

        Returns (route, path_params) tuple.
        """
        method = method.upper()

        # Ultra-fast path: check pre-compiled static routes first
        lookup_key = f"{method}:{path}"
        if lookup_key in self._static_lookup:
            route = self._static_lookup[lookup_key]
            self._update_stats(lookup_key)
            return route, {}

        # Check pattern cache
        cache_key = lookup_key
        if cache_key in self._pattern_cache:
            route, params = self._pattern_cache[cache_key]
            self._update_stats(cache_key)
            return route, params

        # Search through dynamic routes
        if method not in self.routes_by_method:
            return None, {}

        for route in self.routes_by_method[method]:
            if route.param_names:  # Skip static routes (already checked)
                params = route.match(path)
                if params is not None:
                    # Cache the result
                    self._pattern_cache[cache_key] = (route, params)
                    self._update_stats(cache_key)
                    return route, params

        return None, {}

    def _update_stats(self, cache_key: str):
        """Update route matching statistics"""
        self._match_stats[cache_key] = self._match_stats.get(cache_key, 0) + 1

    def get_stats(self) -> Dict[str, Any]:
        """Get route matching statistics for optimization"""
        total_matches = sum(self._match_stats.values())

        return {
            "total_matches": total_matches,
            "cache_size": len(self._pattern_cache),
            "static_routes": sum(
                len(routes) for routes in self._static_routes.values()
            ),
            "dynamic_routes": sum(
                len([r for r in routes if r.param_names])
                for routes in self.routes_by_method.values()
            ),
            "top_routes": sorted(
                self._match_stats.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }

    def clear_cache(self):
        """Clear pattern matching cache"""
        self._pattern_cache.clear()
        self._match_stats.clear()

    def get_all_routes(self) -> List[Route]:
        """Get all registered routes"""
        all_routes = []
        for routes in self.routes_by_method.values():
            all_routes.extend(routes)
        return all_routes
