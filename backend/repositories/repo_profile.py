"""Repository for user profile."""

import datetime

from databases.interfaces import Record

from backend.models import models_user as user_models
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class UserProfileDatabaseRepository(
    BaseAsyncRepository, repo_interfaces.ProfileRepositoryInterface
):
    """Class for interacting with profiles table for user."""

    @postgres_reconnect
    async def collect_user_profile(
        self, user_id: int
    ) -> user_models.UserProfile | None:
        """Collect user profile."""
        user_dict: Record | None = await self.database_connection.fetch_one(
            """
            SELECT *
            FROM profiles
            WHERE user_id=:user_id;
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
            SET first_name=:first_name, last_name=:last_name, birthday=:birthday,
                gender=:gender, sexual_orientation=:sexual_orientation, biography=:biography,
                main_photo_name=:main_photo_name, city=:city, interests=:interests
            WHERE user_id=:user_id
            RETURNING 1;
            """,
            {**user_profile.dict()},
        )
        return result

    @postgres_reconnect
    async def update_last_online(self, user_id: int) -> None:
        """Update last_online field for user."""
        await self.database_connection.execute(
            """
            UPDATE profiles
            SET last_online=:last_online
            WHERE user_id=:user_id;
            """,
            {"user_id": user_id, "last_online": datetime.datetime.now()},
        )

    @postgres_reconnect
    async def update_fame_rating(self, user_id: int, increment: int) -> None:
        """Change user_id fame rating +1 or -1."""
        await self.database_connection.execute(
            """
            UPDATE profiles
            SET fame_rating=fame_rating + :value 
            WHERE user_id=:user_id;
            """,
            {"value": increment, "user_id": user_id},
        )
        return
