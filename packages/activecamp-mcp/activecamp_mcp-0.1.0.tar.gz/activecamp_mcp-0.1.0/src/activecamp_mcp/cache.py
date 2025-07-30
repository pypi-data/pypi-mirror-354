"""Cache management for automation analysis."""

import asyncio
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any

from .models import AutomationAnalysis


class CacheManager:
    """Manages caching of automation analyses."""

    def __init__(self, max_entries: int = 1000, ttl_hours: int = 24):
        """Initialize cache manager.

        Args:
            max_entries: Maximum number of cache entries
            ttl_hours: Time-to-live for cache entries in hours
        """
        self.max_entries = max_entries
        self.ttl = timedelta(hours=ttl_hours)

        # In-memory cache using OrderedDict for LRU behavior
        self._cache: OrderedDict[str, dict[str, Any]] = OrderedDict()

        # Cache statistics
        self._hits = 0
        self._misses = 0

        # Lock for thread safety
        self._lock = asyncio.Lock()

    async def get_automation_analysis(self, automation_id: str) -> AutomationAnalysis | None:
        """Get automation analysis from cache.

        Args:
            automation_id: ID of automation to retrieve

        Returns:
            Cached analysis or None if not found/expired
        """
        async with self._lock:
            if automation_id not in self._cache:
                self._misses += 1
                return None

            entry = self._cache[automation_id]

            # Check if entry has expired
            if self._is_expired(entry):
                del self._cache[automation_id]
                self._misses += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(automation_id)
            self._hits += 1

            return entry["analysis"]

    async def cache_automation_analysis(self, analysis: AutomationAnalysis) -> None:
        """Cache automation analysis.

        Args:
            analysis: Analysis to cache
        """
        async with self._lock:
            # Create cache entry
            entry = {
                "analysis": analysis,
                "cached_at": datetime.now()
            }

            # Add/update entry
            self._cache[analysis.automation_id] = entry

            # Move to end (most recently used)
            self._cache.move_to_end(analysis.automation_id)

            # Enforce size limit (LRU eviction)
            while len(self._cache) > self.max_entries:
                # Remove least recently used item
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]

    async def invalidate_cache(self, automation_id: str) -> None:
        """Invalidate specific cache entry.

        Args:
            automation_id: ID of automation to invalidate
        """
        async with self._lock:
            self._cache.pop(automation_id, None)

    async def clear_all(self) -> None:
        """Clear all cache entries."""
        async with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    async def get_cache_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        async with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0.0

            return {
                "total_entries": len(self._cache),
                "max_entries": self.max_entries,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "ttl_hours": self.ttl.total_seconds() / 3600
            }

    async def cleanup_expired(self) -> int:
        """Remove expired entries from cache.

        Returns:
            Number of entries removed
        """
        async with self._lock:
            expired_keys = []

            for key, entry in self._cache.items():
                if self._is_expired(entry):
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

            return len(expired_keys)

    def _is_expired(self, entry: dict[str, Any]) -> bool:
        """Check if cache entry has expired.

        Args:
            entry: Cache entry to check

        Returns:
            True if expired, False otherwise
        """
        cached_at = entry["cached_at"]
        return datetime.now() - cached_at > self.ttl

    async def get_cached_automation_ids(self) -> list[str]:
        """Get list of cached automation IDs.

        Returns:
            List of automation IDs in cache
        """
        async with self._lock:
            return list(self._cache.keys())

    async def is_cached(self, automation_id: str) -> bool:
        """Check if automation is cached and not expired.

        Args:
            automation_id: ID of automation to check

        Returns:
            True if cached and not expired, False otherwise
        """
        async with self._lock:
            if automation_id not in self._cache:
                return False

            entry = self._cache[automation_id]
            return not self._is_expired(entry)

    async def get_cache_size_bytes(self) -> int:
        """Get approximate cache size in bytes.

        Returns:
            Approximate cache size in bytes
        """
        async with self._lock:
            # This is a rough estimate
            total_size = 0
            for entry in self._cache.values():
                analysis = entry["analysis"]
                # Rough estimate based on string lengths and object overhead
                total_size += len(str(analysis.model_dump())) * 2  # Unicode overhead

            return total_size

