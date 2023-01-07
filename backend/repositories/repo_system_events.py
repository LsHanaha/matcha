"""Repository for connecting to system events."""
from databases.interfaces import Record

from backend.models import models_enums, models_events
from backend.repositories import (BaseAsyncRepository, postgres_reconnect,
                                  repo_interfaces)


class SystemEventsRepository(
    BaseAsyncRepository, repo_interfaces.SystemEventsRepoInterface
):
    """Repository for connecting to system events."""

    @postgres_reconnect
    async def store_new_event(
        self, system_event: models_events.SystemEventModel
    ) -> bool:
        """Insert new system event."""
        result: bool = await self.database_connection.execute(
            """
                INSERT INTO system_events(user_id, target_user_id, type_event)
                VALUES (:user_id, :target_user_id, :type_event)
                ON CONFLICT ON CONSTRAINT uc_users_pair_system
                DO NOTHING RETURNING 1;
            """,
            system_event.dict(exclude={"system_event", "event_time"}),
        )
        if not result:
            return False
        return bool(result)

    @postgres_reconnect
    async def collect_events_for_user(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_events.OutputEventModel]:
        """Collect system events."""
        result: list[Record] = await self.database_connection.fetch_all(
            """
            SELECT s_e.id as id, s_e.user_id as user_id, target_user_id, type_event, first_name, last_name, main_photo_name
            FROM 
            (
                SELECT id as e_id, user_id, target_user_id, type_event            
                FROM system_events            
                WHERE user_id = :user_id
            )  as s_e
            LEFT JOIN profiles as p
            ON p.user_id = s_e.target_user_id
            ORDER BY e_id DESC
            LIMIT :limit OFFSET :offset;
            """,
            {"user_id": user_id, "limit": limit, "offset": offset},
        )
        if not result:
            return []
        return [
            models_events.OutputEventModel(
                system_payload=models_events.RetrieveSystemEventsModel(**row._mapping),
                event_type=models_enums.WebsocketEventTypesEnum.SYSTEM.value,
            )
            for row in result
        ]

    async def update_system_events(self, user_id: int, target_user_id: int) -> bool:
        """Update system events, especially is_read status."""
        result: bool = await self.database_connection.execute(
            """
            UPDATE system_events
            SET is_read = TRUE
            WHERE user_id = :user_id AND target_user_id = :target_user_id;
            """,
            {"user_id": user_id, "target_user_id": target_user_id},
        )
        if not result:
            return False
        return bool(result)
