"""Searching users and recommendations."""


import asyncio

from backend.mathca.mathcha_helpers import CoordinatesMatchaHelpers
from backend.models import (
    models_enums,
    models_location,
    models_matcha,
    models_preferences,
    models_user,
)
from backend.repositories import repo_interfaces
from backend.repositories_redis import redis_recommendations
from backend.settings import settings_base


class MatchaSearch:
    """Contains methods for searching."""

    def __init__(
        self,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
        repo_matcha: repo_interfaces.MatchaInterface,
        repo_preferences: repo_interfaces.PreferenceRepositoryInterface,
        repo_locations: repo_interfaces.LocationRepositoryInterface,
        coordinates_helpers: CoordinatesMatchaHelpers,
    ):
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile
        self._repo_matcha: repo_interfaces.MatchaInterface = repo_matcha
        self._repo_preferences: repo_interfaces.PreferenceRepositoryInterface = (
            repo_preferences
        )
        self._repo_locations: repo_interfaces.LocationRepositoryInterface = (
            repo_locations
        )
        self._coordinates_helpers: CoordinatesMatchaHelpers = coordinates_helpers

    @staticmethod
    def _convert_coordinates_to_query(
        coordinates: models_location.CoordinatesForSearchUsersModels,
    ) -> str:
        """Create query string for coordinates."""
        return (
            f"(latitude > {coordinates.lat_min} AND latitude < {coordinates.lat_max}) AND "
            f"(longitude > {coordinates.lng_min} AND longitude < {coordinates.lng_max})"
        )

    async def _prepare_coordinates_query(
        self,
        params: models_matcha.SearchQueryModel,
    ) -> str:
        """Determine coordinates for recommendations."""
        if not params.distance:
            user_preferences: models_preferences.UserPreferences | None = (
                await self._repo_preferences.collect_user_preference(params.user_id)
            )
            params.distance = (
                user_preferences.max_distance_km if user_preferences else 100
            )
        user_location: models_location.LocationRepositoryModel = (
            await self._repo_locations.collect_user_location(params.user_id)
        )
        coordinates: models_location.CoordinatesForSearchUsersModels = (
            self._coordinates_helpers.calculate_coords_from_distance(
                models_location.CoordinatesLocationModel(
                    latitude=user_location.latitude, longitude=user_location.longitude
                ),
                params.distance,
            )
        )
        return self._convert_coordinates_to_query(coordinates)

    async def find_users(
        self,
        params: models_matcha.SearchQueryModel,
        order_direction: models_enums.SearchOrder,
        offset: int,
        limit: int,
        order_by: str | None = None,
    ) -> models_matcha.SearchUsersModels:
        """Search users."""
        user_profile: models_user.UserProfile = (
            await self._repo_profile.collect_user_profile(params.user_id)
        )
        coordinates_query: str = await self._prepare_coordinates_query(params)
        found_users: models_matcha.SearchUsersModels = (
            await self._repo_matcha.search_users(
                params,
                order_direction,
                order_by,
                offset,
                limit,
                user_profile,
                coordinates_query,
            )
        )
        return found_users


class MatchaRecommendations:
    """Contains models for recommendations."""

    def __init__(
        self,
        repo_recommendations: redis_recommendations.UserRecommendationsService,
        matcha_search_service: MatchaSearch,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
    ):
        self._repo_recommendations: redis_recommendations.UserRecommendationsService = (
            repo_recommendations
        )
        self._matcha_search_service: MatchaSearch = matcha_search_service
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile

    async def _create_recommendations_for_user(
        self, user_id: int, excluded_users: list[int]
    ) -> list[models_user.UserProfile]:
        """Create recommendations for user."""
        pass

    async def _get_list_of_recommended_users(self, user_id: int) -> list[int]:
        """Select list of recommended users."""
        recommended_users_ids: list[int] = []
        for _ in range(settings_base.count_of_recommendations):
            rec_user_id: int | None = (
                await self._repo_recommendations.pop_one_recommendation(user_id)
            )
            if rec_user_id is None:
                break
            recommended_users_ids.append(rec_user_id)
        return recommended_users_ids

    async def get_recommendations(self, user_id: int) -> list[models_user.UserProfile]:
        """Select recommended users which still not marked as interacted."""
        recommended_users_ids: list[int] = await self._get_list_of_recommended_users(
            user_id
        )
        if not recommended_users_ids:
            list_of_recommendations: list[
                models_user.UserProfile
            ] = await self._create_recommendations_for_user(user_id)
            asyncio.create_task(
                self._create_recommendations_for_user(
                    user_id, [user.user_id for user in list_of_recommendations]
                )
            )
            return list_of_recommendations
        if not self._repo_recommendations.collect_count_of_recommendations:
            asyncio.create_task(
                self._create_recommendations_for_user(user_id, recommended_users_ids)
            )
        return await self._repo_profile.collect_list_of_profiles(recommended_users_ids)
