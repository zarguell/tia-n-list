#!/usr/bin/env python3
"""
Tests for SimpleMemory.
"""

import json
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

import pytest

from src.simple_memory import SimpleMemory


class TestSimpleMemory:
    """Test suite for SimpleMemory."""

    @pytest.fixture
    def temp_memory_file(self):
        """Create temporary memory file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = Path(f.name)

        yield temp_file

        # Cleanup
        if temp_file.exists():
            temp_file.unlink()

    @pytest.fixture
    def sample_memory_data(self):
        """Create sample memory data for testing."""
        return {
            "used_articles": {
                "2025-11-07": ["article-1", "article-2", "article-3"],
                "2025-11-06": ["article-4", "article-5"],
                "2025-11-05": ["article-6"]
            },
            "last_cleanup": "2025-11-07T10:00:00.000000"
        }

    @pytest.fixture
    def memory_with_data(self, temp_memory_file, sample_memory_data):
        """Create SimpleMemory instance with sample data."""
        with open(temp_memory_file, 'w') as f:
            json.dump(sample_memory_data, f)

        return SimpleMemory(temp_memory_file)

    @pytest.fixture
    def empty_memory(self, temp_memory_file):
        """Create empty SimpleMemory instance."""
        return SimpleMemory(temp_memory_file)

    def test_initialization_empty(self, temp_memory_file):
        """Test SimpleMemory initialization with empty file."""
        memory = SimpleMemory(temp_memory_file)

        # Should create default structure
        assert memory._memory_data == {
            "used_articles": {},
            "last_cleanup": memory._memory_data["last_cleanup"]
        }

    def test_initialization_with_data(self, memory_with_data, sample_memory_data):
        """Test SimpleMemory initialization with existing data."""
        memory = memory_with_data

        assert memory._memory_data["used_articles"] == sample_memory_data["used_articles"]
        assert "last_cleanup" in memory._memory_data

    def test_initialization_with_corrupted_data(self, temp_memory_file):
        """Test SimpleMemory initialization with corrupted JSON."""
        # Write invalid JSON
        with open(temp_memory_file, 'w') as f:
            f.write("{ invalid json")

        memory = SimpleMemory(temp_memory_file)

        # Should create default structure
        assert "used_articles" in memory._memory_data
        assert "last_cleanup" in memory._memory_data

    def test_load_memory_normalize_legacy_format(self, temp_memory_file):
        """Test memory loading with legacy format normalization."""
        legacy_data = {
            "last_reports": {
                "2025-11-07": ["article-1", "article-2"],
                "2025-11-06": ["article-3"]
            }
        }

        with open(temp_memory_file, 'w') as f:
            json.dump(legacy_data, f)

        memory = SimpleMemory(temp_memory_file)

        # Should normalize to used_articles format
        assert "used_articles" in memory._memory_data
        assert "last_reports" not in memory._memory_data
        assert "2025-11-07" in memory._memory_data["used_articles"]
        assert "2025-11-06" in memory._memory_data["used_articles"]

    def test_load_memory_normalize_datetime_format(self, temp_memory_file):
        """Test memory loading with datetime format normalization."""
        data_with_datetime = {
            "used_articles": {
                "2025-11-07T10:00:00.000000": ["article-1"],
                "2025-11-06": ["article-2"]
            }
        }

        with open(temp_memory_file, 'w') as f:
            json.dump(data_with_datetime, f)

        memory = SimpleMemory(temp_memory_file)

        # Should normalize to YYYY-MM-DD format
        assert "2025-11-07" in memory._memory_data["used_articles"]
        assert "2025-11-06" in memory._memory_data["used_articles"]
        # Should not have datetime format
        assert "2025-11-07T10:00:00.000000" not in memory._memory_data["used_articles"]

    def test_get_used_articles(self, memory_with_data):
        """Test getting used articles for a specific date."""
        memory = memory_with_data
        target_date = date(2025, 11, 7)

        used_articles = memory.get_used_articles(target_date)

        assert used_articles == {"article-1", "article-2", "article-3"}

    def test_get_used_articles_no_data(self, empty_memory):
        """Test getting used articles for date with no data."""
        memory = empty_memory
        target_date = date(2025, 11, 7)

        used_articles = memory.get_used_articles(target_date)

        assert used_articles == set()

    def test_mark_articles_used(self, empty_memory):
        """Test marking articles as used."""
        memory = empty_memory
        target_date = date(2025, 11, 7)
        article_ids = ["article-1", "article-2", "article-3"]

        memory.mark_articles_used(article_ids, target_date)

        # Verify articles were marked
        used_articles = memory.get_used_articles(target_date)
        assert used_articles == {"article-1", "article-2", "article-3"}

        # Verify file was saved
        assert memory.memory_file.exists()

        # Verify file content
        with open(memory.memory_file, 'r') as f:
            saved_data = json.load(f)
            assert "2025-11-07" in saved_data["used_articles"]
            assert set(saved_data["used_articles"]["2025-11-07"]) == {"article-1", "article-2", "article-3"}

    def test_mark_articles_used_add_to_existing(self, memory_with_data):
        """Test marking articles as used when date already has data."""
        memory = memory_with_data
        target_date = date(2025, 11, 7)
        new_article_ids = ["article-4", "article-1"]  # article-1 already exists

        memory.mark_articles_used(new_article_ids, target_date)

        used_articles = memory.get_used_articles(target_date)

        # Should have original + new (no duplicates)
        expected = {"article-1", "article-2", "article-3", "article-4"}
        assert used_articles == expected

    def test_get_recently_used_articles(self, memory_with_data):
        """Test getting recently used articles within specified days."""
        memory = memory_with_data
        today = date(2025, 11, 8)  # Day after the sample data

        # Test 7 days back (should include all)
        recent = memory.get_recently_used_articles(days_back=7)
        expected = {"article-1", "article-2", "article-3", "article-4", "article-5", "article-6"}
        assert recent == expected

        # Test 1 day back (should only include 2025-11-07)
        recent = memory.get_recently_used_articles(days_back=1)
        expected = {"article-1", "article-2", "article-3"}
        assert recent == expected

    def test_get_recently_used_articles_empty(self, empty_memory):
        """Test getting recently used articles from empty memory."""
        memory = empty_memory

        recent = memory.get_recently_used_articles(days_back=7)
        assert recent == set()

    def test_cleanup_old_entries(self, memory_with_data):
        """Test cleanup of old memory entries."""
        memory = memory_with_data
        cutoff_date = date(2025, 11, 6)

        memory.cleanup_old_entries(days_to_keep=2)  # Keep last 2 days

        # Should remove 2025-11-05 (older than cutoff)
        assert "2025-11-07" in memory._memory_data["used_articles"]
        assert "2025-11-06" in memory._memory_data["used_articles"]
        assert "2025-11-05" not in memory._memory_data["used_articles"]

    def test_cleanup_old_entries_no_data(self, empty_memory):
        """Test cleanup with no data."""
        memory = empty_memory

        # Should not raise error
        memory.cleanup_old_entries(days_to_keep=30)

        assert memory._memory_data["used_articles"] == {}

    def test_get_statistics(self, memory_with_data):
        """Test memory statistics generation."""
        memory = memory_with_data
        stats = memory.get_statistics()

        assert stats["total_days"] == 3
        assert stats["total_articles"] == 6
        assert stats["recent_articles_7d"] == 6
        assert stats["oldest_date"] == "2025-11-05"
        assert stats["newest_date"] == "2025-11-07"

    def test_get_statistics_empty(self, empty_memory):
        """Test statistics generation with empty memory."""
        memory = empty_memory
        stats = memory.get_statistics()

        assert stats["total_days"] == 0
        assert stats["total_articles"] == 0
        assert stats["recent_articles_7d"] == 0
        assert stats["oldest_date"] is None
        assert stats["newest_date"] is None

    def test_get_statistics_with_invalid_dates(self, temp_memory_file):
        """Test statistics with invalid date formats."""
        data_with_invalid_dates = {
            "used_articles": {
                "2025-11-07": ["article-1"],
                "invalid-date": ["article-2"],  # Should be ignored
                "2025-11-05": ["article-3"]
            }
        }

        with open(temp_memory_file, 'w') as f:
            json.dump(data_with_invalid_dates, f)

        memory = SimpleMemory(temp_memory_file)
        stats = memory.get_statistics()

        # Should ignore invalid dates
        assert stats["total_days"] == 2
        assert stats["total_articles"] == 2
        assert stats["oldest_date"] == "2025-11-05"
        assert stats["newest_date"] == "2025-11-07"

    def test_save_memory_updates_timestamp(self, empty_memory):
        """Test that saving memory updates the cleanup timestamp."""
        memory = empty_memory
        old_timestamp = memory._memory_data["last_cleanup"]

        # Mark some articles as used (which saves the file)
        memory.mark_articles_used(["article-1"], date.today())

        new_timestamp = memory._memory_data["last_cleanup"]
        assert new_timestamp != old_timestamp

    def test_default_memory_file_creation(self):
        """Test SimpleMemory creates default memory file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            default_file = Path(temp_dir) / "default_memory.json"

            memory = SimpleMemory(default_file)

            # Should create the file
            assert default_file.exists()

            # Should have default structure
            with open(default_file, 'r') as f:
                data = json.load(f)
                assert "used_articles" in data
                assert "last_cleanup" in data

    def test_concurrent_usage(self, memory_with_data):
        """Test memory behavior with concurrent-like usage."""
        memory = memory_with_data

        # Simulate multiple operations
        target_date = date(2025, 11, 8)

        # Mark articles as used
        memory.mark_articles_used(["article-7", "article-8"], target_date)

        # Get recently used articles
        recent = memory.get_recently_used_articles(days_back=7)
        assert "article-7" in recent
        assert "article-8" in recent

        # Mark more articles for same date
        memory.mark_articles_used(["article-9"], target_date)

        # Verify all articles are tracked
        used = memory.get_used_articles(target_date)
        expected = {"article-7", "article-8", "article-9"}
        assert used == expected

    def test_memory_persistence_across_instances(self, temp_memory_file, sample_memory_data):
        """Test that memory persists across different instances."""
        # Create initial memory with data
        with open(temp_memory_file, 'w') as f:
            json.dump(sample_memory_data, f)

        memory1 = SimpleMemory(temp_memory_file)

        # Add new articles
        target_date = date(2025, 11, 8)
        memory1.mark_articles_used(["article-7"], target_date)

        # Create new instance
        memory2 = SimpleMemory(temp_memory_file)

        # Verify data persists
        used = memory2.get_used_articles(target_date)
        assert used == {"article-7"}

        # Verify original data still exists
        old_used = memory2.get_used_articles(date(2025, 11, 7))
        assert old_used == {"article-1", "article-2", "article-3"}

    def test_edge_case_article_ids(self, empty_memory):
        """Test handling of edge case article IDs."""
        memory = empty_memory
        target_date = date(2025, 11, 7)

        # Test with empty article IDs
        memory.mark_articles_used([], target_date)
        used = memory.get_used_articles(target_date)
        assert used == set()

        # Test with None and empty string in article IDs
        memory.mark_articles_used(["article-1", "", "article-2"], target_date)
        used = memory.get_used_articles(target_date)
        assert used == {"article-1", "", "article-2"}

        # Test with duplicate article IDs
        memory.mark_articles_used(["article-1", "article-1", "article-3"], target_date)
        used = memory.get_used_articles(target_date)
        assert used == {"article-1", "", "article-2", "article-3"}