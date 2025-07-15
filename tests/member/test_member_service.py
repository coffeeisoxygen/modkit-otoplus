import pytest
from src.backend.models.md_member import Member
from src.backend.services.sr_member import MemberService


@pytest.mark.unit
class TestMemberService:
    def test_create_member_admin_success(self, db_session, admin_user, member_create):
        service = MemberService(db_session)
        result = service.create_member(member_create, admin_user)
        assert result.success
        assert isinstance(result.value, Member)
        assert result.value.name == member_create.name

    def test_create_member_forbidden_for_non_admin(
        self, db_session, user, member_create
    ):
        service = MemberService(db_session)
        result = service.create_member(member_create, user)
        assert not result.success
        assert result.value is not None
        assert "admin" in str(result.value)

    def test_get_member_admin_success(self, db_session, admin_user, member):
        service = MemberService(db_session)
        result = service.get_member(member.id, admin_user)
        assert result.success
        assert isinstance(result.value, Member)
        assert result.value.id == member.id

    def test_get_member_forbidden_for_non_admin(self, db_session, user, member):
        service = MemberService(db_session)
        result = service.get_member(member.id, user)
        assert not result.success
        assert result.value is not None
        assert "admin" in str(result.value)

    def test_update_member_admin_success(
        self, db_session, admin_user, member, member_update
    ):
        service = MemberService(db_session)
        result = service.update_member(member.id, member_update, admin_user)
        assert result.success
        assert isinstance(result.value, Member)
        assert result.value.urlreport == member_update.urlreport
        assert result.value.is_active == member_update.is_active

    def test_update_member_forbidden_for_non_admin(
        self, db_session, user, member, member_update
    ):
        service = MemberService(db_session)
        result = service.update_member(member.id, member_update, user)
        assert not result.success
        assert result.value is not None
        assert "admin" in str(result.value)

    def test_delete_member_admin_success(self, db_session, admin_user, member):
        service = MemberService(db_session)
        result = service.delete_member(member.id, admin_user)
        assert result.success
        assert isinstance(result.value, dict)
        assert result.value["deleted"] is True

    def test_delete_member_forbidden_for_non_admin(self, db_session, user, member):
        service = MemberService(db_session)
        result = service.delete_member(member.id, user)
        assert not result.success
        assert result.value is not None
        assert "admin" in str(result.value)

    def test_list_members_admin_success(self, db_session, admin_user, member):
        service = MemberService(db_session)
        result = service.list_members(admin_user)
        assert result.success
        assert isinstance(result.value, list)
        assert any(m.id == member.id for m in result.value)

    def test_list_members_forbidden_for_non_admin(self, db_session, user):
        service = MemberService(db_session)
        result = service.list_members(user)
        assert not result.success
        assert result.value is not None
        assert "admin" in str(result.value)
