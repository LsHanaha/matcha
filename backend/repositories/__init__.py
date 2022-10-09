"""Base classes for repositories."""
import typing
from functools import wraps

import backoff
import databases
from asyncpg import PostgresConnectionError

from backend import settings


class BaseAsyncRepository:
    """Database repo."""

    def __init__(self, database_connection: databases.Database):
        self.database_connection: databases.Database = database_connection


def postgres_reconnect(func: typing.Callable):
    """Postgres reconnect decorator."""

    @backoff.on_exception(
        backoff.expo,
        (PostgresConnectionError,),
        max_tries=settings.settings_base.database_max_reties_count,
    )
    @wraps(func)
    async def inner(*args, **kwargs):
        return await func(args, kwargs)

    return inner()
