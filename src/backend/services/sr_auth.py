from sqlalchemy.exc import SQLAlchemyError

from src.backend.core.app_jwt import create_access_token
from src.backend.services.base import AppService
from src.backend.services.sr_user import UserCRUD
from src.backend.utils.exceptions.app_exceptions import AppException
from src.backend.utils.result.service_result import ServiceResult
from src.backend.utils.security import verify_password


class AuthService(AppService):
    def login(self, username: str, password: str) -> ServiceResult:
        user = UserCRUD(self.db).get_by_username(username)
        if not user:
            return ServiceResult(AppException.UserNameNotFoundError(username))

        if not verify_password(password, user.password):
            return ServiceResult(AppException.InvalidCredentialsError())

        try:
            token = create_access_token(data={"sub": str(user.id)})
            return ServiceResult({"access_token": token, "token_type": "bearer"})
        except SQLAlchemyError as e:
            return ServiceResult(AppException.DatabaseError(str(e)))
