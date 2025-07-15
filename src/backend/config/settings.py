from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()  # pastikan ini dulu


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class SettingsLoadError(RuntimeError):
    def __init__(self, original_exc: Exception):
        super().__init__(
            "Gagal memuat konfigurasi aplikasi dari .env. "
            "Pastikan SECRET_KEY dan ALGORITHM sudah di-set."
        )
        self.original_exc = original_exc


# ✅ FUNGSI AMAN UNTUK AKSES SETTINGS
@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()  # type: ignore
    except Exception as exc:
        raise SettingsLoadError(exc) from exc
