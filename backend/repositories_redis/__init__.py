"""Common methods for redis repos."""
import typing
from functools import wraps

import backoff
import redis
from redis import asyncio as aioredis

from backend import settings


class BaseRedisRepository:
    """Common for all redis instances."""

    def __init__(self, redis_connection: aioredis.Redis):
        self._redis_connection: aioredis.Redis = redis_connection


def redis_reconnect(func: typing.Callable):
    """Postgres reconnect decorator."""

    @backoff.on_exception(
        backoff.expo,
        (redis.ConnectionError, ConnectionResetError, TimeoutError),
        max_tries=settings.settings_base.redis_max_reties_count,
    )
    @wraps(func)
    async def inner(*args, **kwargs):
        return await func(*args, **kwargs)

    return inner
