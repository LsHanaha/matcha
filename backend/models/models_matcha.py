"""Models fore core functionality."""

import datetime

import pydantic


class VisitedUserModel(pydantic.BaseModel):
    """Model for handling likes and visiting."""

    id: int | None
    user_id: int
    target_user_id: int
    last_visit_time: datetime.datetime | None
    is_liked: bool | None = False
    is_blocked: bool | None = False
    is_reported: bool | None = False

    def check_is_blocked(self):
        """Set likes as false if love is gone."""
        if self.is_blocked or self.is_reported:
            self.is_liked = False
        if self.is_reported:
            self.is_blocked = True
