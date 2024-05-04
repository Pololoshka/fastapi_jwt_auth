from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AppSettings(Settings):
    app_host: str
    app_port: int = 8000
    debug: bool = False


class AuthenticationSettings(Settings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 30


class DBSettings(Settings):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )
