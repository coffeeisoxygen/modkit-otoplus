"""module for user validation functions."""

from src.backend.exceptions.cst_exception import AppException
from src.backend.utils.validator.cmn_validator import (
    validate_alphanumeric_name,
    validate_strength_password,
)


def validate_username(v: str) -> str:
    """Validate the username.

    This function checks if the provided username meets the required criteria.

    Args:
        v (str): The username to validate.

    Raises:
        AppException.UsernameValidationError: If the username is invalid.

    Returns:
        str: The validated username.
    """
    if not validate_alphanumeric_name(v):
        raise AppException.UsernameValidationError()
    return v


def validate_password(v: str) -> str:
    """Validate the password.

    This function checks if the provided password meets the required criteria.

    Args:
        v (str): The password to validate.

    Raises:
        AppException.PasswordValidationError: If the password is invalid.

    Returns:
        str: The validated password.
    """
    if not validate_strength_password(v):
        raise AppException.PasswordValidationError()
    return v
