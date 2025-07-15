"""Dependency untuk otentikasi JWT dan otorisasi user.

Hasan Maki and Copilot
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from src.backend.config.database import DBSession
from src.backend.services.sr_user import UserCRUD
from src.backend.utils.exceptions.app_exceptions import AppException
from src.backend.utils.security import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: DBSession = Depends()):
    """Ambil user dari JWT token.

    Args:
        token (str): JWT token dari header Authorization.
        db (DBSession): Session database.

    Returns:
        User: User yang terautentikasi.

    Raises:
        HTTPException: Jika token tidak valid atau user tidak ditemukan.

    Hasan Maki and Copilot
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception from None

    user = UserCRUD(db).get_by_id(int(user_id))
    if not user:
        raise AppException.UserNotFouncError(int(user_id))
    return user
