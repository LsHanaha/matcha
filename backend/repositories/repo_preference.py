"""Database repository for user preference."""

from databases.interfaces import Record

from backend.models import models_enums, models_preferences, models_user
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class PreferenceDatabaseRepository(
    BaseAsyncRepository, repo_interfaces.PreferenceRepositoryInterface
):
    """User preferences."""

    @postgres_reconnect
    async def collect_user_preference(
        self, user_id: int
    ) -> models_preferences.UserPreferences | None:
        """Collect user preferences."""
        preferences: Record | None = await self.database_connection.fetch_one(
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
            """,
            {**new_preferences.dict()},
        )
        return bool(result)

    async def determine_sexual_preferences_for_user(
        self,
        user_profile: models_user.UserProfile,
    ) -> str:
        """Prepare search query for expected gender and preferences."""
        expected_preferences: list[str]
        if (
            user_profile.sexual_orientation
            == models_enums.SexualPreferencesEnum.HOMOSEXUAL
        ):
            expected_preferences = [
                str(models_enums.SexualPreferencesEnum.HOMOSEXUAL),
                str(models_enums.SexualPreferencesEnum.BI),
            ]
            return f"sexual_orientation in ({','.join(expected_preferences)}) AND gender={user_profile.gender}"
        elif (
            user_profile.sexual_orientation
            == models_enums.SexualPreferencesEnum.HETEROSEXUAL
        ):
            expected_preferences = [
                str(models_enums.SexualPreferencesEnum.HETEROSEXUAL),
                str(models_enums.SexualPreferencesEnum.BI),
            ]
            return f"sexual_orientation in ({','.join(expected_preferences)}) AND gender={int(not user_profile.gender)}"
        else:
            return (
                "NOT ("
                f"sexual_orientation={models_enums.SexualPreferencesEnum.HOMOSEXUAL} "
                f"AND gender={int(not user_profile.gender)}) "
                "OR NOT ("
                f"sexual_orientation={models_enums.SexualPreferencesEnum.HOMOSEXUAL} "
                f"AND gender={user_profile.gender})"
            )
