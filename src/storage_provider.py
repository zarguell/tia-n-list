"""Storage provider abstraction for Tia N. List project.

This module provides a unified interface for different storage backends,
enabling the system to use SQLite, JSON, or other storage mechanisms
interchangeably through a common API.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date
from pathlib import Path


class StorageProvider(ABC):
    """Abstract base class for storage providers.

    This class defines the unified interface that all storage providers
    must implement, ensuring compatibility across different storage
    backends (SQLite, JSON, etc.).
    """

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the storage provider.

        This method should set up any necessary directories, databases,
        or other infrastructure required by the storage backend.
        """
        pass

    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about stored data.

        Returns:
            Dictionary containing statistics about sources, articles,
            IOCs, and other stored data.
        """
        pass

    # Source Management Methods
    @abstractmethod
    def add_source(self, name: str, url: str, **metadata) -> str:
        """Add a new RSS source configuration.

        Args:
            name: Human-readable name of the source.
            url: RSS/Atom feed URL.
            **metadata: Additional source metadata.

        Returns:
            Unique source identifier.
        """
        pass

    @abstractmethod
    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get source configuration by ID.

        Args:
            source_id: Unique source identifier.

        Returns:
            Source configuration dictionary or None if not found.
        """
        pass

    @abstractmethod
    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all configured sources.

        Returns:
            List of source configuration dictionaries.
        """
        pass

    @abstractmethod
    def update_source(self, source_id: str, **updates) -> bool:
        """Update source configuration.

        Args:
            source_id: Unique source identifier.
            **updates: Fields to update.

        Returns:
            True if update was successful, False otherwise.
        """
        pass

    # Article Management Methods
    @abstractmethod
    def add_article(self, source_id: str, guid: str, title: str, url: str,
                   published_at: datetime, raw_content: str = None, **metadata) -> str:
        """Add a new article to storage.

        Args:
            source_id: ID of the source the article came from.
            guid: Article GUID from the feed.
            title: Article title.
            url: Article URL.
            published_at: Publication datetime.
            raw_content: Raw RSS content.
            **metadata: Additional article metadata.

        Returns:
            Unique article identifier.
        """
        pass

    @abstractmethod
    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get article by ID.

        Args:
            article_id: Unique article identifier.

        Returns:
            Article data dictionary or None if not found.
        """
        pass

    @abstractmethod
    def get_articles_by_source(self, source_id: str, limit: int = None,
                              status: str = None) -> List[Dict[str, Any]]:
        """Get articles from a specific source.

        Args:
            source_id: ID of the source.
            limit: Maximum number of articles to return.
            status: Filter by article status.

        Returns:
            List of article data dictionaries.
        """
        pass

    @abstractmethod
    def get_recent_articles(self, days: int = 7, status: str = "processed",
                           limit: int = None) -> List[Dict[str, Any]]:
        """Get recent articles within the specified date range.

        Args:
            days: Number of days to look back.
            status: Filter by article status.
            limit: Maximum number of articles to return.

        Returns:
            List of article data dictionaries.
        """
        pass

    @abstractmethod
    def get_articles_by_date_range(self, start_date: date, end_date: date = None,
                                  status: str = None) -> List[Dict[str, Any]]:
        """Get articles within a specific date range.

        Args:
            start_date: Start date of range.
            end_date: End date of range (optional).
            status: Filter by article status.

        Returns:
            List of article data dictionaries.
        """
        pass

    @abstractmethod
    def update_article(self, article_id: str, **updates) -> bool:
        """Update article data.

        Args:
            article_id: Unique article identifier.
            **updates: Fields to update.

        Returns:
            True if update was successful, False otherwise.
        """
        pass

    @abstractmethod
    def enhance_article_content(self, article_id: str, full_content: str,
                              fetch_method: str) -> bool:
        """Enhance article with full scraped content.

        Args:
            article_id: Unique article identifier.
            full_content: Full scraped content.
            fetch_method: Method used to fetch content.

        Returns:
            True if enhancement was successful, False otherwise.
        """
        pass

    @abstractmethod
    def process_article(self, article_id: str, processed_content: str,
                       analysis: Dict[str, Any], iocs: List[Dict[str, Any]],
                       processing_metadata: Dict[str, Any]) -> bool:
        """Mark article as processed with analysis results.

        Args:
            article_id: Unique article identifier.
            processed_content: Processed article content.
            analysis: Article analysis results.
            iocs: Extracted IOCs.
            processing_metadata: Processing metadata.

        Returns:
            True if processing was successful, False otherwise.
        """
        pass

    # IOC Management Methods
    @abstractmethod
    def save_iocs_for_date(self, process_date: date, article_id: str,
                          iocs: List[Dict[str, Any]]) -> bool:
        """Save IOCs for a specific date.

        Args:
            process_date: Date of processing.
            article_id: Article ID IOCs were extracted from.
            iocs: List of IOC data.

        Returns:
            True if save was successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_iocs_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get all IOCs extracted on a specific date.

        Args:
            target_date: Date to get IOCs for.

        Returns:
            List of IOC data dictionaries.
        """
        pass

    @abstractmethod
    def get_recent_iocs(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get IOCs from the last N days.

        Args:
            days: Number of days to look back.

        Returns:
            List of IOC data dictionaries.
        """
        pass

    @abstractmethod
    def get_article_iocs(self, article_id: str) -> List[Dict[str, Any]]:
        """Get all IOCs for a specific article.

        Args:
            article_id: Unique article identifier.

        Returns:
            List of IOC data dictionaries.
        """
        pass

    # Utility Methods
    @abstractmethod
    def get_unprocessed_articles(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get articles that haven't been processed yet.

        Args:
            limit: Maximum number of articles to return.

        Returns:
            List of article data dictionaries.
        """
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check the health of the storage provider.

        Returns:
            Dictionary containing health status information.
        """
        pass