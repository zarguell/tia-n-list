"""Tests for persona module (updated version without joke API)."""

from unittest.mock import patch
from src import persona


def test_persona_module_import():
    """Test that persona module can be imported without issues."""
    # This test ensures the module loads correctly after removing joke functionality
    assert hasattr(persona, 'format_article_summary')
    assert hasattr(persona, 'get_top_articles_for_summary')
    # These functions should no longer exist after removing joke functionality
    assert not hasattr(persona, 'fetch_joke_of_the_day')
    assert not hasattr(persona, 'add_joke_to_content')


def test_format_article_summary_high_score():
    """Test formatting article summary with high relevance score."""
    result = persona.format_article_summary(
        "Critical Vulnerability in Exchange Server",
        "A critical remote code execution vulnerability was discovered...",
        85
    )

    assert "🟢" in result  # High relevance emoji
    assert "Critical Vulnerability in Exchange Server" in result
    assert "Tia's take" in result
    assert "critical intelligence" in result
    assert "Relevance Score: 85/100" in result


def test_format_article_summary_medium_score():
    """Test formatting article summary with medium relevance score."""
    result = persona.format_article_summary(
        "Security Advisory Released",
        "A security advisory was released for multiple products...",
        65
    )

    assert "🟡" in result  # Medium relevance emoji
    assert "Security Advisory Released" in result
    assert "Tia's note" in result
    assert "Interesting development" in result
    assert "Relevance Score: 65/100" in result


def test_format_article_summary_low_score():
    """Test formatting article summary with low relevance score."""
    result = persona.format_article_summary(
        "Minor Security Update",
        "A minor security update was released...",
        25
    )

    assert "🔴" in result  # Low relevance emoji
    assert "Minor Security Update" in result
    # Low score should not have personal notes
    assert "Tia's take" not in result
    assert "Tia's note" not in result
    assert "Relevance Score: 25/100" in result


def test_get_top_articles_for_summary_success():
    """Test getting top articles for summary."""
    # Mock database calls
    with patch('src.persona.database.get_top_articles') as mock_get_articles, \
         patch('src.persona.database.get_all_sources') as mock_get_sources:

        mock_articles = [
            {
                'id': 'article1',
                'title': 'Test Article 1',
                'source_id': 'source1',
                'score': 90,
                'summary': 'Test summary 1',
                'url': 'https://example.com/1'
            },
            {
                'id': 'article2',
                'title': 'Test Article 2',
                'source_id': 'source2',
                'score': 70,
                'summary': 'Test summary 2',
                'url': 'https://example.com/2'
            }
        ]
        mock_sources = [
            {'id': 'source1', 'name': 'Krebs on Security'},
            {'id': 'source2', 'name': 'Schneier on Security'}
        ]

        mock_get_articles.return_value = mock_articles
        mock_get_sources.return_value = mock_sources

        result = persona.get_top_articles_for_summary(5)

        assert len(result) == 2
        assert result[0]['title'] == 'Test Article 1'
        assert result[0]['source'] == 'Krebs on Security'
        assert result[0]['score'] == 90
        assert result[1]['title'] == 'Test Article 2'
        assert result[1]['source'] == 'Schneier on Security'
        assert result[1]['score'] == 70


def test_get_top_articles_for_summary_database_error():
    """Test handling of database errors."""
    with patch('src.persona.database.get_top_articles') as mock_get:
        mock_get.side_effect = Exception("Database connection failed")

        result = persona.get_top_articles_for_summary(5)

        assert result == []