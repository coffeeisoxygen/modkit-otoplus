import ipaddress

from pydantic import AnyHttpUrl

from src.backend.schemas.exception import (
    IPAddressValidationError,
    NameValidationError,
    PasswordValidationError,
    PinValidationError,
    URLReportValidationError,
)


def validate_name(v: str) -> str:
    """Validating member name."""
    if v is not None and (not isinstance(v, str) or not v.isalnum()):
        raise NameValidationError()
    return v


def validate_ip(v: str) -> str:
    """Validating member IP address."""
    if v is not None:
        try:
            ipaddress.ip_address(v)
        except Exception as e:
            raise IPAddressValidationError() from e
    return v


def validate_url(v: str | None) -> str | None:
    """Validating member URL report."""
    if v is not None:
        try:
            AnyHttpUrl(v)
        except Exception as e:
            raise URLReportValidationError() from e
    return v


def validate_pin(v: str | int) -> str:
    """Validating member PIN."""
    if v is not None:
        if isinstance(v, int):
            v = str(v)
        if not v.isdigit() or len(v) != 6:
            raise PinValidationError()
    return v


def validate_password(v: str) -> str:
    """Validating member password."""
    if v is not None and (not isinstance(v, str) or not (6 <= len(v) <= 10)):
        raise PasswordValidationError()
    return v
