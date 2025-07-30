"""Tests for cache manager."""

from datetime import datetime

import pytest

from activecamp_mcp.cache import CacheManager
from activecamp_mcp.models import AutomationAnalysis, FlowGraph


class TestCacheManager:
    """Test CacheManager class."""

    @pytest.fixture
    def cache_manager(self):
        """Create a CacheManager instance."""
        return CacheManager()

    @pytest.fixture
    def sample_analysis(self):
        """Create a sample automation analysis."""
        return AutomationAnalysis(
            automation_id="13",
            name="Test Automation",
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.now()
        )

    @pytest.mark.asyncio
    async def test_cache_and_retrieve_analysis(self, cache_manager, sample_analysis):
        """Test caching and retrieving automation analysis."""
        # Cache the analysis
        await cache_manager.cache_automation_analysis(sample_analysis)

        # Retrieve from cache
        result = await cache_manager.get_automation_analysis("13")

        assert result is not None
        assert result.automation_id == "13"
        assert result.name == "Test Automation"

    @pytest.mark.asyncio
    async def test_get_nonexistent_analysis(self, cache_manager):
        """Test retrieving non-existent analysis returns None."""
        result = await cache_manager.get_automation_analysis("999")
        assert result is None

    @pytest.mark.asyncio
    async def test_cache_expiration(self, cache_manager, sample_analysis):
        """Test cache expiration functionality."""
        # Create a cache manager with short TTL for testing
        short_ttl_cache = CacheManager(ttl_hours=0.0001)  # Very short TTL (0.36 seconds)

        # Cache the analysis
        await short_ttl_cache.cache_automation_analysis(sample_analysis)

        # Verify it's initially cached
        result = await short_ttl_cache.get_automation_analysis("13")
        assert result is not None

        # Wait for expiration
        import asyncio
        await asyncio.sleep(1)  # Wait longer than TTL

        # Should return None for expired cache
        result = await short_ttl_cache.get_automation_analysis("13")
        assert result is None

    @pytest.mark.asyncio
    async def test_invalidate_cache(self, cache_manager, sample_analysis):
        """Test cache invalidation."""
        # Cache the analysis
        await cache_manager.cache_automation_analysis(sample_analysis)

        # Verify it's cached
        result = await cache_manager.get_automation_analysis("13")
        assert result is not None

        # Invalidate cache
        await cache_manager.invalidate_cache("13")

        # Should return None after invalidation
        result = await cache_manager.get_automation_analysis("13")
        assert result is None

    @pytest.mark.asyncio
    async def test_clear_all_cache(self, cache_manager, sample_analysis):
        """Test clearing all cache."""
        # Cache multiple analyses
        await cache_manager.cache_automation_analysis(sample_analysis)

        analysis2 = AutomationAnalysis(
            automation_id="15",
            name="Another Automation",
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.now()
        )
        await cache_manager.cache_automation_analysis(analysis2)

        # Verify both are cached
        assert await cache_manager.get_automation_analysis("13") is not None
        assert await cache_manager.get_automation_analysis("15") is not None

        # Clear all cache
        await cache_manager.clear_all()

        # Both should be None after clearing
        assert await cache_manager.get_automation_analysis("13") is None
        assert await cache_manager.get_automation_analysis("15") is None

    @pytest.mark.asyncio
    async def test_cache_statistics(self, cache_manager, sample_analysis):
        """Test cache statistics."""
        # Initially empty
        stats = await cache_manager.get_cache_stats()
        assert stats["total_entries"] == 0
        assert stats["hit_rate"] == 0.0

        # Cache an analysis
        await cache_manager.cache_automation_analysis(sample_analysis)

        # Hit the cache
        await cache_manager.get_automation_analysis("13")
        await cache_manager.get_automation_analysis("13")

        # Miss the cache
        await cache_manager.get_automation_analysis("999")

        stats = await cache_manager.get_cache_stats()
        assert stats["total_entries"] == 1
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 2/3  # 2 hits out of 3 total requests

    @pytest.mark.asyncio
    async def test_cache_size_limit(self, cache_manager):
        """Test cache size limit enforcement."""
        # Set a small cache size limit for testing
        cache_manager.max_entries = 2

        # Cache 3 analyses
        for i in range(3):
            analysis = AutomationAnalysis(
                automation_id=str(i),
                name=f"Automation {i}",
                triggers=[],
                blocks=[],
                flow_graph=FlowGraph(nodes=[], edges=[]),
                contact_changes=[],
                analysis_timestamp=datetime.now()
            )
            await cache_manager.cache_automation_analysis(analysis)

        # Only the last 2 should be in cache (LRU eviction)
        assert await cache_manager.get_automation_analysis("0") is None  # Evicted
        assert await cache_manager.get_automation_analysis("1") is not None
        assert await cache_manager.get_automation_analysis("2") is not None

    @pytest.mark.asyncio
    async def test_cache_update_existing(self, cache_manager, sample_analysis):
        """Test updating existing cache entry."""
        # Cache initial analysis
        await cache_manager.cache_automation_analysis(sample_analysis)

        # Update the analysis
        updated_analysis = AutomationAnalysis(
            automation_id="13",
            name="Updated Automation",  # Changed name
            triggers=[],
            blocks=[],
            flow_graph=FlowGraph(nodes=[], edges=[]),
            contact_changes=[],
            analysis_timestamp=datetime.now()
        )

        # Cache the updated version
        await cache_manager.cache_automation_analysis(updated_analysis)

        # Should get the updated version
        result = await cache_manager.get_automation_analysis("13")
        assert result.name == "Updated Automation"
