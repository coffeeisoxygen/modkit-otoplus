"""API endpoints for user management.

This module defines the FastAPI routes for creating, retrieving, updating,
and deleting users in the system.
"""

from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.schemas.sc_user import UserCreate, UserRead, UserUpdate
from src.backend.services.sr_user import UserService
from src.backend.utils.result.service_result import handle_result

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, db: DBSession):
    """Create a new user.

    Args:
        data (UserCreate): The user creation data.
        db (DBSession): The database session.

    Returns:
        UserRead: The created user.
    """
    result = UserService(db).create_user(data)
    return handle_result(result)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: DBSession):
    """Retrieve a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (DBSession): The database session.

    Returns:
        UserRead: The user data.
    """
    result = UserService(db).get_user(user_id)
    return handle_result(result)


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, data: UserUpdate, db: DBSession):
    """Update an existing user by ID.

    Args:
        user_id (int): The ID of the user to update.
        data (UserUpdate): The updated user data.
        db (DBSession): The database session.

    Returns:
        UserRead: The updated user.
    """
    result = UserService(db).update_user(user_id, data)
    return handle_result(result)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: DBSession):
    """Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (DBSession): The database session.

    Returns:
        Any: The result of the deletion operation.
    """
    result = UserService(db).delete_user(user_id)
    return handle_result(result)
