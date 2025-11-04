"""JSON storage provider implementation for Tia N. List project.

This module implements the StorageProvider interface using JSON files,
providing git-friendly storage that can be easily version controlled
and tracked.
"""

import json
import hashlib
from datetime import datetime, date, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import re

from .storage_provider import StorageProvider


class JSONStorageProvider(StorageProvider):
    """JSON-based storage provider implementing the StorageProvider interface."""

    def __init__(self, data_dir: str = "data"):
        """Initialize JSON storage with data directory."""
        self.data_dir = Path(data_dir)
        self.sources_dir = self.data_dir / "sources"
        self.articles_dir = self.data_dir / "articles"
        self.content_dir = self.data_dir / "content"
        self.processed_dir = self.data_dir / "processed"
        self.reports_dir = self.data_dir / "reports"

    def initialize(self) -> None:
        """Initialize the storage provider."""
        # Ensure directories exist
        for directory in [self.data_dir, self.sources_dir, self.articles_dir,
                         self.content_dir, self.processed_dir, self.reports_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string with robust error handling."""
        if not datetime_str:
            return datetime.now(timezone.utc)

        try:
            # Handle various datetime formats
            if datetime_str.endswith('Z'):
                # ISO format with Z suffix
                return datetime.fromisoformat(datetime_str[:-1] + '+00:00')
            elif '+00:00' in datetime_str and datetime_str.count('+00:00') > 1:
                # Fix double timezone issue
                cleaned = datetime_str.replace('+00:00+00:00', '+00:00')
                return datetime.fromisoformat(cleaned)
            else:
                # Standard ISO format
                return datetime.fromisoformat(datetime_str)
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse datetime '{datetime_str}': {e}")
            return datetime.now(timezone.utc)

    def _generate_article_id(self, source_id: str, title: str, pub_date: datetime) -> str:
        """Generate unique article ID based on source, title hash, and date."""
        title_hash = hashlib.md5(title.encode()).hexdigest()[:8]
        date_str = pub_date.strftime("%Y-%m-%d")
        return f"{source_id}-{date_str}-{title_hash}"

    def _get_article_date_path(self, article_date: datetime) -> Path:
        """Get the directory path for an article based on its date."""
        return self.articles_dir / f"{article_date.year:04d}" / f"{article_date.month:02d}" / f"{article_date.day:02d}"

    def _get_processed_date_path(self, process_date: date) -> Path:
        """Get the directory path for processed data based on date."""
        return self.processed_dir / f"{process_date.year:04d}" / f"{process_date.month:02d}" / f"{process_date.day:02d}"

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about stored data."""
        stats = {
            "sources": {
                "total": 0,
                "active": 0
            },
            "articles": {
                "total": 0,
                "by_status": {},
                "by_source": {},
                "recent_7_days": 0
            },
            "iocs": {
                "total": 0,
                "recent_7_days": 0,
                "by_type": {}
            }
        }

        # Source statistics
        sources = self.get_all_sources()
        stats["sources"]["total"] = len(sources)
        stats["sources"]["active"] = sum(1 for s in sources if s.get("active", True))

        # Article statistics
        for article_file in self.articles_dir.rglob("*.json"):
            with open(article_file, 'r', encoding='utf-8') as f:
                article = json.load(f)

                stats["articles"]["total"] += 1

                status = article.get("status", "unknown")
                stats["articles"]["by_status"][status] = stats["articles"]["by_status"].get(status, 0) + 1

                source_id = article["source_id"]
                stats["articles"]["by_source"][source_id] = stats["articles"]["by_source"].get(source_id, 0) + 1

                # Check if recent
                pub_datetime = self._parse_datetime(article["published_at"])
                if pub_datetime.timestamp() >= (datetime.now(timezone.utc).timestamp() - 7 * 24 * 3600):
                    stats["articles"]["recent_7_days"] += 1

        # IOC statistics
        for ioc_file in self.processed_dir.rglob("iocs.json"):
            with open(ioc_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                iocs = data.get("iocs", [])

                stats["iocs"]["total"] += len(iocs)

                for ioc in iocs:
                    # Check if recent
                    ext_datetime = self._parse_datetime(ioc["extracted_at"])
                    if ext_datetime.timestamp() >= (datetime.now(timezone.utc).timestamp() - 7 * 24 * 3600):
                        stats["iocs"]["recent_7_days"] += 1

                    # Count by type
                    ioc_type = ioc.get("type", "unknown")
                    stats["iocs"]["by_type"][ioc_type] = stats["iocs"]["by_type"].get(ioc_type, 0) + 1

        return stats

    # Source Management Methods
    def add_source(self, name: str, url: str, **metadata) -> str:
        """Add a new RSS source configuration."""
        source_id = name.lower().replace(" ", "-").replace("/", "-")
        source_file = self.sources_dir / f"{source_id}.json"

        source_data = {
            "id": source_id,
            "name": name,
            "url": url,
            "last_fetched": None,
            "fetch_interval_hours": 1,
            "quality_score": 50,  # Default score
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat() + "Z",
            "metadata": metadata
        }

        with open(source_file, 'w', encoding='utf-8') as f:
            json.dump(source_data, f, indent=2, ensure_ascii=False)

        return source_id

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get source configuration by ID."""
        source_file = self.sources_dir / f"{source_id}.json"
        if not source_file.exists():
            return None

        with open(source_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all configured sources."""
        sources = []
        for source_file in self.sources_dir.glob("*.json"):
            with open(source_file, 'r', encoding='utf-8') as f:
                sources.append(json.load(f))
        return sources

    def update_source(self, source_id: str, **updates) -> bool:
        """Update source configuration."""
        source_data = self.get_source(source_id)
        if not source_data:
            return False

        source_data.update(updates)
        source_data["updated_at"] = datetime.now(timezone.utc).isoformat() + "Z"

        source_file = self.sources_dir / f"{source_id}.json"
        with open(source_file, 'w', encoding='utf-8') as f:
            json.dump(source_data, f, indent=2, ensure_ascii=False)

        return True

    # Article Management Methods
    def add_article(self, source_id: str, guid: str, title: str, url: str,
                   published_at: datetime, raw_content: str = None, **metadata) -> str:
        """Add a new article to storage."""
        article_id = self._generate_article_id(source_id, title, published_at)
        article_dir = self._get_article_date_path(published_at)
        article_dir.mkdir(parents=True, exist_ok=True)

        article_file = article_dir / f"{article_id}.json"

        article_data = {
            "id": article_id,
            "source_id": source_id,
            "guid": guid,
            "title": title,
            "url": url,
            "published_at": published_at.isoformat(),
            "fetched_at": datetime.now(timezone.utc).isoformat() + "Z",
            "status": "fetched",
            "content": {
                "raw": raw_content or "",
                "full": "",
                "processed": ""
            },
            "analysis": {
                "score": None,
                "relevance_score": None,
                "threat_category": None,
                "summary": None,
                "key_entities": [],
                "ttps": []
            },
            "content_source": "rss",
            "content_fetch_method": None,
            "processing_metadata": {},
            **metadata
        }

        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=2, ensure_ascii=False)

        return article_id

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get article by ID."""
        # Search for article file by ID across all date directories
        for article_file in self.articles_dir.rglob(f"{article_id}.json"):
            with open(article_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def get_articles_by_source(self, source_id: str, limit: int = None,
                              status: str = None) -> List[Dict[str, Any]]:
        """Get articles from a specific source."""
        articles = []
        for article_file in self.articles_dir.rglob("*.json"):
            with open(article_file, 'r', encoding='utf-8') as f:
                article = json.load(f)
                if article["source_id"] == source_id:
                    if status is None or article.get("status") == status:
                        articles.append(article)
                        if limit and len(articles) >= limit:
                            break

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x["published_at"], reverse=True)
        return articles[:limit] if limit else articles

    def get_recent_articles(self, days: int = 7, status: str = "processed",
                           limit: int = None) -> List[Dict[str, Any]]:
        """Get recent articles within the specified date range."""
        articles = []
        cutoff_date = datetime.now(timezone.utc).timestamp() - (days * 24 * 3600)

        for article_file in self.articles_dir.rglob("*.json"):
            with open(article_file, 'r', encoding='utf-8') as f:
                article = json.load(f)
                if status is None or article.get("status") == status:
                    pub_datetime = self._parse_datetime(article["published_at"])
                    if pub_datetime.timestamp() >= cutoff_date:
                        articles.append(article)

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x["published_at"], reverse=True)
        return articles[:limit] if limit else articles

    def get_articles_by_date_range(self, start_date: date, end_date: date = None,
                                  status: str = None) -> List[Dict[str, Any]]:
        """Get articles within a specific date range."""
        if end_date is None:
            end_date = start_date

        articles = []
        current_date = start_date

        while current_date <= end_date:
            date_path = self.articles_dir / f"{current_date.year:04d}" / f"{current_date.month:02d}" / f"{current_date.day:02d}"
            if date_path.exists():
                for article_file in date_path.glob("*.json"):
                    with open(article_file, 'r', encoding='utf-8') as f:
                        article = json.load(f)
                        if status is None or article.get("status") == status:
                            articles.append(article)

            current_date = date.fromordinal(current_date.toordinal() + 1)

        # Sort by published date (newest first)
        articles.sort(key=lambda x: x["published_at"], reverse=True)
        return articles

    def update_article(self, article_id: str, **updates) -> bool:
        """Update article data."""
        # Find the article file
        article_file = None
        for f in self.articles_dir.rglob(f"{article_id}.json"):
            article_file = f
            break

        if not article_file:
            return False

        with open(article_file, 'r', encoding='utf-8') as f:
            article_data = json.load(f)

        # Handle nested updates
        if "content" in updates:
            article_data["content"].update(updates.pop("content"))
        if "analysis" in updates:
            article_data["analysis"].update(updates.pop("analysis"))

        article_data.update(updates)
        article_data["updated_at"] = datetime.now(timezone.utc).isoformat() + "Z"

        with open(article_file, 'w', encoding='utf-8') as f:
            json.dump(article_data, f, indent=2, ensure_ascii=False)

        return True

    def enhance_article_content(self, article_id: str, full_content: str,
                              fetch_method: str) -> bool:
        """Enhance article with full scraped content."""
        return self.update_article(
            article_id,
            content={"full": full_content},
            content_source="enhanced",
            content_fetch_method=fetch_method
        )

    def process_article(self, article_id: str, processed_content: str,
                       analysis: Dict[str, Any], iocs: List[Dict[str, Any]],
                       processing_metadata: Dict[str, Any]) -> bool:
        """Mark article as processed with analysis results."""
        # Update article with processing results
        success = self.update_article(
            article_id,
            status="processed",
            content={"processed": processed_content},
            analysis=analysis,
            processing_metadata=processing_metadata
        )

        if success:
            # Save IOCs separately
            self.save_iocs_for_date(
                datetime.now(timezone.utc).date(),
                article_id,
                iocs
            )

        return success

    # IOC Management Methods
    def save_iocs_for_date(self, process_date: date, article_id: str,
                          iocs: List[Dict[str, Any]]) -> bool:
        """Save IOCs for a specific date."""
        processed_dir = self._get_processed_date_path(process_date)
        processed_dir.mkdir(parents=True, exist_ok=True)

        iocs_file = processed_dir / "iocs.json"

        # Load existing IOCs for the date
        existing_iocs = {"date": process_date.isoformat(), "iocs": []}
        if iocs_file.exists():
            with open(iocs_file, 'r', encoding='utf-8') as f:
                existing_iocs = json.load(f)

        # Add new IOCs with article reference
        for ioc in iocs:
            ioc.update({
                "article_id": article_id,
                "extracted_at": datetime.now(timezone.utc).isoformat() + "Z"
            })
            existing_iocs["iocs"].append(ioc)

        # Save updated IOCs
        with open(iocs_file, 'w', encoding='utf-8') as f:
            json.dump(existing_iocs, f, indent=2, ensure_ascii=False)

        return True

    def get_iocs_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get all IOCs extracted on a specific date."""
        iocs_file = self._get_processed_date_path(target_date) / "iocs.json"
        if not iocs_file.exists():
            return []

        with open(iocs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("iocs", [])

    def get_recent_iocs(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get IOCs from the last N days."""
        all_iocs = []
        current_date = date.fromordinal(datetime.now(timezone.utc).date().toordinal() - days)

        while current_date <= datetime.now(timezone.utc).date():
            daily_iocs = self.get_iocs_by_date(current_date)
            all_iocs.extend(daily_iocs)
            current_date = date.fromordinal(current_date.toordinal() + 1)

        # Sort by extraction time (newest first)
        all_iocs.sort(key=lambda x: x["extracted_at"], reverse=True)
        return all_iocs

    def get_article_iocs(self, article_id: str) -> List[Dict[str, Any]]:
        """Get all IOCs for a specific article."""
        # Search through recent IOC files for the article
        all_iocs = []
        current_date = date.fromordinal(datetime.now(timezone.utc).date().toordinal() - 30)  # Search last 30 days

        while current_date <= datetime.now(timezone.utc).date():
            daily_iocs = self.get_iocs_by_date(current_date)
            article_iocs = [ioc for ioc in daily_iocs if ioc.get("article_id") == article_id]
            all_iocs.extend(article_iocs)
            current_date = date.fromordinal(current_date.toordinal() + 1)

        # Sort by extraction time (newest first)
        all_iocs.sort(key=lambda x: x["extracted_at"], reverse=True)
        return all_iocs

    # Utility Methods
    def get_unprocessed_articles(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get articles that haven't been processed yet."""
        unprocessed = []

        for article_file in self.articles_dir.rglob("*.json"):
            with open(article_file, 'r', encoding='utf-8') as f:
                article = json.load(f)
                if article.get("status") != "processed":
                    unprocessed.append(article)
                    if limit and len(unprocessed) >= limit:
                        break

        # Sort by published date (newest first)
        unprocessed.sort(key=lambda x: x["published_at"], reverse=True)
        return unprocessed[:limit] if limit else unprocessed

    def health_check(self) -> Dict[str, Any]:
        """Check the health of the storage provider."""
        health = {
            "status": "healthy",
            "checks": {},
            "issues": []
        }

        try:
            # Check directories exist and are accessible
            required_dirs = [self.data_dir, self.sources_dir, self.articles_dir,
                           self.content_dir, self.processed_dir, self.reports_dir]

            for directory in required_dirs:
                if not directory.exists():
                    health["status"] = "unhealthy"
                    health["issues"].append(f"Directory {directory} does not exist")
                    health["checks"][directory.name] = False
                elif not directory.is_dir():
                    health["status"] = "unhealthy"
                    health["issues"].append(f"Path {directory} is not a directory")
                    health["checks"][directory.name] = False
                else:
                    health["checks"][directory.name] = True

            # Check if we can read/write in data directory
            test_file = self.data_dir / ".health_check"
            try:
                test_file.write_text("test")
                test_file.unlink()
                health["checks"]["read_write"] = True
            except Exception as e:
                health["status"] = "unhealthy"
                health["issues"].append(f"Read/write test failed: {e}")
                health["checks"]["read_write"] = False

        except Exception as e:
            health["status"] = "unhealthy"
            health["issues"].append(f"Health check failed: {e}")

        return health