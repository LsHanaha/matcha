"""Models for websocket events."""


import datetime

import pydantic

from backend.models import models_enums, models_user


class CommonForEvents(pydantic.BaseModel):
    """Common fields for all events."""

    id: int | None = None
    user_id: int
    target_user_id: int
    event_time: datetime.datetime | None = None
    is_read: bool = False


class SystemEventModel(CommonForEvents):
    """System event model for handling system messages to users."""

    event_type: models_enums.SystemEventTypesEnum


class ChatEventModel(CommonForEvents):
    """Chat event model for handling messages from/to users."""

    text: str
    matcha_pair_id: int | None = None


class RetrieveSystemEventsModel(SystemEventModel, models_user.UserProfileEventsModel):
    """Model for retrieving system events."""


class RetrieveChatEventsModel(ChatEventModel, models_user.UserProfileEventsModel):
    """Model for retrieving chat events."""


class IncomeEventModel(ChatEventModel):
    """Income event, right now uses only for chat."""


class OutputEventModel(pydantic.BaseModel):
    """Output event model."""

    system_payload: RetrieveSystemEventsModel | None = None
    chat_payload: RetrieveChatEventsModel | None = None
    event_type: models_enums.WebsocketEventTypesEnum
