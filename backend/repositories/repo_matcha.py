"""Matcha repository - search and recommend"""

from datetime import date

from databases.interfaces import Record

from backend.models import models_enums, models_matcha, models_user
from backend.repositories import (
    BaseAsyncRepository,
    postgres_reconnect,
    repo_interfaces,
)
from backend.settings import settings_base


class MatchaDatabaseRepository(BaseAsyncRepository, repo_interfaces.MatchaInterface):
    """Search users."""

    async def _collect_rows(
        self,
        array_of_queries: list[str],
        query_mods: dict,
        interests: list[str] | None,
        is_count: bool = False,
        excluded_users_query: str = "",
    ) -> list[dict] | int:
        """Return records from database."""
        (
            coordinates_query,
            sexual_preferences_query,
            age_gap_query,
            fame_rating_gap_query,
        ) = array_of_queries

        query: str = f"""
            SELECT u.user_id as user_id, first_name, last_name, birthday, gender, sexual_orientation, biography, 
                   main_photo_name, fame_rating, last_online, interests, city, interests_common
            FROM (
                SELECT puser_id as user_id, first_name, last_name, birthday, gender, sexual_orientation, biography, 
                       main_photo_name, fame_rating, last_online, interests, pcity as city,
                       cardinality(interests & ARRAY[{','.join(interests) if interests else ''}]::integer[]) 
                       as interests_common
                FROM 
                (
                    SELECT p.user_id as puser_id, p.city as pcity, *
                    FROM profiles as p
                    LEFT JOIN user_locations as l
                    ON l.user_id = p.user_id
                ) as p_l
                WHERE (
                    ({coordinates_query})
                    AND ({sexual_preferences_query})
                    AND {fame_rating_gap_query} 
                    AND {age_gap_query}
                    AND puser_id != :user_id
                    {excluded_users_query}
                )
            ) as u
            LEFT JOIN visits as v
            ON v.target_user_id = u.user_id and v.user_id = :user_id 
            WHERE (is_paired is NULL AND is_blocked is NULL AND is_reported is NULL AND is_match is NULL)
            {f"ORDER BY {query_mods.pop('order_by')} {query_mods.pop('order_direction')} LIMIT :limit OFFSET :offset ;" 
             if not is_count else ''}
        """

        if is_count:
            query = f"SELECT COUNT (*) FROM ({query}) as c;"
            del query_mods["limit"]
            del query_mods["offset"]
        result: list[Record] | Record = await self.database_connection.fetch_all(
            query,
            query_mods,
        )
        if is_count:
            return result[0]._mapping.get("count", 0)
        if not result:
            return []
        return [dict(row) for row in result]

    async def _collect_total_amount_of_rows(
        self, array_of_queries: list[str], query_mods: dict, interests: list[str] | None
    ) -> int:
        """Return amount of records."""
        return await self._collect_rows(
            array_of_queries, query_mods, interests, is_count=True
        )

    @staticmethod
    def determine_sexual_preferences_for_user(
        user_profile: models_user.UserProfile,
    ) -> str:
        """Prepare search query for expected gender and preferences."""
        expected_preferences: list[str]
        if (
            user_profile.sexual_orientation
            == models_enums.SexualPreferencesEnum.HOMOSEXUAL
        ):
            expected_preferences = [
                str(models_enums.SexualPreferencesEnum.HOMOSEXUAL.value),
                str(models_enums.SexualPreferencesEnum.BI.value),
            ]
            return f"sexual_orientation in ({','.join(expected_preferences)}) AND gender={user_profile.gender}"
        elif (
            user_profile.sexual_orientation
            == models_enums.SexualPreferencesEnum.HETEROSEXUAL
        ):
            expected_preferences = [
                str(models_enums.SexualPreferencesEnum.HETEROSEXUAL.value),
                str(models_enums.SexualPreferencesEnum.BI.value),
            ]
            return f"sexual_orientation in ({','.join(expected_preferences)}) AND gender={int(not user_profile.gender)}"
        else:
            return (
                f"(sexual_orientation != {models_enums.SexualPreferencesEnum.HOMOSEXUAL} "
                f"AND gender != {int(not user_profile.gender)}"
                ") OR ("
                f"sexual_orientation != {models_enums.SexualPreferencesEnum.HOMOSEXUAL} "
                f"AND gender != {user_profile.gender})"
            )

    def _make_query_entities(
        self,
        params: models_matcha.SearchQueryModel,
        order_direction: models_enums.SearchOrder,
        order_by: str | None,
        offset: int,
        limit: int,
        user_profile: models_user.UserProfile,
        coordinates_query: str,
    ) -> (list[str], dict):
        """Make entities for query."""
        query_mods: dict = {
            "user_id": params.user_id,
            "order_by": order_by if order_by else "user_id",
            "order_direction": order_direction.name,
            "limit": limit,
            "offset": offset,
        }

        age_gap_query: str = ""
        if params.age_gap:
            min_age: str = date.strftime(
                date(
                    date.today().year - params.age_gap[0],
                    date.today().month,
                    date.today().day,
                ),
                "%Y-%m-%d",
            )
            max_age: str = date.strftime(
                date(
                    date.today().year - params.age_gap[1],
                    date.today().month,
                    date.today().day,
                ),
                "%Y-%m-%d",
            )
            age_gap_query = f"(birthday > '{max_age}' AND birthday < '{min_age}')"

        fame_rating_gap_query: str = ""
        if params.fame_rating_gap:
            query_mods["min_rating"] = params.fame_rating_gap[0]
            query_mods["max_rating"] = params.fame_rating_gap[1]
            fame_rating_gap_query = (
                "(fame_rating >:min_rating AND fame_rating <:max_rating)"
            )

        sexual_preferences_query: str = self.determine_sexual_preferences_for_user(
            user_profile
        )
        array_of_queries = [
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
        user_profile: models_user.UserProfile,
        coordinates_query: str,
    ) -> models_matcha.SearchUsersModels:
        """Search users."""
        array_of_queries, query_mods = self._make_query_entities(
            params,
            order_direction,
            order_by,
            offset,
            limit,
            user_profile,
            coordinates_query,
        )
        records: list[dict] = await self._collect_rows(
            array_of_queries, query_mods, params.interests_id
        )
        amount: int = await self._collect_total_amount_of_rows(
            array_of_queries, query_mods, params.interests_id
        )
        return models_matcha.SearchUsersModels(users=records, amount=amount)

    @postgres_reconnect
    async def recommend_users(
        self,
        params: models_matcha.SearchQueryModel,
        user_profile: models_user.UserProfile,
        coordinates_query: str,
        order_direction: models_enums.SearchOrder = models_enums.SearchOrder.ASC,
        excluded_users: list[int] | None = None,
        order_by: str = "fame_rating, interests_common",
        limit: int = settings_base.limit_recommendations,
        offset: int = 0,
    ) -> list[models_user.UserProfile]:
        """Create new list of recommended users for user_id."""
        array_of_queries, query_mods = self._make_query_entities(
            params,
            order_direction,
            order_by,
            offset,
            limit,
            user_profile,
            coordinates_query,
        )
        excluded_users_query: str = ""
        if excluded_users:
            excluded_users_query = (
                f" AND puser_id NOT IN ({','.join(map(str, excluded_users))})"
            )
        records: list[dict] = await self._collect_rows(
            array_of_queries,
            query_mods,
            params.interests_id,
            excluded_users_query=excluded_users_query,
        )
        return [models_user.UserProfile(**record) for record in records]
