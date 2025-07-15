from src.backend.exceptions.cst_exception import AppException
from src.backend.models.md_member import Member
from src.backend.services.base import AppService
from src.backend.services.service_result import ServiceResult


class BalanceService(AppService):
    def get_balance(self, member_id: int) -> ServiceResult:
        member = self.db.get(Member, member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        return ServiceResult({"balance": member.balance})

    def deduct_balance(self, member_id: int, amount: float) -> ServiceResult:
        member = self.db.get(Member, member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        if member.balance < amount:
            return ServiceResult(AppException.InsufficientBalanceError(member.balance))
        member.balance -= amount
        self.db.commit()
        self.db.refresh(member)
        return ServiceResult(member)

    def add_balance(self, member_id: int, amount: float) -> ServiceResult:
        member = self.db.get(Member, member_id)
        if not member:
            return ServiceResult(AppException.MemberNotFoundError(member_id))
        member.balance += amount
        self.db.commit()
        self.db.refresh(member)
        return ServiceResult(member)
