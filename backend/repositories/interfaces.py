"""Interfaces for database repositories."""

from abc import ABC, abstractmethod

from backend.models import location_models
from backend.models import user as user_models


class AuthRepositoryInterface(ABC):
    """Interface for auth purpose."""

    @abstractmethod
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""

    @abstractmethod
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account."""

    @abstractmethod
    async def collect_user_from_db(
        self, username: str | None, user_id: int | None, email: str | None
    ) -> user_models.UserAuth | None:
        """Collect user by unique parameter."""

    @abstractmethod
    async def update_password(self, new_password: str, user_id: int) -> bool:
        """Update password for user."""


class ProfileRepositoryInterface(ABC):
    """Interface for user profile."""

    @abstractmethod
    async def collect_user_profile(self, user_id: int) -> user_models.UserProfile:
        """Collect =profile for a user."""

    @abstractmethod
    async def update_user_profile(self, user_profile: user_models.UserProfile) -> bool:
        """Update profile for a user."""


class LocationRepositoryInterface(ABC):
    """Interface for user location."""

    @abstractmethod
    async def collect_user_location(
        self, user_id: int
    ) -> location_models.LocationRepositoryModel | None:
        """Get user location from database."""

    @abstractmethod
    async def update_user_location(
        self, user_id: int, new_location: location_models.LocationRepositoryModel
    ) -> bool:
        """Update user location."""


""
