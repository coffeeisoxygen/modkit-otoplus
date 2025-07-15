"""Database engine, session, and initialization logic.

Hasan Maki and Copilot
"""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.backend.core.app_settings import get_settings

settings = get_settings()

# --- Config ---
DATABASE_URL = settings.DATABASE_URL
DATABASE_ECHO = settings.DATABASE_ECHO

# --- Engine ---
engine = create_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

# --- Session (for scripts / Streamlit) ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Session (for FastAPI via Depends) ---


def get_session() -> Generator[Session, None, None]:
    """Get a new database session.

    This function provides a new SQLAlchemy database session for each request.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A new SQLAlchemy database session.

    Hasan Maki and Copilot
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_session)]


# --- Dev-only Init ---
def create_database_and_tables() -> None:
    """Create DB & tables — dev only.

    Hasan Maki and Copilot
    """
    Base.metadata.create_all(engine)


Base = declarative_base()

# Example usage for Streamlit/scripts:
# with SessionLocal() as session:
#     members = session.query(Member).all()

# Example usage in FastAPI:
# @app.get("/members")
# def list_members(session: DBSession):
#     return session.exec(select(Member)).all()
