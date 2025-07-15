from sqlalchemy.exc import SQLAlchemyError

from src.backend.core.app_settings import get_settings
from src.backend.exceptions.app_exceptions import AppException
from src.backend.schemas.sc_user import UserCreate
from src.backend.services.base import AppService
from src.backend.services.service_result import ServiceResult
from src.backend.services.sr_user import UserCRUD


class AdminSeeder(AppService):
    def seed_admin(self) -> ServiceResult:
        settings = get_settings()
        username = settings.ADMIN_USERNAME
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD

        crud = UserCRUD(self.db)
        existing = crud.get_by_username(username)
        if existing:
            return ServiceResult({"message": "Admin already exists."})

        try:
            admin_data = UserCreate(
                username=username,
                email=email,
                password=password,
                password_confirm=password,
                is_active=True,
                is_superuser=True,
            )
            user = crud.create(admin_data)
            return ServiceResult({"message": "Admin created", "id": user.id})
        except SQLAlchemyError as e:
            return ServiceResult(AppException.DatabaseError(str(e)))
