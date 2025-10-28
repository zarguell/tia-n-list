"""Tests for the ingestion module."""

import pytest
import tempfile
import yaml
import requests
from pathlib import Path
from unittest.mock import Mock, patch
from src import ingestion, database


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


@pytest.fixture
def sample_config():
    """Create a sample feeds configuration."""
    config = {
        'feeds': [
            {
                'name': 'Test Feed 1',
                'url': 'https://example.com/feed1.xml'
            },
            {
                'name': 'Test Feed 2',
                'url': 'https://example.com/feed2.xml'
            }
        ]
    }
    return config


@pytest.fixture
def temp_config_file(sample_config):
    """Create a temporary config file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump(sample_config, f)
        temp_file = f.name

    yield temp_file

    # Cleanup
    Path(temp_file).unlink()


def test_load_feeds_config_file_exists(temp_config_file, sample_config):
    """Test loading feeds from an existing config file."""
    feeds = ingestion.load_feeds_config(temp_config_file)
    assert feeds == sample_config['feeds']


def test_load_feeds_config_file_not_exists():
    """Test loading feeds when config file doesn't exist."""
    feeds = ingestion.load_feeds_config("nonexistent.yml")
    assert feeds == []


def test_load_feeds_config_empty_file():
    """Test loading feeds from empty config file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        yaml.dump({}, f)
        temp_file = f.name

    try:
        feeds = ingestion.load_feeds_config(temp_file)
        assert feeds == []
    finally:
        Path(temp_file).unlink()


def test_add_feeds_to_database(temp_db):
    """Test adding feeds to database."""
    feeds = [
        {'name': 'Feed 1', 'url': 'https://example.com/feed1.xml'},
        {'name': 'Feed 2', 'url': 'https://example.com/feed2.xml'}
    ]

    source_ids = ingestion.add_feeds_to_database(feeds)

    assert len(source_ids) == 2
    assert all(id_ > 0 for id_ in source_ids)

    # Verify feeds were added
    sources = database.get_all_sources()
    assert len(sources) == 2
    assert sources[0]['name'] == 'Feed 1'
    assert sources[1]['name'] == 'Feed 2'


def test_fetch_feed_success():
    """Test successful feed fetching."""
    mock_response = Mock()
    mock_response.content = b"""
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Test Feed</title>
            <item>
                <title>Test Article</title>
                <link>https://example.com/article</link>
                <description>Test content</description>
            </item>
        </channel>
    </rss>
    """
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        with patch('feedparser.parse') as mock_parse:
            mock_feed = Mock()
            mock_feed.bozo = False
            mock_feed.entries = []
            mock_parse.return_value = mock_feed

            result = ingestion.fetch_feed('https://example.com/feed.xml')

            assert result == mock_feed
            mock_response.raise_for_status.assert_called_once()
            mock_parse.assert_called_once_with(mock_response.content)


def test_fetch_feed_request_error():
    """Test feed fetching with request error."""
    with patch('requests.get', side_effect=requests.RequestException("Network error")):
        result = ingestion.fetch_feed('https://example.com/feed.xml')
        assert result is None


def test_fetch_feed_parsing_error():
    """Test feed fetching with parsing error."""
    mock_response = Mock()
    mock_response.content = b"invalid xml"
    mock_response.raise_for_status.return_value = None

    with patch('requests.get', return_value=mock_response):
        with patch('feedparser.parse', side_effect=Exception("Parse error")):
            result = ingestion.fetch_feed('https://example.com/feed.xml')
            assert result is None


def test_extract_articles_from_feed(temp_db):
    """Test extracting articles from feed data."""
    # Create a source
    source_id = database.add_source("Test Source", "https://example.com/feed.xml")

    # Mock feed data with proper Mock configuration
    mock_entry1 = Mock()
    mock_entry1.title = "Article 1"
    mock_entry1.link = "https://example.com/article1"
    mock_entry1.id = "guid1"
    mock_entry1.content = [Mock(value="Content 1")]
    mock_entry1.summary = None
    mock_entry1.description = None
    # Configure mock to return actual values for .get() calls
    mock_entry1.get = lambda key, default='': {
        'title': "Article 1",
        'link': "https://example.com/article1",
        'id': "guid1",
        'content': [Mock(value="Content 1")]
    }.get(key, default)

    mock_entry2 = Mock()
    mock_entry2.title = "Article 2"
    mock_entry2.link = "https://example.com/article2"
    mock_entry2.id = "guid2"
    mock_entry2.content = None
    mock_entry2.summary = "Content 2"
    mock_entry2.description = None
    # Configure mock to return actual values for .get() calls
    mock_entry2.get = lambda key, default='': {
        'title': "Article 2",
        'link': "https://example.com/article2",
        'id': "guid2",
        'summary': "Content 2"
    }.get(key, default)

    mock_feed = Mock()
    mock_feed.entries = [mock_entry1, mock_entry2]

    articles = ingestion.extract_articles_from_feed(mock_feed, source_id)

    assert len(articles) == 2

    assert articles[0]['source_id'] == source_id
    assert articles[0]['guid'] == 'guid1'
    assert articles[0]['title'] == 'Article 1'
    assert articles[0]['url'] == 'https://example.com/article1'
    assert articles[0]['raw_content'] == 'Content 1'

    assert articles[1]['source_id'] == source_id
    assert articles[1]['guid'] == 'guid2'
    assert articles[1]['title'] == 'Article 2'
    assert articles[1]['url'] == 'https://example.com/article2'
    assert articles[1]['raw_content'] == 'Content 2'


def test_extract_articles_fallback_content(temp_db):
    """Test extracting articles with fallback content fields."""
    source_id = database.add_source("Test Source", "https://example.com/feed.xml")

    # Mock entry with no title or link (should be skipped)
    mock_entry = Mock()
    mock_entry.title = ""
    mock_entry.link = "https://example.com/article"
    mock_entry.id = "guid1"

    mock_feed = Mock()
    mock_feed.entries = [mock_entry]

    articles = ingestion.extract_articles_from_feed(mock_feed, source_id)
    assert len(articles) == 0


def test_extract_articles_guid_fallback(temp_db):
    """Test GUID fallback to link when no ID is present."""
    source_id = database.add_source("Test Source", "https://example.com/feed.xml")

    mock_entry = Mock()
    mock_entry.title = "Article"
    mock_entry.link = "https://example.com/article"
    # Configure get to return None for 'id' but actual values for other fields
    def mock_get(key, default=None):
        # Simulate dict.get() behavior - if key doesn't exist, return default
        result = default
        if key == 'title':
            result = "Article"
        elif key == 'link':
            result = "https://example.com/article"
        # Note: 'id' key doesn't exist, so return default
        return result
    mock_entry.get = mock_get
    mock_entry.content = [Mock(value="Content")]

    mock_feed = Mock()
    mock_feed.entries = [mock_entry]

    articles = ingestion.extract_articles_from_feed(mock_feed, source_id)

    assert len(articles) == 1
    assert articles[0]['guid'] == 'https://example.com/article'  # Should use link as GUID


def test_strip_html_tags():
    """Test HTML tag stripping."""
    html = "<p>This is <strong>bold</strong> text with <a href='link'>a link</a>.</p>"
    expected = "This is bold text with a link."
    result = ingestion.strip_html_tags(html)
    assert result == expected


def test_strip_html_tags_empty():
    """Test HTML tag stripping with empty input."""
    assert ingestion.strip_html_tags("") == ""
    assert ingestion.strip_html_tags(None) == ""


def test_ingest_single_feed_success(temp_db):
    """Test ingesting a single feed successfully."""
    # Mock feed data
    mock_entry = Mock()
    # Configure mock get to return actual values for all attributes
    def mock_get(key, default=None):
        if key == 'title':
            return "Test Article"
        elif key == 'link':
            return "https://example.com/article"
        elif key == 'id':
            return "guid1"
        return default
    mock_entry.get = mock_get
    # Configure strip() method for title and link access
    mock_entry.configure_mock(**{
        'title': Mock(strip=lambda: "Test Article"),
        'link': Mock(strip=lambda: "https://example.com/article"),
        'id': "guid1",
        'content': [Mock(value="Test content")]
    })

    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = [mock_entry]

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        result = ingestion.ingest_single_feed(
            "https://example.com/feed.xml",
            "Test Feed"
        )

        assert result['successful'] is True
        assert result['articles_found'] == 1
        assert result['new_articles'] == 1
        assert result['error'] is None

        # Verify article was added to database
        articles = database.get_articles_by_status('fetched')
        assert len(articles) == 1
        assert articles[0]['title'] == 'Test Article'


def test_ingest_single_feed_fetch_failure(temp_db):
    """Test ingesting a single feed when fetch fails."""
    with patch('src.ingestion.fetch_feed', return_value=None):
        result = ingestion.ingest_single_feed("https://example.com/feed.xml")

        assert result['successful'] is False
        assert result['articles_found'] == 0
        assert result['new_articles'] == 0
        assert result['error'] == 'Failed to fetch feed'


def test_ingest_single_feed_no_articles(temp_db):
    """Test ingesting a single feed with no articles."""
    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = []

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        result = ingestion.ingest_single_feed("https://example.com/feed.xml")

        assert result['successful'] is True
        assert result['articles_found'] == 0
        assert result['new_articles'] == 0
        assert result['error'] is None


def test_ingest_all_feeds_success(temp_db, temp_config_file):
    """Test ingesting all feeds from configuration."""
    # Mock feed data
    mock_entry = Mock()
    mock_entry.title = "Test Article"
    mock_entry.link = "https://example.com/article"
    mock_entry.id = "guid1"
    mock_entry.content = [Mock(value="Test content")]
    # Configure mock get to return actual values
    def mock_get(key, default=None):
        if key == 'title':
            return "Test Article"
        elif key == 'link':
            return "https://example.com/article"
        elif key == 'id':
            return "guid1"
        return default
    mock_entry.get = mock_get
    # Configure strip() to work on title and link
    mock_entry.title.strip = lambda: "Test Article"
    mock_entry.link.strip = lambda: "https://example.com/article"

    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = [mock_entry]

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        with patch('time.sleep'):  # Skip sleep for testing
            result = ingestion.ingest_all_feeds(temp_config_file, delay_between_feeds=0)

            assert result['total_feeds'] == 2
            assert result['successful_feeds'] == 2
            assert result['failed_feeds'] == 0
            assert result['total_articles'] == 2
            assert result['new_articles'] == 2

            # Verify articles were added to database
            articles = database.get_articles_by_status('fetched')
            assert len(articles) == 2


def test_ingest_all_feeds_no_config():
    """Test ingesting feeds with no configuration file."""
    result = ingestion.ingest_all_feeds("nonexistent.yml")

    assert result['total_feeds'] == 0
    assert result['successful_feeds'] == 0
    assert result['failed_feeds'] == 0
    assert result['total_articles'] == 0
    assert result['new_articles'] == 0


def test_validate_feed_url_valid():
    """Test validating a valid feed URL."""
    mock_entry = Mock()
    mock_entry.title = "Test Article"
    mock_entry.link = "https://example.com/article"

    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = [mock_entry]

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        result = ingestion.validate_feed_url("https://example.com/feed.xml")
        assert result is True


def test_validate_feed_url_invalid():
    """Test validating an invalid feed URL."""
    with patch('src.ingestion.fetch_feed', return_value=None):
        result = ingestion.validate_feed_url("https://example.com/invalid.xml")
        assert result is False


def test_validate_feed_url_no_entries():
    """Test validating a feed URL with no entries."""
    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = []

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        result = ingestion.validate_feed_url("https://example.com/empty.xml")
        assert result is False


def test_validate_feed_url_invalid_entries():
    """Test validating a feed URL with invalid entries."""
    mock_entry = Mock()
    mock_entry.title = ""  # No title
    mock_entry.link = ""   # No link
    # Configure get to return the actual empty strings
    mock_entry.get = lambda key, default='': {'title': '', 'link': ''}.get(key, default)

    mock_feed = Mock()
    mock_feed.bozo = False
    mock_feed.entries = [mock_entry]

    with patch('src.ingestion.fetch_feed', return_value=mock_feed):
        result = ingestion.validate_feed_url("https://example.com/bad.xml")
        assert result is False


