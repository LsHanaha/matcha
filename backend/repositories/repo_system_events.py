"""Repository for connecting to system events."""
from databases.interfaces import Record

from backend.models import models_enums, models_events
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class SystemEventsRepository(
    BaseAsyncRepository, repo_interfaces.SystemEventsRepoInterface
):
    """Repository for connecting to system events."""

    @postgres_reconnect
    async def store_new_event(
        self, system_event: models_events.SystemEventModel
    ) -> models_events.SystemEventModel | None:
        """Insert new system event."""
        result: Record = await self.database_connection.fetch_one(
            """
                INSERT INTO system_events(user_id, target_user_id, type_event)
                VALUES (:user_id, :target_user_id, :type_event)
                ON CONFLICT ON CONSTRAINT uc_users_pair_system
                DO NOTHING RETURNING *;
            """,
            system_event.dict(exclude={"system_event", "event_time"}),
        )
        if not result:
            return None
        return models_events.SystemEventModel(**result._mapping)

    @postgres_reconnect
    async def collect_system_events_for_user(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_events.RetrieveSystemEventsModel]:
        """Collect system events."""
        result: list[Record] = await self.database_connection.fetch_all(
            """
            SELECT e_id as id, s_e.user_id as user_id, target_user_id, type_event, first_name, last_name, main_photo_name
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
            models_events.RetrieveSystemEventsModel(**row._mapping) for row in result
        ]

    async def update_system_events(self, user_id: int) -> bool:
        """Update system events, especially is_read status."""
        result: bool = await self.database_connection.execute(
            """
            UPDATE system_events
            SET is_read = TRUE
            WHERE user_id = :user_id AND is_read = false AND event_time < NOW();
            """,
            {"user_id": user_id},
        )
        if not result:
            return False
        return bool(result)
