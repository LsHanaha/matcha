"""User's models."""
import datetime
import typing

import pydantic
from pydantic import EmailStr

from backend.models import models_enums as enums_models


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

    user_id: int | None
    first_name: str
    last_name: str
    birthday: datetime.date
    gender: enums_models.GenderEnum
    sexual_preferences: enums_models.SexualPreferencesEnum = (
        enums_models.SexualPreferencesEnum.BI
    )
    biography: str | None
    main_photo_name: str
    interests: list[int]


class AuthResponse(pydantic.BaseModel):
    """Return tokens after authentication."""

    access_token: str
    refresh_token: str
