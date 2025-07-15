from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.mlog.cst_logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: D103, RUF029
    logger.info("🟢 Starting application...")
    yield
    logger.info("🔴 Shutting down application...")
