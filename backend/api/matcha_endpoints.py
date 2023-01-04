"""Endpoint for searching and recommendations."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.mathca.matcha_search import MatchaSearch
from backend.models import models_enums, models_matcha
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/search/", response_model=models_matcha.SearchUsersModels)
@inject
async def search_users(
    params: models_matcha.SearchQueryModel,
    order_direction: models_enums.SearchOrder = models_enums.SearchOrder.ASC,
    offset: int = 0,
    limit: int = 10,
    order_by: str | None = None,
    matcha_search: MatchaSearch = fastapi.Depends(
        Provide[ioc.IOCContainer.matcha_search_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Search users by parameters."""
    if not settings_base.debug:
        authorize.jwt_required()

    return await matcha_search.find_users(
        params,
        order_by=order_by,
        order_direction=order_direction,
        offset=offset,
        limit=limit,
    )
