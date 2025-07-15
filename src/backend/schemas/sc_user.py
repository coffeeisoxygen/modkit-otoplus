"""User schemas."""

from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from src.backend.exceptions import cst_exception
from src.backend.utils.validator.user_validator import (
    validate_password,
    validate_username,
)


class UserBase(BaseModel):
    """Base model for user schemas."""

    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return validate_username(v)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str = Field(..., min_length=8)
    password_confirm: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password(v)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserCreate":
        if self.password != self.password_confirm:
            raise cst_exception.AppException.PasswordConfirmValidationError()
        return self


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    username: str | None = Field(default=None, min_length=3, max_length=20)
    email: EmailStr | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None
    password: str | None = Field(default=None, min_length=8)

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        return validate_username(v) if v else v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        return validate_password(v) if v else v


class User(UserBase):
    """Schema for a user with additional fields (from DB)."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserRead(BaseModel):
    """Schema for returning user data in responses (without password)."""

    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
