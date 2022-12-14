"""Endpoints for auth service."""

import fastapi
from dependency_injector.wiring import Provide, inject
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from backend import ioc
from backend.api.locations import LocationService
from backend.auth import auth_handle_mail, auth_tokens
from backend.auth.__main__ import check_is_password_valid
from backend.helpers import update_last_online
from backend.models import models_user as user_models
from backend.repositories import repo_interfaces

ROUTER_OBJ: fastapi.APIRouter = fastapi.APIRouter()


@ROUTER_OBJ.post("/register/")
@inject
async def create_user(
    new_user: user_models.UserAuth,
    background_tasks: fastapi.BackgroundTasks,
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository],
    ),
) -> dict[str, bool]:
    """Create new user."""
    user_in_db: user_models.UserAuth | None = await db_repository.collect_user_from_db(
        email=new_user.email
    )
    if user_in_db:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_409_CONFLICT,
            detail="User with such email already exist",
        )
    user_id: int = await db_repository.create_user(new_user)
    # background_tasks.add_task(
    #     auth_handle_mail.send_activate_account_mail, user_id, new_user.email
    # )
    return {"status": bool(user_id)}


@ROUTER_OBJ.post("/login/", response_model=user_models.LoginResponse)
@inject
async def login_user(
    user: user_models.UserLogin,
    background_tasks: fastapi.BackgroundTasks,
    request: fastapi.Request,
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
    ),
    location_service: LocationService = fastapi.Depends(
        Provide[ioc.IOCContainer.location_service]
    ),
    _=fastapi.Depends(update_last_online),
    authorize: AuthJWT = fastapi.Depends(),
) -> user_models.LoginResponse:
    """Validate user and return tokens."""
    user_in_db: user_models.UserAuth = await db_repository.collect_user_from_db(
        username=user.username
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
    background_tasks.add_task(
        location_service.update_user_location, user_in_db.id, request.client.host
    )
    return user_models.LoginResponse(
        access_token=auth_tokens.create_access_token(authorize, user_in_db.id),
        refresh_token=auth_tokens.create_refresh_token(authorize, user_in_db.id),
    )


@ROUTER_OBJ.post("/activate/")
@inject
async def activate_user(
    activation_token: str,
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
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
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(AuthJWT),
) -> dict[str, str]:
    """Activate user."""

    authorize.jwt_refresh_token_required(token=refresh_token)
    user_id: int = authorize.get_jwt_subject()
    user_in_db: user_models.UserAuth = await db_repository.collect_user_from_db(
        user_id=user_id
    )
    if not user_in_db.is_active:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN, detail="User is not active"
        )
    return {"access_token": auth_tokens.create_access_token(authorize, user_id)}


@ROUTER_OBJ.post("/restore-password-query/")
@inject
async def restore_password_query(
    email: str,
    background_tasks: fastapi.BackgroundTasks,
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
    ),
) -> dict:
    """Query for restore token."""
    user_in_db: user_models.UserAuth | None = await db_repository.collect_user_from_db(
        email=email
    )
    if not user_in_db:
        raise fastapi.HTTPException(
            status_code=404, detail="User not found. Try different email"
        )
    # background_tasks.add_task(auth_handle_mail.send_password_restore_mail, email)
    return {"status": True}


@ROUTER_OBJ.post("/restore-password/")
@inject
async def restore_user_password(
    restore_token: str,
    new_password: str,
    db_repository: repo_interfaces.AuthRepositoryInterface = fastapi.Depends(
        Provide[ioc.IOCContainer.auth_repository]
    ),
    authorize: AuthJWT = fastapi.Depends(),
) -> dict:
    """Restore user password with restore token."""
    authorize.jwt_required(token=restore_token)
    user_id: int = authorize.get_jwt_subject()
    result: bool = await db_repository.update_password(new_password, user_id)
    return {"status": result}
