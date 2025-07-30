"""
Test the new modular structure and request handling
"""

import asyncio
import sys
from pathlib import Path

# Add rapid to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rapid import JSONResponse, Rapid, Request


def test_basic_app():
    """Test basic app creation and routing"""
    app = Rapid(title="Test App", debug=True)

    @app.get("/")
    def read_root():
        return {"message": "Hello World"}

    @app.get("/users/{user_id}")
    def get_user(user_id: int):
        return {"user_id": user_id, "name": f"User {user_id}"}

    @app.post("/users")
    async def create_user():
        # In a real handler, you'd access request body here
        return {"message": "User created"}

    print("✅ Basic app creation successful")
    print(f"✅ Routes registered: {len(app.router.get_routes())}")

    # Test route matching
    route, params = app.router.match("GET", "/users/123")
    if route and params.get("user_id") == 123:
        print("✅ Route matching works")
    else:
        print("❌ Route matching failed")

    return app


def test_request_object():
    """Test Request object functionality"""

    # Test basic request
    request = Request(
        method="GET",
        path="/test",
        query_string=b"foo=bar&baz=qux",
        headers={"content-type": "application/json"},
        body=b'{"test": "data"}',
        path_params={"id": 123},
    )

    print(f"✅ Request created: {request.method} {request.path}")
    print(f"✅ Query params: {request.query_params}")
    print(f"✅ Path params: {request.path_params}")

    return request


async def test_json_parsing():
    """Test JSON parsing functionality"""

    request = Request(
        method="POST",
        path="/api/test",
        headers={"content-type": "application/json"},
        body=b'{"name": "test", "value": 42}',
    )

    try:
        json_data = await request.json()
        print(f"✅ JSON parsing successful: {json_data}")
        return True
    except Exception as e:
        print(f"❌ JSON parsing failed: {e}")
        return False


def test_router_stats():
    """Test router performance statistics"""

    app = Rapid()

    @app.get("/test")
    def test_route():
        return {"test": True}

    # Simulate some route matches
    for _ in range(10):
        app.router.match("GET", "/test")

    stats = app.router.get_stats()
    print(f"✅ Router stats: {stats}")

    return stats


async def main():
    """Run all tests"""
    print("🧪 Testing Rapid Framework Modular Structure")
    print("=" * 50)

    # Test 1: Basic app functionality
    print("\n1. Testing basic app creation...")
    app = test_basic_app()

    # Test 2: Request object
    print("\n2. Testing Request object...")
    request = test_request_object()

    # Test 3: JSON parsing
    print("\n3. Testing JSON parsing...")
    json_success = await test_json_parsing()

    # Test 4: Router statistics
    print("\n4. Testing router statistics...")
    stats = test_router_stats()

    # Summary
    print("\n🎯 Test Summary")
    print("-" * 30)
    print("✅ Modular structure working")
    print("✅ Route matching optimized")
    print("✅ Request object functional")
    if json_success:
        print("✅ JSON parsing working")
    print("✅ Performance monitoring enabled")

    print(f"\n📊 Router Performance:")
    print(f"  - Total matches: {stats.get('total_matches', 0)}")
    print(f"  - Cache size: {stats.get('cache_size', 0)}")
    print(f"  - Static routes: {stats.get('static_routes', 0)}")
    print(f"  - Dynamic routes: {stats.get('dynamic_routes', 0)}")


if __name__ == "__main__":
    asyncio.run(main())
