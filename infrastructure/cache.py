"""Caching the matcher's answer, and knowing when to forget it.

Storing is easy. Invalidation -- knowing the stored answer is now a lie --
is the hard half, and the classic source of bugs where users see stale data.

The trick used here is a VERSION NUMBER baked into every cache key:

    propose:42:v7     <- answers computed while the data was at version 7

When anything relevant changes we bump the version to 8. Every old key
becomes unreachable in one step, without hunting down individual entries.
Redis evicts the orphans on its own.
"""

from django.core.cache import cache

VERSION_KEY = "match:data_version"
TTL_SECONDS = 300  # 5 minutes: a safety net in case a bump is ever missed


def data_version() -> int:
    """The current version of the underlying data."""
    version = cache.get(VERSION_KEY)
    if version is None:
        version = 1
        cache.set(VERSION_KEY, version, None)  # None = never expires
    return version


def invalidate() -> None:
    """Something changed -- every cached answer is now suspect."""
    try:
        cache.incr(VERSION_KEY)
    except ValueError:  # key had expired or never existed
        cache.set(VERSION_KEY, 1, None)


def proposal_key(request_id: int) -> str:
    return f"propose:{request_id}:v{data_version()}"
