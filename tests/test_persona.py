"""Tests for persona module."""

import pytest
from unittest.mock import patch, Mock
from src import persona


def test_fetch_joke_of_the_day_success():
    """Test successful joke fetching."""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            'setup': 'Why did the cybersecurity researcher cross the road?',
            'punchline': 'Because he was looking for vulnerabilities!'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        joke = persona.fetch_joke_of_the_day()

        assert joke == "Why did the cybersecurity researcher cross the road? Because he was looking for vulnerabilities!"


def test_fetch_joke_of_the_day_no_setup():
    """Test joke fetching when no setup in response."""
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {'setup': '', 'punchline': ''}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        joke = persona.fetch_joke_of_the_day()

        assert joke == "Why don't scientists trust atoms? Because they make up everything!"


def test_fetch_joke_of_the_day_request_error():
    """Test joke fetching when request fails."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Network error")

        joke = persona.fetch_joke_of_the_day()

        assert joke is None


def test_format_article_summary():
    """Test article summary formatting."""
    result = persona.format_article_summary(
        "Critical Vulnerability in Exchange Server",
        "A critical remote code execution vulnerability was discovered...",
        85
    )

    assert "🟢 Critical Vulnerability in Exchange Server" in result
    assert "Tia's take" in result
    assert "Relevance Score: 85/100" in result


def test_get_top_articles_for_summary():
    """Test getting top articles for summary."""
    # Mock database calls
    with patch('src.persona.database.get_top_articles') as mock_get:
        mock_articles = [
            {
                'title': 'Test Article 1',
                'source': 'Test Source',
                'score': 90,
                'summary': 'Test summary 1',
                'url': 'https://example.com/1'
            },
            {
                'title': 'Test Article 2',
                'source': 'Test Source',
                'score': 70,
                'summary': 'Test summary 2',
                'url': 'https://example.com/2'
            }
        ]
        mock_get.return_value = mock_articles

        result = persona.get_top_articles_for_summary(5)

        assert len(result) == 2
        assert result[0]['title'] == 'Test Article 1'
        assert result[0]['source'] == 'Test Source'
        assert result[0]['score'] == 90