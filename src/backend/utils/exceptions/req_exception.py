"""Exception handlers for FastAPI application.

Provides handlers for HTTPException, RequestValidationError, and custom
AppExceptionError. Uses centralized logging from mlog.cst_logging.

Hasan Maki and Copilot
"""

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.backend.utils.exceptions.app_exceptions import AppExceptionError
from src.backend.utils.result.service_result import caller_info
from src.mlog.cst_logging import logger


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: RUF029
    """Handle HTTP exceptions.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception raised.

    Returns:
        JSONResponse: The response for the exception.

    Hasan Maki and Copilot
    """
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    logger.error(f"Unhandled HTTP exception: {exc} | caller={caller_info()}")
    raise exc


async def request_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Handle request validation exceptions.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception raised.

    Returns:
        JSONResponse: The response for the validation error.

    Hasan Maki and Copilot
    """
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())},
        )
    logger.error(f"Request validation error: {exc} | caller={caller_info()}")
    raise exc


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle application exceptions.

    Args:
        request (Request): The incoming request.
        exc (Exception): The exception raised.

    Returns:
        JSONResponse: The response for the application exception.

    Hasan Maki and Copilot
    """
    if isinstance(exc, AppExceptionError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"app_exception": exc.exception_case, "context": exc.context},
        )
    logger.error(f"Application exception: {exc} | caller={caller_info()}")
    raise exc
