"""User can set his/her preference for search."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.helpers import update_last_online
from backend.models import models_base, models_preferences
from backend.repositories import repo_interfaces
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.get(
    "/preferences/{user_id}/", response_model=models_preferences.UserPreferences
)
@inject
async def get_preferences(
    user_id: int,
    preferences_repo: repo_interfaces.PreferenceRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.preferences_repository]
    ),
    _=fastapi.Depends(update_last_online),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_preferences.UserPreferences:
    """Get user's preferences."""
    if not settings_base.debug:
        authorize.jwt_required()
    user_preferences: models_preferences.UserPreferences | None = (
        await preferences_repo.collect_user_preference(user_id)
    )
    if not user_preferences:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Preferences for such user not found!",
        )
    return user_preferences


@ROUTER_OBJ.post("/profile/{user_id}/", response_model=models_base.ResponseModel)
@inject
async def update_preferences(
    user_id: int,
    new_preferences: models_preferences.UserPreferences,
    preferences_repo: repo_interfaces.PreferenceRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.preferences_repository]
    ),
    _=fastapi.Depends(update_last_online),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_base.ResponseModel:
    """Update user's preferences."""
    if not settings_base.debug:
        authorize.jwt_required()
    new_preferences.user_id = user_id
    result: bool = await preferences_repo.update_user_preference(new_preferences)
    return models_base.ResponseModel(status=result)
