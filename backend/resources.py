"""Resources for connecting to different targets."""
import json
import typing

import asyncpg
import settings
from databases import Database
from dependency_injector import resources
from redis import asyncio as aioredis


class DatabaseResource(resources.AsyncResource):
    """Database connector."""

    async def asyncpg_init(self, connection: asyncpg.Connection) -> None:
        """Initialize asyncpg codecs."""
        await connection.set_type_codec(
            "jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog"
        )

    async def init(self, *args, **kwargs) -> Database:
        """Initialize database connection."""
        database_connection: Database = Database(
            settings.settings_base.database_dsn,
            min_size=settings.settings_base.min_pool_size,
            max_size=settings.settings_base.max_pool_size,
            init=self.asyncpg_init,
        )
        await database_connection.connect()
        return database_connection

    async def shutdown(self, resource: Database) -> None:
        """Close db connection."""
        await resource.disconnect()


class RedisResource(resources.AsyncResource):
    """Resource for redis connections."""

    ENCODING: typing.Final[str] = "utf-8"

    async def init(self, *args: list, **kwargs: dict) -> aioredis.Redis:
        """Initialize redis connection."""
        return await aioredis.from_url(
            f"redis://:{settings.settings_base.redis_password}@"
            f"{settings.settings_base.redis_host}:{settings.settings_base.redis_port}"
        )

    async def shutdown(self, resource: aioredis.Redis) -> None:
        """Shutdown redis connection."""
        await resource.close()
