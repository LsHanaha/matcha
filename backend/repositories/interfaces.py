"""Interfaces for database repositories."""

from abc import ABC, abstractmethod

from backend.models import user as user_models


class AuthInterface(ABC):
    """Interface for auth purpose."""

    @abstractmethod
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""

    @abstractmethod
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account."""

    @abstractmethod
    async def collect_user_by_email(self, email: str) -> user_models.UserAuth | None:
        """Collect user by email."""

    @abstractmethod
    async def collect_user_by_id(self, user_id: int) -> user_models.UserAuth | None:
        """Collect user by id."""

    @abstractmethod
    async def update_password(self, new_password: str, user_id: int) -> bool:
        """Update password for user."""
