"""
Tests for the routing system
"""

import pytest

from rapid.routing import Route, Router


def test_route_creation():
    """Test basic route creation"""

    def handler():
        return {"test": True}

    route = Route("GET", "/test", handler)
    assert route.method == "GET"
    assert route.path == "/test"
    assert route.handler == handler


def test_static_path_matching():
    """Test matching static paths"""

    def handler():
        return {"test": True}

    route = Route("GET", "/users", handler)

    # Should match exact path
    params = route.match("/users")
    assert params == {}

    # Should not match different paths
    assert route.match("/user") is None
    assert route.match("/users/") is None
    assert route.match("/api/users") is None


def test_path_parameter_matching():
    """Test matching paths with parameters"""

    def handler(user_id):
        return {"user_id": user_id}

    route = Route("GET", "/users/{user_id}", handler)

    # Should extract integer parameter
    params = route.match("/users/123")
    assert params == {"user_id": 123}

    # Should extract string parameter
    params = route.match("/users/abc")
    assert params == {"user_id": "abc"}

    # Should not match without parameter
    assert route.match("/users/") is None
    assert route.match("/users") is None


def test_multiple_path_parameters():
    """Test paths with multiple parameters"""

    def handler(user_id, item_id):
        return {"user_id": user_id, "item_id": item_id}

    route = Route("GET", "/users/{user_id}/items/{item_id}", handler)

    params = route.match("/users/123/items/456")
    assert params == {"user_id": 123, "item_id": 456}

    params = route.match("/users/abc/items/def")
    assert params == {"user_id": "abc", "item_id": "def"}


def test_router_registration():
    """Test router route registration"""
    router = Router()

    @router.route("GET", "/test")
    def test_handler():
        return {"test": True}

    routes = router.get_routes()
    assert len(routes["GET"]) == 1
    assert routes["GET"][0].path == "/test"


def test_router_matching():
    """Test router route matching"""
    router = Router()

    @router.route("GET", "/users/{user_id}")
    def get_user(user_id):
        return {"user_id": user_id}

    @router.route("POST", "/users")
    def create_user():
        return {"created": True}

    # Test GET route matching
    handler, params = router.match("GET", "/users/123")
    assert handler == get_user
    assert params == {"user_id": 123}

    # Test POST route matching
    handler, params = router.match("POST", "/users")
    assert handler == create_user
    assert params == {}

    # Test non-existent route
    handler, params = router.match("DELETE", "/users/123")
    assert handler is None
    assert params == {}


def test_router_method_not_allowed():
    """Test router behavior with unsupported methods"""
    router = Router()

    @router.route("GET", "/test")
    def get_handler():
        return {"method": "GET"}

    # Should not match different method
    handler, params = router.match("POST", "/test")
    assert handler is None
    assert params == {}


def test_root_path():
    """Test root path handling"""

    def handler():
        return {"message": "root"}

    route = Route("GET", "/", handler)

    params = route.match("/")
    assert params == {}

    # Should not match other paths
    assert route.match("") is None
    assert route.match("/test") is None


if __name__ == "__main__":
    pytest.main([__file__])
