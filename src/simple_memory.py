#!/usr/bin/env python3
"""
Simple memory system for tracking used articles in daily digests.
Replaces complex enterprise memory with basic freshness tracking.
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Set, Dict, Optional


class SimpleMemory:
    """Simplified memory system for tracking digest articles."""

    def __init__(self, memory_file: Optional[Path] = None):
        self.memory_file = memory_file or Path("data/simple_memory.json")
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self._memory_data = self._load_memory()

    def _load_memory(self) -> Dict:
        """Load memory data from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    # Convert date strings to proper format if needed
                    return self._normalize_memory_data(data)
            except (json.JSONDecodeError, KeyError):
                pass

        # Return fresh memory structure
        return {
            "used_articles": {},  # date -> [article_ids]
            "last_cleanup": datetime.now().isoformat()
        }

    def _normalize_memory_data(self, data: Dict) -> Dict:
        """Normalize legacy memory data to simple format."""
        if "used_articles" not in data:
            # Convert from legacy format if needed
            if "last_reports" in data:
                data["used_articles"] = data["last_reports"]
            else:
                data["used_articles"] = {}

        # Ensure all dates are in YYYY-MM-DD format
        normalized_articles = {}
        for date_str, articles in data["used_articles"].items():
            try:
                # Parse and reformat date to ensure consistency
                parsed_date = datetime.strptime(date_str.split("T")[0], "%Y-%m-%d")
                normalized_key = parsed_date.strftime("%Y-%m-%d")
                normalized_articles[normalized_key] = articles if isinstance(articles, list) else []
            except (ValueError, AttributeError):
                # Skip invalid dates
                continue

        data["used_articles"] = normalized_articles
        data["last_cleanup"] = datetime.now().isoformat()
        return data

    def _save_memory(self) -> None:
        """Save memory data to file."""
        self._memory_data["last_cleanup"] = datetime.now().isoformat()
        with open(self.memory_file, 'w') as f:
            json.dump(self._memory_data, f, indent=2)

    def get_used_articles(self, target_date: date) -> Set[str]:
        """Get set of article IDs used on target date."""
        date_str = target_date.strftime("%Y-%m-%d")
        return set(self._memory_data.get("used_articles", {}).get(date_str, []))

    def mark_articles_used(self, article_ids: List[str], target_date: date) -> None:
        """Mark articles as used on target date."""
        date_str = target_date.strftime("%Y-%m-%d")
        if "used_articles" not in self._memory_data:
            self._memory_data["used_articles"] = {}

        if date_str not in self._memory_data["used_articles"]:
            self._memory_data["used_articles"][date_str] = []

        # Add new articles (avoid duplicates)
        existing = set(self._memory_data["used_articles"][date_str])
        new_articles = set(article_ids) - existing
        self._memory_data["used_articles"][date_str].extend(new_articles)

        self._save_memory()

    def get_recently_used_articles(self, days_back: int = 7) -> Set[str]:
        """Get all article IDs used in the last N days."""
        cutoff_date = date.today() - timedelta(days=days_back)
        recent_articles = set()

        for date_str, articles in self._memory_data.get("used_articles", {}).items():
            try:
                article_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if article_date >= cutoff_date:
                    recent_articles.update(articles)
            except ValueError:
                continue

        return recent_articles

    def cleanup_old_entries(self, days_to_keep: int = 30) -> None:
        """Remove memory entries older than specified days."""
        cutoff_date = date.today() - timedelta(days=days_to_keep)

        if "used_articles" not in self._memory_data:
            return

        # Filter out old entries
        filtered_articles = {}
        for date_str, articles in self._memory_data["used_articles"].items():
            try:
                article_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                if article_date >= cutoff_date:
                    filtered_articles[date_str] = articles
            except ValueError:
                continue

        self._memory_data["used_articles"] = filtered_articles
        self._save_memory()

    def get_statistics(self) -> Dict:
        """Get memory usage statistics."""
        stats = {
            "total_days": len(self._memory_data.get("used_articles", {})),
            "total_articles": 0,
            "recent_articles_7d": 0,
            "oldest_date": None,
            "newest_date": None
        }

        for date_str, articles in self._memory_data.get("used_articles", {}).items():
            try:
                article_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                article_count = len(articles) if articles else 0

                stats["total_articles"] += article_count

                # Track 7-day recent articles
                if (date.today() - article_date).days <= 7:
                    stats["recent_articles_7d"] += article_count

                # Track date ranges
                if stats["oldest_date"] is None or article_date < stats["oldest_date"]:
                    stats["oldest_date"] = date_str
                if stats["newest_date"] is None or article_date > stats["newest_date"]:
                    stats["newest_date"] = date_str

            except ValueError:
                continue

        return stats