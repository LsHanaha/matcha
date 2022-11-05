"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers

from backend import settings
from backend.api import location_endpoints
from backend.repositories.repo_auth import UserAuthDatabaseResourceRepository
from backend.repositories.repo_location import LocationDatabaseRepository
from backend.repositories.repo_preference import PreferenceDatabaseRepository
from backend.repositories.repo_profile import UserProfileDatabaseRepository


class IOCContainer(containers.DeclarativeContainer):
    """God-like container for maintaining dependencies."""

    database_connection: providers.Resource[
        resources.DatabaseResource
    ] = providers.Resource(resources.DatabaseResource)

    auth_repository: providers.Factory[
        UserAuthDatabaseResourceRepository
    ] = providers.Factory(
        UserAuthDatabaseResourceRepository,
        database_connection=database_connection,
    )
    profile_repository: providers.Factory[
        UserProfileDatabaseRepository
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

    location_client: providers.Resource[location.LocationClient] = providers.Resource(
        location.LocationClient, base_url=settings.settings_location.service_url
    )
    location_service: providers.Factory[location.LocationService] = providers.Factory(
        location.LocationService,
        location_client=location_client,
        location_repository=location_repository,
    )
