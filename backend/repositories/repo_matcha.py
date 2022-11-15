"""Repository for matcha."""

from databases.interfaces import Record

from backend.models import models_matcha, models_user
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class VisitedUsersDatabaseRepo(
    BaseAsyncRepository, repo_interfaces.VisitsRepoInterface
):
    """Repo for handle visits for users."""

    @postgres_reconnect
    async def update_visited_users(
        self, visited_user: models_matcha.VisitedUserModel
    ) -> bool:
        """Update visited user."""
        result: bool = await self.database_connection.execute(
            """
                INSERT INTO visits(user_id, target_user_id, is_liked, 
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
    async def change_is_match(
        self, user_id: int, target_user_id: int, new_status: bool
    ) -> bool:
        """Update is_match field."""
        await self.database_connection.execute(
            """
            UPDATE visits
            SET (is_match=:is_match)
            WHERE (user_id=:user_id AND target_user_id=:taget_user_id) 
                  OR (user_id=:target_user_id AND target_user_id=:user_id);  
            """,
            {
                "is_match": new_status,
                "user_id": user_id,
                "target_user_id": target_user_id,
            },
        )
        return True

    @postgres_reconnect
    async def collect_visited_users(
        self, user_id: int, query_modifier: str | None = None
    ) -> list[models_matcha.VisitedUserModel]:
        """Collect all visited users."""
        result: list[Record] = await self.database_connection.execute(
            f"""
                SELECT *
                FROM visits
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
            user_id, "is_blocked=true and is_reported=true"
        )

    @postgres_reconnect
    async def collect_pair_of_users(
        self, user_id_first: int, user_id_second: int
    ) -> models_matcha.VisitedUserModel | None:
        """Collect pair of users."""
        result: Record = await self.database_connection.execute(
            """
                SELECT *
                FROM visits
                WHERE user_id=:user_id  AND target_user_id=:target_user_id
                LIMIT 1;
            """,
            {"user_id": user_id_first, "target_user_id": user_id_second},
        )
        if not result:
            return None
        return models_matcha.VisitedUserModel(**dict(result))

    @postgres_reconnect
    async def visitors(
        self, target_user_id: int
    ) -> list[models_matcha.VisitedUserModel]:
        """Collect visitors fof user."""
        result: list[Record] = await self.database_connection.execute(
            """
            SELECT *
            FROM visits
            WHERE target_user_id=:target_user_id;
            """,
            {"target_user_id": target_user_id},
        )
        if not result:
            return []
        return [models_matcha.VisitedUserModel(**dict(row)) for row in result]

    @postgres_reconnect
    async def collect_profiles(
        self,
        user_id: int,
        offset: int,
        limit: int,
        query_modifiers: str | None = None,
        visitors: bool = False,
    ) -> list[models_user.UserProfile]:
        """Collect profiles of visited users."""
        result: list[Record] = await self.database_connection.execute(
            f"""
            SELECT p.user_id, p.first_name, p.birthday, p.gender, p.sexual_orientation,
                   p.main_photo_name, p.interests, p.city
            FROM profiles as p
            JOIN visits as v
            ON v.user_id = p.user_id
            WHERE v.{'target_' if visitors else ''}user_id=:user_id {f"AND {query_modifiers}" if query_modifiers else ""}
            ORDER BY v.last_visit_time DESC
            OFFSET :offset
            LIMIT :limit;
            """,
            {"user_id": user_id, "offset": offset, "limit": limit},
        )
        if not result:
            return []
        return [models_user.UserProfile(**dict(row)) for row in result]

    @postgres_reconnect
    async def collect_profiles_except_blocked(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_user.UserProfile]:
        """Collect profiles of not blocked users."""
        return await self._collect_profiles(user_id, offset, limit, "is_blocked=false")

    @postgres_reconnect
    async def collect_profiles_blocked(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_user.UserProfile]:
        """Collect profiles of blocked users."""
        return await self._collect_profiles(user_id, offset, limit, "is_blocked=true")


class MatchedUsersRepoDatabase(
    BaseAsyncRepository, repo_interfaces.MatchedUsersRepoInterface
):
    """Repo for handling matched users."""

    @postgres_reconnect
    async def set_users_pair(self, first_user_id: int, second_user_id: int) -> bool:
        """Set a new pair of users."""

        await self.database_connection.execute(
            """
            INSERT INTO matches(firts_user_id, second_user_id)
            VALUES(:first_user_id, :second_user_id);
            """,
            {"first_user_id": first_user_id, "second_user_id": second_user_id},
        )
        return True

    @postgres_reconnect
    async def delete_users_pair(self, first_user_id: int, second_user_id: int) -> bool:
        """Remove a matched pair of users."""
        await self.database_connection.execute(
            """
            DELETE FROM matches
            WHERE (first_user_id=:first_user_id AND second_user_id=:second_user_id) 
                  OR (first_user_id=:second_user_id AND second_user_id=:first_user_id);
            """,
            {"first_user_id": first_user_id, "second_user_id": second_user_id},
        )
        return True

    @postgres_reconnect
    async def collect_pair_of_users(
        self, first_user_id: int, second_user_id: int
    ) -> models_matcha.MatchedUsers | None:
        """Collect pair of users."""
        result: Record = await self.database_connection.execute(
            """
            SELECT *
            FROM matches
            WHERE first_user_id=:first_user_id AND second_user_id=:second_user_id;
            """,
            {"first_user_id": first_user_id, "second_user_id": second_user_id},
        )
        if not result:
            return None
        return models_matcha.MatchedUsers(**dict(result))
