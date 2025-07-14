"""Member model for database using SQLAlchemy ORM."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .md_base import Base  # Import Base dari md_base.py


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(10), unique=True, index=True, nullable=False)
    ipaddress = Column(String(45), index=True, nullable=False)
    urlreport = Column(String(255), nullable=True)
    pin = Column(String(10), nullable=False)
    password = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Member(name={self.name}, ipaddress={self.ipaddress})>"
