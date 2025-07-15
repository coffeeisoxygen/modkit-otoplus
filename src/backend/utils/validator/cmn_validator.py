import string

from src.backend.exceptions.app_exceptions import AppException


def validate_alphanumeric_name(v: str) -> str:
    """Validating name to be alphanumeric, allow space, dash, underscore."""
    allowed = set(string.ascii_letters + string.digits + " -_")
    if v is not None and (not isinstance(v, str) or any(c not in allowed for c in v)):
        raise AppException.NameValidationError({
            "message": "Name hanya boleh huruf, angka, spasi, strip, atau underscore"
        })
    return v


def validate_strength_password(v: str) -> str:
    """Validasi password kuat: min 1 huruf besar, 1 kecil, 1 angka, 1 simbol (opsional)."""
    if not isinstance(v, str):
        raise AppException.PasswordValidationError({
            "message": "Password harus berupa string"
        })
    if " " in v:
        raise AppException.PasswordValidationError({
            "message": "Password tidak boleh mengandung spasi"
        })
    if not any(c.islower() for c in v):
        raise AppException.PasswordValidationError({
            "message": "Password harus mengandung huruf kecil"
        })
    if not any(c.isupper() for c in v):
        raise AppException.PasswordValidationError({
            "message": "Password harus mengandung huruf besar"
        })
    if not any(c.isdigit() for c in v):
        raise AppException.PasswordValidationError({
            "message": "Password harus mengandung angka"
        })
    if not any(c in string.punctuation for c in v):
        raise AppException.PasswordValidationError({
            "message": "Password harus mengandung simbol (!@#$ dll)"
        })

    return v
