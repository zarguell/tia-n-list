"""Unified feed ingestion module for Tia N. List project.

This module handles fetching and parsing RSS/Atom feeds from various
threat intelligence sources, using the storage provider abstraction
to support multiple storage backends.
"""

import feedparser
import requests
from typing import List, Dict, Any, Optional
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider


class UnifiedIngestion:
    """Unified feed ingestion system using storage provider abstraction."""

    def __init__(self, storage: StorageProvider = None):
        """Initialize ingestion with storage provider backend."""
        self.storage = storage or get_default_storage_provider()

    def fetch_feed(self, feed_url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
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

    def extract_articles_from_feed(self, feed_data: Dict[str, Any], source_id: str,
                                 hours_back: int = 24, max_articles: int = 50) -> List[Dict[str, Any]]:
        """Extract articles from parsed feed data with time filtering.

        Args:
            feed_data: Parsed feed data from feedparser.
            source_id: Storage ID of the feed source.
            hours_back: Only include articles published within this many hours.
            max_articles: Maximum number of articles to extract.

        Returns:
            List of article dictionaries ready for storage.
        """
        # Calculate cutoff time
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours_back)
        articles = []

        for entry in feed_data.entries:
            try:
                if len(articles) >= max_articles:
                    break

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
                        published_time = datetime(*time_struct[:6], tzinfo=timezone.utc)
                        break

                # Skip articles older than cutoff time
                if published_time and published_time < cutoff_time:
                    continue

                # If no publication time, use current time to avoid missing recent articles
                if not published_time:
                    published_time = datetime.now(timezone.utc)

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
                content = self._strip_html_tags(content)

                article_data = {
                    'source_id': source_id,
                    'guid': guid,
                    'title': title,
                    'url': link,
                    'raw_content': content,
                    'published_at': published_time
                }

                articles.append(article_data)

            except Exception as e:
                print(f"Error processing article entry: {e}")
                continue

        return articles

    def ingest_from_sources(self, source_ids: List[str] = None,
                           delay_between_feeds: float = 1.0,
                           hours_back: int = 24,
                           max_articles_per_feed: int = 50) -> Dict[str, Any]:
        """Ingest articles from specified sources.

        Args:
            source_ids: List of source IDs to process. If None, process all active sources.
            delay_between_feeds: Delay in seconds between fetching feeds.
            hours_back: Only include articles published within this many hours.
            max_articles_per_feed: Maximum articles to process from each feed.

        Returns:
            Dictionary with ingestion statistics.
        """
        # Get sources to process
        if source_ids is None:
            sources = self.storage.get_all_sources()
            source_ids = [s['id'] for s in sources if s.get('active', True)]

        stats = {
            'total_sources': len(source_ids),
            'successful_sources': 0,
            'failed_sources': 0,
            'total_articles': 0,
            'new_articles': 0,
            'processed_sources': []
        }

        print(f"Starting ingestion from {len(source_ids)} sources...")

        for source_id in source_ids:
            print(f"\nProcessing source: {source_id}")

            # Get source configuration
            source = self.storage.get_source(source_id)
            if not source:
                print(f"Warning: Source not found: {source_id}")
                stats['failed_sources'] += 1
                continue

            # Check if we should fetch this source (rate limiting)
            if not self._should_fetch_source(source):
                print(f"Skipping {source_id} - fetched recently")
                continue

            # Fetch feed
            feed_data = self.fetch_feed(source['url'])

            if not feed_data:
                print(f"Failed to fetch feed: {source_id}")
                stats['failed_sources'] += 1
                continue

            # Extract articles
            articles = self.extract_articles_from_feed(
                feed_data=feed_data,
                source_id=source_id,
                hours_back=hours_back,
                max_articles=max_articles_per_feed
            )

            print(f"Extracted {len(articles)} articles from {source_id}")

            # Store articles
            new_count = 0
            for article_data in articles:
                article_id = self.storage.add_article(
                    source_id=article_data['source_id'],
                    guid=article_data['guid'],
                    title=article_data['title'],
                    url=article_data['url'],
                    published_at=article_data['published_at'],
                    raw_content=article_data['raw_content']
                )
                if article_id:
                    new_count += 1

            # Update source's last fetched time
            self.storage.update_source(
                source_id,
                last_fetched=datetime.now(timezone.utc).isoformat() + "Z"
            )

            stats['total_articles'] += len(articles)
            stats['new_articles'] += new_count
            stats['successful_sources'] += 1

            stats['processed_sources'].append({
                'source_id': source_id,
                'source_name': source['name'],
                'articles_extracted': len(articles),
                'articles_added': new_count
            })

            # Respectful delay between feeds
            if delay_between_feeds > 0 and source_id != source_ids[-1]:
                time.sleep(delay_between_feeds)

        print(f"\nIngestion completed:")
        print(f"  Sources processed: {stats['successful_sources']}/{stats['total_sources']}")
        print(f"  Total articles found: {stats['total_articles']}")
        print(f"  New articles added: {stats['new_articles']}")

        return stats

    def ingest_single_source(self, source_id: str, hours_back: int = 24,
                           max_articles: int = 50) -> Dict[str, Any]:
        """Ingest articles from a single source.

        Args:
            source_id: ID of the source to process.
            hours_back: Only include articles published within this many hours.
            max_articles: Maximum articles to process.

        Returns:
            Dictionary with ingestion statistics for this source.
        """
        source = self.storage.get_source(source_id)
        if not source:
            return {
                'source_id': source_id,
                'success': False,
                'error': 'Source not found'
            }

        print(f"Processing single source: {source['name']} ({source_id})")

        # Check rate limiting
        if not self._should_fetch_source(source):
            return {
                'source_id': source_id,
                'success': False,
                'error': 'Source fetched too recently'
            }

        # Fetch and process
        feed_data = self.fetch_feed(source['url'])
        if not feed_data:
            return {
                'source_id': source_id,
                'success': False,
                'error': 'Failed to fetch feed'
            }

        articles = self.extract_articles_from_feed(
            feed_data=feed_data,
            source_id=source_id,
            hours_back=hours_back,
            max_articles=max_articles
        )

        # Store articles
        new_count = 0
        for article_data in articles:
            article_id = self.storage.add_article(
                source_id=article_data['source_id'],
                guid=article_data['guid'],
                title=article_data['title'],
                url=article_data['url'],
                published_at=article_data['published_at'],
                raw_content=article_data['raw_content']
            )
            if article_id:
                new_count += 1

        # Update source
        self.storage.update_source(
            source_id,
            last_fetched=datetime.now(timezone.utc).isoformat() + "Z"
        )

        result = {
            'source_id': source_id,
            'source_name': source['name'],
            'success': True,
            'articles_extracted': len(articles),
            'articles_added': new_count
        }

        print(f"Single source ingestion completed: {result}")
        return result

    def _should_fetch_source(self, source: Dict[str, Any]) -> bool:
        """Check if a source should be fetched based on rate limiting."""
        last_fetched = source.get('last_fetched')
        if not last_fetched:
            return True

        try:
            last_fetch_time = datetime.fromisoformat(last_fetched.replace('Z', '+00:00'))
            interval_hours = source.get('fetch_interval_hours', 1)
            next_fetch_time = last_fetch_time + timedelta(hours=interval_hours)

            return datetime.now(timezone.utc) >= next_fetch_time
        except Exception:
            # If we can't parse the time, allow fetching
            return True

    def _strip_html_tags(self, html_content: str) -> str:
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

    def get_ingestion_statistics(self) -> Dict[str, Any]:
        """Get current ingestion statistics."""
        return self.storage.get_statistics()

    def health_check(self) -> Dict[str, Any]:
        """Check the health of the ingestion system."""
        health = {
            "status": "healthy",
            "checks": {},
            "issues": []
        }

        try:
            # Check storage health
            storage_health = self.storage.health_check()
            health["checks"]["storage"] = storage_health["status"] == "healthy"

            if storage_health["status"] != "healthy":
                health["status"] = "degraded"
                health["issues"].extend(storage_health.get("issues", []))

            # Check if we can access sources
            sources = self.storage.get_all_sources()
            health["checks"]["source_access"] = True
            health["source_count"] = len(sources)

            # Test network connectivity (optional)
            try:
                response = requests.get("https://httpbin.org/get", timeout=5)
                health["checks"]["network"] = response.status_code == 200
            except Exception:
                health["checks"]["network"] = False
                health["status"] = "degraded"
                health["issues"].append("Network connectivity check failed")

        except Exception as e:
            health["status"] = "unhealthy"
            health["issues"].append(f"Health check failed: {e}")

        return health


# Global ingestion instance
unified_ingestion = UnifiedIngestion()


def main():
    """Main function for standalone execution."""
    print("Starting unified feed ingestion...")

    stats = unified_ingestion.ingest_from_sources(
        delay_between_feeds=2.0,
        hours_back=24,
        max_articles_per_feed=50
    )

    print("\n=== INGESTION SUMMARY ===")
    print(f"Sources processed: {stats['successful_sources']}/{stats['total_sources']}")
    print(f"Total articles found: {stats['total_articles']}")
    print(f"New articles added: {stats['new_articles']}")
    print(f"Failed sources: {stats['failed_sources']}")

    if stats['failed_sources'] > 0:
        print("\nFailed sources:")
        for source_stat in stats['processed_sources']:
            if source_stat['articles_extracted'] == 0:
                print(f"  - {source_stat['source_id']}: No articles extracted")


if __name__ == "__main__":
    main()