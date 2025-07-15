"""Admin API routes for user, member, and balance management.

Semua endpoint di sini hanya boleh diakses oleh admin (is_superuser=True).

Hasan Maki and Copilot
"""

from fastapi import APIRouter, HTTPException

from src.backend.core.app_dbsetting import DBSession
from src.backend.dependencies.auth_dependency import CurrentUser, require_admin
from src.backend.schemas.sc_member import (
    BalanceResponse,
    BalanceUpdateRequest,
    MemberCreate,
    MemberRead,
    MemberUpdate,
)
from src.backend.schemas.sc_user import UserCreate, UserRead, UserUpdate
from src.backend.services.service_result import handle_result
from src.backend.services.sr_balance import BalanceService
from src.backend.services.sr_member import MemberService
from src.backend.services.sr_user import UserService

member_router = APIRouter(prefix="/admin/members", tags=["Admin Members"])
user_router = APIRouter(prefix="/admin/users", tags=["Admin Users"])

# --- Member endpoints ---


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


@member_router.get("/{member_id}/balance", response_model=BalanceResponse)
def get_member_balance(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> BalanceResponse:
    """Cek saldo member (khusus admin).

    Args:
        member_id (int): ID member.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (harus admin).

    Returns:
        BalanceResponse: Saldo member.

    Raises:
        HTTPException: Jika bukan admin.

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = BalanceService(db).get_balance(member_id)
    value = handle_result(result)
    if not isinstance(value, BalanceResponse):
        raise HTTPException(status_code=400, detail=str(value))
    return value


@member_router.post("/{member_id}/balance/add", response_model=BalanceResponse)
def add_member_balance(
    member_id: int,
    data: BalanceUpdateRequest,
    db: DBSession,
    current_user: CurrentUser,
) -> BalanceResponse:
    """Tambah saldo member (khusus admin).

    Args:
        member_id (int): ID member.
        data (BalanceUpdateRequest): Jumlah saldo yang akan ditambahkan.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (harus admin).

    Returns:
        BalanceResponse: Saldo member setelah penambahan.

    Raises:
        HTTPException: Jika bukan admin.

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = BalanceService(db).add_balance(member_id, data.amount)
    value = handle_result(result)
    if not isinstance(value, BalanceResponse):
        raise HTTPException(status_code=400, detail=str(value))
    return value


@member_router.post("/{member_id}/balance/deduct", response_model=BalanceResponse)
def deduct_member_balance(
    member_id: int,
    data: BalanceUpdateRequest,
    db: DBSession,
    current_user: CurrentUser,
) -> BalanceResponse:
    """Kurangi saldo member (khusus admin).

    Args:
        member_id (int): ID member.
        data (BalanceUpdateRequest): Jumlah saldo yang akan dikurangi.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (harus admin).

    Returns:
        BalanceResponse: Saldo member setelah pengurangan.

    Raises:
        HTTPException: Jika bukan admin.

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = BalanceService(db).deduct_balance(member_id, data.amount)
    value = handle_result(result)
    if not isinstance(value, BalanceResponse):
        raise HTTPException(status_code=400, detail=str(value))
    return value


# --- User endpoints ---


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
