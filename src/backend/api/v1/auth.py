from fastapi import APIRouter, Form

from src.backend.core.app_dbsetting import DBSession
from src.backend.schemas.sc_auth import TokenResponse
from src.backend.services.sr_auth import AuthService
from src.backend.utils.result.service_result import handle_result

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    db: DBSession,
    username: str = Form(...),
    password: str = Form(...),
):
    """Endpoint login user.

    Args:
        username (str): Username user.
        password (str): Password user.
        db (DBSession): Database session.

    Returns:
        TokenResponse: Token hasil login.

    Hasan Maki and Copilot
    """
    result = AuthService(db).login(username, password)
    return handle_result(result)
