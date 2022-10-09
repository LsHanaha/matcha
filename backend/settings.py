"""Module for keeping project variables."""
from functools import lru_cache

import pydantic


class _BaseSettings(pydantic.BaseSettings):
    """Base settings for app like uls prefixes, threads count and etc."""

    debug: bool = True
    doc_prefix: str = "/doc/".rstrip("/") + "/"
    api_prefix: str = "/api/".rstrip("/")

    tags_metadata: list[dict] = [
        {"name": "auth", "description": "Module for authentication and authorization"}
    ]

    postgres_user: str = "username"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_database: str = "matcha"

    database_dsn: str = (
        f"postgresql://{postgres_user}:{postgres_password}@"
        f"{postgres_host}:{postgres_port}/{postgres_database}"
    )
    min_pool_size: int = 10
    max_pool_size: int = 30

    database_max_reties_count: int = 3


@lru_cache
def get_settings():
    return _BaseSettings()


base_settings = get_settings()
