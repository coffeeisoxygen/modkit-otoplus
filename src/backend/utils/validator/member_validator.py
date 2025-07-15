import ipaddress

from pydantic import AnyHttpUrl

from src.backend.exceptions.cst_exception import AppException
from src.backend.utils.validator.cmn_validator import (
    validate_alphanumeric_name,
    validate_strength_password,
)


def validate_member_name(v: str) -> str:
    """Validating member name."""
    if not validate_alphanumeric_name(v):
        raise AppException.NameValidationError()
    return v


def validate_ip(v: str) -> str:
    """Validating member IP address."""
    if v is not None:
        try:
            ipaddress.ip_address(v)
        except Exception as e:
            raise AppException.IPAddressValidationError() from e
    return v


def validate_url(v: str | None) -> str | None:
    """Validating member URL report."""
    if v is not None:
        try:
            AnyHttpUrl(v)
        except Exception as e:
            raise AppException.URLReportValidationError() from e
    return v


def validate_pin(v: str | int) -> str:
    """Validating member PIN."""
    if v is not None:
        if isinstance(v, int):
            v = str(v)
        if not v.isdigit() or len(v) != 6:
            raise AppException.PinValidationError()
    return v


def validate_member_password(v: str) -> str:
    """Validating member password."""
    if not validate_strength_password(v):
        raise AppException.PasswordValidationError()
    return v
