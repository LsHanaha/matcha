"""Endpoints for collection of events."""
import datetime

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.models import models_base, models_events
from backend.repositories import repo_interfaces
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.get(
    "/system/{user_id}/", response_model=list[models_events.RetrieveSystemEventsModel]
)
@inject
async def collect_system_events(
    user_id: int,
    db_connection: repo_interfaces.SystemEventsRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.system_events_repository]
    ),
    offset: int = 0,
    limit: int = 20,
    authorize: AuthJWT = fastapi.Depends(),
) -> list[models_events.RetrieveSystemEventsModel]:
    """Collect all system events."""
    if not settings_base.debug:
        authorize.jwt_required()
    return await db_connection.collect_system_events_for_user(user_id, offset, limit)


@ROUTER_OBJ.post("/system/{user_id}/", response_model=models_base.ResponseModel)
@inject
async def update_system_events(
    user_id: int,
    db_connection: repo_interfaces.SystemEventsRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.system_events_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_base.ResponseModel:
    """Update system events."""
    if not settings_base.debug:
        authorize.jwt_required()
    await db_connection.update_system_events(user_id)
    return models_base.ResponseModel(message="System events updated")


@ROUTER_OBJ.get(
    "/current-chats/{user_id}/",
    response_model=list[models_events.ChatBaseInfoModel],
)
@inject
async def collect_current_chats(
    user_id: int,
    db_connection: repo_interfaces.ChatRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.chat_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> list[models_events.ChatBaseInfoModel]:
    """Collect all current chats."""
    if not settings_base.debug:
        authorize.jwt_required()
    return await db_connection.get_current_chats_for_user(user_id)


@ROUTER_OBJ.get(
    "/messages/{chat_id}/", response_model=list[models_events.ChatEventModel]
)
@inject
async def collect_messages_in_chat(
    chat_id: int,
    offset: int = 0,
    limit: int = 20,
    timestamp: datetime.datetime | None = None,
    db_connection: repo_interfaces.ChatRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.chat_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> list[models_events.ChatEventModel]:
    """Collect messages in chat."""
    if not settings_base.debug:
        authorize.jwt_required()
    return await db_connection.retrieve_messages(chat_id, limit, offset, timestamp)


@ROUTER_OBJ.post("/messages/", response_model=models_base.ResponseModel)
@inject
async def update_messages_in_chat(
    user_pair: models_events.UserPairModel,
    db_connection: repo_interfaces.ChatRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.chat_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_base.ResponseModel:
    """Update messages in chat, that was sent from target_user_id to user_id,
    mark them as read by user_id."""
    if not settings_base.debug:
        authorize.jwt_required()
    await db_connection.update_is_read(user_pair.target_user_id, user_pair.user_id)
    return models_base.ResponseModel(status=True)
