from typing import Any

from fastapi import APIRouter

from src.backend.core.app_dbsetting import DBSession
from src.backend.dependencies.user_auth import CurrentUser
from src.backend.schemas.sc_member import MemberCreate, MemberRead, MemberUpdate
from src.backend.services.service_result import handle_result
from src.backend.services.sr_member import MemberService

router = APIRouter(prefix="/v1/members", tags=["Members"])


@router.get("/", response_model=list[MemberRead])
def list_members(
    db: DBSession,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """List members with pagination. Hasan Maki and Copilot."""
    result = MemberService(db).list_members(current_user, skip, limit)
    return handle_result(result)


@router.get("/{member_id}", response_model=MemberRead)
def get_member_by_id(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> Any:
    """Get Member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).get_member(member_id, current_user)
    return handle_result(result)


@router.post("/", response_model=MemberRead)
def create_member(
    data: MemberCreate,
    db: DBSession,
    current_user: CurrentUser,
) -> Any:
    """Create a new member. Hasan Maki and Copilot."""
    result = MemberService(db).create_member(data, current_user)
    return handle_result(result)


@router.put("/{member_id}", response_model=MemberRead)
def update_member(
    member_id: int,
    data: MemberUpdate,
    db: DBSession,
    current_user: CurrentUser,
) -> Any:
    """Update an existing member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).update_member(member_id, data, current_user)
    return handle_result(result)


@router.delete("/{member_id}", response_model=dict)
def delete_member(
    member_id: int,
    db: DBSession,
    current_user: CurrentUser,
) -> Any:
    """Delete a member by ID. Hasan Maki and Copilot."""
    result = MemberService(db).delete_member(member_id, current_user)
    return handle_result(result)
