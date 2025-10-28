"""Feed ingestion module for Tia N. List project.

This module handles fetching and parsing RSS/Atom feeds from various
threat intelligence sources.
"""

import feedparser
import requests
from typing import List, Dict, Any, Optional
import time
import yaml
from pathlib import Path
from src import database


def load_feeds_config(config_path: str = "config/feeds.yml") -> List[Dict[str, str]]:
    """Load feed configuration from YAML file.

    Args:
        config_path: Path to the feeds configuration file.

    Returns:
        List of feed configurations with 'name' and 'url' keys.
    """
    config_file = Path(config_path)

    if not config_file.exists():
        return []

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config.get('feeds', [])


def add_feeds_to_database(feeds: List[Dict[str, str]]) -> List[int]:
    """Add feeds to the database.

    Args:
        feeds: List of feed configurations with 'name' and 'url' keys.

    Returns:
        List[int]: IDs of added/updated feeds.
    """
    source_ids = []

    for feed in feeds:
        source_id = database.add_source(feed['name'], feed['url'])
        source_ids.append(source_id)

    return source_ids


def fetch_feed(feed_url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """Fetch and parse a single RSS/Atom feed.

    Args:
        feed_url: URL of the feed to fetch.
        timeout: Request timeout in seconds.

    Returns:
        Parsed feed data or None if fetching failed.
    """
    try:
        # Set user agent to avoid being blocked
        headers = {
            'User-Agent': 'Tia-N-List/1.0 (Threat Intelligence Aggregator)'
        }

        response = requests.get(feed_url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Parse the feed
        feed = feedparser.parse(response.content)

        if feed.bozo:
            # Feed is malformed but might still be usable
            print(f"Warning: Feed {feed_url} has parsing issues: {feed.bozo_exception}")

        return feed

    except requests.RequestException as e:
        print(f"Error fetching feed {feed_url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
        return None


def extract_articles_from_feed(feed_data: Dict[str, Any], source_id: int, hours_back: int = 24) -> List[Dict[str, Any]]:
    """Extract articles from parsed feed data with time filtering.

    Args:
        feed_data: Parsed feed data from feedparser.
        source_id: Database ID of the feed source.
        hours_back: Only include articles published within this many hours.

    Returns:
        List of article dictionaries.
    """
    import datetime

    # Calculate cutoff time
    cutoff_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours_back)
    articles = []

    for entry in feed_data.entries:
        try:
            # Extract basic article information
            title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()

            if not title or not link:
                continue

            # Get GUID (use link as fallback if no guid)
            guid = entry.get('id', link)

            # Extract and parse publication date
            published_time = None
            for date_field in ['published_parsed', 'updated_parsed']:
                if hasattr(entry, date_field) and getattr(entry, date_field):
                    # Convert time.struct_time to datetime.datetime for comparison
                    time_struct = getattr(entry, date_field)
                    published_time = datetime.datetime(*time_struct[:6], tzinfo=datetime.timezone.utc)
                    break

            # Skip articles older than cutoff time
            if published_time and published_time < cutoff_time:
                continue

            # Extract content
            content = ''

            # Try different content fields in order of preference
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].value if entry.content else ''
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description

            # Clean up HTML tags from content (basic cleaning)
            content = strip_html_tags(content)

            article = {
                'source_id': source_id,
                'guid': guid,
                'title': title,
                'url': link,
                'raw_content': content,
                'published_at': published_time.isoformat() if published_time else None
            }

            articles.append(article)

        except Exception as e:
            print(f"Error processing article entry: {e}")
            continue

    return articles


def strip_html_tags(html_content: str) -> str:
    """Remove HTML tags from content, keeping text.

    Args:
        html_content: HTML content to clean.

    Returns:
        Plain text content.
    """
    import re

    if not html_content:
        return ''

    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', html_content)

    # Normalize whitespace
    clean = re.sub(r'\s+', ' ', clean).strip()

    return clean


def ingest_all_feeds(
    config_path: str = "config/feeds.yml",
    delay_between_feeds: float = 1.0,
    hours_back: int = 24,
    max_articles_per_feed: int = 50
) -> Dict[str, Any]:
    """Ingest articles from all configured feeds with intelligent filtering.

    Args:
        config_path: Path to the feeds configuration file.
        delay_between_feeds: Delay in seconds between fetching feeds
                            to be respectful to feed providers.
        hours_back: Only include articles published within this many hours.
        max_articles_per_feed: Maximum articles to process from each feed.

    Returns:
        Dictionary with ingestion statistics.
    """
    # Load feed configuration
    feeds = load_feeds_config(config_path)

    if not feeds:
        print("No feeds found in configuration")
        return {
            'total_feeds': 0,
            'successful_feeds': 0,
            'failed_feeds': 0,
            'total_articles': 0,
            'new_articles': 0
        }

    # Ensure feeds are in the database
    add_feeds_to_database(feeds)

    # Get current feed sources from database
    sources = database.get_all_sources()
    source_by_url = {source['url']: source for source in sources}

    stats = {
        'total_feeds': len(feeds),
        'successful_feeds': 0,
        'failed_feeds': 0,
        'total_articles': 0,
        'new_articles': 0
    }

    for feed in feeds:
        print(f"Processing feed: {feed['name']}")

        # Get source ID from database
        source = source_by_url.get(feed['url'])
        if not source:
            print(f"Warning: Source not found in database: {feed['url']}")
            stats['failed_feeds'] += 1
            continue

        # Fetch feed
        feed_data = fetch_feed(feed['url'])

        if not feed_data:
            print(f"Failed to fetch feed: {feed['name']}")
            stats['failed_feeds'] += 1
            continue

        # Extract articles with time and quantity filtering
        articles = extract_articles_from_feed(feed_data, source['id'], hours_back)

        # Limit articles per feed to prevent overload
        if len(articles) > max_articles_per_feed:
            articles = articles[:max_articles_per_feed]
            print(f"Limited to {max_articles_per_feed} most recent articles from {feed['name']}")

        if not articles:
            print(f"No recent articles found in feed: {feed['name']} (last {hours_back} hours)")
            stats['successful_feeds'] += 1
            continue

        print(f"Found {len(articles)} recent articles in {feed['name']} (last {hours_back} hours)")

        # Add articles to database
        before_count = len(database.get_articles_by_status('fetched'))
        database.add_articles(articles)
        after_count = len(database.get_articles_by_status('fetched'))

        new_articles_count = after_count - before_count
        stats['total_articles'] += len(articles)
        stats['new_articles'] += new_articles_count

        print(f"Added {new_articles_count} new articles from {feed['name']}")

        # Update source last_fetched timestamp
        database.update_source_last_fetched(source['id'])

        stats['successful_feeds'] += 1

        # Be respectful to feed providers
        if delay_between_feeds > 0:
            time.sleep(delay_between_feeds)

    print("\nIngestion complete:")
    print(f"  Total feeds: {stats['total_feeds']}")
    print(f"  Successful: {stats['successful_feeds']}")
    print(f"  Failed: {stats['failed_feeds']}")
    print(f"  Total articles found: {stats['total_articles']}")
    print(f"  New articles added: {stats['new_articles']}")

    return stats


def ingest_single_feed(feed_url: str, source_name: str = "") -> Dict[str, Any]:
    """Ingest articles from a single feed.

    Args:
        feed_url: URL of the feed to ingest.
        source_name: Optional name for the source.

    Returns:
        Dictionary with ingestion statistics.
    """
    # Add/update source in database
    if not source_name:
        source_name = feed_url

    source_id = database.add_source(source_name, feed_url)

    # Fetch feed
    feed_data = fetch_feed(feed_url)

    if not feed_data:
        return {
            'successful': False,
            'articles_found': 0,
            'new_articles': 0,
            'error': 'Failed to fetch feed'
        }

    # Extract articles
    articles = extract_articles_from_feed(feed_data, source_id)

    if not articles:
        return {
            'successful': True,
            'articles_found': 0,
            'new_articles': 0,
            'error': None
        }

    # Add articles to database
    before_count = len(database.get_articles_by_status('fetched'))
    database.add_articles(articles)
    after_count = len(database.get_articles_by_status('fetched'))

    new_articles_count = after_count - before_count

    # Update source last_fetched timestamp
    database.update_source_last_fetched(source_id)

    return {
        'successful': True,
        'articles_found': len(articles),
        'new_articles': new_articles_count,
        'error': None
    }


def validate_feed_url(feed_url: str) -> bool:
    """Validate if a URL is accessible and contains a valid feed.

    Args:
        feed_url: URL to validate.

    Returns:
        True if the URL contains a valid feed, False otherwise.
    """
    feed_data = fetch_feed(feed_url)

    if not feed_data:
        return False

    # Check if feed has required elements
    if not hasattr(feed_data, 'entries') or not feed_data.entries:
        return False

    # Check if at least one entry has a title and link
    for entry in feed_data.entries[:3]:  # Check first 3 entries
        if (entry.get('title') and entry.get('link')):
            return True

    return False


if __name__ == "__main__":
    # Initialize database
    database.initialize_database()

    # Run ingestion
    stats = ingest_all_feeds()

    if stats['new_articles'] > 0:
        print(f"\n✅ Successfully ingested {stats['new_articles']} new articles")
    else:
        print("\nℹ️ No new articles found")