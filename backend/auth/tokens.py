"""Create tokens for auth service."""

from fastapi_jwt_auth import AuthJWT

from backend.settings import settings_jwt


def create_access_token(authorize: AuthJWT, user_id: int) -> str:
    """Create access token for user."""
    return authorize.create_access_token(
        subject=user_id, expires_time=settings_jwt.access_token_lifetime_sec
    )


def create_refresh_token(authorize: AuthJWT, user_id: int) -> str:
    """Create access token for user."""
    return authorize.create_refresh_token(subject=user_id)


def create_restore_token(authorize: AuthJWT, email: str) -> str:
    """Create restore token from email."""
    return authorize.create_access_token(
        subject=email, expires_time=settings_jwt.restore_token_lifetime_sec
    )
