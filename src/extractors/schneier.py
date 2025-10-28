"""Schneier on Security-specific content extractor.

This module handles content extraction from Bruce Schneier's blog,
focusing on the main post content while preserving his writing style.
"""

from typing import Optional
from bs4 import BeautifulSoup
from .base import BaseExtractor


class SchneierExtractor(BaseExtractor):
    """Extractor for Schneier on Security articles."""

    def get_supported_domains(self) -> list[str]:
        """Return domains supported by this extractor."""
        return [
            'schneier.com',
            'www.schneier.com'
        ]

    def extract_content(self, url: str, html_content: str) -> Optional[str]:
        """Extract main article content from Schneier HTML.

        Args:
            url: The URL of the Schneier article.
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
            print(f"Schneier extraction failed for {url}: {e}")
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

        # Remove Schneier-specific unwanted elements
        schneier_unwanted = [
            '.entry-meta', '.post-meta', '.byline',
            '.navigation', '.menu', '.widget',
            '.syndication', '.feed-link'
        ]

        for selector in schneier_unwanted:
            for element in soup.select(selector):
                element.decompose()

    def _extract_primary_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract content using primary selectors.

        Args:
            soup: BeautifulSoup object to extract from.

        Returns:
            Extracted content or None.
        """
        # Schneier-specific selectors
        primary_selectors = [
            '.entry-content',
            '.post-content',
            '.entry-body',
            '#main .post',
            '.hentry .entry-content'
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