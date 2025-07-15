from contextlib import asynccontextmanager

from fastapi import FastAPI

# Add this import
from src.backend.core.app_dbsetting import get_session
from src.backend.services.sr_admin import AdminSeeder
from src.mlog.mylog import logger


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001, D103
    db = next(get_session())
    AdminSeeder(db).seed_admin()
    logger.info("🟢 Starting application...")
    yield
    logger.info("🔴 Shutting down application...")
