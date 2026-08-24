from __future__ import annotations

import hashlib
import logging
from threading import Lock

from cachetools import TTLCache

from wedding_planner.tools.search import tavily_search

log = logging.getLogger(__name__)

_tavily_cache: TTLCache[str, str] = TTLCache(maxsize=128, ttl=3600)
_cache_lock = Lock()


def cached_tavily_search(query: str, max_results: int = 5) -> str:
    """Tavily search with TTL caching (1hr). Same query returns cached result."""
    cache_key = hashlib.sha256(f"{query}:{max_results}".encode()).hexdigest()
    with _cache_lock:
        if cache_key in _tavily_cache:
            log.info(f"Cache hit for query: {query[:60]}...")
            return _tavily_cache[cache_key]
    result = tavily_search(query, max_results)
    with _cache_lock:
        _tavily_cache[cache_key] = result
    log.info(f"Cache miss, stored result for: {query[:60]}...")
    return result


def cache_stats() -> dict[str, int]:
    """Return cache statistics."""
    with _cache_lock:
        return {"size": len(_tavily_cache), "maxsize": _tavily_cache.maxsize, "ttl": _tavily_cache.ttl}


def clear_cache() -> None:
    """Clear all cached search results."""
    with _cache_lock:
        _tavily_cache.clear()
    log.info("Tavily cache cleared")
