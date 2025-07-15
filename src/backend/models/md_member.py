"""Member model for database using SQLAlchemy ORM."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.backend.core.app_dbsetting import Base


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(10), unique=True, index=True, nullable=False
    )
    ipaddress: Mapped[str] = mapped_column(String(45), index=True, nullable=False)
    urlreport: Mapped[str | None] = mapped_column(String(255), nullable=True)
    pin: Mapped[str] = mapped_column(String(10), nullable=False)
    password: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allow_no_sign: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    def __repr__(self):
        return f"<Member(name={self.name}, ipaddress={self.ipaddress})>"
