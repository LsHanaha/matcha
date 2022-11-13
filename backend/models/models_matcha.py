"""Models fore core functionality."""

import pydantic


class BlockUserModel(pydantic.BaseModel):
    """Model for blocking/reporting users."""

    id: int | None
    user_id: int
    target_user_id: int
    reported: bool | None
