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


class _JWTSettings(pydantic.BaseSettings):
    """Settings for jwt."""

    authjwt_secret_key: str = "super_secret_key_hwo_cares_its_for_local_dev"
    access_token_lifetime_sec: int = 300
    restore_token_lifetime_sec: int = 300


class _MailSettings(pydantic.BaseSettings):
    """Settings for mail sender."""

    mail_token_lifetime: int = 259200
    mail_user: str | None
    mail_address: str | None
    mail_pwd: str | None
    mail_server: str = "smtp.gmail.com"
    mail_port: int = 587

    def is_enough_settings(self) -> bool:
        """Check is data enough to send a message wia email."""
        return True and self.mail_user and self.mail_pwd and self.mail_address


class _LocationSettings(pydantic.BaseSettings):
    """Settings for location."""

    service_url: str = "http://ipwho.is/"
    max_retries: int = 3


@lru_cache
def _get_settings():
    return _BaseSettings()


@lru_cache
def _get_jwt_settings():
    return _JWTSettings()


settings_base: _BaseSettings = _get_settings()
settings_jwt: _JWTSettings = _get_jwt_settings()
settings_location: _LocationSettings = _LocationSettings()
settings_mail: _MailSettings = _MailSettings()
