from fastapi import APIRouter, HTTPException

from src.backend.core.app_dbsetting import DBSession
from src.backend.schemas.sc_member import MemberCreate, MemberRead, MemberUpdate
from src.backend.services import sr_member

router = APIRouter(prefix="/v1/members", tags=["Members"])


@router.get("/", response_model=list[MemberRead])
def list_members(db: DBSession, skip: int = 0, limit: int = 100):
    """List members with pagination.

    Args:
        db (DBSession): Database session.
        skip (int): Offset.
        limit (int): Limit.

    Returns:
        list[MemberRead]: List of members.
    """
    return sr_member.list_members(db, skip, limit)


@router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(member_id: int, db: DBSession):
    """Get Member by ID.

    Args:
        member_id (int): Member ID.
        db (DBSession): Database session.

    Returns:
        MemberRead: Member data.
    """
    member = sr_member.get_by_id(db, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/", response_model=MemberRead)
def create_member(data: MemberCreate, db: DBSession):
    """Create a new member.

    Args:
        data (MemberCreate): Data member.
        db (DBSession): Database session.

    Returns:
        MemberRead: Created member.
    """
    return sr_member.create_member(db, data)


@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, data: MemberUpdate, db: DBSession):
    """Update an existing member by ID.

    Args:
        member_id (int): Member ID.
        data (MemberUpdate): Data update.
        db (DBSession): Database session.

    Returns:
        MemberRead: Updated member.
    """
    member = sr_member.update_member(db, member_id, data)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, db: DBSession):
    """Delete a member by ID.

    Args:
        member_id (int): Member ID.
        db (DBSession): Database session.

    Returns:
        dict: Result info.
    """
    success = sr_member.delete_member(db, member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"success": True, "message": "Member deleted"}
