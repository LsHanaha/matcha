"""Api for matching users."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.mathca import matches
from backend.models import models_base, models_matcha, models_user
from backend.repositories import repo_interfaces

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/", response_model=models_base.ResponseModel)
@inject
async def update_visit(
    visited_user: models_matcha.VisitedUserModel,
    relationship_db: matches.UsersRelationships = fastapi.Depends(
        Provide[ioc.IOCContainer.user_relationships]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """New visit for user, can change block, like, etc."""
    authorize.jwt_required()
    visited_user.check_is_blocked()
    result: bool = await relationship_db.update_visited(visited_user)
    return models_base.ResponseModel(status=result)


@ROUTER_OBJ.get("/{user_id}/", response_model=list[models_user.UserProfile])
@inject
async def collect_visited_users(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    relationship_db: matches.UsersRelationships = fastapi.Depends(
        Provide[ioc.IOCContainer.user_relationships]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect visited users for specific user."""
    authorize.jwt_required()
    result: list[
        models_user.UserProfile
    ] = await relationship_db.collect_visited_except_banned(user_id, offset, limit)
    return result


@ROUTER_OBJ.get(
    "/blocked/{user_id}/",
    response_model=list[models_user.UserProfile],
)
@inject
async def collect_blocked_users(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    relationship_db: matches.UsersRelationships = fastapi.Depends(
        Provide[ioc.IOCContainer.user_relationships]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect blocked users for specific user."""
    authorize.jwt_required()
    result: list[
        models_user.UserProfile
    ] = await relationship_db.collect_visited_banned(user_id, offset, limit)
    return result


@ROUTER_OBJ.get(
    "/visitors/{user_id}",
    response_model=list[models_user.UserProfile],
)
@inject
async def collect_visitors(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    relationship_db: matches.UsersRelationships = fastapi.Depends(
        Provide[ioc.IOCContainer.user_relationships]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect users who saw user_id profile."""
    authorize.jwt_required()
    result: list[models_user.UserProfile] = await relationship_db.collect_visitors(
        user_id, offset, limit
    )
    return result
