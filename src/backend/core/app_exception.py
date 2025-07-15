from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from src.backend.utils.app_exceptions import AppExceptionError
from src.backend.utils.req_exception import (
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
)


def register_exception_handlers(app: FastAPI):
    """Registering then Exceptions."""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(AppExceptionError, app_exception_handler)
