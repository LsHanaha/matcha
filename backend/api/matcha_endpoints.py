"""Endpoint for searching and recommendations."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.mathca import matcha_search
from backend.models import models_enums, models_matcha, models_user
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/search/", response_model=models_matcha.SearchUsersModels)
@inject
async def search_users(
    params: models_matcha.SearchQueryModel,
    order_direction: models_enums.SearchOrderEnum = models_enums.SearchOrderEnum.ASC,
    offset: int = 0,
    limit: int = 10,
    order_by: str | None = None,
    search_service: matcha_search.MatchaSearch = fastapi.Depends(
        Provide[ioc.IOCContainer.matcha_search_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Search users by parameters."""
    if not settings_base.debug:
        authorize.jwt_required()

    return await search_service.find_users(
        params,
        order_by=order_by,
        order_direction=order_direction,
        offset=offset,
        limit=limit,
    )


@ROUTER_OBJ.get(
    "/recommendations/{user_id}/", response_model=list[models_user.UserProfile]
)
@inject
async def get_recommendations(
    user_id: int,
    recommendations_service: matcha_search.MatchaRecommendations = fastapi.Depends(
        Provide[ioc.IOCContainer.matcha_recommendations_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Get recommended users for user_id."""
    if not settings_base.debug:
        authorize.jwt_required()

    return await recommendations_service.get_recommendations(user_id)
