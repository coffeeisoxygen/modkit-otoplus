"""Member model for database and API.

using pydantic & SQLModel
"""

from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, SQLModel

from src.backend.models.validators import (
    validate_ip,
    validate_name,
    validate_password,
    validate_pin,
    validate_url,
)


# --- SHARED BASE ---
class MemberBase(SQLModel):
    name: str = Field(
        index=True,
        unique=True,
        nullable=False,
        min_length=4,
        max_length=10,
        description="Name of the member",
    )
    ipaddress: str = Field(
        index=True, nullable=False, description="IP address of the member"
    )
    urlreport: str | None = Field(
        default=None,
        nullable=True,
        description="URL Report member to send Response, if Null will send back to Ipaddress",
    )
    pin: str = Field(nullable=False, description="PIN for member authentication")
    password: str = Field(
        nullable=False,
        min_length=6,
        max_length=10,
        description="Password for member authentication",
    )
    is_active: bool = Field(
        default=True, nullable=False, description="Is the member active?"
    )

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return validate_name(v)

    @field_validator("ipaddress", mode="before")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        return validate_ip(v)

    @field_validator("urlreport", mode="before")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        return validate_url(v)

    @field_validator("pin", mode="before")
    @classmethod
    def validate_pin(cls, v: str) -> str:
        return validate_pin(v)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)


# --- CREATE SCHEMA ---
class MemberCreate(MemberBase):
    pass


# --- UPDATE SCHEMA ---
class MemberUpdate(SQLModel):
    name: str | None = None
    ipaddress: str | None = None
    urlreport: str | None = None
    pin: str | None = None
    password: str | None = None
    is_active: bool | None = None

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return validate_name(v)

    @field_validator("ipaddress", mode="before")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        return validate_ip(v)

    @field_validator("urlreport", mode="before")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        return validate_url(v)

    @field_validator("pin", mode="before")
    @classmethod
    def validate_pin(cls, v: str) -> str:
        return validate_pin(v)

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)


# --- TABLE / ORM MODEL ---
class Member(MemberBase, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Member(name={self.name}, ipaddress={self.ipaddress})>"
