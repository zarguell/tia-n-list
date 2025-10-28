"""Tests for blog generation module."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from src import blog_generator, database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    original_db_path = database.DB_PATH
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_db_path = Path(temp_dir) / "test.db"
        database.DB_PATH = temp_db_path
        database.initialize_database()
        yield temp_db_path
        database.DB_PATH = original_db_path


def test_generate_daily_summary_success(temp_db):
    """Test successful daily summary generation."""
    # Mock persona module
    with patch('src.blog_generator.persona.get_top_articles_for_summary') as mock_get:
        mock_articles = [
            {
                'title': 'Critical Vulnerability Discovered',
                'source': 'Threat Intel Source',
                'score': 85,
                'summary': 'A critical RCE vulnerability affects enterprise systems',
                'url': 'https://example.com/vuln'
            }
        ]
        mock_get.return_value = mock_articles

    with patch('src.blog_generator.persona.fetch_joke_of_the_day') as mock_joke:
        mock_joke.return_value = "Why did the firewall go to the doctor? It had a virus!"

        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value = None
            mock_open.return_value.__exit__.return_value = None

        result = blog_generator.generate_daily_summary()

        # Verify file was created
        mock_open.assert_called_once()
        call_args = mock_open.call_args[0]
        assert call_args[0][0].name == Path("hugo/content/posts/2025-10-26-daily-summary.md")
        assert call_args[0][0].mode == 'w'

        # Verify content
        content = mock_open.return_value.__enter__.return_value
        assert "Daily Threat Intelligence Summary" in content
        assert "Critical Vulnerability Discovered" in content
        assert "Threat Intel Source" in content
        assert mock_joke.return_value in content

        assert result is True


def test_generate_daily_summary_no_articles():
    """Test daily summary generation when no articles."""
    with patch('src.blog_generator.persona.get_top_articles_for_summary') as mock_get:
        mock_get.return_value = []

        result = blog_generator.generate_daily_summary()

        assert result is False


def test_generate_deep_dive_article():
    """Test deep-dive article generation."""
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value = None
        mock_open.return_value.__exit__.return_value = None

        result = blog_generator.generate_deep_dive_article(
            "Advanced APT Analysis",
            "Comprehensive analysis of new threat actor capabilities...",
            "Detailed TTPs and attribution analysis"
        )

        # Verify file creation
        mock_open.assert_called_once()
        filepath = mock_open.call_args[0][0][0]
        assert "deep-dive-advanced-apt-analysis" in filepath.name

        # Verify content
        content = mock_open.return_value.__enter__.return_value
        assert "Advanced APT Analysis" in content
        assert "Comprehensive analysis of new threat actor capabilities" in content
        assert "Detailed TTPs and attribution analysis" in content

        assert result is True


def test_generate_daily_summary_error():
    """Test error handling in daily summary generation."""
    with patch('src.blog_generator.persona.get_top_articles_for_summary') as mock_get:
        mock_get.side_effect = Exception("Database error")

        result = blog_generator.generate_daily_summary()

        assert result is False