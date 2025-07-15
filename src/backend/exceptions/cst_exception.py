from http import HTTPStatus

from starlette.responses import JSONResponse


class AppExceptionError(Exception):
    """Base exception class for application-specific errors.

    Attributes:
        status_code (int): HTTP status code.
        context (dict): Contextual information for the error.

    Hasan Maki and Copilot
    """

    def __init__(self, status_code: int, context: dict | None = None):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context or {}

    def __str__(self) -> str:
        return (
            f"<AppException {self.exception_case} - "
            f"status_code={self.status_code} - context={self.context}>"
        )


def app_exception_handler(exc: AppExceptionError):
    """Handle application exceptions and return a JSON response.

    Args:
        exc (AppExceptionError): The exception to handle.

    Returns:
        JSONResponse: The response for the exception.

    Hasan Maki and Copilot
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )


class AppException:
    """Namespace for custom application exceptions. Hasan Maki and Copilot."""

    class UsernameValidationError(AppExceptionError):
        """Exception raised for invalid usernames. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Username cannot be empty"},
            )

    class PasswordHashValidationError(AppExceptionError):
        """Exception raised for errors in the password hash validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Password hash must be a valid hash."},
            )

    class PasswordConfirmValidationError(AppExceptionError):
        """Exception raised for errors in the password confirmation validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Password confirmation does not match."},
            )

    class PinValidationError(AppExceptionError):
        """Exception raised for errors in the pin validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Pin must be a 6-digit integer."},
            )

    class PasswordValidationError(AppExceptionError):
        """Exception raised for errors in the password validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Password must be between 6 and 10 characters."},
            )

    class NameValidationError(AppExceptionError):
        """Exception raised for errors in the name validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "Name must be alphanumeric."},
            )

    class IPAddressValidationError(AppExceptionError):
        """Exception raised for errors in the IP address validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context
                or {"message": "IP address must be a valid IPv4 or IPv6 address."},
            )

    class URLReportValidationError(AppExceptionError):
        """Exception raised for errors in the URL report validation. Hasan Maki and Copilot."""

        def __init__(self, context: dict | None = None):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                context or {"message": "urlreport must be a valid URL."},
            )

    class UserNotFoundError(AppExceptionError):
        """Exception raised when a user is not found. Hasan Maki and Copilot."""

        def __init__(self, user_id: int):
            super().__init__(
                HTTPStatus.NOT_FOUND,
                {"message": f"User ID {user_id} not found"},
            )

    class UserNameNotFoundError(AppExceptionError):
        """Exception raised when a username is not found. Hasan Maki and Copilot."""

        def __init__(self, username: str):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {"message": f"Username '{username}' not found"},
            )

    class UsernameAlreadyExistsError(AppExceptionError):
        """Exception raised when a username already exists. Hasan Maki and Copilot."""

        def __init__(self, username: str):
            super().__init__(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {"message": f"Username '{username}' already exists"},
            )

    class DatabaseError(AppExceptionError):
        """Exception raised for database errors. Hasan Maki and Copilot."""

        def __init__(self, error: str):
            super().__init__(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"message": "Database error", "detail": error},
            )

    class InvalidCredentialsError(AppExceptionError):
        """Exception raised for invalid credentials. Hasan Maki and Copilot."""

        def __init__(self):
            super().__init__(
                HTTPStatus.UNAUTHORIZED,
                {"message": "Invalid username or password"},
            )

    class InvalidTokenError(AppExceptionError):
        """Exception raised for invalid tokens. Hasan Maki and Copilot."""

        def __init__(self):
            super().__init__(
                HTTPStatus.UNAUTHORIZED,
                {"message": "Invalid or expired token"},
            )

    class ForbiddenActionError(AppExceptionError):
        """Exception raised for forbidden actions. Hasan Maki and Copilot."""

        def __init__(self, action: str):
            super().__init__(
                HTTPStatus.FORBIDDEN,
                {
                    "message": f"Action '{action}' is forbidden, Admin Only or contact Admin."
                },
            )

    class MemberNotFoundError(AppExceptionError):
        """Exception raised when a member is not found. Hasan Maki and Copilot."""

        def __init__(self, member_id: int):
            super().__init__(
                HTTPStatus.NOT_FOUND,
                {"message": f"Member ID {member_id} not found"},
            )
