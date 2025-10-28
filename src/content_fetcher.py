"""Content fetcher module for Tia N. List project.

This module handles fetching full article content from URLs when RSS feeds
only provide partial content. Implements respectful scraping practices.
"""

import time
import random
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import trafilatura
from trafilatura import fetch_url, extract
from .extractors import get_extractor_for_url


class ContentFetchError(Exception):
    """Custom exception for content fetching errors."""
    pass


class ContentFetcher:
    """Handles fetching and extracting article content from URLs."""

    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """Initialize the content fetcher.

        Args:
            min_delay: Minimum delay between requests in seconds.
            max_delay: Maximum delay between requests in seconds.
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = 0

        # Configure respectful headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Tia N. List Threat Intelligence Bot (contact for inquiries)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def _rate_limit(self) -> None:
        """Apply rate limiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        delay = random.uniform(self.min_delay, self.max_delay)

        if time_since_last < delay:
            sleep_time = delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid for content fetching.

        Args:
            url: URL to validate.

        Returns:
            True if URL is valid, False otherwise.
        """
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme) and parsed.scheme in ['http', 'https']
        except Exception:
            return False

    def _detect_paywall(self, html_content: str) -> bool:
        """Detect if content is behind a paywall.

        Args:
            html_content: HTML content to analyze.

        Returns:
            True if paywall detected, False otherwise.
        """
        paywall_indicators = [
            'subscribe', 'premium', 'paywall', 'subscription required',
            'limited free articles', 'create an account', 'sign in',
            'upgrade to premium', 'members only'
        ]

        content_lower = html_content.lower()
        return any(indicator in content_lower for indicator in paywall_indicators)

    def _extract_with_trafilatura(self, url: str) -> Optional[str]:
        """Extract content using Trafilatura library.

        Args:
            url: URL to extract content from.

        Returns:
            Extracted content or None if extraction failed.
        """
        try:
            downloaded = fetch_url(url)
            if downloaded is None:
                return None

            result = extract(downloaded, include_comments=False, include_formatting=False)
            if result and len(result.strip()) > 100:  # Minimum content length
                return result.strip()

        except Exception as e:
            print(f"Trafilatura extraction failed for {url}: {e}")

        return None

    def _extract_with_website_specific(self, url: str) -> Optional[str]:
        """Extract content using website-specific extractors.

        Args:
            url: URL to extract content from.

        Returns:
            Extracted content or None if extraction failed.
        """
        try:
            # Get appropriate extractor for this URL
            extractor = get_extractor_for_url(url)
            if not extractor:
                return None

            # Fetch HTML content
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # Use website-specific extraction
            content = extractor.extract_content(url, response.text)
            return content

        except Exception as e:
            print(f"Website-specific extraction failed for {url}: {e}")
            return None

    def _extract_with_beautifulsoup(self, url: str) -> Optional[str]:
        """Extract content using BeautifulSoup as fallback.

        Args:
            url: URL to extract content from.

        Returns:
            Extracted content or None if extraction failed.
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'ads']):
                element.decompose()

            # Try common content selectors
            content_selectors = [
                'article', '.content', '.post-content', '.entry-content',
                '.article-body', '.story-body', '.main-content', '#content'
            ]

            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    text = content_element.get_text(strip=True)
                    if len(text) > 200:  # Minimum content length
                        return text

            # Fallback to main content area
            if soup.body:
                text = soup.body.get_text(strip=True)
                if len(text) > 500:  # Higher threshold for body content
                    return text

        except Exception as e:
            print(f"BeautifulSoup extraction failed for {url}: {e}")

        return None

    def fetch_content(self, url: str) -> Dict[str, Any]:
        """Fetch full article content from URL.

        Args:
            url: URL to fetch content from.

        Returns:
            Dictionary containing:
            - content: Extracted content (str or None)
            - method: Extraction method used ('trafilatura', 'beautifulsoup', or None)
            - success: Boolean indicating if extraction was successful
            - error: Error message if extraction failed
            - paywall_detected: Boolean if paywall was detected
        """
        result = {
            'content': None,
            'method': None,
            'success': False,
            'error': None,
            'paywall_detected': False
        }

        # Validate URL
        if not self._is_valid_url(url):
            result['error'] = "Invalid URL"
            return result

        # Apply rate limiting
        self._rate_limit()

        try:
            # Try website-specific extractors first (highest quality)
            content = self._extract_with_website_specific(url)
            if content:
                result.update({
                    'content': content,
                    'method': 'website_specific',
                    'success': True
                })
                return result

            # Try Trafilatura second (good for news articles)
            content = self._extract_with_trafilatura(url)
            if content:
                result.update({
                    'content': content,
                    'method': 'trafilatura',
                    'success': True
                })
                return result

            # Fallback to BeautifulSoup
            content = self._extract_with_beautifulsoup(url)
            if content:
                result.update({
                    'content': content,
                    'method': 'beautifulsoup',
                    'success': True
                })
                return result

            result['error'] = "No content could be extracted"

        except requests.exceptions.RequestException as e:
            result['error'] = f"Request failed: {str(e)}"
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"

        return result

    def test_extraction(self, url: str) -> Dict[str, Any]:
        """Test content extraction with detailed diagnostics.

        Args:
            url: URL to test extraction on.

        Returns:
            Detailed result including diagnostics.
        """
        result = self.fetch_content(url)

        # Add diagnostics
        if result['success']:
            content = result['content']
            result.update({
                'content_length': len(content),
                'word_count': len(content.split()),
                'estimated_reading_time': len(content.split()) // 200  # 200 WPM average
            })

        return result


# Global instance for reuse
_content_fetcher = None


def get_content_fetcher() -> ContentFetcher:
    """Get or create a global content fetcher instance.

    Returns:
        ContentFetcher instance.
    """
    global _content_fetcher
    if _content_fetcher is None:
        _content_fetcher = ContentFetcher()
    return _content_fetcher


def fetch_article_content(url: str) -> Dict[str, Any]:
    """Convenience function to fetch article content.

    Args:
        url: URL to fetch content from.

    Returns:
        Dictionary with extraction results.
    """
    fetcher = get_content_fetcher()
    return fetcher.fetch_content(url)