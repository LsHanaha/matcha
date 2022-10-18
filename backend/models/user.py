"""User's models."""

# import typing

import pydantic
from pydantic import EmailStr


class UserLogin(pydantic.BaseModel):
    """Model for logging user."""

    username: str = pydantic.Field(..., min_length=4, max_length=12)
    password: str = pydantic.Field(..., min_length=4, max_length=15)


class UserAuth(UserLogin):
    """User authentication model."""

    id: int | None
    email: EmailStr = pydantic.Field(...)
    is_active: bool | None = False


class UserProfile(pydantic.BaseModel):
    """Model for user about table."""

    user_id: int
    first_name: str
    last_name: str
    # gender: typing.Literal["male", "female", None]
    # preferences: list[str]
    # about: str | None
    # interests: list[str]


class AuthResponse(pydantic.BaseModel):
    """Return tokens after authentication."""

    access_token: str
    refresh_token: str
