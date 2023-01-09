"""Here lays the connection manager for handling connections and output
messages."""


import fastapi


class WebsocketConnectionManager:
    """Most simple websocket manager for low-level websockets usage."""

    def __init__(self):
        self._active_connections: dict[int, fastapi.WebSocket] = {}

    async def accept_connect(self, websocket: fastapi.WebSocket, user_id: int) -> None:
        """Connect websocket for user_id."""
        await websocket.accept()
        self._active_connections[user_id] = websocket

    async def handle_disconnect(self, user_id: int) -> None:
        """Remove websocket connection for user_id."""
        connection: fastapi.WebSocket = self._active_connections.pop(user_id)
        await connection.close(reason="Something went wrong. Try to reconnect.")

    async def send_personal_message(self, message: str, target_user_id: int) -> bool:
        """Send message to target_user_id."""
        websocket_connection: fastapi.WebSocket | None = self._active_connections.get(
            target_user_id
        )
        if websocket_connection:
            await websocket_connection.send_text(message)
            return True
        return False
