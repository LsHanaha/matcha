"""Repo for auth."""
from backend.models import user as user_models
from backend.repositories import BaseAsyncRepository, interfaces, postgres_reconnect


class UserAuthDatabaseResource(BaseAsyncRepository, interfaces.AuthInterface):
    """Class for saving and maintaining user auth repo."""

    @postgres_reconnect
    async def create_user(self, user: user_models.UserAuth) -> bool:
        """Create new user."""
        pass

    @postgres_reconnect
    async def validate_user(self, user: user_models.UserAuth) -> bool:
        """Validate user."""
        pass

    @postgres_reconnect
    async def activate_user(self, user_id: str) -> bool:
        """activate user account."""
