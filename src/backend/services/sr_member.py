import json
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.backend.models.md_member import Member
from src.backend.schemas.sc_member import MemberCreate, MemberUpdate
from src.backend.services.base import AppService
from src.backend.services.service_result import ServiceResult
from src.backend.exceptions.app_exceptions import AppException
from src.backend.models.md_user import User
from src.mlog.mylog import logger


class MemberCRUD:
    def __init__(self, db):
        self.db = db

    def get_by_id(self, member_id: int) -> Member | None:
        member = self.db.get(Member, member_id)
        return member

    def get_by_ip(self, ip: str) -> Member | None:
        member = self.db.execute(
            select(Member).where(Member.ipaddress == ip)
        ).scalar_one_or_none()
        return member

    def get_by_name(self, name: str) -> Member | None:
        member = self.db.execute(
            select(Member).where(Member.name == name)
        ).scalar_one_or_none()
        return member

    def create(self, data: MemberCreate) -> Member:
        member = Member(**data.model_dump())
        self.db.add(member)
        self.db.commit()
        self.db.refresh(member)
        logger.info(f"Member created with id: {member.id}")
        return member

    def update(self, member: Member, data: MemberUpdate) -> Member:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(member, field, value)
        self.db.commit()
        self.db.refresh(member)
        logger.info(f"Member id: {member.id} updated successfully")
        return member

    def delete(self, member: Member) -> None:
        self.db.delete(member)
        self.db.commit()
        logger.info(f"Member id: {member.id} deleted successfully")
        return None

    def list(self, skip: int = 0, limit: int = 100) -> list[Member]:
        members = self.db.execute(select(Member).offset(skip).limit(limit)).scalars().all()
        return list(members)


class MemberService(AppService):
    def _check_superuser(self, current_user: User) -> ServiceResult | None:
        if not getattr(current_user, "is_superuser", False):
            return ServiceResult(
                AppException.ForbiddenActionError(
                    "Hanya admin (is_superuser) yang dapat mengelola member"
                )
            )
        return None

    def get_member(self, member_id: int, current_user: User) -> ServiceResult:
        if (result := self._check_superuser(current_user)) is not None:
            return result
        member = MemberCRUD(self.db).get_by_id(member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        return ServiceResult(member)

    def create_member(self, data: MemberCreate, current_user: User) -> ServiceResult:
        if (result := self._check_superuser(current_user)) is not None:
            return result
        try:
            member = MemberCRUD(self.db).create(data)
            return ServiceResult(member)
        except SQLAlchemyError as e:
            return ServiceResult(AppException.DatabaseError(str(e)))

    def update_member(self, member_id: int, data: MemberUpdate, current_user: User) -> ServiceResult:
        if (result := self._check_superuser(current_user)) is not None:
            return result
        crud = MemberCRUD(self.db)
        member = crud.get_by_id(member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        updated_member = crud.update(member, data)
        return ServiceResult(updated_member)

    def delete_member(self, member_id: int, current_user: User) -> ServiceResult:
        if (result := self._check_superuser(current_user)) is not None:
            return result
        crud = MemberCRUD(self.db)
        member = crud.get_by_id(member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        crud.delete(member)
        return ServiceResult({"deleted": True})

    def list_members(self, current_user: User, skip: int = 0, limit: int = 100) -> ServiceResult:
        if (result := self._check_superuser(current_user)) is not None:
            return result
        members = MemberCRUD(self.db).list(skip=skip, limit=limit)
        return ServiceResult(members)


# Helper for serialization
def member_to_json(member: Member) -> str:
    return json.dumps(member_to_dict(member))


def member_to_dict(member: Member) -> dict:
    return {
        "id": member.id,
        "name": member.name,
        "ipaddress": member.ipaddress,
        "urlreport": member.urlreport,
        "pin": member.pin,
        "password": member.password,
        "is_active": member.is_active,
        "allow_no_sign": member.allow_no_sign,
        "created_at": member.created_at.isoformat() if getattr(member, "created_at", None) is not None else None,
    }
