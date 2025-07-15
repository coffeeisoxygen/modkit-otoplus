"""JWT utility functions for token creation and validation.

Hasan Maki and Copilot
"""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt

from src.backend.core.app_settings import get_settings
from src.backend.exceptions.cst_exception import AppException


def create_access_token(data: dict[str, Any], expires_delta: int = 30) -> str:
    """Create a JWT access token with an expiration time.

    Args:
        data (dict[str, Any]): Data to encode in the token.
        expires_delta (int): Expiration time in minutes.

    Returns:
        str: Encoded JWT token.

    Raises:
        AppException.InvalidTokenError: If SECRET_KEY or ALGORITHM is missing.

    Hasan Maki and Copilot
    """
    settings = get_settings()
    secret_key = settings.SECRET_KEY
    algorithm = settings.ALGORITHM
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    if not secret_key or not algorithm:
        raise AppException.InvalidTokenError()
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)
