"""Models for user preference."""

import pydantic

from backend.models import models_enums


class UserPreferences(pydantic.BaseModel):
    """Model for user preference."""

    user_id: int | None
    sexual_preference: models_enums.SexualPreferencesEnum | None
    min_fame_rating: int | None
    min_age: int | None
    max_age: int | None
    max_distance_km: int | None
