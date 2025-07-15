from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.schemas.sc_auth import AuthLogin, TokenResponse
from src.backend.services.sr_auth import AuthService
from src.backend.utils.result.service_result import handle_result

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: AuthLogin, db: DBSession):
    """Endpoint login user.

    Args:
        data (AuthLogin): Data login user.
        db (DBSession): Database session.

    Returns:
        TokenResponse: Token hasil login.

    Hasan Maki and Copilot
    """
    result = AuthService(db).login(data.username, data.password)
    return handle_result(result)
