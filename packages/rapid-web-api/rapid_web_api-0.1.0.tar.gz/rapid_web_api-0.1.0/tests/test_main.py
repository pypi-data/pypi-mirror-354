"""
Tests for the main Rapid application class
"""

import pytest

from rapid import Rapid


def test_rapid_initialization():
    """Test basic Rapid app initialization"""
    app = Rapid()
    assert app.title == "Rapid API"
    assert app.version == "0.1.0"
    assert not app.debug


def test_rapid_custom_initialization():
    """Test Rapid app with custom parameters"""
    app = Rapid(
        title="Test API", description="Test description", version="1.2.3", debug=True
    )
    assert app.title == "Test API"
    assert app.description == "Test description"
    assert app.version == "1.2.3"
    assert app.debug


def test_route_registration():
    """Test route registration with decorators"""
    app = Rapid()

    @app.get("/test")
    def test_handler():
        return {"message": "test"}

    # Check that route was registered
    routes = app.router.get_routes()
    assert len(routes["GET"]) == 1
    assert routes["GET"][0].path == "/test"


def test_multiple_routes():
    """Test registering multiple routes"""
    app = Rapid()

    @app.get("/")
    def root():
        return {"message": "root"}

    @app.post("/items")
    def create_item():
        return {"message": "created"}

    @app.get("/items/{item_id}")
    def get_item(item_id: int):
        return {"item_id": item_id}

    routes = app.router.get_routes()
    assert len(routes["GET"]) == 2
    assert len(routes["POST"]) == 1


def test_event_handlers():
    """Test startup/shutdown event handlers"""
    app = Rapid()

    startup_called = False
    shutdown_called = False

    @app.on_event("startup")
    def startup():
        nonlocal startup_called
        startup_called = True

    @app.on_event("shutdown")
    def shutdown():
        nonlocal shutdown_called
        shutdown_called = True

    # Events should be registered
    assert len(app._startup_handlers) == 1
    assert len(app._shutdown_handlers) == 1


if __name__ == "__main__":
    pytest.main([__file__])
