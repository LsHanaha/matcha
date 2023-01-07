"""Models for websocket events."""


import datetime

import pydantic

from backend.models import models_enums


class CommonForEvents(pydantic.BaseModel):
    """Common fields for all events."""

    user_id: int
    target_user_id: int
    event_time: datetime.datetime | None = None
    is_read: bool = False


class SystemEventModel(CommonForEvents):
    """System event model."""

    event_type: models_enums.SystemEventTypesEnum


class MessagesEventModel(CommonForEvents):
    """Messages event model."""

    text: str


class OutputEventModel(pydantic.BaseModel):
    """Output event model."""

    payload: SystemEventModel | MessagesEventModel
    event_type: models_enums.SocketTypesEnum
