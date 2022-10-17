"""Repo for auth."""
from backend.auth.__main__ import hash_password
from backend.models import user as user_models
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class UserAuthDatabaseResource(BaseAsyncRepository, interfaces.AuthInterface):
    """Class for saving and maintaining user auth repo."""

    @postgres_reconnect
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""
        result: int = await self.database_connection.execute(
            """
                INSERT INTO users(email, password) 
                VALUES (:email, :password) 
                RETURNING 1;
            """,
            {"email": user.email, "password": hash_password(user.password)},
        )
        return bool(result)

    @postgres_reconnect
    async def activate_user(self, user_id: str) -> bool:
        """activate user account."""
        result: int = self.database_connection.execute(
            """
                UPDATE users
                SET is_active=true
                WHERE id=:user_id
                RETURNING 1;
            """,
            {user_id: user_id},
        )
        return bool(result)

    @postgres_reconnect
    async def collect_user_by_email(self, email: str) -> user_models.UserAuth | None:
        """Collect user by email."""
        user: user_models.UserAuth | None = await self.database_connection.execute(
            """
                SELECT * FROM users WHERE users.email = :email;
            """,
            {"email": email},
        )
        if user is None:
            return None
        return user_models.UserAuth(**dict(user))

    @postgres_reconnect
    async def collect_user_by_id(self, user_id: int) -> user_models.UserAuth | None:
        """Collect user by id."""
        user: user_models.UserAuth | None = await self.database_connection.execute(
            """
                SELECT * FROM users WHERE users.id = :user_id,
            """,
            {"user_id": user_id},
        )
        if user is None:
            return None
        return user_models.UserAuth(**dict(user))

    @postgres_reconnect
    async def update_password(self, new_password: str, user_id: int) -> bool:
        """Update password for user."""
        result: int = await self.database_connection.execute(
            """
                UPDATE users
                SET password=:password
                WHERE id=:user_id
                RETURNING 1;
            """,
            {"password": hash_password(new_password), "user_id": user_id},
        )
        return bool(result)
