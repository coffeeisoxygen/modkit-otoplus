from unittest.mock import MagicMock, patch

import pytest
from src.backend.models.md_user import User
from src.backend.schemas.sc_user import UserCreate, UserUpdate
from src.backend.services.user_service import UserService
from src.backend.utils.exceptions.app_exceptions import AppException
from src.backend.utils.result.service_result import ServiceResult


@pytest.fixture
def db():
    return MagicMock()


@pytest.fixture
def user():
    return User(id=1, username="testuser", is_active=True)


@pytest.fixture
def user_create():
    return UserCreate(
        username="testuser",
        password="@Secret123",
        password_confirm="@Secret123",
        email="testuser@example.com",
    )


@pytest.fixture
def user_update():
    return UserUpdate(password="@Newpass123")


def test_get_user_found(db, user):
    with patch(
        "src.backend.services.user_service.UserCRUD.get_by_id", return_value=user
    ):
        service = UserService(db)
        result = service.get_user(user.id)
        assert isinstance(result, ServiceResult)
        assert result.success
        assert result.value == user


def test_get_user_not_found(db):
    with patch(
        "src.backend.services.user_service.UserCRUD.get_by_id", return_value=None
    ):
        service = UserService(db)
        result = service.get_user(999)
        assert not result.success
        assert isinstance(result.value, AppException.UserNotFouncError)


def test_create_user_success(db, user_create, user):
    with (
        patch(
            "src.backend.services.user_service.UserCRUD.get_by_username",
            return_value=None,
        ),
        patch("src.backend.services.user_service.UserCRUD.create", return_value=user),
    ):
        service = UserService(db)
        result = service.create_user(user_create)
        assert result.success
        assert result.value == user


def test_create_user_duplicate(db, user_create):
    with patch(
        "src.backend.services.user_service.UserCRUD.get_by_username", return_value=True
    ):
        service = UserService(db)
        result = service.create_user(user_create)
        assert not result.success
        assert isinstance(result.value, AppException.UsernameAlreadyExistsError)


def test_update_user_success(db, user, user_update):
    with (
        patch(
            "src.backend.services.user_service.UserCRUD.get_by_id", return_value=user
        ),
        patch("src.backend.services.user_service.UserCRUD.update", return_value=user),
    ):
        service = UserService(db)
        result = service.update_user(user.id, user_update)
        assert result.success
        assert result.value == user


def test_update_user_not_found(db, user_update):
    with patch(
        "src.backend.services.user_service.UserCRUD.get_by_id", return_value=None
    ):
        service = UserService(db)
        result = service.update_user(999, user_update)
        assert not result.success
        assert isinstance(result.value, AppException.UserNotFouncError)


def test_delete_user_success(db, user):
    with (
        patch(
            "src.backend.services.user_service.UserCRUD.get_by_id", return_value=user
        ),
        patch("src.backend.services.user_service.UserCRUD.delete", return_value=None),
    ):
        service = UserService(db)
        result = service.delete_user(user.id)
        assert result.success
        assert result.value == {"deleted": True}


def test_delete_user_not_found(db):
    with patch(
        "src.backend.services.user_service.UserCRUD.get_by_id", return_value=None
    ):
        service = UserService(db)
        result = service.delete_user(999)
        assert not result.success
        assert isinstance(result.value, AppException.UserNotFouncError)
