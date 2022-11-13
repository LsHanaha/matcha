"""Endpoints for interests."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.helpers import update_last_online
from backend.models import models_user
from backend.repositories import repo_interfaces

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.get("/interests/all/", response_model=list[models_user.Interests])
@inject
async def collect_all_interests(
    db_connection: repo_interfaces.InterestsRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.interests_repository]
    ),
    _=fastapi.Depends(update_last_online),
    authorize: AuthJWT = fastapi.Depends(),
) -> list[models_user.Interests]:
    """Collect all interests."""
    authorize.jwt_required()
    return await db_connection.collect_all_interests()


@ROUTER_OBJ.get("/interests/find/{name}/", response_model=list[models_user.Interests])
@inject
async def search_interests(
    name: str,
    db_connection: repo_interfaces.InterestsRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.interests_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> list[models_user.Interests]:
    """Search for interests by name."""
    authorize.jwt_required()
    return await db_connection.search_interests_by_name(name)


@ROUTER_OBJ.post("/interests/new/", response_model=models_user.Interests)
@inject
async def add_new_interest(
    name: str,
    db_connection: repo_interfaces.InterestsRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.interests_repository]
    ),
    _=fastapi.Depends(update_last_online),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_user.Interests:
    """Add new interest."""
    authorize.jwt_required()
    return await db_connection.insert_new_interest(name)
