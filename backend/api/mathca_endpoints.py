"""Api for matching users."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.models import models_base, models_matcha
from backend.repositories import repo_interfaces

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/visited-users/", response_model=models_base.ResponseModel)
@inject
async def block_users(
    reported_user: models_matcha.VisitedUserModel,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.visited_users_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Block, report or like user."""
    authorize.jwt_required()
    reported_user.check_is_blocked()
    result: bool = await matcha_db.update_visited_users(reported_user)
    return models_base.ResponseModel(status=result)


@ROUTER_OBJ.get(
    "/visited-users/{user_id}/", response_model=list[models_matcha.VisitedUserModel]
)
@inject
async def collect_visited_users(
    user_id: int,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.visited_users_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect visited users for specific user."""
    authorize.jwt_required()
    result: list[
        models_matcha.VisitedUserModel
    ] = await matcha_db.collect_users_except_blocked(user_id)
    return result


@ROUTER_OBJ.get(
    "/visited-users/blocked/{user_id}/",
    response_model=list[models_matcha.VisitedUserModel],
)
@inject
async def collect_blocked_users(
    user_id: int,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.visited_users_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect blocked users for specific user."""
    authorize.jwt_required()
    result: list[
        models_matcha.VisitedUserModel
    ] = await matcha_db.collect_users_blocked(user_id)
    return result


@ROUTER_OBJ.get(
    "/visited-users/visitors/{target_user_id}",
    response_model=models_matcha.VisitedUserModel,
)
@inject
async def collect_visits(
    target_user_id: int,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.visited_users_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect blocked users for specific user."""
    authorize.jwt_required()
    result: list[models_matcha.VisitedUserModel] = await matcha_db.visitors(
        target_user_id
    )
    return result
