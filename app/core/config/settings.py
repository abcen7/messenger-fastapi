from pydantic import Field, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.lib import main_logger
from app.core.lib.databases import Databases, PostgreSQLDrivers

"""
TODO: Please, add the settings of all services right here.
"""


class DatabaseSettings(BaseSettings):
    """
    For default uses the Postgres
    """

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    ECHO_DEBUG_MODE: bool = False
    USED: Databases = Databases.PostgreSQL
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL
        Returns: PostgresDsn: The constructed PostgresDsn URL.
        """
        return MultiHostUrl.build(
            scheme=PostgreSQLDrivers.DEFAULT_DIALECT,
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            path=self.NAME,
        )

    @computed_field
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.
        Returns: PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        return MultiHostUrl.build(
            scheme=f"{PostgreSQLDrivers.DEFAULT_DIALECT}+{PostgreSQLDrivers.DEFAULT_ASYNC_DRIVER}",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            path=self.NAME,
        )


class ApplicationSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30
    SECRET_KEY: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    db: DatabaseSettings
    app: ApplicationSettings


try:
    settings = Settings(
        db=DatabaseSettings(),
        app=ApplicationSettings(),
    )
    print(settings.model_dump())
except ValidationError as e:
    main_logger.critical("Some environment variables are incorrect.")
    main_logger.critical("Error in .env, validate the app/core/config/settings.py")
    for error in e.errors():
        main_logger.critical(
            f"{error.get('type')} {error.get('loc')} {error.get('msg')}"
        )
    exit(1)
