from fastapi import FastAPI

from src.backend.api.v1.auth import router as auth_router
from src.backend.api.v1.member import router as member_router
from src.backend.api.v1.user import router as user_router


def register_routers(app: FastAPI):
    """Register all routers for the application."""
    app.include_router(auth_router)
    app.include_router(user_router)
    app.include_router(member_router)
