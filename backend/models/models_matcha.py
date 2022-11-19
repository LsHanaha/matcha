"""Models for searching users and recommendations."""
import pydantic


class SearchQueryModel(pydantic.BaseModel):
    """Model for query for search."""

    age_gap: None | tuple[int, int]
    fame_rating_gap: None | tuple[int, int]
    distance: None | int
    interests_id: None | list[int]
