from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.backend.utils.exceptions.app_exceptions import AppExceptionError


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    raise exc


async def request_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())},
        )
    raise exc


async def app_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppExceptionError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"app_exception": exc.exception_case, "context": exc.context},
        )
    raise exc
