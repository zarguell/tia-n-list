"""Website-specific content extractors package.

This package provides modular, extensible content extractors for different
websites. Each extractor is designed to handle the specific HTML structure
and content patterns of a particular site or group of sites.
"""

from typing import Dict, List, Optional, Type
from urllib.parse import urlparse

from .base import BaseExtractor
from .threatpost import ThreatpostExtractor
from .schneier import SchneierExtractor


class ExtractorRegistry:
    """Registry for managing website-specific extractors."""

    def __init__(self):
        """Initialize the extractor registry."""
        self._extractors: Dict[str, Type[BaseExtractor]] = {}
        self._instances: Dict[str, BaseExtractor] = {}
        self._domain_mapping: Dict[str, str] = {}

        # Register built-in extractors
        self.register_builtin_extractors()

    def register_builtin_extractors(self) -> None:
        """Register built-in extractors."""
        self.register('threatpost', ThreatpostExtractor)
        self.register('schneier', SchneierExtractor)

    def register(self, name: str, extractor_class: Type[BaseExtractor]) -> None:
        """Register an extractor class.

        Args:
            name: Name for the extractor.
            extractor_class: Extractor class to register.
        """
        if not issubclass(extractor_class, BaseExtractor):
            raise ValueError(f"Extractor class must inherit from BaseExtractor")

        self._extractors[name] = extractor_class

        # Create instance to get supported domains
        instance = extractor_class()
        self._instances[name] = instance

        # Map domains to extractor names
        for domain in instance.get_supported_domains():
            self._domain_mapping[domain] = name

    def get_extractor_for_url(self, url: str) -> Optional[BaseExtractor]:
        """Get the appropriate extractor for a URL.

        Args:
            url: URL to find extractor for.

        Returns:
            Extractor instance or None if no extractor found.
        """
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            extractor_name = self._domain_mapping.get(domain)
            if extractor_name:
                return self._instances[extractor_name]

        except Exception:
            pass

        return None

    def get_extractor_by_name(self, name: str) -> Optional[BaseExtractor]:
        """Get extractor by name.

        Args:
            name: Name of the extractor.

        Returns:
            Extractor instance or None if not found.
        """
        return self._instances.get(name)

    def list_extractors(self) -> List[Dict]:
        """List all registered extractors.

        Returns:
            List of extractor metadata dictionaries.
        """
        return [instance.get_metadata() for instance in self._instances.values()]

    def can_handle_url(self, url: str) -> bool:
        """Check if any registered extractor can handle the URL.

        Args:
            url: URL to check.

        Returns:
            True if an extractor can handle the URL, False otherwise.
        """
        return self.get_extractor_for_url(url) is not None


# Global registry instance
_registry = None


def get_extractor_registry() -> ExtractorRegistry:
    """Get the global extractor registry.

    Returns:
        ExtractorRegistry instance.
    """
    global _registry
    if _registry is None:
        _registry = ExtractorRegistry()
    return _registry


def get_extractor_for_url(url: str) -> Optional[BaseExtractor]:
    """Get the appropriate extractor for a URL.

    Args:
        url: URL to find extractor for.

    Returns:
        Extractor instance or None if no extractor found.
    """
    registry = get_extractor_registry()
    return registry.get_extractor_for_url(url)


def register_extractor(name: str, extractor_class: Type[BaseExtractor]) -> None:
    """Register a new extractor.

    Args:
        name: Name for the extractor.
        extractor_class: Extractor class to register.
    """
    registry = get_extractor_registry()
    registry.register(name, extractor_class)


# Convenience imports
__all__ = [
    'BaseExtractor',
    'ExtractorRegistry',
    'get_extractor_registry',
    'get_extractor_for_url',
    'register_extractor',
    'ThreatpostExtractor',
    'SchneierExtractor'
]