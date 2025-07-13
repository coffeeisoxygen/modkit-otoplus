from contextlib import asynccontextmanager

from fastapi import FastAPI

from mlog.cst_logging import patch_uvicorn_loggers, setup_logging
from src._version import __version__ as version

# Ensure logging is set up before using the middleware
setup_logging()
patch_uvicorn_loggers()

version = version.split(" ")[0]  # Extract the version number only


@asynccontextmanager
async def lifespan(app: FastAPI):
    # e.g., connect to database, initialize resources
    yield
    # Shutdown logic here
    # e.g., close database connections, cleanup


app = FastAPI(
    lifespan=lifespan,
    title="My FastAPI App",
    description="This is a sample FastAPI application.",
    version=version,
)
