"""Inversion of control for dependency injector."""

import resources
from dependency_injector import containers, providers


class IOCContainer(containers.DeclarativeContainer):
    """God-like container for maintaining dependencies."""

    database_connection: providers.Resource[
        resources.DatabaseResource
    ] = providers.Resource(resources.DatabaseResource)
