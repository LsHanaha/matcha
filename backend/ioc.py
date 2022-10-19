"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers

from backend.repositories.auth import UserAuthDatabaseResourceRepository
from backend.repositories.profile import UserProfileDatabaseRepository


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
