from unittest.mock import MagicMock, patch

import pytest
from src.backend.models.member import Member, MemberCreate, MemberUpdate
from src.backend.services import member_service


@pytest.fixture
def session():
    return MagicMock()


@pytest.fixture
def member():
    return Member(id=1, name="test", ipaddress="127.0.0.1")  # type: ignore


@pytest.fixture
def member_create():
    return MemberCreate(
        name="test", ipaddress="127.0.0.1", pin="123456", password="secret"
    )  # type: ignore


@pytest.fixture
def member_update():
    return MemberUpdate(name="updated", ipaddress="127.0.0.2")


def test_get_by_id_cache_hit(session, member):
    with (
        patch.object(
            member_service.cache, "get", return_value=member.model_dump_json()
        ),
        patch.object(member_service.Member, "model_validate", return_value=member),
    ):
        result = member_service.get_by_id(session, member.id)
        assert result == member


def test_get_by_id_db_hit(session, member):
    session.get.return_value = member
    with (
        patch.object(member_service.cache, "get", return_value=None),
        patch.object(member_service.cache, "set") as cache_set,
    ):
        result = member_service.get_by_id(session, member.id)
        assert result == member
        cache_set.assert_called_once()


def test_get_by_id_not_found(session):
    session.get.return_value = None
    with patch.object(member_service.cache, "get", return_value=None):
        result = member_service.get_by_id(session, 999)
        assert result is None


def test_get_by_ip_cache_hit(session, member):
    with (
        patch.object(
            member_service.cache, "get", return_value=member.model_dump_json()
        ),
        patch.object(member_service.Member, "model_validate", return_value=member),
    ):
        result = member_service.get_by_ip(session, member.ipaddress)
        assert result == member


def test_get_by_ip_db_hit(session, member):
    session.exec.return_value.first.return_value = member
    with (
        patch.object(member_service.cache, "get", return_value=None),
        patch.object(member_service.cache, "set") as cache_set,
    ):
        result = member_service.get_by_ip(session, member.ipaddress)
        assert result == member
        cache_set.assert_called_once()


def test_get_by_ip_not_found(session):
    session.exec.return_value.first.return_value = None
    with patch.object(member_service.cache, "get", return_value=None):
        result = member_service.get_by_ip(session, "0.0.0.0")
        assert result is None


def test_get_by_name_cache_hit(session, member):
    with (
        patch.object(
            member_service.cache, "get", return_value=member.model_dump_json()
        ),
        patch.object(member_service.Member, "model_validate", return_value=member),
    ):
        result = member_service.get_by_name(session, member.name)
        assert result == member


def test_get_by_name_db_hit(session, member):
    session.exec.return_value.first.return_value = member
    with (
        patch.object(member_service.cache, "get", return_value=None),
        patch.object(member_service.cache, "set") as cache_set,
    ):
        result = member_service.get_by_name(session, member.name)
        assert result == member
        cache_set.assert_called_once()


def test_get_by_name_not_found(session):
    session.exec.return_value.first.return_value = None
    with patch.object(member_service.cache, "get", return_value=None):
        result = member_service.get_by_name(session, "notfound")
        assert result is None


def test_create_member(session, member_create):
    session.add = MagicMock()
    session.commit = MagicMock()
    session.refresh = MagicMock()
    with patch(
        "src.backend.services.member_service.Member", autospec=True
    ) as member_mock:
        instance = member_mock.return_value
        instance.id = 1
        session.refresh.return_value = None
        result = member_service.create_member(session, member_create)
        assert result == instance
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()


def test_update_member_success(session, member, member_update):
    session.get.return_value = member
    session.commit = MagicMock()
    session.refresh = MagicMock()
    with patch.object(member_service.cache, "delete") as cache_delete:
        result = member_service.update_member(session, member.id, member_update)
        assert result == member
        session.commit.assert_called_once()
        session.refresh.assert_called_once()
        assert cache_delete.call_count == 3


def test_update_member_not_found(session, member_update):
    session.get.return_value = None
    result = member_service.update_member(session, 999, member_update)
    assert result is None


def test_delete_member_success(session, member):
    session.get.return_value = member
    session.delete = MagicMock()
    session.commit = MagicMock()
    with patch.object(member_service.cache, "delete") as cache_delete:
        result = member_service.delete_member(session, member.id)
        assert result is True
        session.delete.assert_called_once_with(member)
        session.commit.assert_called_once()
        assert cache_delete.call_count == 3


def test_delete_member_not_found(session):
    session.get.return_value = None
    result = member_service.delete_member(session, 999)
    assert result is False


def test_list_members_cache_hit(session, member):
    with (
        patch.object(member_service.cache, "get", return_value="[{}]"),
        patch.object(member_service.Member, "model_validate", return_value=member),
    ):
        result = member_service.list_members(session)
        assert result == [member]


def test_list_members_db_hit(session, member):
    session.exec.return_value.all.return_value = [member]
    with (
        patch.object(member_service.cache, "get", return_value=None),
        patch.object(member_service.cache, "set") as cache_set,
    ):
        result = member_service.list_members(session)
        assert result == [member]
        cache_set.assert_called_once()


def test_list_members_db_empty(session):
    session.exec.return_value.all.return_value = []
    with patch.object(member_service.cache, "get", return_value=None):
        result = member_service.list_members(session)
        assert result == []
