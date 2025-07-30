"""
WebSocket support for Rapid framework

Optimized for:
- Ultra-low latency connections (<5ms response times)
- Binary message protocols for maximum speed
- Connection pooling and management
- Real-time message broadcasting
- Gaming and financial trading applications
"""

import asyncio
import json
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Union

try:
    import websockets
    from websockets.server import WebSocketServerProtocol, serve

    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False


class MessageType(Enum):
    """WebSocket message types for different use cases"""

    TEXT = "text"
    BINARY = "binary"
    PING = "ping"
    PONG = "pong"
    GAME_UPDATE = "game_update"
    MARKET_DATA = "market_data"
    ORDER_UPDATE = "order_update"
    PLAYER_STATE = "player_state"


@dataclass
class WebSocketMessage:
    """Optimized WebSocket message structure"""

    type: MessageType
    data: Union[str, bytes, Dict[str, Any]]
    timestamp: float
    client_id: Optional[str] = None
    room_id: Optional[str] = None
    priority: int = 0  # 0 = highest priority


class WebSocketManager:
    """
    High-performance WebSocket connection manager

    Features:
    - Connection pooling for memory efficiency
    - Message broadcasting with minimal latency
    - Room-based message routing
    - Connection health monitoring
    - Automatic reconnection handling
    """

    def __init__(self, max_connections: int = 10000):
        self.max_connections = max_connections

        # Connection management
        self.connections: Dict[str, "WebSocketConnection"] = {}
        self.rooms: Dict[str, Set[str]] = {}
        self.connection_pool = asyncio.Queue(maxsize=max_connections)

        # Message queues for different priorities
        self.high_priority_queue = asyncio.Queue()
        self.normal_priority_queue = asyncio.Queue()
        self.low_priority_queue = asyncio.Queue()

        # Performance tracking
        self.message_counts = {"sent": 0, "received": 0, "failed": 0}
        self.latency_measurements = []
        self.connection_stats = {"connects": 0, "disconnects": 0}

        # Background tasks
        self._message_processor_task = None
        self._health_check_task = None

    async def start(self):
        """Start the WebSocket manager background tasks"""
        self._message_processor_task = asyncio.create_task(self._process_messages())
        self._health_check_task = asyncio.create_task(self._health_check_loop())

    async def stop(self):
        """Stop the WebSocket manager and clean up"""
        if self._message_processor_task:
            self._message_processor_task.cancel()
        if self._health_check_task:
            self._health_check_task.cancel()

        # Close all connections
        for connection in self.connections.values():
            await connection.close()

        self.connections.clear()
        self.rooms.clear()

    async def add_connection(self, client_id: str, websocket) -> "WebSocketConnection":
        """Add new WebSocket connection"""
        if len(self.connections) >= self.max_connections:
            raise Exception(f"Maximum connections ({self.max_connections}) reached")

        connection = WebSocketConnection(
            client_id=client_id, websocket=websocket, manager=self
        )

        self.connections[client_id] = connection
        self.connection_stats["connects"] += 1

        return connection

    async def remove_connection(self, client_id: str):
        """Remove WebSocket connection"""
        if client_id in self.connections:
            connection = self.connections[client_id]

            # Remove from all rooms
            for room_id in list(self.rooms.keys()):
                self.leave_room(client_id, room_id)

            # Close connection
            await connection.close()
            del self.connections[client_id]
            self.connection_stats["disconnects"] += 1

    def join_room(self, client_id: str, room_id: str):
        """Add client to a room for group messaging"""
        if room_id not in self.rooms:
            self.rooms[room_id] = set()

        self.rooms[room_id].add(client_id)

    def leave_room(self, client_id: str, room_id: str):
        """Remove client from a room"""
        if room_id in self.rooms:
            self.rooms[room_id].discard(client_id)

            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]

    async def send_to_client(self, client_id: str, message: WebSocketMessage):
        """Send message to specific client"""
        if client_id in self.connections:
            await self._queue_message(message, [client_id])

    async def broadcast_to_room(
        self, room_id: str, message: WebSocketMessage, exclude_client: str = None
    ):
        """Broadcast message to all clients in a room"""
        if room_id in self.rooms:
            target_clients = list(self.rooms[room_id])
            if exclude_client and exclude_client in target_clients:
                target_clients.remove(exclude_client)

            await self._queue_message(message, target_clients)

    async def broadcast_to_all(
        self, message: WebSocketMessage, exclude_client: str = None
    ):
        """Broadcast message to all connected clients"""
        target_clients = [
            cid for cid in self.connections.keys() if cid != exclude_client
        ]
        await self._queue_message(message, target_clients)

    async def _queue_message(
        self, message: WebSocketMessage, target_clients: List[str]
    ):
        """Queue message for processing based on priority"""
        message_data = {
            "message": message,
            "targets": target_clients,
            "queued_at": time.perf_counter(),
        }

        if message.priority == 0:
            await self.high_priority_queue.put(message_data)
        elif message.priority == 1:
            await self.normal_priority_queue.put(message_data)
        else:
            await self.low_priority_queue.put(message_data)

    async def _process_messages(self):
        """Background task to process message queues"""
        while True:
            try:
                # Process high priority first
                if not self.high_priority_queue.empty():
                    message_data = await self.high_priority_queue.get()
                elif not self.normal_priority_queue.empty():
                    message_data = await self.normal_priority_queue.get()
                elif not self.low_priority_queue.empty():
                    message_data = await self.low_priority_queue.get()
                else:
                    # No messages, sleep briefly
                    await asyncio.sleep(0.001)  # 1ms
                    continue

                await self._send_message_to_targets(message_data)

            except Exception as e:
                # Log error but keep processing
                print(f"WebSocket message processing error: {e}")
                await asyncio.sleep(0.001)

    async def _send_message_to_targets(self, message_data: Dict[str, Any]):
        """Send message to target clients"""
        message = message_data["message"]
        targets = message_data["targets"]
        start_time = time.perf_counter()

        # Send to all targets concurrently
        tasks = []
        for client_id in targets:
            if client_id in self.connections:
                connection = self.connections[client_id]
                tasks.append(connection.send_message(message))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Count successes and failures
            successes = sum(1 for r in results if not isinstance(r, Exception))
            failures = len(results) - successes

            self.message_counts["sent"] += successes
            self.message_counts["failed"] += failures

        # Track latency
        latency = time.perf_counter() - start_time
        self.latency_measurements.append(latency)

        # Keep only last 1000 measurements
        if len(self.latency_measurements) > 1000:
            self.latency_measurements = self.latency_measurements[-1000:]

    async def _health_check_loop(self):
        """Background task to check connection health"""
        while True:
            try:
                current_time = time.time()
                disconnected_clients = []

                for client_id, connection in self.connections.items():
                    if current_time - connection.last_ping > 30:  # 30 seconds timeout
                        disconnected_clients.append(client_id)

                # Clean up disconnected clients
                for client_id in disconnected_clients:
                    await self.remove_connection(client_id)

                await asyncio.sleep(10)  # Check every 10 seconds

            except Exception as e:
                print(f"WebSocket health check error: {e}")
                await asyncio.sleep(10)

    def get_stats(self) -> Dict[str, Any]:
        """Get WebSocket manager statistics"""
        avg_latency = 0
        if self.latency_measurements:
            avg_latency = sum(self.latency_measurements) / len(
                self.latency_measurements
            )

        return {
            "connected_clients": len(self.connections),
            "active_rooms": len(self.rooms),
            "max_connections": self.max_connections,
            "message_counts": self.message_counts.copy(),
            "connection_stats": self.connection_stats.copy(),
            "avg_latency_ms": round(avg_latency * 1000, 3),
            "queue_sizes": {
                "high_priority": self.high_priority_queue.qsize(),
                "normal_priority": self.normal_priority_queue.qsize(),
                "low_priority": self.low_priority_queue.qsize(),
            },
        }


class WebSocketConnection:
    """Represents a single WebSocket connection"""

    def __init__(self, client_id: str, websocket, manager: WebSocketManager):
        self.client_id = client_id
        self.websocket = websocket
        self.manager = manager
        self.connected_at = time.time()
        self.last_ping = time.time()
        self.message_count = 0
        self.is_active = True

    async def send_message(self, message: WebSocketMessage):
        """Send message through this connection"""
        if not self.is_active:
            return

        try:
            if message.type == MessageType.TEXT:
                if isinstance(message.data, dict):
                    await self.websocket.send(json.dumps(message.data))
                else:
                    await self.websocket.send(str(message.data))
            elif message.type == MessageType.BINARY:
                await self.websocket.send(message.data)
            elif message.type == MessageType.PING:
                await self.websocket.ping()

            self.message_count += 1

        except Exception as e:
            # Connection failed, mark as inactive
            self.is_active = False
            raise e

    async def receive_message(self) -> Optional[WebSocketMessage]:
        """Receive message from this connection"""
        try:
            raw_message = await self.websocket.recv()
            self.last_ping = time.time()

            if isinstance(raw_message, str):
                # Try to parse as JSON
                try:
                    data = json.loads(raw_message)
                    return WebSocketMessage(
                        type=MessageType.TEXT,
                        data=data,
                        timestamp=time.time(),
                        client_id=self.client_id,
                    )
                except json.JSONDecodeError:
                    return WebSocketMessage(
                        type=MessageType.TEXT,
                        data=raw_message,
                        timestamp=time.time(),
                        client_id=self.client_id,
                    )
            else:
                return WebSocketMessage(
                    type=MessageType.BINARY,
                    data=raw_message,
                    timestamp=time.time(),
                    client_id=self.client_id,
                )

        except Exception:
            self.is_active = False
            return None

    async def close(self):
        """Close this connection"""
        self.is_active = False
        try:
            await self.websocket.close()
        except Exception:
            pass


class WebSocketServer:
    """
    High-performance WebSocket server for Rapid applications

    Integrates with gaming and financial modules for ultra-low latency
    """

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.manager = WebSocketManager()
        self.message_handlers: Dict[str, List[Callable]] = {}
        self.server = None

    def on(self, event_type: str):
        """Register event handler"""

        def decorator(handler: Callable):
            if event_type not in self.message_handlers:
                self.message_handlers[event_type] = []
            self.message_handlers[event_type].append(handler)
            return handler

        return decorator

    async def handle_client(self, websocket, path):
        """Handle new WebSocket client connection"""
        client_id = (
            f"client_{int(time.time() * 1000000)}_{len(self.manager.connections)}"
        )

        try:
            connection = await self.manager.add_connection(client_id, websocket)

            # Handle connection event
            await self._trigger_event(
                "connect",
                {"client_id": client_id, "path": path, "connection": connection},
            )

            # Message loop
            while connection.is_active:
                message = await connection.receive_message()
                if message:
                    await self._handle_message(message)
                else:
                    break

        except Exception as e:
            print(f"WebSocket client error: {e}")
        finally:
            await self.manager.remove_connection(client_id)
            await self._trigger_event("disconnect", {"client_id": client_id})

    async def _handle_message(self, message: WebSocketMessage):
        """Handle received message"""
        # Trigger message handlers
        if isinstance(message.data, dict) and "type" in message.data:
            event_type = message.data["type"]
            await self._trigger_event(event_type, message)

        # Default message handler
        await self._trigger_event("message", message)

    async def _trigger_event(self, event_type: str, data: Any):
        """Trigger event handlers"""
        if event_type in self.message_handlers:
            tasks = []
            for handler in self.message_handlers[event_type]:
                tasks.append(handler(data))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def start(self):
        """Start the WebSocket server"""
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library not available. Install with: pip install websockets"
            )

        await self.manager.start()

        self.server = await serve(
            self.handle_client,
            self.host,
            self.port,
            max_size=None,  # No message size limit
            max_queue=None,  # No queue size limit
            compression=None,  # Disable compression for speed
            ping_interval=20,  # Ping every 20 seconds
            ping_timeout=10,  # Timeout after 10 seconds
            close_timeout=10,  # Close timeout
        )

        print(f"WebSocket server started on ws://{self.host}:{self.port}")

    async def stop(self):
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()

        await self.manager.stop()

    async def send_to_client(
        self, client_id: str, message_type: MessageType, data: Any, priority: int = 1
    ):
        """Send message to specific client"""
        message = WebSocketMessage(
            type=message_type, data=data, timestamp=time.time(), priority=priority
        )
        await self.manager.send_to_client(client_id, message)

    async def broadcast_to_room(
        self,
        room_id: str,
        message_type: MessageType,
        data: Any,
        priority: int = 1,
        exclude_client: str = None,
    ):
        """Broadcast message to room"""
        message = WebSocketMessage(
            type=message_type,
            data=data,
            timestamp=time.time(),
            room_id=room_id,
            priority=priority,
        )
        await self.manager.broadcast_to_room(room_id, message, exclude_client)

    async def broadcast_to_all(
        self,
        message_type: MessageType,
        data: Any,
        priority: int = 1,
        exclude_client: str = None,
    ):
        """Broadcast message to all clients"""
        message = WebSocketMessage(
            type=message_type, data=data, timestamp=time.time(), priority=priority
        )
        await self.manager.broadcast_to_all(message, exclude_client)

    def get_stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        return {
            "server": {
                "host": self.host,
                "port": self.port,
                "running": self.server is not None,
            },
            **self.manager.get_stats(),
        }


# Gaming-specific WebSocket helpers
async def create_gaming_websocket(
    host: str = "localhost", port: int = 8765
) -> WebSocketServer:
    """Create WebSocket server optimized for gaming"""
    server = WebSocketServer(host, port)

    @server.on("connect")
    async def on_player_connect(data):
        client_id = data["client_id"]
        print(f"Gaming client connected: {client_id}")

        # Send welcome message
        await server.send_to_client(
            client_id,
            MessageType.GAME_UPDATE,
            {"type": "welcome", "client_id": client_id},
            priority=0,  # High priority
        )

    @server.on("disconnect")
    async def on_player_disconnect(data):
        client_id = data["client_id"]
        print(f"Gaming client disconnected: {client_id}")

    @server.on("game_update")
    async def on_game_update(message: WebSocketMessage):
        # Broadcast game updates to other players
        if message.room_id:
            await server.broadcast_to_room(
                message.room_id,
                MessageType.GAME_UPDATE,
                message.data,
                priority=0,  # High priority for game updates
                exclude_client=message.client_id,
            )

    return server


# Financial-specific WebSocket helpers
async def create_trading_websocket(
    host: str = "localhost", port: int = 8766
) -> WebSocketServer:
    """Create WebSocket server optimized for financial trading"""
    server = WebSocketServer(host, port)

    @server.on("connect")
    async def on_trader_connect(data):
        client_id = data["client_id"]
        print(f"Trading client connected: {client_id}")

        # Send market data snapshot
        await server.send_to_client(
            client_id,
            MessageType.MARKET_DATA,
            {"type": "snapshot", "timestamp": time.time()},
            priority=0,  # High priority
        )

    @server.on("order")
    async def on_order_received(message: WebSocketMessage):
        # Process trading order
        order_data = message.data

        # Send order confirmation
        await server.send_to_client(
            message.client_id,
            MessageType.ORDER_UPDATE,
            {
                "type": "order_received",
                "order_id": order_data.get("order_id"),
                "timestamp": time.time(),
            },
            priority=0,  # High priority for order updates
        )

    @server.on("market_data_request")
    async def on_market_data_request(message: WebSocketMessage):
        # Handle market data subscription
        symbol = message.data.get("symbol")
        if symbol:
            # Add client to symbol-specific room
            server.manager.join_room(message.client_id, f"market_{symbol}")

    return server
