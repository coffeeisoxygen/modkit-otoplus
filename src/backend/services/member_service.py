import json

from sqlmodel import Session, select

from src.backend.mcache.factory import CACHE_TTL, _cache_key, get_cache
from src.backend.mcache.inmemory import InMemoryCacheBackend
from src.backend.models.member import Member, MemberCreate, MemberUpdate
from src.mlog.cst_logging import logger

cache: InMemoryCacheBackend = get_cache()


def get_by_id(session: Session, member_id: int) -> Member | None:
    """Fetch a member by their ID.

    This function first checks the cache for a member with the given ID.
    If a cache hit occurs, the member is returned from the cache.
    If not, the function queries the database for the member.

    Args:
        session (Session): The database session.
        member_id (int): The ID of the member to fetch.

    Returns:
        Member | None: The fetched member or None if not found.
    """
    logger.debug(f"Fetching member by id: {member_id}")
    key = _cache_key("member", id=member_id)
    cached_json = cache.get(key)
    if cached_json:
        logger.debug(f"Cache hit for member id: {member_id}")
        return Member.model_validate(json.loads(cached_json))
    member = session.get(Member, member_id)
    if member:
        logger.debug(f"Member found in DB for id: {member_id}, caching result")
        cache.set(key, member.model_dump_json(), ttl=CACHE_TTL)
    else:
        logger.debug(f"No member found in DB for id: {member_id}")
    return member


def get_by_ip(session: Session, ip: str) -> Member | None:
    """Fetch a member by their IP address.

    This function first checks the cache for a member with the given IP address.
    If a cache hit occurs, the member is returned from the cache.
    If not, the function queries the database for the member.

    Args:
        session (Session): The database session.
        ip (str): The IP address of the member to fetch.

    Returns:
        Member | None: The fetched member or None if not found.
    """
    logger.debug(f"Fetching member by ip: {ip}")
    key = _cache_key("member", ip=ip)
    cached_json = cache.get(key)
    if cached_json:
        logger.debug(f"Cache hit for member ip: {ip}")
        return Member.model_validate(json.loads(cached_json))
    member = session.exec(select(Member).where(Member.ipaddress == ip)).first()
    if member:
        logger.debug(f"Member found in DB for ip: {ip}, caching result")
        cache.set(key, member.model_dump_json(), ttl=CACHE_TTL)
    else:
        logger.debug(f"No member found in DB for ip: {ip}")
    return member


def get_by_name(session: Session, name: str) -> Member | None:
    """Fetch a member by their name.

    This function first checks the cache for a member with the given name.
    If a cache hit occurs, the member is returned from the cache.
    If not, the function queries the database for the member.

    Args:
        session (Session): The database session.
        name (str): The name of the member to fetch.

    Returns:
        Member | None: The fetched member or None if not found.
    """
    logger.debug(f"Fetching member by name: {name}")
    key = _cache_key("member", name=name)
    cached_json = cache.get(key)
    if cached_json:
        logger.debug(f"Cache hit for member name: {name}")
        return Member.model_validate(json.loads(cached_json))
    member = session.exec(select(Member).where(Member.name == name)).first()
    if member:
        logger.debug(f"Member found in DB for name: {name}, caching result")
        cache.set(key, member.model_dump_json(), ttl=CACHE_TTL)
    else:
        logger.debug(f"No member found in DB for name: {name}")
    return member


def create_member(session: Session, data: MemberCreate) -> Member:
    """Create a new member in the database."""
    logger.info(f"Creating new member with data: {data}")
    member = Member(**data.dict())
    session.add(member)
    session.commit()
    session.refresh(member)
    logger.info(f"Member created with id: {member.id}")
    return member


def update_member(
    session: Session, member_id: int, data: MemberUpdate
) -> Member | None:
    """Get a member by their ID and update their information."""
    logger.info(f"Updating member id: {member_id} with data: {data}")
    member = session.get(Member, member_id)  # <- langsung ke DB
    if not member:
        logger.warning(f"Member id: {member_id} not found for update")
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(member, field, value)
    session.commit()
    session.refresh(member)

    # Clear cache
    logger.debug(f"Clearing cache for updated member id: {member_id}")
    cache.delete(f"member:id:{member_id}")
    cache.delete(f"member:ip:{member.ipaddress}")
    cache.delete(f"member:name:{member.name}")

    logger.info(f"Member id: {member_id} updated successfully")
    return member


def delete_member(session: Session, member_id: int) -> bool:
    """Delete a member by their ID."""
    logger.info(f"Deleting member id: {member_id}")
    member = session.get(Member, member_id)  # <- langsung ke DB
    if not member:
        logger.warning(f"Member id: {member_id} not found for deletion")
        return False
    session.delete(member)
    session.commit()

    # Clear cache
    logger.debug(f"Clearing cache for deleted member id: {member_id}")
    cache.delete(f"member:id:{member_id}")
    cache.delete(f"member:ip:{member.ipaddress}")
    cache.delete(f"member:name:{member.name}")

    logger.info(f"Member id: {member_id} deleted successfully")
    return True


def list_members(session: Session, skip: int = 0, limit: int = 100) -> list[Member]:
    """List members with pagination and caching."""
    logger.debug(f"Listing members with skip: {skip}, limit: {limit}")
    key = _cache_key("members:list", skip=skip, limit=limit)
    cached_json = cache.get(key)
    if cached_json:
        logger.debug("Cache hit for member list")
        return [Member.model_validate(m) for m in json.loads(cached_json)]
    members = session.exec(select(Member).offset(skip).limit(limit)).all()
    if members:
        logger.debug(f"Members found in DB, caching result with count: {len(members)}")
        cache.set(
            key,
            json.dumps([json.loads(m.model_dump_json()) for m in members]),
            ttl=CACHE_TTL,
        )
    else:
        logger.debug("No members found in DB for listing")
    return list(members)
