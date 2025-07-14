from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.backend.schemas.validators import (
    validate_ip,
    validate_name,
    validate_password,
    validate_pin,
    validate_url,
)


class MemberBase(BaseModel):
    name: str
    ipaddress: str
    urlreport: str | None = None
    pin: str
    password: str
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return validate_name(v)

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
        return validate_password(v)

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    name: str | None = None
    ipaddress: str | None = None
    urlreport: str | None = None
    pin: str | None = None
    password: str | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        return validate_name(v) if v is not None else v

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
        return validate_password(v) if v is not None else v

class MemberRead(MemberBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
