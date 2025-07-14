"""Database engine, session, and initialization logic."""

import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.backend.models.md_base import Base  # Ganti ini, jangan deklarasi ulang!

# --- Load env ---
load_dotenv(dotenv_path=".env")

# --- Config ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./modkit.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() in ("true", "1", "yes")

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


def get_session():
    """Get a new database session.

    This function provides a new SQLAlchemy database session for each request.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A new SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(get_session)]


# --- Dev-only Init ---
def create_database_and_tables():
    """Create DB & tables — dev only."""
    Base.metadata.create_all(engine)


# Example usage for Streamlit/scripts:
# with SessionLocal() as session:
#     members = session.query(Member).all()

# Example usage in FastAPI:
# @app.get("/members")
# def list_members(session: DBSession):
#     return session.exec(select(Member)).all()
