"""Configuration management"""
import os
from pydantic_settings import BaseSettings
from typing import List


def _build_async_db_url() -> str:
    raw = os.environ.get("DATABASE_URL", "")
    if raw.startswith("postgresql://") or raw.startswith("postgres://"):
        return raw.replace("postgresql://", "postgresql+asyncpg://", 1).replace(
            "postgres://", "postgresql+asyncpg://", 1
        ).split("?")[0]
    return "postgresql+asyncpg://covenant:covenant@localhost:5432/covenant"


class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = _build_async_db_url()
    DATABASE_POOL_SIZE: int = 5

    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str = "change-me-in-production-use-env-var"
    JWT_SECRET: str = "jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS512"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: List[str] = ["*"]

    ENABLE_QUANTUM_OPTIMIZATION: bool = False
    ENABLE_BLOCKCHAIN: bool = False

    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    RATE_LIMIT_MAX_REQUESTS: int = 300

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
