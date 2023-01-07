"""Here lays the connection manager for handling connections and output
messages."""


import fastapi


class WebsocketConnectionManager:
    """Most simple websocket manager for low-level websockets usage."""

    def __init__(self):
        self.active_connections: dict[int, fastapi.WebSocket] = {}

    async def accept_connect(self, websocket: fastapi.WebSocket, user_id: int) -> None:
        """Connect websocket for user_id."""
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def handle_disconnect(self, user_id: int) -> None:
        """Remove websocket connection for user_id."""
        self.active_connections.pop(user_id)

    async def send_personal_message(self, message: str, target_user_id: int) -> None:
        """Send message to target_user_id."""
        websocket_connection: fastapi.WebSocket | None = self.active_connections.get(
            target_user_id
        )
        if not websocket_connection:
            raise fastapi.websockets.WebSocketDisconnect(
                code=fastapi.status.HTTP_404_NOT_FOUND, reason="Connection not found"
            )
        await websocket_connection.send_text(message)
