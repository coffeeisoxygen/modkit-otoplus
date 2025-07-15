"""User API routes for user management.

Provides endpoints for creating, reading, updating, and deleting users.
All endpoints require authentication except for user creation.
"""

from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.dependencies.user_auth import CurrentUser
from src.backend.schemas.sc_user import UserCreate, UserRead, UserUpdate
from src.backend.services.sr_user import UserService
from src.backend.utils.result.service_result import handle_result

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, db: DBSession):
    """Create a new user.

    Args:
        data (UserCreate): The user creation payload.
        db (DBSession): Database session dependency.

    Returns:
        UserRead: The created user.
    """
    result = UserService(db).create_user(data)
    return handle_result(result)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: CurrentUser):
    """Get the currently authenticated user's information.

    Args:
        current_user (UserModel): The current authenticated user.

    Returns:
        UserRead: The current user's data.
    """
    return current_user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: DBSession, _: CurrentUser):
    """Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (DBSession): Database session dependency.
        _ (UserModel): The current authenticated user (unused, for auth only).

    Returns:
        UserRead: The requested user's data.
    """
    result = UserService(db).get_user(user_id)
    return handle_result(result)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: DBSession, _: CurrentUser):
    """Update an existing user's information.

    Args:
        user_id (int): The ID of the user to update.
        data (UserUpdate): The update payload.
        db (DBSession): Database session dependency.
        _ (UserModel): The current authenticated user (unused, for auth only).

    Returns:
        UserRead: The updated user's data.
    """
    result = UserService(db).update_user(user_id, data)
    return handle_result(result)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: DBSession, _: CurrentUser):
    """Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (DBSession): Database session dependency.
        _ (UserModel): The current authenticated user (unused, for auth only).

    Returns:
        Any: The result of the delete operation.
    """
    result = UserService(db).delete_user(user_id)
    return handle_result(result)
