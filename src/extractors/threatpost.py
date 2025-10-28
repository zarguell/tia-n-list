"""Threatpost-specific content extractor.

This module handles content extraction from Threatpost articles,
focusing on the main article content while removing ads and navigation.
"""

from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseExtractor


class ThreatpostExtractor(BaseExtractor):
    """Extractor for Threatpost articles."""

    def get_supported_domains(self) -> list[str]:
        """Return domains supported by this extractor."""
        return [
            'threatpost.com',
            'www.threatpost.com'
        ]

    def extract_content(self, url: str, html_content: str) -> Optional[str]:
        """Extract main article content from Threatpost HTML.

        Args:
            url: The URL of the Threatpost article.
            html_content: Raw HTML content from the URL.

        Returns:
            Extracted main content or None if extraction failed.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove unwanted elements
            self._remove_unwanted_elements(soup)

            # Try primary content selectors
            content = self._extract_primary_content(soup)
            if content and self.validate_content(content):
                return self.clean_text(content)

            # Try fallback selectors
            content = self._extract_fallback_content(soup)
            if content and self.validate_content(content):
                return self.clean_text(content)

            return None

        except Exception as e:
            print(f"Threatpost extraction failed for {url}: {e}")
            return None

    def _remove_unwanted_elements(self, soup: BeautifulSoup) -> None:
        """Remove unwanted elements from the HTML.

        Args:
            soup: BeautifulSoup object to clean.
        """
        # Remove common unwanted elements
        unwanted_selectors = [
            'script', 'style', 'nav', 'header', 'footer', 'aside',
            '.advertisement', '.ads', '.sidebar', '.newsletter',
            '.social-share', '.related-posts', '.comments',
            '.author-bio', '.tags', '.categories', '.metadata'
        ]

        for selector in unwanted_selectors:
            for element in soup.select(selector):
                element.decompose()

        # Remove Threatpost-specific unwanted elements
        threatpost_unwanted = [
            '.entry-utility', '.post-meta', '.byline',
            '.featured-image', '.thumbnail', '.caption'
        ]

        for selector in threatpost_unwanted:
            for element in soup.select(selector):
                element.decompose()

    def _extract_primary_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract content using primary selectors.

        Args:
            soup: BeautifulSoup object to extract from.

        Returns:
            Extracted content or None.
        """
        # Threatpost-specific selectors
        primary_selectors = [
            '.entry-content',
            '.post-content',
            '.article-content',
            '.content-area',
            'article .content',
            '.post-body'
        ]

        for selector in primary_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                text = content_element.get_text(separator='\n', strip=True)
                if len(text) > 200:
                    return text

        return None

    def _extract_fallback_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract content using fallback selectors.

        Args:
            soup: BeautifulSoup object to extract from.

        Returns:
            Extracted content or None.
        """
        # More generic selectors
        fallback_selectors = [
            'main article',
            'article',
            '.main-content',
            '#content',
            '.content',
            'main'
        ]

        for selector in fallback_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                text = content_element.get_text(separator='\n', strip=True)
                if len(text) > 500:  # Higher threshold for generic selectors
                    return text

        return None