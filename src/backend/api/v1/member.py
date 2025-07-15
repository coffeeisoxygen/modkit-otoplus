from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.models.md_user import User
from src.backend.schemas.sc_member import MemberCreate, MemberRead, MemberUpdate
from src.backend.services.service_result import handle_result
from src.backend.services.sr_member import MemberService

router = APIRouter(prefix="/v1/members", tags=["Members"])


def get_service(db: DBSession) -> MemberService:
    """Get MemberService instance. Hasan Maki and Copilot."""
    return MemberService(db)


@router.get("/", response_model=list[MemberRead])
def list_members(db: DBSession, current_user: User, skip: int = 0, limit: int = 100):
    """List members with pagination. Hasan Maki and Copilot."""
    result = MemberService(db).list_members(current_user, skip, limit)
    return handle_result(result)


@router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(member_id: int, db: DBSession, current_user: User):
    """Get Member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).get_member(member_id, current_user)
    return handle_result(result)


@router.post("/", response_model=MemberRead)
def create_member(data: MemberCreate, db: DBSession, current_user: User):
    """Create a new member. Hasan Maki and Copilot."""
    result = MemberService(db).create_member(data, current_user)
    return handle_result(result)


@router.put("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int, data: MemberUpdate, db: DBSession, current_user: User
):
    """Update an existing member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).update_member(member_id, data, current_user)
    return handle_result(result)


@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: int, db: DBSession, current_user: User):
    """Delete a member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).delete_member(member_id, current_user)
    return handle_result(result)
