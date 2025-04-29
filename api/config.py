from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, MySQLDsn, MariaDBDsn


class Config(BaseSettings):
    app_debug: bool = False

    database_url: PostgresDsn | MySQLDsn | MariaDBDsn

    cors_allowed_domains: set[str] = set()


config = Config()
