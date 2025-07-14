"""Cache backend factory for selecting and instantiating the appropriate cache backend.

This module loads cache configuration from environment variables and provides a factory
function to obtain a cache backend instance. Currently, only the in-memory cache backend
is supported. Redis backend is planned for future support.
"""

import os

from dotenv import load_dotenv

from src.backend.mcache.inmemory import InMemoryCacheBackend

# from src.backend.mcache.redis_backend import RedisCacheBackend  # future support

load_dotenv()

CACHE_SERVICE = os.getenv("CACHE_SERVICE", "inmemory").lower()
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", 100))


def get_cache() -> InMemoryCacheBackend:
    """Factory function to get a cache backend instance.

    Selects and returns an instance of the configured cache backend.
    Currently supports only the in-memory cache backend. Raises a
    NotImplementedError for unsupported or unimplemented backends.

    Raises:
        NotImplementedError: If the selected cache backend is not implemented or supported.

    Returns:
        InMemoryCacheBackend: An instance of the in-memory cache backend.
    """
    if CACHE_SERVICE == "inmemory":
        return InMemoryCacheBackend(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL)
    elif CACHE_SERVICE == "redis":
        raise NotImplementedError("Redis cache backend not implemented yet.")
    else:
        raise NotImplementedError(f"Cache backend '{CACHE_SERVICE}' not supported.")
