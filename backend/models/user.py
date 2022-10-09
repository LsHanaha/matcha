"""User's models."""

import typing

import pydantic
from pydantic import EmailStr


class UserAuth(pydantic.BaseModel):
    """User authentication model."""

    email: EmailStr = pydantic.Field(...)
    password: str = pydantic.Field(..., min_length=4, max_length=15)
    active: bool


class User(pydantic.BaseModel):
    """Model for user about table."""

    user_id: str
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
