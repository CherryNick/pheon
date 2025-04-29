from pathlib import Path
from typing import Annotated

from fastapi import Depends
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).resolve().parent.parent


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(env_path /".env", env_path / ".env.example"),
        extra="ignore",
    )


class DataBaseConfig(BaseConfig):
    path: str | None = Field(None, alias="DATABASE_PATH")
    host: str | None = Field(None, alias="DATABASE_HOST")
    port: int | None = Field(None, alias="DATABASE_PORT")
    user: str | None = Field(None, alias="DATABASE_USER")
    password: str | None = Field(None, alias="DATABASE_PASSWORD")
    db_name: str | None = Field(None, alias="DATABASE_NAME")
    driver: str = Field(..., alias="DATABASE_DRIVER")
    sync_driver: str = Field(..., alias="DATABASE_SYNC_DRIVER")

    echo: bool = Field(False, alias="DATABASE_ECHO")
    pool_size: int | None = Field(None, alias="DATABASE_POOL_SIZE")
    max_overflow: int | None = Field(None, alias="DATABASE_MAX_OVERFLOW")
    pool_timeout: int | None = Field(None, alias="DATABASE_POOL_TIMEOUT")
    pool_recycle: int | None = Field(None, alias="DATABASE_POOL_RECYCLE")

    @model_validator(mode="after")
    def validate_path_or_credentials(self) -> "DataBaseConfig":
        if self.path and any([self.host, self.port, self.user, self.password, self.db_name]):
            raise ValueError("Specify either 'path' or all other database connection fields, not both.")
        if not self.path and not all([self.host, self.port, self.user, self.password, self.db_name]):
            raise ValueError("Either 'path' or all other database connection fields must be specified.")
        return self

    @property
    def uri(self) -> str:
        if self.host:
            return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        else:
            return f"{self.driver}:///{self.path}"

    @property
    def sync_uri(self) -> str:
        if self.host:
            return f"{self.sync_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        else:
            return f"{self.sync_driver}:///{self.path}"


class JWTConfig(BaseConfig):
    secret: str = Field(..., alias="JWT_SECRET")
    algorithm: str = Field("HS256")
    access_token_expire_minutes: int = Field(15)
    refresh_token_expire_minutes: int = Field(60 * 24 * 7)  # 7 days

class SystemConfig(BaseConfig):
    user_password: str = Field(..., alias="SYSTEM_USER_PASSWORD")


class Config(BaseConfig):
    system: SystemConfig = Field(default_factory=SystemConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    database: DataBaseConfig = Field(default_factory=DataBaseConfig)
    cors_origins: list[str] = Field(default=["*"])


def get_config() -> Config:
    return Config()

ConfigDependency = Annotated[Config, Depends(get_config)]
