"""Module contains most of all specific functions for users visits."""

from backend.events import system_events
from backend.models import models_user, models_visits
from backend.models.models_enums import SystemEventTypesEnum
from backend.repositories import repo_interfaces


class UsersRelationships:
    """Module for determine users relationships."""

    def __init__(
        self,
        repo_profile: repo_interfaces.ProfileRepositoryInterface,
        repo_matched: repo_interfaces.MatchedUsersRepoInterface,
        repo_visited: repo_interfaces.VisitsRepoInterface,
        websocket_system_events: system_events.WebsocketSystemEvents,
    ):
        self._repo_profile: repo_interfaces.ProfileRepositoryInterface = repo_profile
        self._repo_matched: repo_interfaces.MatchedUsersRepoInterface = repo_matched
        self._repo_visited: repo_interfaces.VisitsRepoInterface = repo_visited
        self._websocket_system_events: system_events.WebsocketSystemEvents = (
            websocket_system_events
        )

    async def collect_visited(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[models_user.UserProfile]:
        """Collect profiles of users which user_id visit."""
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

    async def collect_visitors(
        self, target_user_id: int, offset: int = 0, limit: int = 10
    ):
        """Collect users who visit target_user_id profile."""
        return await self._repo_visited.collect_profiles(
            target_user_id, offset, limit, visitors=True
        )

    async def update_visited(self, new_visit: models_visits.VisitedUserModel) -> bool:
        """Update visited users.

        Different behaviour for first visit and any interactions with
        another user profile.
        """
        old_visit: models_visits.VisitedUserModel | None = (
            await self._repo_visited.collect_pair_of_users(
                new_visit.user_id, new_visit.target_user_id
            )
        )
        event_type: SystemEventTypesEnum = SystemEventTypesEnum.GUEST
        if old_visit:
            # TODO is it possible to make it all as a transaction?
            if old_visit.is_match != new_visit.is_match:
                await self.update_fame_rating(
                    new_visit.target_user_id, new_visit.is_match
                )
                if old_visit.is_match:
                    await self.retrieve_match(
                        new_visit.user_id, new_visit.target_user_id
                    )
                    event_type = SystemEventTypesEnum.UNLIKE
                else:
                    event_type = (
                        await self.set_match(
                            new_visit.user_id, new_visit.target_user_id
                        )
                        or SystemEventTypesEnum.LIKE
                    )

        await self._websocket_system_events.handle_outcome_event(
            event_type, new_visit.user_id, new_visit.target_user_id
        )
        await self._repo_visited.update_visited_users(new_visit)
        return True

    async def set_match(
        self, user_id: int, target_user_id: int
    ) -> None | SystemEventTypesEnum:
        """If like is set - trying to make a couple"""
        target_user_visit: models_visits.VisitedUserModel | None = (
            await self._repo_visited.collect_pair_of_users(target_user_id, user_id)
        )
        if target_user_visit and target_user_visit.is_match:
            await self._repo_matched.set_users_pair(user_id, target_user_id)
            await self._repo_visited.change_is_match(user_id, target_user_id, True)
            return SystemEventTypesEnum.MATCH

    async def retrieve_match(self, first_user_id: int, second_user_id: int) -> None:
        """Retrieve match in case something changed."""
        await self._repo_matched.delete_users_pair(first_user_id, second_user_id)
        await self._repo_visited.change_is_match(first_user_id, second_user_id, False)

    async def update_fame_rating(self, user_id: int, is_incremented: bool) -> None:
        """update fame rating for user_id."""
        await self._repo_profile.update_fame_rating(
            user_id, 1 if is_incremented else -1
        )
