"""Interfaces for database repositories."""

from abc import ABC, abstractmethod

from backend.models import (
    models_location,
    models_matcha,
    models_preferences,
    models_user,
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


class MatchaRepoInterface(ABC):
    """Interface for core matcha queries."""

    @abstractmethod
    async def block_user(self, reported: models_matcha.BlockUserModel) -> bool:
        """Block or report user."""

    @abstractmethod
    async def collect_blocked_users(
        self, user_id
    ) -> list[models_matcha.BlockUserModel]:
        """Collect all blocked users for current user."""
