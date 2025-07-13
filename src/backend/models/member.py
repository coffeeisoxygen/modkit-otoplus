"""member for our API."""

import ipaddress
from datetime import datetime

from pydantic import AnyHttpUrl, field_validator
from sqlmodel import Field, SQLModel

from src.backend.models.exception import (
    IPAddressValidationError,
    NameValidationError,
    PasswordValidationError,
    PinValidationError,
    URLReportValidationError,
)


# Base class for shared fields and validators
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
    pin: str = Field(
        default=None, nullable=False, description="PIN for member authentication"
    )
    password: str = Field(
        default=None,
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
    def validate_name(cls, value: str) -> str:
        if not isinstance(value, str) or not value.isalnum():
            raise NameValidationError()
        return value

    @field_validator("ipaddress", mode="before")
    @classmethod
    def validate_ipaddress(cls, value: str) -> str:
        try:
            ipaddress.ip_address(value)
        except Exception as err:
            raise IPAddressValidationError() from err
        return value

    @field_validator("urlreport", mode="before")
    @classmethod
    def validate_urlreport(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            AnyHttpUrl(value)
        except Exception as err:
            raise URLReportValidationError() from err
        return value

    @field_validator("pin", mode="before")
    @classmethod
    def validate_pin(cls, value: str | int) -> str:
        if isinstance(value, int):
            value = str(value)
        if not value.isdigit() or len(value) != 6:
            raise PinValidationError()
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not isinstance(value, str) or not (6 <= len(value) <= 10):
            raise PasswordValidationError()
        return value


# For creation (all fields required except urlreport)
class MemberCreate(MemberBase):
    pass


# For update (all fields optional)
class MemberUpdate(SQLModel):
    name: str | None = None
    ipaddress: str | None = None
    urlreport: str | None = None
    pin: str | None = None
    password: str | None = None
    is_active: bool | None = None

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if value is not None and (not isinstance(value, str) or not value.isalnum()):
            raise NameValidationError()
        return value

    @field_validator("ipaddress", mode="before")
    @classmethod
    def validate_ipaddress(cls, value):
        if value is not None:
            try:
                ipaddress.ip_address(value)
            except Exception as err:
                raise IPAddressValidationError() from err
        return value

    @field_validator("urlreport", mode="before")
    @classmethod
    def validate_urlreport(cls, value):
        if value is not None:
            try:
                AnyHttpUrl(value)
            except Exception as err:
                raise URLReportValidationError() from err
        return value

    @field_validator("pin", mode="before")
    @classmethod
    def validate_pin(cls, value):
        if value is not None:
            if isinstance(value, int):
                value = str(value)
            if not value.isdigit() or len(value) != 6:
                raise PinValidationError()
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value):
        if value is not None and (not isinstance(value, str) or not (6 <= len(value) <= 10)):
            raise PasswordValidationError()
        return value


# For delete (just the id)
class MemberDelete(SQLModel):
    id: int


# The ORM/table model
class Member(MemberBase, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Member(name={self.name}, ipaddress={self.ipaddress}, urlreport={self.urlreport}, pin={self.pin}, password={self.password})>"
