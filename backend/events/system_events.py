"""Handling system websocket events."""

from backend.events import WebsocketConnectionManager
from backend.models import models_enums, models_events
from backend.repositories import repo_interfaces


class WebsocketSystemEvents:
    """Handle system websocket events."""

    def __init__(
        self,
        repo_system_events: repo_interfaces.SystemEventsRepoInterface,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
        ws_manager: WebsocketConnectionManager,
    ):
        self._repo_system_events: repo_interfaces.SystemEventsRepoInterface = (
            repo_system_events
        )
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile
        self._ws_manager: WebsocketConnectionManager = ws_manager

    async def handle_outcome_event(
        self,
        event_type: models_enums.SystemEventTypesEnum,
        user_id: int,
        target_user_id: int,
    ) -> None:
        """Handle outcome system event."""
        event: models_events.SystemEventModel = models_events.SystemEventModel(
            event_type=event_type.value, user_id=user_id, target_user_id=target_user_id
        )
        stored_event: models_events.SystemEventModel = (
            await self._repo_system_events.store_new_event(event)
        )
        event_creator_profile = await self._repo_profile.collect_user_profile(
            event.user_id
        )
        await self._ws_manager.send_personal_message(
            models_events.OutputEventModel(
                system_payload=models_events.RetrieveSystemEventsModel(
                    **stored_event.dict(), **event_creator_profile.dict()
                ),
                event_type=models_enums.WebsocketEventTypesEnum.SYSTEM.value,
            ).json(),
            event.target_user_id,
        )
