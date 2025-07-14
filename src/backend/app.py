from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src._version import __version__ as version
from src.mlog.cst_logging import logger, patch_uvicorn_loggers, setup_logging

# Setup logging before anything else
setup_logging()
patch_uvicorn_loggers()
version = version.split(" ")[0]  # Extract the version number only


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, RUF029
    """Application lifespan events."""
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    lifespan=lifespan,
    title="My FastAPI App",
    description="This is a sample FastAPI application.",
    version=version,
)


@app.get("/")
async def read_root():
    logger.info("Hello endpoint accessed")
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
