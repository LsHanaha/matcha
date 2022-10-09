"""Resources for connecting to different targets."""
import json

import asyncpg
import settings
from databases import Database
from dependency_injector import resources


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
