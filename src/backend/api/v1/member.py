from fastapi import APIRouter, Body

from src.backend.core.app_dbsetting import DBSession
from src.backend.dependencies.auth_dependency import (
    CurrentUser,
    require_admin,
    require_owner_or_admin,
)
from src.backend.schemas.sc_member import (
    BalanceResponse,
    MemberCreate,
    MemberRead,
    MemberUpdate,
)
from src.backend.services.service_result import handle_result
from src.backend.services.sr_balance import BalanceService
from src.backend.services.sr_member import MemberService

router = APIRouter(prefix="/v1/members", tags=["Members"])


@router.get("/", response_model=list[MemberRead])
def list_members(
    db: DBSession,
    current_user: CurrentUser,
):
    """List all members.

    Parameters
    ----------
    db : DBSession
        Database session.
    current_user : CurrentUser
        The current authenticated user.

    Returns:
    -------
    list[MemberRead]
        List of member objects.
    """
    require_admin(current_user)
    result = MemberService(db).list_members(current_user)
    return handle_result(result)


@router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """Get a member by ID.

    Parameters
    ----------
    member_id : int
        The ID of the member.
    db : DBSession
        Database session.
    current_user : CurrentUser
        The current authenticated user.

    Returns:
    -------
    MemberRead
        The member object.
    """
    require_admin(current_user)
    result = MemberService(db).get_member(member_id, current_user)
    return handle_result(result)


@router.post("/", response_model=MemberRead)
def create_member(
    data: MemberCreate,
    db: DBSession,
    current_user: CurrentUser,
):
    """Create a new member.

    Parameters
    ----------
    data : MemberCreate
        Data for the new member.
    db : DBSession
        Database session.
    current_user : CurrentUser
        The current authenticated user.

    Returns:
    -------
    MemberRead
        The created member object.
    """
    require_admin(current_user)
    result = MemberService(db).create_member(data, current_user)
    return handle_result(result)


@router.put("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int,
    data: MemberUpdate,
    db: DBSession,
    current_user: CurrentUser,
):
    """Update an existing member.

    Parameters
    ----------
    member_id : int
        The ID of the member to update.
    data : MemberUpdate
        Updated member data.
    db : DBSession
        Database session.
    current_user : CurrentUser
        The current authenticated user.

    Returns:
    -------
    MemberRead
        The updated member object.
    """
    require_admin(current_user)
    result = MemberService(db).update_member(member_id, data, current_user)
    return handle_result(result)


@router.delete("/{member_id}", response_model=dict)
def delete_member(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
):
    """Delete a member by ID.

    Parameters
    ----------
    member_id : int
        The ID of the member to delete.
    db : DBSession
        Database session.
    current_user : CurrentUser
        The current authenticated user.

    Returns:
    -------
    dict
        Result of the deletion.
    """
    require_admin(current_user)
    result = MemberService(db).delete_member(member_id, current_user)
    return handle_result(result)


@router.get("/{member_id}/balance", response_model=BalanceResponse)
def get_member_balance(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> BalanceResponse:
    """Ambil saldo member berdasarkan ID.

    Args:
        member_id (int): ID member yang ingin dicek saldonya.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (admin/owner).

    Returns:
        BalanceResponse: Saldo member.

    Raises:
        HTTPException: Jika bukan admin/owner.

    Hasan Maki and Copilot
    """
    require_owner_or_admin(member_id, current_user)
    result = BalanceService(db).get_balance(member_id)
    return handle_result(result)


@router.post("/{member_id}/balance/add", response_model=BalanceResponse)
def add_member_balance(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
    amount: float = Body(..., embed=True),
) -> BalanceResponse:
    """Tambah saldo member (hanya admin).

    Args:
        member_id (int): ID member.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (harus admin).
        amount (float): Jumlah saldo yang akan ditambahkan.

    Returns:
        BalanceResponse: Saldo member setelah penambahan.

    Raises:
        HTTPException: Jika bukan admin.

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = BalanceService(db).add_balance(member_id, amount)
    return handle_result(result)


@router.post("/{member_id}/balance/deduct", response_model=BalanceResponse)
def deduct_member_balance(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
    amount: float = Body(..., embed=True),
) -> BalanceResponse:
    """Kurangi saldo member (hanya admin).

    Args:
        member_id (int): ID member.
        db (DBSession): Session database.
        current_user (CurrentUser): User yang sedang login (harus admin).
        amount (float): Jumlah saldo yang akan dikurangi.

    Returns:
        BalanceResponse: Saldo member setelah pengurangan.

    Raises:
        HTTPException: Jika bukan admin.

    Hasan Maki and Copilot
    """
    require_admin(current_user)
    result = BalanceService(db).deduct_balance(member_id, amount)
    return handle_result(result)
