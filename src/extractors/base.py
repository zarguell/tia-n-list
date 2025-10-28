"""Base extractor class for website-specific content extraction.

This module provides the abstract interface that all website-specific
extractors must implement, ensuring consistency across different sites.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from urllib.parse import urlparse


class BaseExtractor(ABC):
    """Abstract base class for website-specific content extractors."""

    def __init__(self):
        """Initialize the extractor."""
        self.name = self.__class__.__name__
        self.supported_domains = self.get_supported_domains()

    @abstractmethod
    def get_supported_domains(self) -> list[str]:
        """Return list of domains this extractor supports.

        Returns:
            List of domain names (e.g., ['threatpost.com', 'www.threatpost.com']).
        """
        pass

    @abstractmethod
    def extract_content(self, url: str, html_content: str) -> Optional[str]:
        """Extract main content from HTML.

        Args:
            url: The URL of the article.
            html_content: Raw HTML content from the URL.

        Returns:
            Extracted main content or None if extraction failed.
        """
        pass

    def can_handle(self, url: str) -> bool:
        """Check if this extractor can handle the given URL.

        Args:
            url: URL to check.

        Returns:
            True if this extractor can handle the URL, False otherwise.
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            return domain in self.supported_domains
        except Exception:
            return False

    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata about this extractor.

        Returns:
            Dictionary containing extractor metadata.
        """
        return {
            'name': self.name,
            'supported_domains': self.supported_domains,
            'description': self.__doc__ or "No description available"
        }

    def clean_text(self, text: str) -> str:
        """Clean extracted text.

        Args:
            text: Raw text to clean.

        Returns:
            Cleaned text.
        """
        if not text:
            return ""

        # Remove excessive whitespace
        text = ' '.join(text.split())

        # Remove common unwanted patterns
        unwanted_patterns = [
            'Click here to read more',
            'Read the full article',
            'Subscribe to our newsletter',
            'Follow us on',
            'Share this article',
            'Related articles',
            'Tags:',
            'Category:',
            'Author:',
            'Published:',
        ]

        for pattern in unwanted_patterns:
            text = text.replace(pattern, '')

        return text.strip()

    def validate_content(self, content: str, min_length: int = 200) -> bool:
        """Validate that extracted content meets minimum quality standards.

        Args:
            content: Extracted content to validate.
            min_length: Minimum character length for valid content.

        Returns:
            True if content is valid, False otherwise.
        """
        if not content or len(content) < min_length:
            return False

        # Check for content quality indicators
        quality_indicators = [
            len(content.split()) > 50,  # At least 50 words
            not content.lower().startswith('404'),  # Not an error page
            not content.lower().startswith('page not found'),
            'subscribe' not in content.lower()[:100],  # Not paywalled immediately
        ]

        return all(quality_indicators)