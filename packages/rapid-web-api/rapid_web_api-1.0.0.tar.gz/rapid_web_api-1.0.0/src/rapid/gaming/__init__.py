"""
Gaming module for Rapid - Ultra-low latency real-time applications

Optimized for:
- Real-time gaming with <5ms response times
- WebSocket connections with binary protocols
- Player state synchronization
- High-frequency updates (60+ FPS)
- Minimal memory allocations in hot paths
"""

import asyncio
import json
import time
from typing import Any, Callable, Dict, List, Optional, Set

from ..core.app import Rapid
from ..http.response import JSONResponse

try:
    from ..server.websocket import (
        MessageType,
        WebSocketMessage,
        WebSocketServer,
        create_gaming_websocket,
    )

    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    WebSocketServer = None
    MessageType = None
    WebSocketMessage = None
    create_gaming_websocket = None


class GameServer(Rapid):
    """
    Game server optimized for ultra-low latency real-time applications.

    Features:
    - <5ms WebSocket response targets
    - Binary message protocols for speed
    - Player state management
    - Real-time event broadcasting
    - Anti-cheat integration hooks
    """

    def __init__(
        self,
        title: str = "Rapid Game Server",
        target_fps: int = 60,
        max_players: int = 1000,
        websocket_host: str = "localhost",
        websocket_port: int = 8765,
        **kwargs,
    ):
        super().__init__(title=title, **kwargs)
        self.target_fps = target_fps
        self.max_players = max_players
        self.websocket_host = websocket_host
        self.websocket_port = websocket_port

        # Gaming-specific optimizations
        self.connected_players: Dict[str, "GamePlayer"] = {}
        self.game_rooms: Dict[str, "GameRoom"] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}

        # WebSocket server for real-time communication
        self.websocket_server: Optional[WebSocketServer] = None

        # Performance tracking
        self.frame_times: List[float] = []
        self.player_update_times: List[float] = []

    def on_player_connect(self, handler: Callable):
        """Register handler for player connections"""
        if "player_connect" not in self.event_handlers:
            self.event_handlers["player_connect"] = []
        self.event_handlers["player_connect"].append(handler)
        return handler

    def on_player_disconnect(self, handler: Callable):
        """Register handler for player disconnections"""
        if "player_disconnect" not in self.event_handlers:
            self.event_handlers["player_disconnect"] = []
        self.event_handlers["player_disconnect"].append(handler)
        return handler

    def on_game_event(self, event_type: str):
        """Register handler for specific game events"""

        def decorator(handler: Callable):
            if event_type not in self.event_handlers:
                self.event_handlers[event_type] = []
            self.event_handlers[event_type].append(handler)
            return handler

        return decorator

    async def broadcast_to_players(
        self,
        message: Dict[str, Any],
        room_id: Optional[str] = None,
        exclude_player: Optional[str] = None,
    ):
        """
        Broadcast message to all players or players in a specific room.
        Optimized for minimal latency.
        """
        start_time = time.perf_counter()

        # Determine target players
        if room_id and room_id in self.game_rooms:
            target_players = self.game_rooms[room_id].players
        else:
            target_players = list(self.connected_players.keys())

        # Remove excluded player
        if exclude_player and exclude_player in target_players:
            target_players.remove(exclude_player)

        # Send message to all target players concurrently
        tasks = []
        for player_id in target_players:
            if player_id in self.connected_players:
                player = self.connected_players[player_id]
                tasks.append(player.send_message(message))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        # Track performance
        duration = time.perf_counter() - start_time
        self.player_update_times.append(duration)

        # Keep only last 100 measurements
        if len(self.player_update_times) > 100:
            self.player_update_times = self.player_update_times[-100:]

    async def start_websocket_server(self):
        """Start WebSocket server for real-time gaming communication"""
        if not WEBSOCKET_AVAILABLE:
            print(
                "Warning: WebSocket support not available. Install websockets: pip install websockets"
            )
            return

        if self.websocket_server:
            print("WebSocket server already running")
            return

        # Create gaming WebSocket server
        self.websocket_server = await create_gaming_websocket(
            self.websocket_host, self.websocket_port
        )

        # Add gaming-specific handlers
        await self._setup_gaming_websocket_handlers()

        # Start the server
        await self.websocket_server.start()
        print(
            f"Gaming WebSocket server started on ws://{self.websocket_host}:{self.websocket_port}"
        )

    async def stop_websocket_server(self):
        """Stop WebSocket server"""
        if self.websocket_server:
            await self.websocket_server.stop()
            self.websocket_server = None
            print("Gaming WebSocket server stopped")

    async def _setup_gaming_websocket_handlers(self):
        """Setup gaming-specific WebSocket event handlers"""
        if not self.websocket_server:
            return

        @self.websocket_server.on("player_join_room")
        async def on_player_join_room(message: WebSocketMessage):
            data = message.data
            room_id = data.get("room_id")
            player_id = message.client_id

            if room_id and player_id:
                # Add player to room
                if room_id not in self.game_rooms:
                    self.game_rooms[room_id] = GameRoom(room_id)

                if self.game_rooms[room_id].add_player(player_id):
                    # Join WebSocket room
                    self.websocket_server.manager.join_room(player_id, room_id)

                    # Notify room
                    await self.websocket_server.broadcast_to_room(
                        room_id,
                        MessageType.GAME_UPDATE,
                        {
                            "type": "player_joined",
                            "player_id": player_id,
                            "room_id": room_id,
                            "players_in_room": len(self.game_rooms[room_id].players),
                        },
                        priority=0,  # High priority
                    )

        @self.websocket_server.on("player_position_update")
        async def on_player_position_update(message: WebSocketMessage):
            data = message.data
            player_id = message.client_id

            x = data.get("x", 0)
            y = data.get("y", 0)
            z = data.get("z", 0)
            room_id = data.get("room_id")

            # Update player position
            if player_id in self.connected_players:
                self.connected_players[player_id].update_position(x, y, z)
            else:
                # Create new player
                self.connected_players[player_id] = GamePlayer(player_id)
                self.connected_players[player_id].update_position(x, y, z)

            # Broadcast to room members
            if room_id:
                await self.websocket_server.broadcast_to_room(
                    room_id,
                    MessageType.PLAYER_STATE,
                    {
                        "type": "position_update",
                        "player_id": player_id,
                        "position": {"x": x, "y": y, "z": z},
                        "timestamp": time.time(),
                    },
                    priority=0,  # High priority for position updates
                    exclude_client=player_id,
                )

        @self.websocket_server.on("game_action")
        async def on_game_action(message: WebSocketMessage):
            """Handle generic game actions (shooting, jumping, etc.)"""
            data = message.data
            action_type = data.get("action_type")
            room_id = data.get("room_id")
            player_id = message.client_id

            # Broadcast action to room
            if room_id and action_type:
                await self.websocket_server.broadcast_to_room(
                    room_id,
                    MessageType.GAME_UPDATE,
                    {
                        "type": "game_action",
                        "player_id": player_id,
                        "action_type": action_type,
                        "data": data,
                        "timestamp": time.time(),
                    },
                    priority=0,  # High priority for game actions
                    exclude_client=player_id,
                )

    async def broadcast_game_state(self, room_id: str, game_state: Dict[str, Any]):
        """Broadcast complete game state to room (use sparingly for performance)"""
        if self.websocket_server:
            await self.websocket_server.broadcast_to_room(
                room_id,
                MessageType.GAME_UPDATE,
                {"type": "game_state", "state": game_state, "timestamp": time.time()},
                priority=1,  # Normal priority for full state updates
            )

    async def send_to_player(
        self, player_id: str, message_type: str, data: Dict[str, Any]
    ):
        """Send message to specific player via WebSocket"""
        if self.websocket_server:
            await self.websocket_server.send_to_client(
                player_id,
                MessageType.GAME_UPDATE,
                {"type": message_type, "data": data, "timestamp": time.time()},
                priority=0,  # High priority for direct messages
            )

    def get_game_stats(self) -> Dict[str, Any]:
        """Get real-time game server statistics"""
        avg_frame_time = 0
        avg_update_time = 0

        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)

        if self.player_update_times:
            avg_update_time = sum(self.player_update_times) / len(
                self.player_update_times
            )

        stats = {
            "connected_players": len(self.connected_players),
            "active_rooms": len(self.game_rooms),
            "target_fps": self.target_fps,
            "avg_frame_time_ms": avg_frame_time * 1000,
            "avg_update_time_ms": avg_update_time * 1000,
            "max_players": self.max_players,
            "server_load": len(self.connected_players) / self.max_players,
            "websocket_enabled": WEBSOCKET_AVAILABLE
            and self.websocket_server is not None,
        }

        # Add WebSocket stats if available
        if self.websocket_server:
            stats["websocket_stats"] = self.websocket_server.get_stats()

        return stats


class GamePlayer:
    """Represents a connected game player with optimized messaging"""

    def __init__(self, player_id: str, websocket=None):
        self.player_id = player_id
        self.websocket = websocket
        self.last_ping = time.time()
        self.message_queue = asyncio.Queue(maxsize=100)
        self.position = {"x": 0, "y": 0, "z": 0}
        self.state = {}

    async def send_message(self, message: Dict[str, Any]):
        """Send message to player with error handling"""
        if self.websocket:
            try:
                await self.websocket.send_text(json.dumps(message))
            except Exception:
                # Player disconnected
                pass

    def update_position(self, x: float, y: float, z: float = 0):
        """Update player position with minimal overhead"""
        self.position["x"] = x
        self.position["y"] = y
        self.position["z"] = z


class GameRoom:
    """Manages a game room with multiple players"""

    def __init__(self, room_id: str, max_players: int = 10):
        self.room_id = room_id
        self.max_players = max_players
        self.players: Set[str] = set()
        self.game_state = {}
        self.created_at = time.time()

    def add_player(self, player_id: str) -> bool:
        """Add player to room if space available"""
        if len(self.players) < self.max_players:
            self.players.add(player_id)
            return True
        return False

    def remove_player(self, player_id: str):
        """Remove player from room"""
        self.players.discard(player_id)

    def is_empty(self) -> bool:
        """Check if room is empty"""
        return len(self.players) == 0


# Gaming-specific response types for ultra-fast responses
class BinaryGameResponse:
    """Binary response for minimal overhead gaming data"""

    def __init__(self, data: bytes, message_type: int = 0):
        self.data = data
        self.message_type = message_type

    async def __call__(self, scope: dict, receive: callable, send: callable):
        """Send binary data directly"""
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/octet-stream"],
                    [b"content-length", str(len(self.data)).encode()],
                ],
            }
        )
        await send({"type": "http.response.body", "body": self.data})


class GameEventResponse(JSONResponse):
    """Optimized JSON response for game events"""

    def __init__(self, event_type: str, data: Any, timestamp: Optional[float] = None):
        content = {
            "type": event_type,
            "data": data,
            "timestamp": timestamp or time.time(),
        }
        super().__init__(content=content, use_cache=True)

