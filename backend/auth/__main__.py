"""Initialize auth service for auth service."""

import fastapi_jwt_auth
from passlib.context import CryptContext

from backend import settings


@fastapi_jwt_auth.AuthJWT.load_config
def get_config():
    """Set config for fastapi_jwt_auth."""
    return settings.settings_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_is_password_valid(plain_password: str, hashed_password: str) -> bool:
    """Check is password valid."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    """Make a hash for a password."""
    return pwd_context.hash(password)
