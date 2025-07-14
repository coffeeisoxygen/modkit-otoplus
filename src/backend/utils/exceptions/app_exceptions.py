from starlette.responses import JSONResponse


class AppExceptionError(Exception):
    """Base exception class for application-specific errors."""

    def __init__(self, status_code: int, context: dict | None = None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context or {}

    def __str__(self):
        return (
            f"<AppException {self.exception_case} - "
            f"status_code={self.status_code} - context={self.context}>"
        )


def app_exception_handler(exc: AppExceptionError):
    """Handle application exceptions and return a JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )


class AppException:
    """Namespace for custom application exceptions."""

    class UsernameValidationError(AppExceptionError):
        """Exception raised for invalid usernames."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self, status_code, context or {"message": "Username cannot be empty"}
            )

    class PinValidationError(AppExceptionError):
        """Exception raised for errors in the pin validation."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self,
                status_code,
                context or {"message": "Pin must be a 6-digit integer."},
            )

    class PasswordValidationError(AppExceptionError):
        """Exception raised for errors in the password validation."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self,
                status_code,
                context or {"message": "Password must be between 6 and 10 characters."},
            )

    class NameValidationError(AppExceptionError):
        """Exception raised for errors in the name validation."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self, status_code, context or {"message": "Name must be alphanumeric."}
            )

    class IPAddressValidationError(AppExceptionError):
        """Exception raised for errors in the IP address validation."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self,
                status_code,
                context
                or {"message": "IP address must be a valid IPv4 or IPv6 address."},
            )

    class URLReportValidationError(AppExceptionError):
        """Exception raised for errors in the URL report validation."""

        def __init__(self, context: dict | None = None):
            status_code = 422
            AppExceptionError.__init__(
                self,
                status_code,
                context or {"message": "urlreport must be a valid URL."},
            )

    class UserNotFound(AppExceptionError):
        """Exception raised when a user is not found."""

        def __init__(self, user_id: int):
            super().__init__(422, {"message": f"User ID {user_id} not found"})

    class UsernameAlreadyExists(AppExceptionError):
        """Exception raised when a username already exists."""

        def __init__(self, username: str):
            super().__init__(422, {"message": f"Username '{username}' already exists"})

    class DatabaseError(AppExceptionError):
        """Exception raised for database errors."""

        def __init__(self, error: str):
            super().__init__(500, {"message": "Database error", "detail": error})
