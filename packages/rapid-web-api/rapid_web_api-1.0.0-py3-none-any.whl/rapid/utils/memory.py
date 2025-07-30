"""
Memory optimization utilities for Rapid framework

Provides object pooling for Request/Response objects to reduce GC pressure
"""

import threading
from collections import deque
from typing import Any, Callable, Dict, Optional

from ..http.request import Request
from ..http.response import JSONResponse


class ObjectPool:
    """Generic object pool with thread safety"""

    def __init__(self, factory: Callable, max_size: int = 100):
        self.factory = factory
        self.max_size = max_size
        self._pool = deque()
        self._lock = threading.RLock()
        self._created_count = 0
        self._borrowed_count = 0
        self._returned_count = 0

    def get(self):
        """Get object from pool or create new one"""
        with self._lock:
            if self._pool:
                obj = self._pool.popleft()
                self._borrowed_count += 1
                return obj
            else:
                obj = self.factory()
                self._created_count += 1
                self._borrowed_count += 1
                return obj

    def put(self, obj):
        """Return object to pool"""
        with self._lock:
            if len(self._pool) < self.max_size:
                # Reset object state if possible
                if hasattr(obj, "reset"):
                    obj.reset()
                self._pool.append(obj)
                self._returned_count += 1

    def stats(self) -> Dict[str, int]:
        """Get pool statistics"""
        with self._lock:
            return {
                "pool_size": len(self._pool),
                "max_size": self.max_size,
                "created": self._created_count,
                "borrowed": self._borrowed_count,
                "returned": self._returned_count,
                "active": self._borrowed_count - self._returned_count,
            }

    def clear(self):
        """Clear the pool"""
        with self._lock:
            self._pool.clear()


class PooledRequest(Request):
    """Request object designed for pooling"""

    def reset(self):
        """Reset request state for reuse"""
        self.method = ""
        self.path = ""
        self.query_string = b""
        self.headers = {}
        self.body = b""
        self.path_params = {}

        # Clear caches
        self._json = None
        self._form = None
        self._query_params = None
        self._files = None

    def reinitialize(
        self,
        method: str,
        path: str,
        query_string: bytes = b"",
        headers: Dict[str, str] = None,
        body: bytes = b"",
        path_params: Dict[str, Any] = None,
    ):
        """Reinitialize with new request data"""
        self.method = method
        self.path = path
        self.query_string = query_string
        self.headers = headers or {}
        self.body = body
        self.path_params = path_params or {}

        # Clear caches
        self._json = None
        self._form = None
        self._query_params = None
        self._files = None


class PooledJSONResponse(JSONResponse):
    """JSON response object designed for pooling"""

    def reset(self):
        """Reset response state for reuse"""
        self.content = None
        self.status_code = 200
        self.headers = {"content-type": "application/json"}
        self.media_type = "application/json"
        self.cache_key = None
        self.use_cache = False

    def reinitialize(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        cache_key: Optional[str] = None,
        use_cache: bool = False,
    ):
        """Reinitialize with new response data"""
        self.content = content
        self.status_code = status_code
        self.headers = headers or {"content-type": "application/json"}
        self.headers.setdefault("content-type", "application/json")
        self.media_type = "application/json"
        self.cache_key = cache_key
        self.use_cache = use_cache


# Global object pools
request_pool = ObjectPool(lambda: PooledRequest("", ""), max_size=200)
response_pool = ObjectPool(lambda: PooledJSONResponse(), max_size=200)


class RequestPool:
    """High-level interface for request pooling"""

    @staticmethod
    def get_request(
        method: str,
        path: str,
        query_string: bytes = b"",
        headers: Dict[str, str] = None,
        body: bytes = b"",
        path_params: Dict[str, Any] = None,
    ) -> PooledRequest:
        """Get a pooled request object"""
        req = request_pool.get()
        req.reinitialize(method, path, query_string, headers, body, path_params)
        return req

    @staticmethod
    def return_request(request: PooledRequest):
        """Return request to pool"""
        request_pool.put(request)

    @staticmethod
    def stats() -> Dict[str, int]:
        """Get pool statistics"""
        return request_pool.stats()


class ResponsePool:
    """High-level interface for response pooling"""

    @staticmethod
    def get_json_response(
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        cache_key: Optional[str] = None,
        use_cache: bool = False,
    ) -> PooledJSONResponse:
        """Get a pooled JSON response object"""
        resp = response_pool.get()
        resp.reinitialize(content, status_code, headers, cache_key, use_cache)
        return resp

    @staticmethod
    def return_response(response: PooledJSONResponse):
        """Return response to pool"""
        response_pool.put(response)

    @staticmethod
    def stats() -> Dict[str, int]:
        """Get pool statistics"""
        return response_pool.stats()


def get_pool_stats() -> Dict[str, Dict[str, int]]:
    """Get statistics for all pools"""
    return {"requests": RequestPool.stats(), "responses": ResponsePool.stats()}


def clear_all_pools():
    """Clear all object pools"""
    request_pool.clear()
    response_pool.clear()
