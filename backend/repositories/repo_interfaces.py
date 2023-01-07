"""Interfaces for database repositories."""

from abc import ABC, abstractmethod
from typing import Protocol

from backend.models import (
    models_enums,
    models_events,
    models_location,
    models_matcha,
    models_preferences,
    models_user,
    models_visits,
)
from backend.settings import settings_base


class AuthRepositoryInterface(ABC):
    """Interface for auth purpose."""

    @abstractmethod
    async def create_user(self, user: models_user.UserAuth) -> bool:
        """Create new user."""

    @abstractmethod
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account."""

    @abstractmethod
    async def collect_user_from_db(
        self,
        username: str | None = None,
        user_id: int | None = None,
        email: str | None = None,
    ) -> models_user.UserAuth | None:
        """Collect user by unique parameter."""

    @abstractmethod
    async def update_password(self, new_password: str, user_id: int) -> bool:
        """Update password for user."""


class ProfileRepositoryInterface(ABC):
    """Interface for user profile."""

    @abstractmethod
    async def collect_user_profile(self, user_id: int) -> models_user.UserProfile:
        """Collect =profile for a user."""

    @abstractmethod
    async def collect_list_of_profiles(
        self, list_of_ids: list[int]
    ) -> list[models_user.UserProfile]:
        """Collect list of profiles for list of ids."""

    @abstractmethod
    async def update_user_profile(self, user_profile: models_user.UserProfile) -> bool:
        """Update profile for a user."""

    @abstractmethod
    async def update_last_online(self, user_id: int):
        """Update last_online field for user."""

    @abstractmethod
    async def update_fame_rating(self, user_id: int, change_value: int) -> None:
        """Change user_id fame rating +1 or -1."""


class LocationRepositoryInterface(ABC):
    """Interface for user location."""

    @abstractmethod
    async def collect_user_location(
        self, user_id: int
    ) -> models_location.LocationRepositoryModel | None:
        """Get user location from database."""

    @abstractmethod
    async def update_user_location(
        self, user_id: int, new_location: models_location.LocationRepositoryModel
    ) -> bool:
        """Update user location."""


class PreferenceRepositoryInterface(ABC):
    """Interface for user location."""

    @abstractmethod
    async def collect_user_preference(
        self, user_id: int
    ) -> models_preferences.UserPreferences | None:
        """Get user location from database."""

    @abstractmethod
    async def update_user_preference(
        self, new_preferences: models_preferences.UserPreferences
    ) -> bool:
        """Update user location."""


class InterestsRepositoryInterface(ABC):
    """Interface for user repository."""

    @abstractmethod
    async def collect_all_interests(self) -> list[models_user.Interests]:
        """Collect all interests."""

    @abstractmethod
    async def search_interests_by_name(
        self, pattern: str
    ) -> list[models_user.Interests]:
        """Return result of search for interests by name."""

    @abstractmethod
    async def insert_new_interest(self, name: str) -> models_user.Interests:
        """Insert nes interest."""


class VisitsRepoInterface(ABC):
    """Interface for core matcha queries."""

    @abstractmethod
    async def update_visited_users(
        self, visited_user: models_visits.VisitedUserModel
    ) -> bool:
        """Store visited user."""

    @abstractmethod
    async def change_is_match(
        self, user_id: int, target_user_id: int, new_status: bool
    ) -> bool:
        """Change is match parameter for user."""

    @abstractmethod
    async def collect_visited_users(
        self, user_id: int, query_modifier: str | None = None
    ) -> list[models_visits.VisitedUserModel]:
        """Collect users."""

    @abstractmethod
    async def collect_users_except_blocked(
        self, user_id: int
    ) -> list[models_visits.VisitedUserModel]:
        """Collect all visited users except blocked."""

    @abstractmethod
    async def collect_users_blocked(
        self, user_id: int
    ) -> list[models_visits.VisitedUserModel]:
        """Collect all blocked users."""

    @abstractmethod
    async def collect_pair_of_users(
        self, user_id_first: int, user_id_second: int
    ) -> models_visits.VisitedUserModel | None:
        """collect pair for users for checking stuff."""

    @abstractmethod
    async def visitors(
        self, target_user_id: int
    ) -> list[models_visits.VisitedUserModel]:
        """Collect visitors for user."""

    @abstractmethod
    async def collect_profiles(
        self,
        user_id: int,
        offset: int,
        limit: int,
        query_modifiers: str | None = None,
        visitors: bool = False,
    ) -> list[models_user.UserProfile]:
        """Collect profiles of visited users."""

    @abstractmethod
    async def collect_profiles_except_blocked(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_user.UserProfile]:
        """Collect profiles of not blocked users."""

    @abstractmethod
    async def collect_profiles_blocked(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_user.UserProfile]:
        """Collect profiles of blocked users."""


class MatchedUsersRepoInterface(ABC):
    """Matched users database interface."""

    @abstractmethod
    async def set_users_pair(self, first_user_id: int, second_user_id: int) -> bool:
        """Set a new pair of matched users."""

    @abstractmethod
    async def delete_users_pair(self, first_user_id: int, second_user_id: int) -> bool:
        """Delete a pair of matched users."""

    @abstractmethod
    async def collect_pair_of_users(
        self, first_user_id: int, second_user_id: int
    ) -> models_visits.MatchedUsers | None:
        """Collect pair of users."""


class MatchaInterface(ABC):
    """Search users."""

    @abstractmethod
    async def search_users(
        self,
        params: models_matcha.SearchQueryModel,
        order_direction: models_enums.SearchOrderEnum,
        order_by: str,
        offset: int,
        limit: int,
        user_profile: models_user.UserProfile,
        coordinates_query: str,
    ) -> models_matcha.SearchUsersModels:
        """Search users by params."""

    @abstractmethod
    async def recommend_users(
        self,
        params: models_matcha.SearchQueryModel,
        user_profile: models_user.UserProfile,
        coordinates_query: str,
        excluded_users: list[int] | None = None,
        order_direction: models_enums.SearchOrderEnum = models_enums.SearchOrderEnum.ASC,
        order_by: str = "fame_rating, interests_common",
        limit: int = settings_base.limit_recommendations,
        offset: int = 0,
    ) -> list[models_user.UserProfile]:
        """Recommended users."""
        pass

    @staticmethod
    @abstractmethod
    def determine_sexual_preferences_for_user(
        user_profile: models_user.UserProfile,
    ) -> str:
        """Determine sexual preferences for user."""


class SystemEventsRepoInterface(Protocol):
    """System events repository interface."""

    async def store_new_event(
        self, system_event: models_events.SystemEventModel
    ) -> models_events.SystemEventModel | None:
        """Insert new system event."""

    async def collect_system_events_for_user(
        self, user_id: int, offset: int, limit: int
    ) -> list[models_events.RetrieveSystemEventsModel]:
        """Collect system events."""

    async def update_system_events(self, user_id: int) -> bool:
        """Update system events."""
