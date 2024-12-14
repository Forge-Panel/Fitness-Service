from pydantic_settings import BaseSettings
from pydantic import AnyUrl, PostgresDsn, MySQLDsn, MariaDBDsn


class Config(BaseSettings):
    debug: bool = False

    database_url: AnyUrl | PostgresDsn | MySQLDsn | MariaDBDsn

    forge_secret: str

    cors_allowed_domains: set[str] = set()


config = Config()
