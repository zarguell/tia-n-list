"""AI Context Builder for Tia N. List project.

This module provides intelligent content retrieval and context building
capabilities for AI processing, enabling better synthesis and analysis
of threat intelligence data.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Tuple
import re
from collections import defaultdict, Counter

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider


class AIContextBuilder:
    """Intelligent context builder for AI prompting and content synthesis."""

    def __init__(self, storage: StorageProvider = None):
        """Initialize context builder with storage backend."""
        self.storage = storage or get_default_storage_provider()

    def get_recent_articles(self, days: int = 7, status: str = "processed",
                           min_score: int = 50, limit: int = None) -> List[Dict[str, Any]]:
        """Get recent high-quality articles for AI context."""
        articles = self.storage.get_recent_articles(days=days, status=status)

        # Filter by minimum score
        filtered_articles = [
            article for article in articles
            if (article.get("analysis", {}).get("score") or 0) >= min_score
        ]

        return filtered_articles[:limit] if limit else filtered_articles

    def get_articles_by_source(self, source_id: str, limit: int = 10,
                              status: str = "processed") -> List[Dict[str, Any]]:
        """Get recent articles from a specific source."""
        return self.storage.get_articles_by_source(
            source_id=source_id,
            limit=limit,
            status=status
        )

    def get_articles_by_threat_category(self, category: str, days: int = 30,
                                       limit: int = 20) -> List[Dict[str, Any]]:
        """Get articles by threat category."""
        articles = self.storage.get_recent_articles(days=days, status="processed")

        category_articles = [
            article for article in articles
            if article.get("analysis", {}).get("threat_category") == category
        ]

        return category_articles[:limit] if limit else category_articles

    def get_articles_by_score_range(self, min_score: int, max_score: int = 100,
                                   days: int = 7, limit: int = 15) -> List[Dict[str, Any]]:
        """Get articles within a specific score range."""
        articles = self.storage.get_recent_articles(days=days, status="processed")

        score_filtered = [
            article for article in articles
            if min_score <= (article.get("analysis", {}).get("score") or 0) <= max_score
        ]

        return score_filtered[:limit] if limit else score_filtered

    def get_high_impact_articles(self, days: int = 7, min_score: int = 80,
                                limit: int = 10) -> List[Dict[str, Any]]:
        """Get high-impact articles for priority analysis."""
        return self.get_articles_by_score_range(
            min_score=min_score,
            days=days,
            limit=limit
        )

    def get_related_articles(self, article_id: str, similarity_threshold: float = 0.3,
                            max_related: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Find articles related to a given article based on content similarity."""
        target_article = self.storage.get_article(article_id)
        if not target_article:
            return []

        target_words = self._extract_keywords(target_article)
        recent_articles = self.storage.get_recent_articles(days=14, status="processed")

        related_articles = []
        for article in recent_articles:
            if article["id"] == article_id:
                continue

            article_words = self._extract_keywords(article)
            similarity = self._calculate_jaccard_similarity(target_words, article_words)

            if similarity >= similarity_threshold:
                related_articles.append((article, similarity))

        # Sort by similarity and return top matches
        related_articles.sort(key=lambda x: x[1], reverse=True)
        return related_articles[:max_related]

    def build_context_for_synthesis(self, target_date: date = None,
                                   days_back: int = 7,
                                   include_io_cs: bool = True,
                                   max_articles: int = 20) -> Dict[str, Any]:
        """Build comprehensive context for AI synthesis and blog generation."""
        if target_date is None:
            target_date = date.today()

        # Get articles from the date range
        articles = self.storage.get_articles_by_date_range(
            start_date=target_date - timedelta(days=days_back),
            end_date=target_date,
            status="processed"
        )

        # Sort by score and limit
        articles.sort(key=lambda x: x.get("analysis", {}).get("score", 0), reverse=True)
        articles = articles[:max_articles]

        # Get IOCs if requested
        iocs = []
        if include_io_cs:
            for i in range(days_back):
                check_date = target_date - timedelta(days=i)
                iocs.extend(self.storage.get_iocs_by_date(check_date))

        # Build context structure
        context = {
            "target_date": target_date.isoformat(),
            "date_range": {
                "start": (target_date - timedelta(days=days_back)).isoformat(),
                "end": target_date.isoformat(),
                "days": days_back
            },
            "articles": articles,
            "iocs": iocs[:50],  # Limit IOCs to avoid context overflow
            "statistics": self._calculate_context_statistics(articles, iocs),
            "threat_landscape": self._analyze_threat_landscape(articles),
            "trending_topics": self._identify_trending_topics(articles),
            "key_sources": self._analyze_source_contributions(articles)
        }

        return context

    def build_prompt_context(self, articles: List[Dict[str, Any]],
                           context_type: str = "synthesis") -> str:
        """Build formatted prompt context from articles."""
        if not articles:
            return "No articles available for analysis."

        context_parts = []

        if context_type == "synthesis":
            context_parts.append("THREAT INTELLIGENCE BRIEFING DATA")
            context_parts.append("=" * 50)
            context_parts.append(f"Processing {len(articles)} articles for synthesis\n")

        elif context_type == "ioc_extraction":
            context_parts.append("ARTICLES FOR IOC/TTP EXTRACTION")
            context_parts.append("=" * 45)

        elif context_type == "relevance_filtering":
            context_parts.append("ARTICLES FOR RELEVANCE ASSESSMENT")
            context_parts.append("=" * 45)

        # Format each article
        for i, article in enumerate(articles, 1):
            context_parts.append(f"\nArticle {i}:")
            context_parts.append(f"Title: {article['title']}")
            context_parts.append(f"Source: {article['source_id']}")
            context_parts.append(f"URL: {article['url']}")
            context_parts.append(f"Published: {article['published_at']}")

            # Use best available content
            content = article.get("content", {})
            if content.get("processed"):
                article_content = content["processed"]
            elif content.get("full"):
                article_content = content["full"]
            else:
                article_content = content.get("raw", "")

            # Truncate content if too long
            if len(article_content) > 3000:
                article_content = article_content[:3000] + "...[truncated]"

            context_parts.append(f"Content: {article_content}")

            # Add existing analysis if available
            analysis = article.get("analysis", {})
            if analysis.get("threat_category"):
                context_parts.append(f"Threat Category: {analysis['threat_category']}")
            if analysis.get("score"):
                context_parts.append(f"Score: {analysis['score']}")

            context_parts.append("-" * 40)

        return "\n".join(context_parts)

    def get_daily_summary_context(self, target_date: date = None) -> Dict[str, Any]:
        """Get context for daily summary generation."""
        if target_date is None:
            target_date = date.today()

        articles = self.storage.get_articles_by_date_range(
            start_date=target_date,
            end_date=target_date,
            status="processed"
        )

        iocs = self.storage.get_iocs_by_date(target_date)

        return {
            "date": target_date.isoformat(),
            "articles": articles,
            "iocs": iocs,
            "summary_stats": {
                "total_articles": len(articles),
                "high_score_articles": len([a for a in articles if (a.get("analysis", {}).get("score") or 0) >= 80]),
                "total_iocs": len(iocs),
                "unique_sources": len(set(a["source_id"] for a in articles))
            }
        }

    def _extract_keywords(self, article: Dict[str, Any]) -> set:
        """Extract keywords from article title and content."""
        text = article.get("title", "") + " " + article.get("content", {}).get("raw", "")

        # Simple keyword extraction (can be enhanced with NLP libraries)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Filter out common words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
            'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who',
            'boy', 'did', 'use', 'from', 'have', 'them', 'she', 'many', 'time',
            'will', 'with', 'would', 'there', 'been', 'each', 'much', 'some',
            'your', 'what', 'this', 'that', 'said', 'were', 'their', 'than',
            'when', 'make', 'like', 'into', 'just', 'know', 'take', 'come',
            'could', 'over', 'think', 'also', 'after', 'back', 'well', 'even',
            'only', 'good', 'most', 'such', 'very', 'more', 'great', 'must',
            'still', 'through', 'should', 'before', 'being', 'going', 'where',
            'might', 'does', 'said', 'says', 'according'
        }

        keywords = {word for word in words if word not in stop_words and len(word) > 3}
        return keywords

    def _calculate_jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets."""
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def _calculate_context_statistics(self, articles: List[Dict[str, Any]],
                                    iocs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics for the context."""
        stats = {
            "articles": {
                "total": len(articles),
                "average_score": 0,
                "threat_categories": {},
                "sources": {}
            },
            "iocs": {
                "total": len(iocs),
                "by_type": {},
                "by_confidence": {}
            }
        }

        if articles:
            scores = [(a.get("analysis", {}).get("score") or 0) for a in articles]
            stats["articles"]["average_score"] = sum(scores) / len(scores)

            # Count threat categories
            categories = [a.get("analysis", {}).get("threat_category", "unknown") for a in articles]
            stats["articles"]["threat_categories"] = dict(Counter(categories))

            # Count sources
            sources = [a["source_id"] for a in articles]
            stats["articles"]["sources"] = dict(Counter(sources))

        if iocs:
            # Count IOC types
            ioc_types = [ioc.get("type", "unknown") for ioc in iocs]
            stats["iocs"]["by_type"] = dict(Counter(ioc_types))

            # Count confidence levels
            confidences = [ioc.get("confidence", "unknown") for ioc in iocs]
            stats["iocs"]["by_confidence"] = dict(Counter(confidences))

        return stats

    def _analyze_threat_landscape(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the threat landscape from articles."""
        categories = defaultdict(list)

        for article in articles:
            category = article.get("analysis", {}).get("threat_category", "uncategorized")
            categories[category].append({
                "title": article["title"],
                "score": article.get("analysis", {}).get("score", 0),
                "source": article["source_id"]
            })

        # Calculate category dominance
        total_articles = len(articles)
        landscape = {}

        for category, cat_articles in categories.items():
            landscape[category] = {
                "count": len(cat_articles),
                "percentage": (len(cat_articles) / total_articles * 100) if total_articles > 0 else 0,
                "average_score": sum((a.get("score") or 0) for a in cat_articles) / len(cat_articles) if cat_articles else 0,
                "top_articles": sorted(cat_articles, key=lambda x: (x.get("score") or 0), reverse=True)[:3]
            }

        return landscape

    def _identify_trending_topics(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify trending topics from articles."""
        all_keywords = []

        for article in articles:
            keywords = self._extract_keywords(article)
            all_keywords.extend(keywords)

        # Count keyword frequency
        keyword_counts = Counter(all_keywords)

        # Get top trending topics
        trending = [
            {"topic": topic, "frequency": count}
            for topic, count in keyword_counts.most_common(10)
            if count > 1  # Only include topics that appear multiple times
        ]

        return trending

    def _analyze_source_contributions(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze source contributions to the context."""
        source_stats = defaultdict(lambda: {
            "count": 0,
            "total_score": 0,
            "articles": []
        })

        for article in articles:
            source_id = article["source_id"]
            score = (article.get("analysis", {}).get("score") or 0)

            source_stats[source_id]["count"] += 1
            source_stats[source_id]["total_score"] += score
            source_stats[source_id]["articles"].append({
                "title": article["title"],
                "score": score,
                "threat_category": article.get("analysis", {}).get("threat_category")
            })

        # Calculate averages and sort
        contributions = {}
        for source_id, stats in source_stats.items():
            contributions[source_id] = {
                "article_count": stats["count"],
                "average_score": stats["total_score"] / stats["count"] if stats["count"] > 0 else 0,
                "total_score": stats["total_score"],
                "top_articles": sorted(stats["articles"], key=lambda x: (x.get("score") or 0), reverse=True)[:3]
            }

        return contributions


# Global context builder instance
context_builder = AIContextBuilder()