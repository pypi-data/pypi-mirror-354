"""
Optimized JSON serialization utilities for Rapid
"""

import json
import time
import uuid
from datetime import date, datetime
from typing import Any, Dict, Union

# Try to import faster JSON libraries
try:
    import orjson

    HAS_ORJSON = True
except ImportError:
    HAS_ORJSON = False

try:
    import ujson

    HAS_UJSON = True
except ImportError:
    HAS_UJSON = False


class RapidJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for common Python types.

    Handles datetime, UUID, and other non-serializable objects.
    """

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif hasattr(obj, "__dict__"):
            # Handle dataclasses and simple objects
            return obj.__dict__
        elif hasattr(obj, "_asdict"):
            # Handle namedtuples
            return obj._asdict()
        else:
            return str(obj)


def dumps(
    obj: Any,
    *,
    ensure_ascii: bool = False,
    separators: tuple = (",", ":"),
    default: callable = None,
) -> str:
    """
    Fast JSON serialization with automatic library selection.

    Uses orjson > ujson > stdlib json for best performance.
    """
    start_time = time.perf_counter()

    if HAS_ORJSON:
        # orjson is fastest but returns bytes
        try:
            options = orjson.OPT_NON_STR_KEYS
            # Note: OPT_UTF8 was removed in newer orjson versions
            # The default behavior is already UTF-8
            result = orjson.dumps(obj, option=options, default=default).decode("utf-8")
            duration = time.perf_counter() - start_time
            perf_stats.record_call(duration, "orjson")
            return result
        except (TypeError, ValueError, AttributeError):
            # Fallback if orjson can't handle the object or has different API
            pass

    if HAS_UJSON:
        try:
            result = ujson.dumps(
                obj,
                ensure_ascii=ensure_ascii,
                escape_forward_slashes=False,
                default=default or RapidJSONEncoder().default,
            )
            duration = time.perf_counter() - start_time
            perf_stats.record_call(duration, "ujson")
            return result
        except (TypeError, ValueError):
            pass

    # Fallback to stdlib json
    result = json.dumps(
        obj,
        ensure_ascii=ensure_ascii,
        separators=separators,
        default=default or RapidJSONEncoder().default,
        cls=RapidJSONEncoder,
    )
    duration = time.perf_counter() - start_time
    perf_stats.record_call(duration, "stdlib")
    return result


def loads(s: Union[str, bytes]) -> Any:
    """
    Fast JSON deserialization with automatic library selection.

    Uses orjson > ujson > stdlib json for best performance.
    """

    if HAS_ORJSON:
        try:
            if isinstance(s, str):
                s = s.encode("utf-8")
            return orjson.loads(s)
        except (TypeError, ValueError, orjson.JSONDecodeError):
            pass

    if HAS_UJSON:
        try:
            if isinstance(s, bytes):
                s = s.decode("utf-8")
            return ujson.loads(s)
        except (TypeError, ValueError):
            pass

    # Fallback to stdlib json
    if isinstance(s, bytes):
        s = s.decode("utf-8")

    return json.loads(s)


def dumps_bytes(obj: Any, **kwargs) -> bytes:
    """
    Serialize object to JSON bytes for direct HTTP response.

    More efficient for web responses than string serialization.
    """

    if HAS_ORJSON:
        try:
            options = orjson.OPT_NON_STR_KEYS
            # Note: OPT_UTF8 was removed in newer orjson versions
            return orjson.dumps(obj, option=options, default=kwargs.get("default"))
        except (TypeError, ValueError, AttributeError):
            pass

    # Fallback to string then encode
    json_str = dumps(obj, **kwargs)
    return json_str.encode("utf-8")


class ResponseCache:
    """
    Simple in-memory cache for JSON responses.

    Useful for frequently requested static data.
    """

    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, bytes] = {}
        self.max_size = max_size
        self._access_order = []

    def get(self, key: str) -> bytes:
        """Get cached response"""
        if key in self.cache:
            # Move to end (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            return self.cache[key]
        return None

    def set(self, key: str, value: bytes):
        """Cache response"""
        if len(self.cache) >= self.max_size:
            # Remove least recently used
            oldest = self._access_order.pop(0)
            del self.cache[oldest]

        self.cache[key] = value
        self._access_order.append(key)

    def clear(self):
        """Clear all cached responses"""
        self.cache.clear()
        self._access_order.clear()


class PerformanceStats:
    """Track JSON serialization performance metrics"""

    def __init__(self):
        self.total_calls = 0
        self.total_time = 0.0
        self.cache_hits = 0
        self.cache_misses = 0
        self.library_usage = {"orjson": 0, "ujson": 0, "stdlib": 0}

    def record_call(self, duration: float, library: str, cache_hit: bool = False):
        self.total_calls += 1
        self.total_time += duration
        self.library_usage[library] += 1
        if cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1

    def get_stats(self) -> Dict[str, Any]:
        avg_time = self.total_time / max(self.total_calls, 1)
        cache_hit_rate = self.cache_hits / max(self.total_calls, 1)
        return {
            "total_calls": self.total_calls,
            "average_time_ms": avg_time * 1000,
            "cache_hit_rate": cache_hit_rate,
            "library_usage": self.library_usage,
        }


# Global instances
response_cache = ResponseCache(max_size=2000)  # Increased cache size
perf_stats = PerformanceStats()


def cached_json_response(obj: Any, cache_key: str = None, ttl: int = None) -> bytes:
    """
    Generate cached JSON response.

    Args:
        obj: Object to serialize
        cache_key: Custom cache key (auto-generated if None)
        ttl: Time-to-live in seconds (not implemented yet)

    Returns:
        JSON bytes ready for HTTP response
    """

    if cache_key is None:
        # Generate simple cache key from object hash
        cache_key = f"json_{hash(str(obj))}"

    cached = response_cache.get(cache_key)
    if cached is not None:
        return cached

    # Generate and cache response
    json_bytes = dumps_bytes(obj)
    response_cache.set(cache_key, json_bytes)

    return json_bytes


def benchmark_json_libs():
    """
    Benchmark available JSON libraries.

    Useful for development and optimization.
    """
    import time

    test_data = {
        "string": "Hello, World!" * 100,
        "number": 12345.67,
        "array": list(range(1000)),
        "nested": {
            "users": [
                {"id": i, "name": f"User {i}", "active": i % 2 == 0} for i in range(100)
            ]
        },
        "timestamp": datetime.now().isoformat(),
    }

    libraries = []

    if HAS_ORJSON:
        libraries.append(("orjson", orjson.dumps, orjson.loads))

    if HAS_UJSON:
        libraries.append(("ujson", ujson.dumps, ujson.loads))

    libraries.append(("stdlib", json.dumps, json.loads))

    print("JSON Library Benchmark")
    print("-" * 40)

    for name, dumps_func, loads_func in libraries:
        # Serialization benchmark
        start_time = time.time()
        for _ in range(1000):
            if name == "orjson":
                result = dumps_func(test_data)
            else:
                result = dumps_func(test_data)

        serialize_time = time.time() - start_time

        # Deserialization benchmark
        json_str = dumps_func(test_data)
        if name == "orjson" and isinstance(json_str, bytes):
            json_str = json_str
        elif isinstance(json_str, bytes):
            json_str = json_str.decode("utf-8")

        start_time = time.time()
        for _ in range(1000):
            loads_func(json_str)

        deserialize_time = time.time() - start_time

        print(
            f"{name:>10}: serialize={serialize_time:.3f}s, deserialize={deserialize_time:.3f}s"
        )


def get_performance_stats() -> Dict[str, Any]:
    """Get current JSON performance statistics"""
    return perf_stats.get_stats()


def clear_performance_stats():
    """Clear all performance statistics"""
    global perf_stats
    perf_stats = PerformanceStats()


if __name__ == "__main__":
    benchmark_json_libs()
