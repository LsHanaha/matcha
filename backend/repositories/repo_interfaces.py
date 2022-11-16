"""Interfaces for database repositories."""

from abc import ABC, abstractmethod

from backend.models import (
    models_location,
    models_preferences,
    models_user,
    models_visits,
)


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
