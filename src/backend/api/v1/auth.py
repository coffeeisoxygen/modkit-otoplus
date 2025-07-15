from fastapi import APIRouter, Depends

from src.backend.config.database import DBSession
from src.backend.schemas.sc_auth import AuthLogin, TokenResponse
from src.backend.services.sr_auth import AuthService
from src.backend.utils.result.service_result import handle_result

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: AuthLogin, db: DBSession = Depends()):
    result = AuthService(db).login(data.username, data.password)
    return handle_result(result)
