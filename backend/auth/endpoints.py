"""Endpoints for auth service."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from backend import ioc
from backend.auth import tokens
from backend.auth.__main__ import check_is_password_valid
from backend.models import user as user_models
from backend.repositories import auth as db_auth_repository

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/register/")
@inject
async def create_user(
    new_user: user_models.UserAuth,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository],
    ),
) -> dict[str, bool]:
    """Create new user."""
    user_in_db: user_models.UserAuth | None = await db_repository.collect_user_by_email(
        new_user.email
    )
    if user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="User with such email already exist",
        )
    result: bool = await db_repository.create_user(new_user)
    return {"status": result}


@ROUTER_OBJ.post("/login/", response_model=user_models.AuthResponse)
@inject
async def validate_user(
    user: user_models.UserAuth,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> user_models.AuthResponse:
    """Validate user and return tokens."""
    user_in_db: user_models.UserAuth = await db_repository.collect_user_by_email(
        user.email
    )
    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail="User with such credentials does not exist",
        )
    if not user_in_db.is_active:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="User is not active"
        )
    if not check_is_password_valid(user.password, user_in_db.password):
        raise AuthJWTException("Wrong username or password")
    return user_models.AuthResponse(
        access_token=tokens.create_access_token(authorize, user_in_db.id),
        refresh_token=tokens.create_refresh_token(authorize, user_in_db.id),
    )


@ROUTER_OBJ.post("/activate/")
@inject
async def activate_user(
    activation_token: str,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[db_auth_repository.UserAuthDatabaseResource]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> dict[str, bool]:
    """Activate user."""
    authorize.jwt_required(token=activation_token)
    await db_repository.activate_user(authorize.get_jwt_subject())
    return {"status": True}


@ROUTER_OBJ.post("/refresh-access/")
@inject
async def refresh_access_token(
    refresh_token: str,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[db_auth_repository.UserAuthDatabaseResource]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> dict[str, str]:
    """Activate user."""

    authorize.jwt_refresh_token_required(token=refresh_token)
    current_user: int = authorize.get_jwt_subject()
    user_in_db: user_models.UserAuth = await db_repository.collect_user_by_id(
        current_user
    )
    if not user_in_db.is_active:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="User is not active"
        )
    return {"access_token": tokens.create_access_token(authorize, current_user)}


@ROUTER_OBJ.post("/restore-password-query/")
@inject
async def restore_password_query(
    email: str,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[db_auth_repository.UserAuthDatabaseResource]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> bool:
    """Query for restore token."""


@ROUTER_OBJ.post("/restore-password/")
@inject
async def restore_user_password(
    restore_token: str,
    new_password: str,
    db_repository: db_auth_repository.UserAuthDatabaseResource = fastapi.Depends(
        Provide[db_auth_repository.UserAuthDatabaseResource]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> dict:
    """Restore user password with restore token."""
    authorize.jwt_required(token=restore_token)
    user_id: int = authorize.get_jwt_subject()
    result: bool = await db_repository.update_password(new_password, user_id)
    return {"status": result}
