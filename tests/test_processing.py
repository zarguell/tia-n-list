"""Tests for the processing module."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from src import processing, database, llm_client


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


def create_sample_article(article_id=1, title='Critical Vulnerability in Exchange Server',
                          content='A critical remote code execution vulnerability was discovered in Microsoft Exchange Server that could allow attackers to gain complete control of affected systems.',
                          status='fetched', source_id=None):
    """Create a sample article for testing."""
    return {
        'id': article_id,
        'title': title,
        'url': 'https://example.com/vulnerability',
        'raw_content': content,
        'status': status,
        'source_id': source_id,
        'guid': f'test-{article_id}'
    }


def test_is_relevant_article_true(temp_db):
    """Test relevant article detection."""
    # Create a relevant article in database
    database.add_articles([create_sample_article()])

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.is_relevant_article.return_value = {
            'is_relevant': True,
            'relevance_score': 85,
            'reasoning': 'Contains critical security vulnerability'
        }

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [sample_article()]

            processing.filter_articles_for_relevance()

            # Verify the mock was called correctly
            mock_client.is_relevant_article.assert_called_once_with(
                'Critical Vulnerability in Exchange Server',
                'A critical remote code execution vulnerability was discovered in Microsoft Exchange Server that could allow attackers to gain complete control of affected systems.'
            )

            # Check database was updated
            updated_article = database.get_article_by_id(1)
            assert updated_article is not None
            assert updated_article['status'] == 'processed'
            assert updated_article['score'] == 85
            assert 'vulnerability' in updated_article['summary'].lower()


def test_is_relevant_article_false(temp_db):
    """Test irrelevant article detection."""
    article = create_sample_article(
        article_id=1,
        title='Microsoft Stock Price Update',
        content='Microsoft stocks rose 2% in quarterly earnings report.'
    )

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.is_relevant_article.return_value = {
            'is_relevant': False,
            'relevance_score': 20,
            'reasoning': 'General business news without security impact'
        }

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [article]

            processing.filter_articles_for_relevance()

            # Verify status was updated to rejected
            updated_article = database.get_article_by_id(1)
            assert updated_article is not None
            assert updated_article['status'] == 'rejected'


def test_llm_client_error(temp_db):
    """Test handling of LLM client errors."""
    article = create_sample_article(
        article_id=1,
        title='Test Article',
        content='Test content'
    )

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client_class.side_effect = ValueError("API key missing")

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [article]

            processing.filter_articles_for_relevance()

            # Article should be marked rejected due to error
            updated_article = database.get_article_by_id(1)
            assert updated_article is not None
            assert updated_article['status'] == 'rejected'


def test_extract_iocs_and_ttps_success(temp_db):
    """Test successful IOC and TTP extraction."""
    # Create processed article
    source_id = database.add_source("Test Source", "https://example.com/feed")
    article_data = create_sample_article(
        article_id=1,
        title='APT28 Malware Analysis',
        content='New APT28 malware uses C2 domain evil.com and employs PowerShell living-off-the-land techniques. File hashes: 7a3b5c9e2a9f8d3d6e1a3e2e1c1b2d3f6e.',
        status='processed'
    )

    inserted_ids = database.add_articles([article_data])
    article_id = inserted_ids[0]

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.extract_iocs_and_ttps.return_value = {
            'iocs': [
                {
                    'type': 'domain',
                    'value': 'evil.com',
                    'confidence': 'high',
                    'context': 'C2 server mentioned in analysis'
                },
                {
                    'type': 'file_hash',
                    'value': '7a3b5c9e2a9f8d3d6e1a3e2e1c1b2d3f6e.',
                    'confidence': 'high',
                    'context': 'Malware sample hash'
                }
            ],
            'ttps': [
                {
                    'technique': 'T1059.001',  # PowerShell
                    'tactic': 'TA0002',  # Execution
                    'description': 'PowerShell living-off-the-land',
                    'confidence': 'high'
                }
            ]
        }

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [database.get_article_by_id(article_id)]

            processing.extract_iocs_and_ttps()

            # Verify IOCs were stored
            iocs = database.get_iocs_by_article_id(article_id)
            assert len(iocs) == 2

            domains = [ioc for ioc in iocs if ioc['type'] == 'domain']
            hashes = [ioc for ioc in iocs if ioc['type'] == 'file_hash']

            assert len(domains) == 1
            assert domains[0]['value'] == 'evil.com'
            assert len(hashes) == 1
            assert hashes[0]['value'] == '7a3b5c9e2a9f8d3d6e1a3e2e1c1b2d3f6e.'

            # Verify TTP data was added to processed content
            updated_article = database.get_article_by_id(article_id)
            assert 'T1059.001' in updated_article['processed_content']
            assert 'PowerShell' in updated_article['processed_content']


def test_extract_iocs_and_ttps_no_iocs(temp_db):
    """Test extraction when no IOCs found."""
    source_id = database.add_source("Test Source", "https://example.com/feed")
    article_data = create_sample_article(
        article_id=1,
        title='General Security Article',
        content='This article discusses general security best practices without specific indicators.',
        status='processed'
    )
    # Set the source_id for the article
    article_data['source_id'] = source_id

    inserted_ids = database.add_articles([article_data])
    article_id = inserted_ids[0]

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.extract_iocs_and_ttps.return_value = {
            'iocs': [],
            'ttps': []
        }

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [database.get_article_by_id(article_id)]

            processing.extract_iocs_and_ttps()

            # Verify no IOCs stored
            iocs = database.get_iocs_by_article_id(article_id)
            assert len(iocs) == 0

            # Verify processed content was updated
            updated_article = database.get_article_by_id(article_id)
            assert 'TTPs' in updated_article['processed_content']


def test_extract_iocs_and_ttps_error(temp_db):
    """Test handling of extraction errors."""
    article_data = create_sample_article(
        article_id=1,
        title='Test Article',
        content='Test content',
        status='processed'
    )

    inserted_ids = database.add_articles([article_data])
    article_id = inserted_ids[0]

    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.extract_iocs_and_ttps.side_effect = Exception("API error")

        with patch('src.processing.database.get_articles_by_status') as mock_get:
            mock_get.return_value = [database.get_article_by_id(article_id)]

            # Should not crash, just print error
            processing.extract_iocs_and_ttps()

            # Verify error handling - no IOCs should be added
            iocs = database.get_iocs_by_article_id(article_id)
            assert len(iocs) == 0


def test_process_new_articles_integration(temp_db):
    """Test the full processing pipeline integration."""
    with patch('src.llm_client.LLMClient') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.is_relevant_article.return_value = {
            'is_relevant': True,
            'relevance_score': 80,
            'reasoning': 'Relevant security content'
        }
        mock_client.extract_iocs_and_ttps.return_value = {
            'iocs': [{'type': 'domain', 'value': 'malicious.com', 'confidence': 'high'}],
            'ttps': [{'technique': 'T1059', 'tactic': 'TA0002', 'confidence': 'high'}]
        }

        # Create test articles
        source_id = database.add_source("Test Source", "https://example.com/feed")
        relevant_article = {
            'source_id': source_id,
            'guid': 'relevant-1',
            'title': 'Relevant Security Article',
            'url': 'https://example.com/relevant',
            'raw_content': 'Relevant security content',
            'status': 'fetched'
        }
        irrelevant_article = {
            'source_id': source_id,
            'guid': 'irrelevant-1',
            'title': 'Irrelevant Article',
            'url': 'https://example.com/irrelevant',
            'raw_content': 'Irrelevant content',
            'status': 'fetched'
        }

        database.add_articles([relevant_article, irrelevant_article])

        # Run processing pipeline
        processing.process_new_articles()

        # Verify results
        processed_articles = database.get_articles_by_status('processed')
        rejected_articles = database.get_articles_by_status('rejected')
        iocs = database.get_iocs_by_article_id(database.get_all_sources()[0]['id'])

        # Should have 1 processed, 1 rejected, and 1 IOC
        assert len(processed_articles) == 1
        assert len(rejected_articles) == 1
        assert len(iocs) == 1

        # Verify processed article has TTPs in content
        processed_article = processed_articles[0]
        assert 'TTPs' in processed_article['processed_content']