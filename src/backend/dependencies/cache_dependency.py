from typing import Annotated

from src.backend.mcache.inmemory import InMemoryCacheBackend


def get_cache() -> InMemoryCacheBackend:
    """Factory function to get an instance of the in-memory cache backend."""
    return InMemoryCacheBackend()


cache = Annotated[InMemoryCacheBackend, "cache"]
