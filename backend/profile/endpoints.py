"""Endpoints for user's profile."""


import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from backend import ioc
from backend.auth import tokens
from backend.models import base as models_base
from backend.models import user as models_user
from backend.repositories import profile as profile_repositories

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.get("/profile/{user_id}/", response_model=models_user.UserProfile)
@inject
async def get_profile(
    user_id: int,
    profile_repository: profile_repositories.UserProfileDatabaseRepository = fastapi.Depends(
        Provide[ioc.IOCContainer.profile_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_user.UserProfile:
    """Get user profile."""
    authorize.jwt_required()
    user_profile: models_user.UserProfile | None = (
        await profile_repository.collect_user_profile(user_id)
    )
    if not user_profile:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="Profile for such user not found!",
        )
    return user_profile


@ROUTER_OBJ.post("/profile/{user_id}/", response_model=models_base.ResponseModel)
@inject
async def update_profile(
    user_id: int,
    profile_data: models_user.UserProfile,
    profile_repository: profile_repositories.UserProfileDatabaseRepository = fastapi.Depends(
        Provide[ioc.IOCContainer.profile_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_base.ResponseModel:
    """Update profile for user."""
    authorize.jwt_required()
    profile_data.user_id = user_id
    result: bool = await profile_repository.update_user_profile(profile_data)
    return models_base.ResponseModel(status=result)
