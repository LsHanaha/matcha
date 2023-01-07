"""Module for handling websocket connections."""


import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.events import WebsocketConnectionManager
from backend.helpers import update_last_online
from backend.models import models_events
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.websocket("/")
@inject
async def websocket_endpoint(
    websocket: fastapi.WebSocket,
    token: str | None = fastapi.Query(default=None),
    _=fastapi.Depends(update_last_online),
    ws_manager: WebsocketConnectionManager = fastapi.Depends(
        Provide[ioc.IOCContainer.websocket_manager]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Handle income websocket events."""
    if not settings_base.debug:
        authorize.jwt_required("websocket", token=token)
    user_id: int = authorize.get_jwt_subject()
    await ws_manager.accept_connect(websocket, user_id)
    try:
        while True:
            event: models_events.ChatEventModel = await websocket.receive_json()

    except fastapi.websockets.WebSocketDisconnect:
        await ws_manager.handle_disconnect(user_id)
