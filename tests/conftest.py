import uuid
from unittest.mock import MagicMock

import pytest
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.backend.app import app
from src.backend.core.app_dbsetting import Base, get_session
from src.backend.models.md_member import Member
from src.backend.models.md_user import User
from src.backend.schemas.sc_member import MemberCreate, MemberUpdate
from src.backend.schemas.sc_user import UserCreate, UserUpdate

# Use file-based SQLite for test reliability
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Seed admin user
    session = TestingSessionLocal()
    try:
        if not session.query(User).filter_by(username="Administrator").first():
            admin = User(
                username="Administrator",
                email="admin@example.com",
                password=bcrypt.hash("@Admin12345"),
                is_active=True,
                is_superuser=True,
            )
            session.add(admin)
            session.commit()
    finally:
        session.close()
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


@pytest.fixture
def member_create() -> MemberCreate:
    unique = uuid.uuid4().hex[:8]
    return MemberCreate(
        name=f"member_{unique}",
        ipaddress=f"192.168.1.{int(unique[:2], 16) % 255}",
        urlreport="http://example.com/report",
        pin="123456",
        password="Abc123@",
        is_active=True,
        allow_no_sign=False,
    )


@pytest.fixture
def member_update() -> MemberUpdate:
    return MemberUpdate(urlreport="http://example.com/updated", is_active=False)


@pytest.fixture
def member(db_session) -> Member:
    unique = uuid.uuid4().hex[:8]
    member = Member(
        name=f"member_{unique}",
        ipaddress=f"192.168.1.{int(unique[:2], 16) % 255}",
        urlreport="http://example.com/report",
        pin="123456",
        password="Abc123@",
        is_active=True,
        allow_no_sign=False,
    )
    db_session.add(member)
    db_session.commit()
    db_session.refresh(member)
    return member


@pytest.fixture
def admin_user() -> User:
    unique = uuid.uuid4().hex[:8]
    return User(
        id=999,
        username=f"admin_{unique}",
        email=f"admin_{unique}@example.com",
        password="hashed",
        is_active=True,
        is_superuser=True,
    )
