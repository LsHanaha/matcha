"""Interfaces for database repositories."""

from abc import ABC, abstractmethod

from backend.models import user as user_models


class AuthInterface(ABC):
    """Interface for auth purpose."""

    @abstractmethod
    async def validate_user(self, user: user_models.UserAuth) -> bool:
        """Check user is valid."""

    @abstractmethod
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""

    @abstractmethod
    async def activate_user(self, user_id: str) -> bool:
        """Activate user account."""
