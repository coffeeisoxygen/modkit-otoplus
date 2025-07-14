from cachetools import TTLCache

from src.backend.mcache.base import BaseCacheBackend


class InMemoryCacheBackend(BaseCacheBackend):
    """In-memory cache backend implementation using cachetools.TTLCache.

    This class provides a simple in-memory cache with time-to-live (TTL) support for each item.
    It implements the BaseCacheBackend interface and supports basic cache operations such as
    get, set, delete, and clear. The cache size and default TTL can be configured via the constructor.

    Args:
        maxsize (int): Maximum number of items the cache can hold.
        ttl (int): Default time-to-live (in seconds) for cache items.
    """

    def __init__(self, maxsize: int = 500, ttl: int = 300):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> str | None:
        return self.cache.get(key)

    def set(self, key: str, value: str, ttl: int = 60):
        # TTL per-item: pakai .set() method
        self.cache.set(key, value, ttl=ttl)  # type: ignore

    def delete(self, key: str):
        self.cache.pop(key, None)

    def clear(self):
        self.cache.clear()
