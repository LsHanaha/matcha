"""Base models for service."""

import pydantic


class ResponseModel(pydantic.BaseModel):
    """Model for server responses."""

    status: bool
