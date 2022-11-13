"""Repository for matcha."""

from databases.interfaces import Record

from backend.models import models_matcha
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class MatchaCoreDatabaseRepo(BaseAsyncRepository, repo_interfaces.MatchaRepoInterface):
    """Repo for core matcha features."""

    @postgres_reconnect
    async def block_user(self, reported: models_matcha.BlockUserModel) -> bool:
        """Block user."""
        result: bool = await self.database_connection.execute(
            """
            INSERT INTO blocked_users(user_id, target_user_id, reported)
            VALUES (:user_id, :target_user_id, :reported)
            ON CONFLICT(uc_blocked_users_pairs)
            DO UPDATE SET 
            reported=:reported
            WHERE user_id=:user_id AND target_user_id=:target_user_id
            RETURNING 1;
            """,
            reported.dict(),
        )
        return result

    @postgres_reconnect
    async def collect_blocked_users(
        self, user_id
    ) -> list[models_matcha.BlockUserModel]:
        """Collect list of blocked users."""
        results: Record = self.database_connection.execute(
            """
            SELECT *
            FROM blocked_users
            WHERE user_id=:user_id;
            """,
            {"user_id": user_id},
        )
        if not results:
            return []
        return [models_matcha.BlockUserModel(**dict(row)) for row in results]
