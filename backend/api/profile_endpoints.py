"""Endpoints for user's profile."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.models import models_base, models_user
from backend.repositories import repo_interfaces
from backend.repositories_redis.redis_avatars import UsersAvatarsRedisRepo
from backend.settings import settings_base

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.get("/profile/{user_id}/", response_model=models_user.UserProfile)
@inject
async def get_profile(
    user_id: int,
    profile_repository: repo_interfaces.ProfileRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.profile_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_user.UserProfile:
    """Get user profile."""
    if not settings_base.debug:
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
    profile_repository: repo_interfaces.ProfileRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.profile_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> models_base.ResponseModel:
    """Update profile for user."""
    if not settings_base.debug:
        authorize.jwt_required()
    profile_data.user_id = user_id
    result: bool = await profile_repository.update_user_profile(profile_data)
    return models_base.ResponseModel(status=result)


@ROUTER_OBJ.post("/avatars-store/", response_model=models_base.ResponseModel)
@inject
async def store_avatars(
    user_id: int,
    files: list[fastapi.UploadFile] = fastapi.File(...),
    user_avatars_repo: UsersAvatarsRedisRepo = fastapi.Depends(
        Provide[ioc.IOCContainer.avatars_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Method for storing user avatars."""
    if not settings_base.debug:
        authorize.jwt_required()
    new_files: list[models_user.UserAvatar] = [
        models_user.UserAvatar(name=file.filename, file=file.file.read())
        for file in files
    ]
    await user_avatars_repo.store_avatars(user_id, new_files)
    return models_base.ResponseModel(status=True)


@ROUTER_OBJ.get(
    "/avatars-retrieve/{user_id}/", response_model=list[models_user.UserAvatar]
)
@inject
async def retrieve_avatars(
    user_id: int,
    user_avatars_repo: UsersAvatarsRedisRepo = fastapi.Depends(
        Provide[ioc.IOCContainer.avatars_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Method for retrieving user avatars.

    Actual files is a bytes encoded in base64
    """
    if not settings_base.debug:
        authorize.jwt_required()
    user_avatars: list[
        models_user.UserAvatar
    ] = await user_avatars_repo.collect_avatars(user_id)
    return user_avatars


@ROUTER_OBJ.post("/avatars-delete/", response_model=models_base.ResponseModel)
@inject
async def delete_avatar(
    user_id: int,
    file_name: str,
    user_avatars_repo: UsersAvatarsRedisRepo = fastapi.Depends(
        Provide[ioc.IOCContainer.avatars_service]
    ),
    authorize: AuthJWT = fastapi.Depends(),
):
    """Method for removing avatar for a user."""
    if not settings_base.debug:
        authorize.jwt_required()
    result = await user_avatars_repo.delete_avatar(user_id, file_name)
    return models_base.ResponseModel(status=result)
