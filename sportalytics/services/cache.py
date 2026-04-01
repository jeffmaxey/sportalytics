"""Small Redis cache helpers with fail-open behavior for service reads."""

from __future__ import annotations

import json
import os
from typing import Any

import redis

_CACHE_PREFIX = "sportalytics:v1"
_REDIS_URL = os.getenv("SPORTALYTICS_REDIS_URL", "redis://localhost:6379/0")

_client: redis.Redis | None = None


def _get_client() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis.from_url(
            _REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=0.2,
            socket_timeout=0.2,
        )
    return _client


def make_cache_key(namespace: str, **params: Any) -> str:
    parts = [f"{k}={params[k]}" for k in sorted(params)]
    suffix = "|".join(parts) if parts else "all"
    return f"{_CACHE_PREFIX}:{namespace}:{suffix}"


def cache_get_json(key: str) -> Any | None:
    try:
        raw = _get_client().get(key)
        if not raw:
            return None
        return json.loads(raw)
    except Exception:
        return None


def cache_set_json(key: str, payload: Any, ttl_seconds: int) -> None:
    try:
        _get_client().setex(key, ttl_seconds, json.dumps(payload, default=str))
    except Exception:
        return None


