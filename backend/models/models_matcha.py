"""Models for searching users and recommendations."""
import pydantic

from backend.models import models_user


class SearchQueryModel(pydantic.BaseModel):
    """Model for query for search."""

    user_id: int
    age_gap: None | tuple[int, int]
    fame_rating_gap: None | tuple[int, int]
    distance: None | int
    interests_id: None | list[str]


class SearchUsersModels(pydantic.BaseModel):
    """Return founded users and their total amount."""

    users: list[models_user.UserProfile]
    amount: int = 0
