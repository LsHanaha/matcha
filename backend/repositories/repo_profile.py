"""Repository for user profile."""

from databases.interfaces import Record

from backend.models import models_user as user_models
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class UserProfileDatabaseRepository(
    BaseAsyncRepository, interfaces.ProfileRepositoryInterface
):
    """Class for interacting with profiles table for user."""

    @postgres_reconnect
    async def collect_user_profile(
        self, user_id: int
    ) -> user_models.UserProfile | None:
        """Collect user profile."""
        user_dict: Record | None = await self.database_connection.execute(
            """
            SELECT * 
            FROM profiles
            WHERE user_id=:user_id
            """,
            {"user_id": user_id},
        )
        if user_dict is None:
            return None
        return user_models.UserProfile(**dict(user_dict))

    @postgres_reconnect
    async def update_user_profile(self, user_profile: user_models.UserProfile) -> bool:
        """Update profile for a user."""

        result: bool = await self.database_connection.execute(
            """
            UPDATE profiles
            SET first_name=:first_name, last_name:=last_name, birthday=:birthday,
                gender=:gender, sexual_preferences=sexual_preferences, biography=:biography,
                main_photo_name=:main_photo_name
            WHERE user_id=:user_id
            RETURNING 1;
            """,
            {**user_profile.dict()},
        )
        return result
