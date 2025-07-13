"""Database engine, session, and initialization logic."""

import os  # noqa: I001
from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from src.backend.models.member import Member
# --- CONFIGURABLE DATABASE URL ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# --- ENGINE ---
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)

# --- SESSION MAKER (Manual use in Streamlit / scripts) ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- CONTEXTMANAGER FOR FASTAPI Depends() ---
@contextmanager
def get_session():
    """Yield a SQLModel Session for database operations within a context manager."""
    with Session(engine) as session:
        yield session


# --- ANNOTATED DEPENDENCY FOR FASTAPI ROUTES ---
DBSession = Annotated[Session, Depends(get_session)]


# --- DEV-ONLY: CREATE TABLES (Not for production) ---
def create_database_and_tables():
    """(DEV ONLY) Create the database and tables if they do not exist."""
    SQLModel.metadata.create_all(engine)


# sample usage :
# in streamlit (frontend) or scripts, you can use:
# from backend.core import SessionLocal
# from backend.models import Member
# def get_members():
#     with SessionLocal() as session:
#         return session.query(Member).all()

# # in Fast Api routes, you can use:
# from backend.core import DBSession
# @app.get("/members")
# def list_members(session: DBSession):
#     return session.exec(select(Member)).all()
