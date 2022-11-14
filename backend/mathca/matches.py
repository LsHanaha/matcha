"""Module contains most of all specific funtions for user profile."""

from backend.models import models_matcha, models_user
from backend.repositories import repo_interfaces

"""
1. Вернуть профили - забаненные и нет
2. При обновлении лайка увеличить/уменьшить фэйм рэйтинг
3. При обновлении проверить матчинг
"""


class UsersRelationships:
    """Module for determine users relationships."""

    def __init__(
        self,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
        repo_matched: repo_interfaces.MatchedUsersRepoInterface,
        repo_visited: repo_interfaces.VisitsRepoInterface,
    ):
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile
        self._repo_matched: repo_interfaces.MatchedUsersRepoInterface = repo_matched
        self._repo_visited: repo_interfaces.VisitsRepoInterface = repo_visited

    async def collect_visited(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[models_user.UserProfile]:
        """Collect profiles of visited users."""
        return await self._repo_visited.collect_profiles(user_id, offset, limit)

    async def collect_visited_except_banned(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[models_user.UserProfile]:
        """Collect profiles of users except banned."""
        return await self._repo_visited.collect_profiles_except_blocked(
            user_id, offset, limit
        )

    async def collect_visited_banned(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[models_user.UserProfile]:
        """Collect profiles of users that banned."""
        return await self._repo_visited.collect_profiles_blocked(user_id, offset, limit)

    async def update_visited(self):
        """Update visited users."""

    async def check_is_match(self):
        pass

    async def update_fame_rating(self):
        pass
