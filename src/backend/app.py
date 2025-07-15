from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

from mlog.cst_logging import logger, patch_uvicorn_loggers, setup_logging
from src._version import __version__ as version
from src.backend.api.v1.member import router as member_router
from src.backend.api.v1.user import router as user_router
from src.backend.utils.exceptions.app_exceptions import AppExceptionError
from src.backend.utils.exceptions.req_exception import (
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
)

# Load .env
load_dotenv()

# Setup logging before anything else
setup_logging()
patch_uvicorn_loggers()
version = version.split(" ")[0]


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, RUF029
    """Application lifespan events (startup/shutdown)."""
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    lifespan=lifespan,
    title="modkit-otoplus",
    description="Menjembatani transaksi antara otomax dan addon addon otoplus.",
    version=version,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(member_router)
app.include_router(user_router)


# Register the handler for FastAPI's HTTPException, not Starlette's
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(AppExceptionError, app_exception_handler)


@app.get("/")
async def read_root():
    """Root endpoint."""
    logger.info("Hello endpoint accessed")
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
