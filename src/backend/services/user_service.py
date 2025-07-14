from sqlalchemy.exc import SQLAlchemyError

from src.backend.models.md_user import User
from src.backend.schemas.sc_user import UserCreate, UserUpdate
from src.backend.services.base import AppCRUD, AppService
from src.backend.utils.exceptions.app_exceptions import AppException
from src.backend.utils.result.service_result import ServiceResult
from src.backend.utils.security import hash_password


class UserCRUD(AppCRUD):
    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, data: UserCreate) -> User:
        user_data = data.model_dump(exclude={"password_confirm"})
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        return None


class UserService(AppService):
    def get_user(self, user_id: int) -> ServiceResult:
        user = UserCRUD(self.db).get_by_id(user_id)
        if not user:
            return ServiceResult(AppException.UserNotFouncError(user_id))
        return ServiceResult(user)

    def create_user(self, data: UserCreate) -> ServiceResult:
        if UserCRUD(self.db).get_by_username(data.username):
            return ServiceResult(AppException.UsernameAlreadyExistsError(data.username))
        try:
            user = UserCRUD(self.db).create(data)
            return ServiceResult(user)
        except SQLAlchemyError as e:
            return ServiceResult(AppException.DatabaseError(str(e)))

    def update_user(self, user_id: int, data: UserUpdate) -> ServiceResult:
        crud = UserCRUD(self.db)
        user = crud.get_by_id(user_id)
        if not user:
            return ServiceResult(AppException.UserNotFouncError(user_id))
        updated_user = crud.update(user, data)
        return ServiceResult(updated_user)

    def delete_user(self, user_id: int) -> ServiceResult:
        crud = UserCRUD(self.db)
        user = crud.get_by_id(user_id)
        if not user:
            return ServiceResult(AppException.UserNotFouncError(user_id))
        crud.delete(user)
        return ServiceResult({"deleted": True})
