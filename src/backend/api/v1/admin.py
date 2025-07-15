"""Admin API routes for user, member, and balance management.

Semua endpoint di sini hanya boleh diakses oleh admin (is_superuser=True).

Hasan Maki and Copilot
"""

from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.dependencies.auth_dependency import CurrentUser, require_admin
from src.backend.schemas.sc_member import MemberCreate, MemberRead, MemberUpdate
from src.backend.schemas.sc_user import UserCreate, UserRead, UserUpdate
from src.backend.services.service_result import handle_result
from src.backend.services.sr_member import MemberService
from src.backend.services.sr_user import UserService

member_router = APIRouter(prefix="/admin/members", tags=["Admin Members"])
user_router = APIRouter(prefix="/admin/users", tags=["Admin Users"])


@member_router.get("/", response_model=list[MemberRead])
def list_members(db: DBSession, current_user: CurrentUser):
    """List all members (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = MemberService(db).list_members(current_user)
    return handle_result(result)


@member_router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(member_id: int, db: DBSession, current_user: CurrentUser):
    """Get a member by ID (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = MemberService(db).get_member(member_id, current_user)
    return handle_result(result)


@member_router.post("/", response_model=MemberRead)
def create_member(data: MemberCreate, db: DBSession, current_user: CurrentUser):
    """Create a new member (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = MemberService(db).create_member(data, current_user)
    return handle_result(result)


@member_router.put("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int, data: MemberUpdate, db: DBSession, current_user: CurrentUser
):
    """Update an existing member (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = MemberService(db).update_member(member_id, data, current_user)
    return handle_result(result)


@member_router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, db: DBSession, current_user: CurrentUser):
    """Delete a member by ID (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = MemberService(db).delete_member(member_id, current_user)
    return handle_result(result)


@user_router.post("/", response_model=UserRead)
def create_user(data: UserCreate, db: DBSession, current_user: CurrentUser):
    """Create a new user (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = UserService(db).create_user(data)
    return handle_result(result)


@user_router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: DBSession, current_user: CurrentUser):
    """Get a user by ID (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = UserService(db).get_user(user_id)
    return handle_result(result)


@user_router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, data: UserUpdate, db: DBSession, current_user: CurrentUser
):
    """Update a user by ID (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = UserService(db).update_user(user_id, data)
    return handle_result(result)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: DBSession, current_user: CurrentUser):
    """Delete a user by ID (admin only).

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = UserService(db).delete_user(user_id)
    return handle_result(result)
