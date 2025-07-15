"""Dependency untuk otentikasi JWT dan otorisasi user.

Hasan Maki and Copilot
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.backend.core.app_dbsetting import DBSession
from src.backend.core.app_jwt import decode_access_token
from src.backend.exceptions.cst_exception import AppException
from src.backend.models.md_user import User as UserModel
from src.backend.services.sr_user import UserCRUD

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(db: DBSession, token: str = Depends(oauth2_scheme)) -> UserModel:
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
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except AppException.InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err

    user = UserCRUD(db).get_by_id(int(user_id))
    if not user:
        raise AppException.UserNotFoundError(int(user_id))
    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]


def require_admin(current_user: UserModel) -> UserModel:
    """Dependency untuk validasi admin (is_superuser).

    Hanya admin yang boleh akses. Raises HTTPException 403 jika bukan admin.
    Hasan Maki and Copilot
    """
    if not getattr(current_user, "is_superuser", False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user


def require_owner_or_admin(member_id: int, current_user: UserModel) -> UserModel:
    """Dependency untuk validasi owner atau admin.

    Hanya admin atau owner (user.id == member_id) yang boleh akses.
    Raises HTTPException 403 jika tidak memenuhi syarat.
    Hasan Maki and Copilot
    """
    if not (
        getattr(current_user, "is_superuser", False)
        or getattr(current_user, "id", None) == member_id
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return current_user
