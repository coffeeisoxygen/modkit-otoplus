from unittest.mock import MagicMock, patch
from datetime import datetime
import json

import pytest
from src.backend.models.md_member import Member
from src.backend.schemas.sc_member import MemberCreate, MemberUpdate, MemberRead
from src.backend.services import member_service


@pytest.fixture
def session():
    return MagicMock()


@pytest.fixture
def member():
    return Member(
        id=1, name="test", ipaddress="127.0.0.1", urlreport=None, pin="123456", password="secret", is_active=True
    )


@pytest.fixture
def member_create():
    return MemberCreate(
        name="test", ipaddress="127.0.0.1", urlreport=None, pin="123456", password="secret", is_active=True
    )


@pytest.fixture
def member_update():
    return MemberUpdate(name="updated", ipaddress="127.0.0.2")


def test_get_by_id_cache_hit(session, member):
    member_dict = {
        "id": member.id or 1,
        "name": member.name or "test",
        "ipaddress": member.ipaddress or "127.0.0.1",
        "urlreport": member.urlreport or "http://localhost",
        "pin": member.pin or "123456",
        "password": member.password or "secret",
        "is_active": member.is_active if member.is_active is not None else True,
        "created_at": member.created_at if hasattr(member, "created_at") and member.created_at else datetime.now(),
    }
    # Simulate cache returning JSON string
    with patch.object(member_service.cache, "get", return_value=json.dumps(member_dict)):
        result = member_service.get_by_id(session, member.id)
        assert isinstance(result, MemberRead)
        assert result.id == member.id


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
    from datetime import datetime
    member_dict = {
        "id": member.id,
        "name": member.name,
        "ipaddress": member.ipaddress,
        "urlreport": member.urlreport,
        "pin": member.pin,
        "password": member.password,
        "is_active": member.is_active,
        "created_at": member.created_at.isoformat() if member.created_at else datetime.now().isoformat(),
    }
    with patch.object(member_service.cache, "get", return_value=json.dumps([member_dict])):
        result = member_service.list_members(session)
        # Convert types from JSON (all str) to correct types for MemberRead
        member_dict_cast = member_dict.copy()
        member_dict_cast["id"] = int(member_dict_cast["id"])
        member_dict_cast["is_active"] = bool(member_dict_cast["is_active"])
        from datetime import datetime as dt
        member_dict_cast["created_at"] = dt.fromisoformat(member_dict_cast["created_at"])
        assert result == [MemberRead(**member_dict_cast)]


def test_list_members_db_hit(session, member):
    member.created_at = member.created_at or datetime.now()
    session.execute.return_value.scalars.return_value.all.return_value = [member]
    with (
        patch.object(member_service.cache, "get", return_value=None),
        patch.object(member_service.cache, "set") as cache_set,
    ):
        result = member_service.list_members(session)
        expected = [MemberRead(
            id=member.id,
            name=member.name,
            ipaddress=member.ipaddress,
            urlreport=member.urlreport,
            pin=member.pin,
            password=member.password,
            is_active=member.is_active,
            created_at=member.created_at,
        )]
        assert result == expected
        cache_set.assert_called_once()


def test_list_members_db_empty(session):
    session.exec.return_value.all.return_value = []
    with patch.object(member_service.cache, "get", return_value=None):
        result = member_service.list_members(session)
        assert result == []
