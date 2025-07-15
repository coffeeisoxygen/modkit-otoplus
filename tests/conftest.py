import uuid
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.app import app
from src.backend.core.app_dbsetting import Base, get_session
from src.backend.models.md_user import User
from src.backend.schemas.sc_user import UserCreate, UserUpdate

# Use file-based SQLite for test reliability
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    app.dependency_overrides[get_session] = lambda: db_session


@pytest.fixture
def session():
    """Mocked SQLModel session, no real DB."""
    return MagicMock()


@pytest.fixture
def user_payload():
    unique = uuid.uuid4().hex[:8]
    return {
        "username": f"testuser_{unique}",
        "password": "@Secret123",
        "password_confirm": "@Secret123",
        "email": f"testuser_{unique}@example.com",
    }


@pytest.fixture
def user_create():
    unique = uuid.uuid4().hex[:8]
    return UserCreate(
        username=f"testuser_{unique}",
        email=f"testuser_{unique}@example.com",
        password="@Secret123",
        password_confirm="@Secret123",
    )


@pytest.fixture
def user_update():
    return UserUpdate(password="@Newpass123")


@pytest.fixture
def user():
    unique = uuid.uuid4().hex[:8]
    return User(
        id=1,
        username=f"testuser_{unique}",
        email=f"testuser_{unique}@example.com",
        password="hashed",
        is_active=True,
        is_superuser=False,
    )


@pytest.fixture
def db():
    return MagicMock()
