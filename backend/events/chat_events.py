"""Handler for websocket chat events."""


import fastapi

from backend.events import WebsocketConnectionManager
from backend.models import models_enums, models_events, models_user
from backend.repositories import repo_interfaces


class WebsocketChatEvents:
    """Handle chat events from and to websocket."""

    def __init__(
        self,
        repo_chat: repo_interfaces.ChatRepoInterface,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
        ws_manager: WebsocketConnectionManager,
    ):
        self._repo_chat: repo_interfaces.ChatRepoInterface = repo_chat
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile
        self._ws_manager: WebsocketConnectionManager = ws_manager

    async def handle_income_message(
        self, message: models_events.ChatEventModel
    ) -> None:
        """handle new message from usr_id to target_user_id."""
        await self.handle_is_read_messages(message.target_user_id, message.user_id)
        stored_message: models_events.ChatEventModel | None = (
            await self._repo_chat.store_new_message(message)
        )
        if not stored_message:
            raise fastapi.websockets.WebSocketDisconnect(
                fastapi.status.WS_1006_ABNORMAL_CLOSURE
            )
        await self.handle_outcome_message(stored_message)

    async def handle_outcome_message(
        self,
        message_raw: models_events.ChatEventModel | None = None,
        message_with_profile: models_events.RetrieveChatEventsModel | None = None,
    ) -> None:
        """Handle outcome message from user_id to target_user_id."""
        if not message_with_profile:
            user_info: models_user.UserProfile = (
                await self._repo_profile.collect_user_profile(
                    user_id=message_raw.user_id
                )
            )
            await self._ws_manager.send_personal_message(
                models_events.OutputEventModel(
                    chat_payload=models_events.ChatEventModel(
                        **user_info.dict(), **message_raw.dict()
                    ),
                    event_type=models_enums.WebsocketEventTypesEnum.CHAT,
                ).json(),
                message_raw.target_user_id,
            )
        else:
            await self._ws_manager.send_personal_message(
                models_events.OutputEventModel(
                    chat_payload=message_with_profile,
                    event_type=models_enums.WebsocketEventTypesEnum.CHAT,
                ).json(),
                message_with_profile.target_user_id,
            )
        raise fastapi.websockets.WebSocketDisconnect(
            fastapi.status.WS_1003_UNSUPPORTED_DATA
        )

    async def handle_is_read_messages(self, user_id: int, target_user_id: int) -> None:
        """Set messages is_read in chat for user_id, that was sent from
        target_user_id."""
        await self._repo_chat.update_is_read(user_id, target_user_id)
