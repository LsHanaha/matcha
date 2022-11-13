"""Repository for matcha."""

from databases.interfaces import Record

from backend.models import models_matcha
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class VisitedUsersDatabaseRepo(
    BaseAsyncRepository, repo_interfaces.MatchaRepoInterface
):
    """Repo for handle visits for users."""

    @postgres_reconnect
    async def update_visited_users(
        self, visited_user: models_matcha.VisitedUserModel
    ) -> bool:
        """Update visited user."""
        result: bool = await self.database_connection.execute(
            """
                INSERT INTO blocked_users(user_id, target_user_id, is_liked, 
                                          is_blocked, is_reported)
                VALUES (:user_id, :target_user_id, :is_liked, :is_blocked, :is_reported)
                ON CONFLICT(uc_users_pair_visits)
                DO UPDATE SET 
                is_liked=:is_liked, is_blocked=:is_blocked, is_reported=:is_reported
                WHERE user_id=:user_id AND target_user_id=:target_user_id
                RETURNING 1;
            """,
            visited_user.dict(),
        )
        return result

    @postgres_reconnect
    async def collect_visited_users(
        self, user_id: int, query_modifier: str | None = None
    ) -> list[models_matcha.VisitedUserModel]:
        """Collect all visited users."""
        result: list[Record] = await self.database_connection.execute(
            f"""
                SELECT *
                FROM blocked_users
                WHERE user_id=:user_id 
                {f" AND {query_modifier}" if query_modifier else ""};
            """,
            {"user_id": user_id},
        )
        if not result:
            return []
        return [models_matcha.VisitedUserModel(**dict(row)) for row in result]

    @postgres_reconnect
    async def collect_users_except_blocked(
        self, user_id: int
    ) -> list[models_matcha.VisitedUserModel]:
        """Collect all visited_users_except_blocked."""
        return await self.collect_visited_users(
            user_id, "is_blocked != true and is_reported != true"
        )

    @postgres_reconnect
    async def collect_users_blocked(
        self, user_id: int
    ) -> list[models_matcha.VisitedUserModel]:
        """Collect blocked users."""
        return await self.collect_visited_users(
            user_id, "is_blocked == true and is_reported == true"
        )

    @postgres_reconnect
    async def collect_pair_of_users(
        self, user_id_first: int, user_id_second: int
    ) -> models_matcha.VisitedUserModel | None:
        """Collect pair of users."""
        result: Record = await self.database_connection.execute(
            """
                SELECT *
                FROM blocked_users
                WHERE user_id=:user_id  AND target_user_id=:target_user_id
                LIMIT 1;
            """,
            {"user_id": user_id_first, "target_user_id": user_id_second},
        )
        if not result:
            return None
        return models_matcha.VisitedUserModel(**dict(result))
