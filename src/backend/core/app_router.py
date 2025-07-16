from fastapi import FastAPI

from src.backend.api.v1.admin import member_router as admin_member_router
from src.backend.api.v1.admin import user_router as admin_user_router
from src.backend.api.v1.auth import router as public_auth_router

# from src.backend.api.v1.member import router as public_member_router
from src.backend.api.v1.user import router as public_user_router


def register_routers(app: FastAPI):
    """Register all routers for the application."""
    app.include_router(public_auth_router)
    app.include_router(public_user_router)
    # app.include_router(public_member_router)
    app.include_router(admin_member_router)
    app.include_router(admin_user_router)
