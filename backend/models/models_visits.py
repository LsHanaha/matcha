"""Models fore user visits."""

import datetime

import pydantic


class VisitedUserModel(pydantic.BaseModel):
    """Model for handling likes and visiting."""

    user_id: int
    target_user_id: int
    last_visit_time: datetime.datetime | None
    is_match: bool | None = False
    is_blocked: bool | None = False
    is_reported: bool | None = False
    is_paired: bool = False

    def check_is_blocked(self):
        """Set likes as false if love is gone."""
        if self.is_blocked or self.is_reported:
            self.is_match = False
            self.is_paired = False
            self.is_blocked = True


class MatchedUsers(pydantic.BaseModel):
    """Models for matched users."""

    id: int | None
    first_user_id: int
    second_user_id: int
