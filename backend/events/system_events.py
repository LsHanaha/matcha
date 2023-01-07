"""Handling system websocket events."""

from backend.events import WebsocketConnectionManager
from backend.models import models_enums, models_events
from backend.repositories import repo_interfaces


class WebsocketSystemEvents:
    """Handle system websocket events."""

    def __init__(
        self,
        repo_system_events: repo_interfaces.SystemEventsRepoInterface,
        ws_manager: WebsocketConnectionManager,
    ):
        self._repo_system_events: repo_interfaces.SystemEventsRepoInterface = (
            repo_system_events
        )
        self._ws_manager: WebsocketConnectionManager = ws_manager

    async def handle_outcome_event(self, event: models_events.SystemEventModel) -> None:
        """Handle income system event."""
        await self._repo_system_events.store_new_event(event)
        await self._ws_manager.send_personal_message(
            models_events.OutputEventModel(
                system_payload=event,
                event_type=models_enums.WebsocketEventTypesEnum.SYSTEM.value,
            ).json(),
            event.target_user_id,
        )
