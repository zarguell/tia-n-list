#!/usr/bin/env python3
"""
RSS Feed Importer Script

This script extracts RSS feed URLs from text files, validates them, gets feed names dynamically,
and adds them to the ./data/sources/ directory.

Usage:
    # From a text file with mixed content
    python scripts/add_feeds.py --file feeds.txt

    # From direct URLs
    python scripts/add_feeds.py --url "https://example.com/feed.xml" --url "https://another.com/feed"

    # From clipboard (pasted content)
    python scripts/add_feeds.py --clipboard

    # Dry run (test without adding)
    python scripts/add_feeds.py --file feeds.txt --dry-run
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import requests
import feedparser
from urllib.parse import urlparse, urljoin

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from json_storage import JSONStorage
except ImportError:
    print("Error: Could not import JSONStorage. Make sure you're running from the project root.")
    sys.exit(1)


class FeedImporter:
    """RSS Feed Importer for adding new sources to the threat intelligence system."""

    def __init__(self, sources_dir: Path = None):
        """Initialize the feed importer.

        Args:
            sources_dir: Path to the sources directory. Defaults to ./data/sources/
        """
        self.sources_dir = sources_dir or Path("data/sources")
        self.sources_dir.mkdir(parents=True, exist_ok=True)
        self.storage = JSONStorage()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Tia-N-List-Feed-Importer/1.0 (https://tia-n-list.com)'
        })

    def extract_urls_from_text(self, text: str) -> List[str]:
        """Extract RSS feed URLs from mixed text content.

        Args:
            text: Text content that may contain RSS URLs

        Returns:
            List of cleaned and valid RSS URLs
        """
        # Pattern to match URLs in quotes or on their own line
        url_patterns = [
            r'"([^"]*(?:feed|rss|atom)[^"]*)"',      # URLs in double quotes
            r"'([^']*(?:feed|rss|atom)[^']*)'",       # URLs in single quotes
            r'(?:^|\s)(https?://[^\s]*(?:feed|rss|atom)[^\s]*)',  # URLs on their own
        ]

        urls = set()

        for pattern in url_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                url = match.strip('\'"')
                if self.is_valid_rss_url(url):
                    urls.add(url)

        return list(urls)

    def is_valid_rss_url(self, url: str) -> bool:
        """Check if a URL appears to be a valid RSS/Atom feed URL.

        Args:
            url: URL to validate

        Returns:
            True if URL appears to be a valid RSS feed
        """
        url = url.strip()

        # Must be HTTP/HTTPS
        if not url.startswith(('http://', 'https://')):
            return False

        # Basic URL validation
        try:
            parsed = urlparse(url)
            if not parsed.netloc or not parsed.path:
                return False
        except Exception:
            return False

        # RSS/Atom indicators in URL
        rss_indicators = [
            'feed', 'rss', 'atom', 'xml',
            '/rss', '/feed', '/atom',
            'rss.xml', 'feed.xml', 'atom.xml'
        ]

        url_lower = url.lower()
        return any(indicator in url_lower for indicator in rss_indicators)

    def clean_url(self, url: str) -> str:
        """Clean and normalize a URL.

        Args:
            url: URL to clean

        Returns:
            Cleaned URL
        """
        url = url.strip()
        url = url.strip('\'"')

        # Remove trailing commas, semicolons, quotes
        url = url.rstrip('.,;\'"')

        # Ensure proper scheme
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url.lstrip('/')

        return url

    def get_feed_info(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Get information about an RSS feed including its name.

        Args:
            url: URL of the RSS feed
            timeout: Request timeout in seconds

        Returns:
            Dictionary with feed information
        """
        print(f"  📡 Fetching feed info: {url}")

        try:
            # Fetch the feed
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()

            # Parse the feed
            feed = feedparser.parse(response.content)

            if feed.bozo and feed.bozo_exception:
                print(f"    ⚠️  Feed has parsing issues: {feed.bozo_exception}")

            # Extract feed information
            feed_info = {
                'url': url,
                'title': self._extract_feed_title(feed, url),
                'description': self._extract_feed_description(feed),
                'language': feed.feed.get('language', 'en') if hasattr(feed, 'feed') else 'en',
                'total_entries': len(feed.entries) if hasattr(feed, 'entries') else 0,
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'validation_status': 'success'
            }

            print(f"    ✅ {feed_info['title']}")
            print(f"    📄 {feed_info['total_entries']} entries")

            return feed_info

        except requests.exceptions.RequestException as e:
            print(f"    ❌ Network error: {e}")
            return {
                'url': url,
                'title': self._generate_title_from_url(url),
                'description': '',
                'language': 'en',
                'total_entries': 0,
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'validation_status': f'network_error: {e}'
            }
        except Exception as e:
            print(f"    ❌ Parsing error: {e}")
            return {
                'url': url,
                'title': self._generate_title_from_url(url),
                'description': '',
                'language': 'en',
                'total_entries': 0,
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'validation_status': f'parsing_error: {e}'
            }

    def _extract_feed_title(self, feed, url: str) -> str:
        """Extract the title from a parsed feed.

        Args:
            feed: Parsed feed object
            url: Original URL (used as fallback)

        Returns:
            Feed title
        """
        if hasattr(feed, 'feed') and feed.feed:
            # Try different title fields
            for field in ['title', 'name', 'description']:
                if hasattr(feed.feed, field) and getattr(feed.feed, field):
                    title = str(getattr(feed.feed, field)).strip()
                    if title and len(title) > 0:
                        # Clean up the title
                        title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove invalid filename chars
                        title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                        return title

        # Fallback to URL-based title
        return self._generate_title_from_url(url)

    def _extract_feed_description(self, feed) -> str:
        """Extract the description from a parsed feed.

        Args:
            feed: Parsed feed object

        Returns:
            Feed description
        """
        if hasattr(feed, 'feed') and feed.feed:
            for field in ['description', 'subtitle', 'summary']:
                if hasattr(feed.feed, field) and getattr(feed.feed, field):
                    desc = str(getattr(feed.feed, field)).strip()
                    if desc and len(desc) > 0:
                        # Limit description length
                        return desc[:200] + ('...' if len(desc) > 200 else '')

        return ''

    def _generate_title_from_url(self, url: str) -> str:
        """Generate a title from the URL when feed parsing fails.

        Args:
            url: URL to generate title from

        Returns:
            Generated title
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')

            # Remove common TLDs and clean up
            domain = re.sub(r'\.(com|org|net|gov|edu|io|co\.\w+)$', '', domain)

            # Convert to title case
            title = domain.replace('-', ' ').replace('_', ' ').title()

            return title

        except Exception:
            return "Unknown Feed"

    def feed_exists(self, url: str) -> bool:
        """Check if a feed already exists in the sources directory.

        Args:
            url: URL to check

        Returns:
            True if feed already exists
        """
        # Check in existing source files
        for source_file in self.sources_dir.glob("*.json"):
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    source = json.load(f)
                    if source.get('url') == url:
                        return True
            except Exception:
                continue

        # Check in database
        try:
            sources = self.storage.get_all_sources()
            return any(source.get('url') == url for source in sources)
        except Exception:
            pass

        return False

    def generate_source_id(self, title: str, url: str) -> str:
        """Generate a unique source ID from title and URL.

        Args:
            title: Feed title
            url: Feed URL

        Returns:
            Unique source ID
        """
        # Clean title for use as ID
        clean_title = re.sub(r'[^a-zA-Z0-9\s-]', '', title.lower())
        clean_title = re.sub(r'\s+', '-', clean_title.strip())

        # Get domain from URL for uniqueness
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '').replace('.', '-')
        except Exception:
            domain = "unknown"

        # Combine title and domain
        base_id = f"{clean_title}-{domain}"

        # Ensure uniqueness
        counter = 1
        source_id = base_id
        while (self.sources_dir / f"{source_id}.json").exists():
            source_id = f"{base_id}-{counter}"
            counter += 1

        return source_id

    def add_feed(self, url: str, dry_run: bool = False) -> Optional[Dict[str, Any]]:
        """Add a single RSS feed to the sources directory.

        Args:
            url: URL of the RSS feed to add
            dry_run: If True, don't actually add the feed

        Returns:
            Dictionary with result information or None if failed
        """
        url = self.clean_url(url)

        if not self.is_valid_rss_url(url):
            print(f"❌ Invalid RSS URL: {url}")
            return None

        if self.feed_exists(url):
            print(f"⚠️  Feed already exists: {url}")
            return {
                'url': url,
                'status': 'exists',
                'message': 'Feed already exists'
            }

        # Get feed information
        feed_info = self.get_feed_info(url)

        if dry_run:
            print(f"🔍 DRY RUN: Would add feed: {feed_info['title']}")
            return {
                'url': url,
                'status': 'dry_run',
                'feed_info': feed_info
            }

        # Generate source ID
        source_id = self.generate_source_id(feed_info['title'], url)

        # Create source data
        source_data = {
            'id': source_id,
            'name': feed_info['title'],
            'url': url,
            'active': True,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'metadata': {
                'language': feed_info['language'],
                'description': feed_info['description'],
                'validation_status': feed_info['validation_status'],
                'total_entries': feed_info['total_entries'],
                'last_checked': feed_info['last_updated'],
                'import_source': 'add_feeds_script'
            }
        }

        # Save to file
        try:
            source_file = self.sources_dir / f"{source_id}.json"
            with open(source_file, 'w', encoding='utf-8') as f:
                json.dump(source_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Added feed: {source_data['name']} -> {source_file}")

            return {
                'url': url,
                'status': 'added',
                'source_id': source_id,
                'source_file': str(source_file),
                'feed_info': feed_info
            }

        except Exception as e:
            print(f"❌ Failed to save feed {url}: {e}")
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }

    def add_feeds_from_text(self, text: str, dry_run: bool = False) -> List[Dict[str, Any]]:
        """Add multiple feeds from text content.

        Args:
            text: Text content containing RSS URLs
            dry_run: If True, don't actually add the feeds

        Returns:
            List of results for each feed
        """
        urls = self.extract_urls_from_text(text)

        if not urls:
            print("No RSS URLs found in the provided text.")
            return []

        print(f"Found {len(urls)} RSS URLs in text:")
        for url in urls:
            print(f"  - {url}")
        print()

        results = []
        for url in urls:
            result = self.add_feed(url, dry_run)
            if result:
                results.append(result)
            time.sleep(1)  # Be respectful to servers

        return results

    def add_feeds_from_file(self, file_path: str, dry_run: bool = False) -> List[Dict[str, Any]]:
        """Add feeds from a text file.

        Args:
            file_path: Path to text file containing RSS URLs
            dry_run: If True, don't actually add the feeds

        Returns:
            List of results for each feed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            print(f"📁 Reading feeds from: {file_path}")
            return self.add_feeds_from_text(content, dry_run)

        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return []
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return []


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Import RSS feeds from text files or direct URLs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From text file with mixed content
  python scripts/add_feeds.py --file feeds.txt

  # From direct URLs
  python scripts/add_feeds.py --url "https://example.com/feed.xml" --url "https://another.com/feed"

  # From clipboard (pasted content)
  python scripts/add_feeds.py --clipboard

  # Dry run to test without adding
  python scripts/add_feeds.py --file feeds.txt --dry-run
        """
    )

    # Input sources
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--file', '-f', help='Text file containing RSS URLs')
    input_group.add_argument('--url', '-u', action='append', help='Direct RSS URL (can be used multiple times)')
    input_group.add_argument('--clipboard', '-c', action='store_true', help='Read RSS URLs from clipboard')

    # Options
    parser.add_argument('--dry-run', '-n', action='store_true', help='Test without actually adding feeds')
    parser.add_argument('--sources-dir', default='data/sources', help='Sources directory path (default: data/sources)')

    args = parser.parse_args()

    # Initialize importer
    importer = FeedImporter(Path(args.sources_dir))

    print("🛡️  Tia N. List - RSS Feed Importer")
    print("=" * 50)

    results = []

    # Process based on input type
    if args.file:
        results = importer.add_feeds_from_file(args.file, args.dry_run)

    elif args.url:
        print(f"📡 Processing {len(args.url)} direct URLs:")
        print()
        for url in args.url:
            result = importer.add_feed(url, args.dry_run)
            if result:
                results.append(result)
            time.sleep(1)

    elif args.clipboard:
        try:
            import pyperclip
            content = pyperclip.paste()
            print("📋 Reading RSS URLs from clipboard:")
            print()
            results = importer.add_feeds_from_text(content, args.dry_run)
        except ImportError:
            print("❌ pyperclip not installed. Install with: pip install pyperclip")
            return
        except Exception as e:
            print(f"❌ Error reading clipboard: {e}")
            return

    # Summary
    print()
    print("📊 Summary:")
    print("=" * 30)

    if not results:
        print("No feeds were processed.")
        return

    # Count by status
    status_counts = {}
    for result in results:
        status = result.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1

    for status, count in status_counts.items():
        icon = {"added": "✅", "exists": "⚠️", "dry_run": "🔍", "error": "❌"}.get(status, "•")
        print(f"{icon} {status.replace('_', ' ').title()}: {count}")

    if args.dry_run:
        print()
        print("🔍 This was a DRY RUN. No feeds were actually added.")
        print("   Run again without --dry-run to add the feeds.")


if __name__ == "__main__":
    main()