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
            INSERT INTO preferences(user_id, sexual_preferences, min_fame_rating, min_age, max_age, max_distance_km)
            VALUES (:user_id, :sexual_preferences, :min_fame_rating, :min_age, :max_age, :max_distance_km)
            ON CONFLICT(user_id)
            DO UPDATE SET
            sexual_preferences=:sexual_preferences, min_fame_rating=:min_fame_rating, min_age=:min_age, 
                max_age=:max_age, max_distance_km=:max_distance_km
            WHERE user_id=:user_id
            RETURNING 1;
            """
        )
        return bool(result)
