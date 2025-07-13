"""Custom exceptions for validation errors in the application."""


class PinValidationError(ValueError):
    """Exception raised for errors in the pin validation."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Pin must be a 6-digit integer."
        super().__init__(message)


class PasswordValidationError(ValueError):
    """Exception raised for errors in the password validation."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Password must be between 6 and 10 characters."
        super().__init__(message)


class NameValidationError(ValueError):
    """Exception raised for errors in the name validation."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "Name must be alphanumeric."
        super().__init__(message)


class IPAddressValidationError(ValueError):
    """Exception raised for errors in the IP address validation."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "IP address must be a valid IPv4 or IPv6 address."
        super().__init__(message)


class URLReportValidationError(ValueError):
    """Exception raised for errors in the URL report validation."""

    def __init__(self, message: str | None = None):
        if message is None:
            message = "urlreport must be a valid URL."
        super().__init__(message)
