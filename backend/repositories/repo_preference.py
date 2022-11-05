"""Database repository for user preference."""

from databases.interfaces import Record

from backend.models import models_preferences
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class PreferenceDatabaseRepository(
    BaseAsyncRepository, interfaces.PreferenceRepositoryInterface
):
    """User preferences."""

    @postgres_reconnect
    async def collect_user_preference(
        self, user_id: int
    ) -> models_preferences.UserPreferences | None:
        """Collect user preferences."""
        preferences: Record | None = await self.database_connection.execute(
            """
                SELECT *
                FROM preferences
                WHERE user_id=:user_id; 
            """,
            {"user_id": user_id},
        )
        if not preferences:
            return None
        return models_preferences.UserPreferences(**dict(preferences))

    @postgres_reconnect
    async def update_user_preference(
        self, new_preferences: models_preferences.UserPreferences
    ) -> bool:
        """Update preferences for user."""

        result: int = await self.database_connection.execute(
            """
            
            """
        )
