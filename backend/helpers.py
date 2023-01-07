"""Helpers for project."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT

from backend import ioc
from backend.repositories import repo_interfaces
from backend.settings import settings_base


async def update_last_online(
    profile_repo: repo_interfaces.ProfileRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.profile_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> None:
    """Update last time visit for a user."""
    try:
        if not settings_base.debug:
            return
        authorize.jwt_required()
        await profile_repo.update_last_online(authorize.get_jwt_subject())
    except Exception:
        # If you can't update last online tolerate it and just write about in logger
        pass
