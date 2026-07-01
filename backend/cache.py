"""
cache.py — Redis-backed permission cache.

All public functions fail silently if Redis is unreachable so that the
backend continues to work correctly (just slower, always hitting PostgreSQL).
"""
import json
import logging

import redis

from .config import config

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Client — created once at import time.  decode_responses=True means all
# values come back as Python str, not bytes.
# ---------------------------------------------------------------------------
try:
    _client: redis.Redis = redis.Redis.from_url(
        config.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=2,
        socket_timeout=2,
    )
    # Eagerly test connectivity so we know right away whether Redis is up.
    _client.ping()
    logger.info("Redis cache connected at %s", config.REDIS_URL)
except Exception as exc:  # noqa: BLE001
    logger.warning("Redis unavailable at startup (%s) — cache disabled.", exc)
    _client = None  # type: ignore[assignment]


def _key(user_id: str) -> str:
    """Canonical cache key for a user's permission list."""
    return f"user:{user_id}:permissions"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_cached_permissions(user_id: str) -> list[str] | None:
    """
    Return the cached permission list for *user_id*, or ``None`` on a cache
    miss, connection failure, or any other Redis error.
    """
    if _client is None:
        return None
    try:
        raw = _client.get(_key(user_id))
        if raw is None:
            return None
        return json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        logger.warning("cache.get failed for %s: %s", user_id, exc)
        return None


def set_cached_permissions(user_id: str, permissions: list[str]) -> None:
    """
    Store *permissions* for *user_id* with the configured TTL.
    Silently no-ops on any Redis error.
    """
    if _client is None:
        return
    try:
        _client.setex(
            _key(user_id),
            config.CACHE_TTL_SECONDS,
            json.dumps(permissions),
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("cache.set failed for %s: %s", user_id, exc)


def invalidate_user_cache(user_id: str) -> None:
    """
    Remove the cached permissions for a single user.
    Silently no-ops on any Redis error.
    """
    if _client is None:
        return
    try:
        _client.delete(_key(user_id))
    except Exception as exc:  # noqa: BLE001
        logger.warning("cache.invalidate_user failed for %s: %s", user_id, exc)


def invalidate_all_cache() -> None:
    """
    Remove **all** user-permission cache keys (``user:*:permissions``).

    Uses SCAN instead of KEYS so this is safe to call on a large keyspace.
    Called whenever role-permission or user-role assignments change, because
    we cannot cheaply determine which users are affected without an extra DB
    query (MVP trade-off — optimise to targeted invalidation in Phase 3+).

    Silently no-ops on any Redis error.
    """
    if _client is None:
        return
    try:
        cursor = 0
        pattern = "user:*:permissions"
        while True:
            cursor, keys = _client.scan(cursor, match=pattern, count=100)
            if keys:
                _client.delete(*keys)
            if cursor == 0:
                break
        logger.debug("invalidate_all_cache: removed all user permission keys")
    except Exception as exc:  # noqa: BLE001
        logger.warning("cache.invalidate_all failed: %s", exc)
