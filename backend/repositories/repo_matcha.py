"""Matcha repository - search and recommend"""

from databases.interfaces import Record

from backend.models import models_enums, models_location, models_matcha
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)


class MatchaDatabaseRepository(BaseAsyncRepository, repo_interfaces.MatchaInterface):
    """Search users."""

    async def _collect_rows(
        self, array_of_queries: list[str], query_mods: dict, is_count: bool = False
    ) -> list[dict] | int:
        """Return records from database."""
        (
            interests_query,
            coordinates_query,
            sexual_preferences_query,
            age_gap_query,
            fame_rating_gap_query,
        ) = array_of_queries
        query: str = f"""
                SELECT * {interests_query} FROM 
                (SELECT * 
                FROM profiles as p
                WHERE :preferences_query
                LEFT JOIN user_locations as locations
                ON locations.user_id = p.user_id) as p_l 
                WHERE {coordinates_query} AND {sexual_preferences_query}
                      {age_gap_query} {fame_rating_gap_query}
                ORDER BY :order_by :order_direction
                LIMIT :limit
                OFFSET :offset
            """
        if is_count:
            query = f"SELECT COUNT (*) FROM ({query})"
        result: list[Record] | Record = await self.database_connection.fetch_all(
            query,
            query_mods,
        )
        if is_count:
            return result[0]
        if not result:
            return []
        return [dict(row) for row in result]

    async def _collect_total_amount_of_rows(
        self, array_of_queries: list[str], query_mods: dict
    ) -> int:
        """Return amount of records."""
        return await self._collect_rows(array_of_queries, query_mods, is_count=True)

    @staticmethod
    async def _make_query_entities(
        params: models_matcha.SearchQueryModel,
        order_direction: models_enums.SearchOrder,
        order_by: str | None,
        offset: int,
        limit: int,
        sexual_preferences_query: str,
        coordinates_query: str,
    ) -> (list[str], dict):
        """Make entities for query."""
        query_mods: dict = {
            "user_id": params.user_id,
            "order_by": "p_l." + order_by if order_by else "p_l.user_id",
            "order_direction": order_direction.name,
            "limit": limit,
            "offset": offset,
        }

        age_gap_query: str = ""
        if params.age_gap:
            query_mods["min_age"] = params.age_gap[0]
            query_mods["max_age"] = params.age_gap[1]
            age_gap_query = " AND  (p_l.birthday >:min_age AND p_l.birthday <:max_age)"

        fame_rating_gap_query: str = ""
        if params.fame_rating_gap:
            query_mods["min_rating"] = params.fame_rating_gap[0]
            query_mods["max_rating"] = params.fame_rating_gap[1]
            fame_rating_gap_query = (
                " AND  (p_l.fame_rating >:min_rating AND p_l.fame_rating <:max_rating)"
            )
        interests_query: str = ""
        if params.interests_id:
            interests_query = "cardinality(p_l.interests & ARRAY:interests_array)"
            query_mods["interests_array"] = params.interests_id

        array_of_queries = [
            interests_query,
            coordinates_query,
            sexual_preferences_query,
            age_gap_query,
            fame_rating_gap_query,
        ]
        return array_of_queries, query_mods

    @postgres_reconnect
    async def search_users(
        self,
        params: models_matcha.SearchQueryModel,
        order_direction: models_enums.SearchOrder,
        order_by: str | None,
        offset: int,
        limit: int,
        sexual_preferences_query: str,
        coordinates_query: str,
    ) -> models_matcha.SearchUsersModels:
        """Search users."""
        array_of_queries, query_mods = self._make_query_entities(
            params,
            order_direction,
            order_by,
            offset,
            limit,
            sexual_preferences_query,
            coordinates_query,
        )
        records: list[dict] = await self._collect_rows(array_of_queries, query_mods)
        amount: int = await self._collect_total_amount_of_rows(
            array_of_queries, query_mods
        )
        return models_matcha.SearchUsersModels(users=records, amount=amount)
