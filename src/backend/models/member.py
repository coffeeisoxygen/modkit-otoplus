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


class Member(SQLModel, table=True):
    """Model For Registered Member to Consume Api."""

    id: int | None = Field(default=None, index=True, primary_key=True, nullable=False)
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

    @field_validator("urlreport", mode="before")
    @classmethod
    def validate_urlreport(cls, value: str | None) -> str | None:
        """Ensure urlreport is a valid URL if not None."""
        if value is None:
            return value
        try:
            AnyHttpUrl(value)
        except Exception as err:
            raise URLReportValidationError() from err
        return value

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
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Ensure name is alphanumeric only."""
        if not isinstance(value, str) or not value.isalnum():
            raise NameValidationError()
        return value

    @field_validator("ipaddress", mode="before")
    @classmethod
    def validate_ipaddress(cls, value: str) -> str:
        """Ensure ipaddress is a valid IPvAnyAddress."""
        try:
            ipaddress.ip_address(value)
        except Exception as err:
            raise IPAddressValidationError() from err
        return value

    @field_validator("pin", mode="before")
    @classmethod
    def validate_pin(cls, value: str | int) -> str:
        """Ensure pin is exactly 6-digit numeric string."""
        if isinstance(value, int):
            value = str(value)
        if not value.isdigit() or len(value) != 6:
            raise PinValidationError()
        return value

    @field_validator("password", mode="before")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """Ensure password is a string with length between 6 and 10."""
        if not isinstance(value, str) or not (6 <= len(value) <= 10):
            raise PasswordValidationError()
        return value

    def __repr__(self):
        return f"<Member(name={self.name}, ipaddress={self.ipaddress}, urlreport={self.urlreport}, pin={self.pin}, password={self.password})>"
