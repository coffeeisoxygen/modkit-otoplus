from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file.

    Semua konfigurasi aplikasi diambil dari environment variable
    dan didefinisikan di sini agar terpusat dan mudah di-maintain.

    Hasan Maki and Copilot
    """

    ENV_MODE: str
    DATABASE_NAME: str
    DATABASE_URL: str
    DATABASE_ECHO: bool = False
    CACHE_SERVICE: str = "inmemory"
    CACHE_TTL: int = 3600
    CACHE_MAX_SIZE: int = 100
    SECRET_KEY: str
    ALGORITHM: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "forbid",  # error jika ada field .env yang tidak didefinisikan
    }


@lru_cache
def get_settings() -> Settings:
    """Get application settings.

    This function retrieves the application settings from the environment variables.

    Returns:
        Settings: The application settings.

    Hasan Maki and Copilot
    """
    return Settings()  # type: ignore
