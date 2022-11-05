"""Models for user preference."""

import pydantic

from backend.models import models_enums


class UserPreferences(pydantic.BaseModel):
    """Model for user preference."""

    user_id: int
    sexual_preferences: models_enums.SexualPreferencesEnum
    min_fame_rating: int
    min_age: int
    max_age: int
    max_distance_km: int
