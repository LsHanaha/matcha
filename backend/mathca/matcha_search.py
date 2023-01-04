"""Searching users and recommendations."""


from backend.mathca.mathcha_helpers import CoordinatesMatchaHelpers
from backend.models import (
    models_enums,
    models_location,
    models_matcha,
    models_preferences,
    models_user,
)
from backend.repositories import repo_interfaces


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
            f"(longitude > {coordinates.lng_min} AND longitude < {coordinates.lat_max})"
        )

    async def _prepare_coordinates_query(
        self,
        params: models_matcha.SearchQueryModel,
        user_preferences: models_preferences.UserPreferences | None = None,
    ) -> str:
        """Determine coordinates for recommendations."""
        if not user_preferences:
            user_preferences = await self._repo_preferences.collect_user_preference(
                params.user_id
            )
        if not params.distance:
            params.distance = user_preferences.max_distance_km
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
