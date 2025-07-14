from fastapi import APIRouter, HTTPException

from src.backend.config.database import DBSession
from src.backend.schemas.sc_member import MemberCreate, MemberRead, MemberUpdate
from src.backend.services import member_service

router = APIRouter(prefix="/v1/members", tags=["Members"])


@router.get("/", response_model=list[MemberRead])
def list_members(session: DBSession, skip: int = 0, limit: int = 100):
    """List members with pagination."""
    return member_service.list_members(session, skip, limit)


@router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(member_id: int, session: DBSession):
    """Get Member by ID."""
    member = member_service.get_by_id(session, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/", response_model=MemberRead)
def create_member(data: MemberCreate, session: DBSession):
    """Create a new member.

    This endpoint allows for the creation of a new member in the system.

    Args:
        data (MemberCreate): _description_
        session (DBSession): _description_

    Returns:
        _type_: _description_
    """
    return member_service.create_member(session, data)


@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, data: MemberUpdate, session: DBSession):
    """Update an existing member by ID."""
    member = member_service.update_member(session, member_id, data)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, session: DBSession):
    """Delete a member by ID."""
    success = member_service.delete_member(session, member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"success": True, "message": "Member deleted"}
