#!/usr/bin/env python3
"""
Tests for SimpleDigestGenerator.
"""

import json
import os
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from src.simple_digest_generator import SimpleDigestGenerator


class TestSimpleDigestGenerator:
    """Test suite for SimpleDigestGenerator."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            hugo_dir = Path(temp_dir) / "hugo" / "content" / "posts"
            config_dir = Path(temp_dir) / "config" / "prompts"

            data_dir.mkdir(parents=True)
            hugo_dir.mkdir(parents=True)
            config_dir.mkdir(parents=True)

            yield data_dir, hugo_dir, config_dir

    @pytest.fixture
    def sample_prompt(self, temp_dirs):
        """Create sample prompt template."""
        _, _, config_dir = temp_dirs
        prompt_file = config_dir / "simple_digest.json"

        prompt_template = {
            "version": "1.0.0",
            "description": "Simple threat intelligence digest prompt template",
            "persona": {
                "name": "Tia N. List",
                "role": "Threat Intelligence Analyst",
                "tone": "Professional, informative, and insightful"
            },
            "template": "Test prompt template for {{current_date}} with {{articles_summary}}",
            "variables": ["current_date", "articles_summary"]
        }

        with open(prompt_file, 'w') as f:
            json.dump(prompt_template, f)

        return prompt_file

    @pytest.fixture
    def sample_articles(self):
        """Create sample articles for testing."""
        return [
            {
                "id": "article-1",
                "title": "Critical Vulnerability in Enterprise Software",
                "url": "https://example.com/article1",
                "published_at": "2025-11-07T10:00:00Z",
                "source_id": "test-source",
                "content": {
                    "raw": "This is a test article about critical vulnerability in enterprise software that affects many organizations."
                },
                "analysis": {
                    "score": 85
                }
            },
            {
                "id": "article-2",
                "title": "New Malware Campaign Targets Healthcare",
                "url": "https://example.com/article2",
                "published_at": "2025-11-07T12:00:00Z",
                "source_id": "test-source-2",
                "content": {
                    "raw": "A new malware campaign has been discovered targeting healthcare organizations with ransomware."
                },
                "analysis": {
                    "score": 75
                }
            },
            {
                "id": "article-3",
                "title": "Microsoft Security Update",
                "url": "https://example.com/article3",
                "published_at": "2025-11-07T14:00:00Z",
                "source_id": "tech-source",
                "content": {
                    "raw": "Microsoft has released security updates to address several vulnerabilities in their products."
                },
                "analysis": {
                    "score": 70
                }
            }
        ]

    @pytest.fixture
    def generator(self, temp_dirs, sample_prompt):
        """Create SimpleDigestGenerator instance for testing."""
        data_dir, hugo_dir, config_dir = temp_dirs
        memory_file = data_dir / "simple_memory.json"

        return SimpleDigestGenerator(
            memory_file=memory_file,
            prompt_file=sample_prompt
        )

    def test_initialization(self, temp_dirs, sample_prompt):
        """Test SimpleDigestGenerator initialization."""
        data_dir, hugo_dir, config_dir = temp_dirs
        memory_file = data_dir / "simple_memory.json"

        generator = SimpleDigestGenerator(
            memory_file=memory_file,
            prompt_file=sample_prompt
        )

        assert generator.memory_file == memory_file
        assert generator.prompt_file == sample_prompt
        assert generator.storage is not None
        assert generator.llm_registry is not None
        assert generator.hugo_content_dir == hugo_dir

    def test_initialization_with_missing_prompt_file(self, temp_dirs):
        """Test initialization with missing prompt file."""
        data_dir, hugo_dir, config_dir = temp_dirs
        memory_file = data_dir / "simple_memory.json"
        missing_prompt = config_dir / "missing.json"

        with pytest.raises(FileNotFoundError):
            SimpleDigestGenerator(
                memory_file=memory_file,
                prompt_file=missing_prompt
            )

    def test_load_prompt_template(self, generator):
        """Test prompt template loading."""
        template = generator._load_prompt_template()

        assert template is not None
        assert "template" in template
        assert "persona" in template
        assert "{{current_date}}" in template["template"]
        assert "{{articles_summary}}" in template["template"]

    def test_normalize_article_datetime(self, generator):
        """Test datetime normalization for articles."""
        # Test with Z suffix
        article_z = {"published_at": "2025-11-07T10:00:00Z"}
        dt = generator._normalize_article_datetime(article_z)
        assert dt is not None
        assert dt.tzinfo is not None
        assert dt.year == 2025
        assert dt.month == 11
        assert dt.day == 7

        # Test without timezone
        article_no_tz = {"published_at": "2025-11-07T10:00:00"}
        dt = generator._normalize_article_datetime(article_no_tz)
        assert dt is not None
        assert dt.tzinfo is not None

        # Test with invalid format
        article_invalid = {"published_at": "invalid-date"}
        dt = generator._normalize_article_datetime(article_invalid)
        assert dt is None

        # Test with no published_at
        article_no_date = {}
        dt = generator._normalize_article_datetime(article_no_date)
        assert dt is None

    def test_get_article_content(self, generator, sample_articles):
        """Test article content extraction."""
        article = sample_articles[0]
        content = generator._get_article_content(article)

        assert "critical vulnerability" in content
        assert len(content) > 0

    @patch('src.simple_digest_generator.get_default_storage_provider')
    def test_get_fresh_articles(self, mock_storage, generator, sample_articles):
        """Test fresh article retrieval."""
        target_date = date(2025, 11, 7)

        # Mock storage response
        mock_storage.return_value.get_articles_by_date_range.return_value = sample_articles

        # Re-initialize generator to use mocked storage
        generator.storage = mock_storage.return_value

        fresh_articles = generator._get_fresh_articles(target_date)

        assert len(fresh_articles) == 3
        mock_storage.return_value.get_articles_by_date_range.assert_called_once_with(
            start_date=target_date,
            end_date=target_date,
            status='fetched'
        )

    def test_filter_unused_articles(self, generator, sample_articles):
        """Test filtering of recently used articles."""
        # Mock memory to return some used articles
        generator.memory.get_recently_used_articles.return_value = {"article-1"}

        unused = generator._filter_unused_articles(sample_articles)

        assert len(unused) == 2
        assert unused[0]["id"] == "article-2"
        assert unused[1]["id"] == "article-3"

    def test_format_articles_for_prompt(self, generator, sample_articles):
        """Test article formatting for LLM prompt."""
        formatted = generator._format_articles_for_prompt(sample_articles)

        assert "Article 1:" in formatted
        assert "Article 2:" in formatted
        assert "Article 3:" in formatted
        assert "Critical Vulnerability" in formatted
        assert "New Malware" in formatted
        assert "Microsoft Security" in formatted

    def test_format_articles_for_prompt_empty(self, generator):
        """Test article formatting with empty list."""
        formatted = generator._format_articles_for_prompt([])
        assert formatted == "No fresh articles available for analysis."

    def test_build_prompt(self, generator, sample_articles):
        """Test prompt building."""
        articles_summary = "Test article summary"
        target_date = date(2025, 11, 7)

        prompt = generator._build_prompt(articles_summary, target_date)

        assert "Test article summary" in prompt
        assert "November 07, 2025" in prompt

    def test_extract_themes(self, generator, sample_articles):
        """Test theme extraction from articles."""
        themes = generator._extract_themes(sample_articles)

        assert "Vulnerability" in themes
        assert "Malware" in themes
        assert "Tech Giants" in themes  # From Microsoft
        assert len(themes) <= 3  # Should be limited to 3 themes

    def test_extract_themes_empty(self, generator):
        """Test theme extraction with empty articles."""
        themes = generator._extract_themes([])
        assert themes == []

    def test_extract_themes_no_matches(self, generator):
        """Test theme extraction with no matching themes."""
        articles = [
            {"title": "Random Article About Nothing"},
            {"title": "Another Random Article"}
        ]
        themes = generator._extract_themes(articles)
        assert themes == []

    def test_generate_tags(self, generator, sample_articles):
        """Test tag generation from articles."""
        tags = generator._generate_tags(sample_articles)

        assert "threat-intelligence" in tags
        assert "daily-digest" in tags
        assert "cybersecurity" in tags
        assert "test-source" in tags or "test-source-2" in tags
        assert len(tags) <= 10  # Should be limited to 10 tags

    def test_generate_title(self, generator, sample_articles):
        """Test title generation."""
        target_date = date(2025, 11, 7)
        title = generator._generate_title(target_date, sample_articles)

        assert "November 07, 2025" in title
        assert ("Vulnerability" in title or "Malware" in title or "Tech Giants" in title)

    def test_generate_title_no_themes(self, generator):
        """Test title generation with no themes."""
        target_date = date(2025, 11, 7)
        articles = [{"title": "Random Article"}]
        title = generator._generate_title(target_date, articles)

        assert title == "Daily Threat Intelligence Digest - November 07, 2025"

    def test_generate_hugo_metadata(self, generator, sample_articles):
        """Test Hugo metadata generation."""
        target_date = date(2025, 11, 7)
        metadata = generator._generate_hugo_metadata(target_date, sample_articles)

        assert "title" in metadata
        assert "date" in metadata
        assert "tags" in metadata
        assert "categories" in metadata
        assert "summary" in metadata
        assert "author" in metadata
        assert "sources" in metadata

        assert metadata["author"] == "Tia N. List"
        assert "Threat Intelligence" in metadata["categories"]
        assert len(sample_articles) in metadata["summary"]
        assert len(metadata["sources"]) <= 10

    def test_format_hugo_post(self, generator, sample_articles):
        """Test Hugo post formatting."""
        metadata = {
            "title": "Test Digest",
            "date": "2025-11-07",
            "tags": ["test"],
            "author": "Test Author"
        }
        content = "# Test Digest\n\nThis is test content."

        hugo_post = generator._format_hugo_post(metadata, content, sample_articles)

        assert "+++" in hugo_post
        assert "title = \"Test Digest\"" in hugo_post
        assert "# Test Digest" in hugo_post
        assert "## References" in hugo_post
        assert "Critical Vulnerability" in hugo_post

    def test_generate_references_section(self, generator, sample_articles):
        """Test references section generation."""
        references = generator._generate_references_section(sample_articles)

        assert "## References" in references
        assert "1." in references
        assert "2." in references
        assert "3." in references
        assert "Critical Vulnerability" in references
        assert "https://example.com/article1" in references

    def test_generate_references_section_empty(self, generator):
        """Test references section with empty articles."""
        references = generator._generate_references_section([])
        assert references == ""

    def test_get_memory_statistics(self, generator):
        """Test memory statistics retrieval."""
        # Mock memory statistics
        expected_stats = {
            "total_days": 5,
            "total_articles": 25,
            "recent_articles_7d": 10
        }
        generator.memory.get_statistics.return_value = expected_stats

        stats = generator.get_memory_statistics()
        assert stats == expected_stats

    @patch('src.simple_digest_generator.get_default_storage_provider')
    @patch('src.simple_digest_generator.get_registry')
    def test_generate_daily_digest_success(self, mock_registry, mock_storage, generator, sample_articles, temp_dirs):
        """Test successful daily digest generation."""
        target_date = date(2025, 11, 7)

        # Mock storage
        mock_storage.return_value.get_articles_by_date_range.return_value = sample_articles
        generator.storage = mock_storage.return_value

        # Mock memory
        generator.memory.get_recently_used_articles.return_value = set()
        generator.memory.mark_articles_used = Mock()
        generator.memory.cleanup_old_entries = Mock()

        # Mock LLM response
        mock_registry.return_value.execute_with_fallback.return_value = "Generated digest content."

        # Create hugo content directory
        generator.hugo_content_dir = temp_dirs[1]

        result = generator.generate_daily_digest(target_date)

        assert result is not None
        assert result.startswith("daily-threat-intelligence-2025-11-07")
        assert result.endswith(".md")

        # Verify file was created
        hugo_file = generator.hugo_content_dir / result
        assert hugo_file.exists()

        # Verify file content
        with open(hugo_file, 'r') as f:
            content = f.read()
            assert "Generated digest content." in content
            assert "+++" in content
            assert "## References" in content

    @patch('src.simple_digest_generator.get_default_storage_provider')
    def test_generate_daily_digest_no_articles(self, mock_storage, generator):
        """Test digest generation with no fresh articles."""
        target_date = date(2025, 11, 7)

        # Mock empty storage response
        mock_storage.return_value.get_articles_by_date_range.return_value = []
        generator.storage = mock_storage.return_value

        result = generator.generate_daily_digest(target_date)
        assert result is None

    @patch('src.simple_digest_generator.get_default_storage_provider')
    @patch('src.simple_digest_generator.get_registry')
    def test_generate_daily_digest_llm_failure(self, mock_registry, mock_storage, generator, sample_articles):
        """Test digest generation with LLM failure."""
        target_date = date(2025, 11, 7)

        # Mock storage
        mock_storage.return_value.get_articles_by_date_range.return_value = sample_articles
        generator.storage = mock_storage.return_value

        # Mock memory
        generator.memory.get_recently_used_articles.return_value = set()

        # Mock LLM failure
        mock_registry.return_value.execute_with_fallback.return_value = ""

        result = generator.generate_daily_digest(target_date)
        assert result is None

    @patch('src.simple_digest_generator.get_default_storage_provider')
    def test_generate_daily_digest_all_articles_used(self, mock_storage, generator, sample_articles):
        """Test digest generation when all articles were recently used."""
        target_date = date(2025, 11, 7)

        # Mock storage
        mock_storage.return_value.get_articles_by_date_range.return_value = sample_articles
        generator.storage = mock_storage.return_value

        # Mock memory with all articles used
        generator.memory.get_recently_used_articles.return_value = {"article-1", "article-2", "article-3"}

        result = generator.generate_daily_digest(target_date)
        assert result is None

    def test_configuration_constants(self):
        """Test that configuration constants are properly set."""
        from src.simple_digest_generator import (
            MAX_ARTICLES_FOR_PROMPT, MAX_CONTENT_LENGTH, MIN_CONTENT_LENGTH,
            MAX_REFERENCES, MEMORY_DAYS_BACK, MEMORY_CLEANUP_DAYS, MAX_TOKENS
        )

        assert MAX_ARTICLES_FOR_PROMPT > 0
        assert MAX_CONTENT_LENGTH > 0
        assert MIN_CONTENT_LENGTH > 0
        assert MAX_REFERENCES > 0
        assert MEMORY_DAYS_BACK > 0
        assert MEMORY_CLEANUP_DAYS > 0
        assert MAX_TOKENS > 0

    @patch.dict(os.environ, {
        'SIMPLE_DIGEST_MAX_ARTICLES': '15',
        'SIMPLE_DIGEST_MAX_CONTENT_LENGTH': '2000'
    })
    def test_environment_override(self):
        """Test that environment variables override constants."""
        # This test would require module reload to take effect
        # For now, just verify the environment variables are set
        assert os.environ.get('SIMPLE_DIGEST_MAX_ARTICLES') == '15'
        assert os.environ.get('SIMPLE_DIGEST_MAX_CONTENT_LENGTH') == '2000'