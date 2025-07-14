from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src._version import __version__ as version
from src.mlog.cst_logging import logger, patch_uvicorn_loggers, setup_logging

# Load .env
load_dotenv()

# Setup logging before anything else
setup_logging()
patch_uvicorn_loggers()
version = version.split(" ")[0]


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: RUF029
    """Application lifespan events (startup/shutdown)."""
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
    """Root endpoint."""
    logger.info("Hello endpoint accessed")
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # Simulate data fetching process
    item_data = f"Item data for {item_id}"
    return {"item_id": item_id, "cached": False, "data": item_data}


if __name__ == "__main__":
    uvicorn.run("src.backend.app:app", host="0.0.0.0", port=8000, reload=True)
