"""Api for matching users."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.models import models_base, models_matcha
from backend.repositories import repo_interfaces

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/block-users/", response_model=models_base.ResponseModel)
@inject
async def block_users(
    reported_user: models_matcha.BlockUserModel,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.matcha_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Block or report user."""
    authorize.jwt_required()
    result: bool = await matcha_db.block_user(reported_user)
    return models_base.ResponseModel(status=result)


@ROUTER_OBJ.get(
    "/block-users/{user_id}/", response_model=list[models_matcha.BlockUserModel]
)
@inject
async def collect_block_users(
    user_id: int,
    matcha_db: repo_interfaces.MatchaRepoInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.matcha_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Collect blocked users for specific user."""
    authorize.jwt_required()
    result: list[models_matcha.BlockUserModel] = await matcha_db.collect_blocked_users(
        user_id
    )
    return result
