"""Tests for the database module."""

import pytest
import tempfile
from pathlib import Path
from src import database


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


def test_initialize_database(temp_db):
    """Test database initialization creates required tables."""
    conn = database.get_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = [row[0] for row in cursor.fetchall()]

    expected_tables = ['sources', 'articles', 'iocs']
    for table in expected_tables:
        assert table in tables

    conn.close()


def test_add_source(temp_db):
    """Test adding a new source."""
    source_id = database.add_source("Test Source", "https://example.com/feed")
    assert source_id is not None
    assert source_id > 0

    # Verify the source was added
    sources = database.get_all_sources()
    assert len(sources) == 1
    assert sources[0]['name'] == "Test Source"
    assert sources[0]['url'] == "https://example.com/feed"


def test_add_duplicate_source(temp_db):
    """Test adding a source with duplicate URL replaces the existing one."""
    source_id1 = database.add_source("Source 1", "https://example.com/feed")
    source_id2 = database.add_source("Source 2", "https://example.com/feed")

    # Should get different IDs (INSERT OR REPLACE creates new row)
    assert source_id1 != source_id2

    sources = database.get_all_sources()
    assert len(sources) == 1
    assert sources[0]['name'] == "Source 2"  # Name should be updated


def test_update_source_last_fetched(temp_db):
    """Test updating source last_fetched timestamp."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    # Initially should be None
    sources = database.get_all_sources()
    assert sources[0]['last_fetched'] is None

    # Update last_fetched
    database.update_source_last_fetched(source_id)

    # Check it was updated
    sources = database.get_all_sources()
    assert sources[0]['last_fetched'] is not None


def test_add_articles(temp_db):
    """Test adding multiple articles."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    articles = [
        {
            'source_id': source_id,
            'guid': 'article-1',
            'title': 'Article 1',
            'url': 'https://example.com/article-1',
            'raw_content': 'Content 1'
        },
        {
            'source_id': source_id,
            'guid': 'article-2',
            'title': 'Article 2',
            'url': 'https://example.com/article-2',
            'raw_content': 'Content 2'
        }
    ]

    inserted_ids = database.add_articles(articles)
    assert len(inserted_ids) == 2
    assert all(id_ > 0 for id_ in inserted_ids)


def test_add_duplicate_articles(temp_db):
    """Test that duplicate articles (same guid) are ignored."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    articles = [
        {
            'source_id': source_id,
            'guid': 'article-1',
            'title': 'Article 1',
            'url': 'https://example.com/article-1',
            'raw_content': 'Content 1'
        }
    ]

    inserted_ids1 = database.add_articles(articles)
    inserted_ids2 = database.add_articles(articles)  # Same articles again

    # Should only insert once
    assert len(inserted_ids1) == 1
    assert len(inserted_ids2) == 1
    assert inserted_ids1[0] == inserted_ids2[0]


def test_get_article_by_id(temp_db):
    """Test retrieving an article by ID."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    article = {
        'source_id': source_id,
        'guid': 'article-1',
        'title': 'Test Article',
        'url': 'https://example.com/article',
        'raw_content': 'Test content'
    }

    inserted_ids = database.add_articles([article])
    article_id = inserted_ids[0]

    retrieved = database.get_article_by_id(article_id)
    assert retrieved is not None
    assert retrieved['title'] == 'Test Article'
    assert retrieved['guid'] == 'article-1'
    assert retrieved['status'] == 'fetched'


def test_get_article_by_id_not_found(temp_db):
    """Test retrieving a non-existent article."""
    result = database.get_article_by_id(999)
    assert result is None


def test_get_articles_by_status(temp_db):
    """Test retrieving articles by status."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    articles = [
        {
            'source_id': source_id,
            'guid': 'article-1',
            'title': 'Article 1',
            'url': 'https://example.com/article-1',
            'raw_content': 'Content 1'
        },
        {
            'source_id': source_id,
            'guid': 'article-2',
            'title': 'Article 2',
            'url': 'https://example.com/article-2',
            'raw_content': 'Content 2'
        }
    ]

    inserted_ids = database.add_articles(articles)

    # Update status of one article
    database.update_article_status(inserted_ids[0], 'processed')

    # Test getting fetched articles
    fetched = database.get_articles_by_status('fetched')
    assert len(fetched) == 1
    assert fetched[0]['guid'] == 'article-2'

    # Test getting processed articles
    processed = database.get_articles_by_status('processed')
    assert len(processed) == 1
    assert processed[0]['guid'] == 'article-1'


def test_update_article_processed_content(temp_db):
    """Test updating article with processed content."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    article = {
        'source_id': source_id,
        'guid': 'article-1',
        'title': 'Test Article',
        'url': 'https://example.com/article',
        'raw_content': 'Test content'
    }

    inserted_ids = database.add_articles([article])
    article_id = inserted_ids[0]

    # Update with processed content
    database.update_article_processed_content(
        article_id,
        "Processed content",
        "Article summary",
        85
    )

    # Verify update
    updated = database.get_article_by_id(article_id)
    assert updated['processed_content'] == "Processed content"
    assert updated['summary'] == "Article summary"
    assert updated['score'] == 85
    assert updated['status'] == 'processed'


def test_add_iocs(temp_db):
    """Test adding IOCs to database."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    article = {
        'source_id': source_id,
        'guid': 'article-1',
        'title': 'Test Article',
        'url': 'https://example.com/article',
        'raw_content': 'Test content'
    }

    inserted_ids = database.add_articles([article])
    article_id = inserted_ids[0]

    iocs = [
        {
            'article_id': article_id,
            'type': 'domain',
            'value': 'evil.com'
        },
        {
            'article_id': article_id,
            'type': 'ip_address',
            'value': '192.168.1.100'
        }
    ]

    inserted_ioc_ids = database.add_iocs(iocs)
    assert len(inserted_ioc_ids) == 2

    # Verify IOCs were added
    retrieved_iocs = database.get_iocs_by_article_id(article_id)
    assert len(retrieved_iocs) == 2

    domains = [ioc for ioc in retrieved_iocs if ioc['type'] == 'domain']
    ips = [ioc for ioc in retrieved_iocs if ioc['type'] == 'ip_address']

    assert len(domains) == 1
    assert domains[0]['value'] == 'evil.com'
    assert len(ips) == 1
    assert ips[0]['value'] == '192.168.1.100'


def test_add_duplicate_iocs(temp_db):
    """Test that duplicate IOCs are ignored."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    article = {
        'source_id': source_id,
        'guid': 'article-1',
        'title': 'Test Article',
        'url': 'https://example.com/article',
        'raw_content': 'Test content'
    }

    inserted_ids = database.add_articles([article])
    article_id = inserted_ids[0]

    iocs = [
        {
            'article_id': article_id,
            'type': 'domain',
            'value': 'evil.com'
        }
    ]

    # Add the same IOC twice
    inserted_ioc_ids1 = database.add_iocs(iocs)
    inserted_ioc_ids2 = database.add_iocs(iocs)

    # Should only insert once
    assert len(inserted_ioc_ids1) == 1
    assert len(inserted_ioc_ids2) == 1
    assert inserted_ioc_ids1[0] == inserted_ioc_ids2[0]


def test_get_top_articles(temp_db):
    """Test retrieving top articles by score."""
    source_id = database.add_source("Test Source", "https://example.com/feed")

    articles = [
        {
            'source_id': source_id,
            'guid': 'article-1',
            'title': 'Article 1',
            'url': 'https://example.com/article-1',
            'raw_content': 'Content 1'
        },
        {
            'source_id': source_id,
            'guid': 'article-2',
            'title': 'Article 2',
            'url': 'https://example.com/article-2',
            'raw_content': 'Content 2'
        },
        {
            'source_id': source_id,
            'guid': 'article-3',
            'title': 'Article 3',
            'url': 'https://example.com/article-3',
            'raw_content': 'Content 3'
        }
    ]

    inserted_ids = database.add_articles(articles)

    # Update articles with different scores
    database.update_article_processed_content(inserted_ids[0], "Processed 1", "Summary 1", 70)
    database.update_article_processed_content(inserted_ids[1], "Processed 2", "Summary 2", 90)
    database.update_article_processed_content(inserted_ids[2], "Processed 3", "Summary 3", 80)

    # Get top 2 articles
    top_articles = database.get_top_articles(2)
    assert len(top_articles) == 2

    # Should be ordered by score (descending)
    assert top_articles[0]['score'] == 90
    assert top_articles[1]['score'] == 80

    # Should include source name
    assert 'source_name' in top_articles[0]
    assert top_articles[0]['source_name'] == "Test Source"


def test_get_top_articles_empty_db(temp_db):
    """Test getting top articles from empty database."""
    top_articles = database.get_top_articles(5)
    assert len(top_articles) == 0