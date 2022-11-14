"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers

from backend import settings
from backend.api import locations
from backend.mathca import matches
from backend.repositories import (
    repo_auth,
    repo_interests,
    repo_interfaces,
    repo_location,
    repo_matcha,
    repo_preference,
    repo_profile,
)
from backend.repositories_redis.redis_avatars import UsersAvatarsRedisRepo


class IOCContainer(containers.DeclarativeContainer):
    """God-like container for maintaining dependencies."""

    redis_connection: providers.Resource[resources.RedisResource] = providers.Resource(
        resources.RedisResource
    )
    database_connection: providers.Resource[
        resources.DatabaseResource
    ] = providers.Resource(resources.DatabaseResource)

    auth_repository: providers.Factory[
        repo_interfaces.AuthRepositoryInterface
    ] = providers.Factory(
        repo_auth.UserAuthDatabaseResourceRepository,
        database_connection=database_connection,
    )
    profile_repository: providers.Factory[
        repo_interfaces.ProfileRepositoryInterface
    ] = providers.Factory(
        repo_profile.UserProfileDatabaseRepository,
        database_connection=database_connection,
    )
    location_repository: providers.Factory[
        repo_interfaces.LocationRepositoryInterface
    ] = providers.Factory(
        repo_location.LocationDatabaseRepository,
        database_connection=database_connection,
    )
    preferences_repository: providers.Factory[
        repo_interfaces.PreferenceRepositoryInterface
    ] = providers.Factory(
        repo_preference.PreferenceDatabaseRepository,
        database_connection=database_connection,
    )
    interests_repository: providers.Factory[
        repo_interfaces.InterestsRepositoryInterface
    ] = providers.Factory(
        repo_interests.InterestsDatabaseRepository,
        database_connection=database_connection,
    )
    visited_users_repository: providers.Factory[
        repo_interfaces.VisitsRepoInterface
    ] = providers.Factory(
        repo_matcha.VisitedUsersDatabaseRepo, database_connection=database_connection
    )
    matched_repository: providers.Factory[
        repo_interfaces.MatchedUsersRepoInterface
    ] = providers.Factory(
        repo_matcha.MatchedUsersRepoDatabase, database_connection=database_connection
    )
    user_relationships: providers.Factory[
        matches.UsersRelationships
    ] = providers.Factory(
        matches.UsersRelationships,
        repo_profile=profile_repository,
        repo_matched=matched_repository,
        repo_visited=visited_users_repository,
    )

    location_client: providers.Resource[locations.LocationClient] = providers.Resource(
        locations.LocationClient,
        base_url=settings.settings_location.service_url,
    )
    location_service: providers.Factory[locations.LocationService] = providers.Factory(
        locations.LocationService,
        location_client=location_client,
        location_repository=location_repository,
    )

    avatars_service: providers.Resource[UsersAvatarsRedisRepo] = providers.Resource(
        UsersAvatarsRedisRepo, redis_connection=redis_connection
    )
