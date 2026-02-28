import warnings

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_SECRET_KEY = "your-secret-key-change-this-in-production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_name: str = "WebApp"
    debug: bool = False
    log_level: str = "info"
    cors_origins: list[str] = ["http://localhost:5746"]
    metrics_enabled: bool = True

    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "webapp"

    secret_key: str = _INSECURE_SECRET_KEY
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 24 * 60

    @model_validator(mode="after")
    def _validate_secret_key(self) -> "Settings":
        if self.secret_key == _INSECURE_SECRET_KEY:
            if not self.debug:
                raise ValueError("SECRET_KEY must be changed from the default value in production (DEBUG=False)")
            warnings.warn("Using insecure default SECRET_KEY — change this before deploying", stacklevel=1)
        return self

    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Settings()
