"""Repo for auth."""
from backend.auth.__main__ import hash_password
from backend.models import user as user_models
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class UserAuthDatabaseResourceRepository(
    BaseAsyncRepository, interfaces.AuthRepositoryInterface
):
    """Class for saving and maintaining user auth repo."""

    @postgres_reconnect
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""
        result: int = await self.database_connection.execute(
            """
                INSERT INTO users(username, email, password) 
                VALUES (:username, :email, :password) 
                RETURNING 1;
            """,
            {
                "username": user.username,
                "email": user.email,
                "password": hash_password(user.password),
            },
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
    async def collect_user_from_db(
        self,
        username: str | None = None,
        email: str | None = None,
        user_id: int | None = None,
    ) -> user_models.UserAuth | None:
        """Collect user by one of his unique parameter."""

        query_modifier: str
        query_builder: dict[str, str]
        if username:
            query_modifier = "users.username = :username"
            query_builder = {"username": username}
        elif user_id:
            query_modifier = "users.id = :user_id"
            query_builder = {"user_id": str(user_id)}
        elif email:
            query_modifier = "users.email = :email"
            query_builder = {"email": email}
        else:
            raise ValueError(
                "Cannot fetch user from database because not enough data for query."
            )

        user: user_models.UserAuth | None = await self.database_connection.execute(
            f"""
                SELECT * FROM users WHERE {query_modifier};
            """,
            query_builder,
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
