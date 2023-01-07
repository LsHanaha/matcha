"""Endpoints for collection of events."""
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
