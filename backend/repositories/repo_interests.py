"""Repository for interests."""

from databases.interfaces import Record

from backend.models import models_user
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class InterestsDatabaseRepository(
    BaseAsyncRepository, repo_interfaces.InterestsRepositoryInterface
):
    """Interests postgres repo."""

    @postgres_reconnect
    async def collect_all_interests(self) -> list[models_user.Interests]:
        """Collect list of all interests."""

        records: Record = await self.database_connection.execute(
            """
            SELECT *
            FROM interests;
            """
        )
        if not records:
            return []
        return [models_user.Interests(**dict(rec)) for rec in records]

    @postgres_reconnect
    async def search_interests_by_name(
        self, pattern: str
    ) -> list[models_user.Interests]:
        """Search interests by name."""

        records: Record = await self.database_connection.execute(
            """
            SELECT *
            FROM interests
            WHERE name LIKE '%:name%'
            ORDER BY name ASC;
            """,
            {"name": pattern},
        )
        return [models_user.Interests(dict(rec)) for rec in records]

    @postgres_reconnect
    async def insert_new_interest(self, name: str) -> models_user.Interests:
        """Add new interest."""

        # TODO add handler for unique violation error  if needed
        new_id: int = await self.database_connection.execute(
            """
            INSERT INTO interests(name)
            VALUES (:name)
            RETURNING id;
            """,
            {"name": name},
        )
        return models_user.Interests(id=new_id, name=name)
