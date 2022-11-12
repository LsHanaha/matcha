"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers

from backend import settings
from backend.api import locations
from backend.repositories import repo_interfaces
from backend.repositories.repo_auth import UserAuthDatabaseResourceRepository
from backend.repositories.repo_interests import InterestsDatabaseRepository
from backend.repositories.repo_location import LocationDatabaseRepository
from backend.repositories.repo_preference import PreferenceDatabaseRepository
from backend.repositories.repo_profile import UserProfileDatabaseRepository
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
        UserAuthDatabaseResourceRepository,
        database_connection=database_connection,
    )
    profile_repository: providers.Factory[
        repo_interfaces.ProfileRepositoryInterface
    ] = providers.Factory(
        UserProfileDatabaseRepository, database_connection=database_connection
    )
    location_repository: providers.Factory[
        LocationDatabaseRepository
    ] = providers.Factory(
        LocationDatabaseRepository, database_connection=database_connection
    )
    preferences_repository: providers.Factory[
        PreferenceDatabaseRepository
    ] = providers.Factory(
        PreferenceDatabaseRepository, database_connection=database_connection
    )
    interests_repository: providers.Factory[
        InterestsDatabaseRepository
    ] = providers.Factory(
        InterestsDatabaseRepository, database_connection=database_connection
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
