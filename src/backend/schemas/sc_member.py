from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.backend.utils.validator.member_validator import (
    validate_ip,
    validate_member_name,
    validate_member_password,
    validate_pin,
    validate_url,
)


class MemberBase(BaseModel):
    name: str = Field(..., min_length=6)
    ipaddress: str
    urlreport: str | None = None
    pin: str = Field(..., min_length=6, max_length=6)
    password: str = Field(..., min_length=6)
    is_active: bool = True
    allow_no_sign: bool = False
    balance: float = 0.0

    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return validate_member_name(v)

    @field_validator("ipaddress")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        return validate_ip(v)

    @field_validator("urlreport")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        return validate_url(v)

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, v: str) -> str:
        return validate_pin(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_member_password(v)


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    name: str | None = None
    ipaddress: str | None = None
    urlreport: str | None = None
    pin: str | None = None
    password: str | None = None
    is_active: bool | None = None
    allow_no_sign: bool | None = None
    balance: float | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        return validate_member_name(v) if v is not None else v

    @field_validator("ipaddress")
    @classmethod
    def validate_ip(cls, v: str | None) -> str | None:
        return validate_ip(v) if v is not None else v

    @field_validator("urlreport")
    @classmethod
    def validate_url(cls, v: str | None) -> str | None:
        return validate_url(v) if v is not None else v

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, v: str | None) -> str | None:
        return validate_pin(v) if v is not None else v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        return validate_member_password(v) if v is not None else v


class MemberRead(MemberBase):
    id: int
    created_at: datetime
