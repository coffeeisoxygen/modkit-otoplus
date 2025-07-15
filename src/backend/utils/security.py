from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from src.backend.config.settings import get_settings
from src.backend.utils.exceptions.app_exceptions import AppException

settings = get_settings()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM: str = settings.ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt. Hasan Maki and Copilot."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password. Hasan Maki and Copilot."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: int = 30) -> str:
    """Create a JWT access token with an expiration time. Hasan Maki and Copilot."""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    if not SECRET_KEY or not ALGORITHM:
        raise AppException.InvalidTokenError()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
