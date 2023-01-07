"""User's models."""

import datetime

import pydantic
from pydantic import EmailStr

from backend.models import models_enums


class UserLogin(pydantic.BaseModel):
    """Model for logging user."""

    username: str = pydantic.Field(..., min_length=4, max_length=12)
    password: str = pydantic.Field(..., min_length=4, max_length=15)


class UserAuth(UserLogin):
    """User authentication model."""

    id: int | None
    email: EmailStr = pydantic.Field(...)
    is_active: bool | None = False


class UserProfileEventsModel(pydantic.BaseModel):
    """User profile model for events."""

    first_name: str
    last_name: str
    main_photo_name: str


class UserProfile(UserProfileEventsModel):
    """Model for user about table."""

    user_id: int | None
    birthday: datetime.date
    gender: models_enums.GenderEnum
    sexual_orientation: models_enums.SexualPreferencesEnum = (
        models_enums.SexualPreferencesEnum.BI
    )
    biography: str | None
    interests: list[int]
    city: str

    def _is_profile_filled(self):
        """Check is user fill his/her profile."""
        for key, val in self.dict().items():
            if not val:
                if key in (self.biography, self.user_id):
                    continue
                return False
        return True


class Interests(pydantic.BaseModel):
    """Model for interests."""

    id: int
    name: str


class LoginResponse(pydantic.BaseModel):
    """Return tokens after authentication."""

    access_token: str
    refresh_token: str


class UserAvatar(pydantic.BaseModel):
    """Model for user avatar."""

    name: str
    file: bytes
