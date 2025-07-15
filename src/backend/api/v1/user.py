"""User API routes for user management (public/user only).

Hanya endpoint /me yang tersedia di sini.
Endpoint CRUD user dipindahkan ke router admin.

Hasan Maki and Copilot
"""

from fastapi import APIRouter

from src.backend.dependencies.auth_dependency import CurrentUser
from src.backend.schemas.sc_user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: CurrentUser):
    """Get the currently authenticated user's information.

    Args:
        current_user (UserModel): The current authenticated user.

    Returns:
        UserRead: The current user's data.

    Hasan Maki and Copilot
    """
    return current_user
