"""Source Quality Tracking Module

This module tracks and manages the quality of RSS feed sources over time.
It maintains quality scores, tracks article relevance, and provides
recommendations for source prioritization.
"""

import statistics
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from src import database


class SourceQualityTracker:
    """Tracks and analyzes source quality over time."""

    def __init__(self):
        self.quality_thresholds = {
            'high_quality': 70.0,    # Sources with scores > 70
            'medium_quality': 40.0,  # Sources with scores 40-70
            'low_quality': 40.0      # Sources with scores < 40
        }

    def calculate_source_quality_score(self, source_id: int, days_back: int = 7) -> Optional[Dict[str, Any]]:
        """Calculate a comprehensive quality score for a source.

        Args:
            source_id: Database ID of the source
            days_back: Number of days to look back for analysis

        Returns:
            Dictionary with quality metrics or None if no data available
        """
        # Get articles from the source
        articles = database.get_articles_by_source_id(source_id, days_back)

        if not articles:
            return None

        # Basic metrics
        total_articles = len(articles)
        content_lengths = [len(article.get('raw_content', '')) for article in articles]
        avg_content_length = statistics.mean(content_lengths) if content_lengths else 0

        # Content quality categorization
        full_content_articles = len([a for a in articles if len(a.get('raw_content', '')) > 1000])
        partial_content_articles = len([a for a in articles if 100 < len(a.get('raw_content', '')) <= 1000])
        headline_only_articles = len([a for a in articles if len(a.get('raw_content', '')) <= 100])

        # Processing metrics (how many articles were processed vs rejected)
        processed_articles = len([a for a in articles if a.get('status') == 'processed'])
        rejected_articles = len([a for a in articles if a.get('status') == 'rejected'])
        fetched_articles = len([a for a in articles if a.get('status') == 'fetched'])

        # Relevance score (based on processing outcomes)
        if processed_articles + rejected_articles > 0:
            relevance_rate = processed_articles / (processed_articles + rejected_articles)
        else:
            relevance_rate = 0.5  # Neutral if no processing data

        # Content length score (0-40 points max)
        length_score = min(avg_content_length / 2000, 1.0) * 40

        # Content completeness score (0-30 points max)
        completeness_rate = full_content_articles / total_articles if total_articles > 0 else 0
        completeness_score = completeness_rate * 30

        # Relevance score (0-20 points max)
        relevance_score = relevance_rate * 20

        # Consistency score (0-10 points max) - lower variation is better
        if len(content_lengths) > 1:
            std_dev = statistics.stdev(content_lengths)
            consistency_score = max(0, 1 - (std_dev / avg_content_length)) * 10
        else:
            consistency_score = 5  # Neutral for single articles

        # Total quality score (0-100)
        total_score = length_score + completeness_score + relevance_score + consistency_score

        return {
            'source_id': source_id,
            'total_articles': total_articles,
            'avg_content_length': avg_content_length,
            'full_content_articles': full_content_articles,
            'partial_content_articles': partial_content_articles,
            'headline_only_articles': headline_only_articles,
            'processed_articles': processed_articles,
            'rejected_articles': rejected_articles,
            'fetched_articles': fetched_articles,
            'relevance_rate': relevance_rate,
            'completeness_rate': completeness_rate,
            'length_score': length_score,
            'completeness_score': completeness_score,
            'relevance_score': relevance_score,
            'consistency_score': consistency_score,
            'total_score': total_score,
            'quality_tier': self._get_quality_tier(total_score),
            'analysis_date': datetime.now(timezone.utc).isoformat()
        }

    def _get_quality_tier(self, score: float) -> str:
        """Determine quality tier based on score."""
        if score >= self.quality_thresholds['high_quality']:
            return 'high'
        elif score >= self.quality_thresholds['medium_quality']:
            return 'medium'
        else:
            return 'low'

    def update_source_quality_scores(self, days_back: int = 7) -> Dict[int, Dict[str, Any]]:
        """Update quality scores for all sources.

        Args:
            days_back: Number of days to look back for analysis

        Returns:
            Dictionary mapping source_id to quality metrics
        """
        sources = database.get_all_sources()
        quality_scores = {}

        for source in sources:
            score_data = self.calculate_source_quality_score(source['id'], days_back)
            if score_data:
                quality_scores[source['id']] = score_data

        return quality_scores

    def get_source_recommendations(self, max_sources: int = 10) -> Dict[str, List[Dict[str, Any]]]:
        """Get recommendations for source processing based on quality.

        Args:
            max_sources: Maximum number of sources to recommend per tier

        Returns:
            Dictionary with recommendations by quality tier
        """
        quality_scores = self.update_source_quality_scores()

        # Get all sources for name mapping
        all_sources = database.get_all_sources()
        source_by_id = {source['id']: source for source in all_sources}

        # Categorize sources by quality tier
        high_quality = []
        medium_quality = []
        low_quality = []

        for source_id, metrics in quality_scores.items():
            source_info = source_by_id.get(source_id, {})
            recommendation = {
                'source_id': source_id,
                'source_name': source_info.get('name', f"Source {source_id}"),
                'source_url': source_info.get('url', ''),
                'quality_score': metrics['total_score'],
                'quality_tier': metrics['quality_tier'],
                'avg_content_length': metrics['avg_content_length'],
                'total_articles': metrics['total_articles'],
                'relevance_rate': metrics['relevance_rate'],
                'completeness_rate': metrics['completeness_rate'],
                'recommendation': self._get_processing_recommendation(metrics)
            }

            if metrics['quality_tier'] == 'high':
                high_quality.append(recommendation)
            elif metrics['quality_tier'] == 'medium':
                medium_quality.append(recommendation)
            else:
                low_quality.append(recommendation)

        # Sort by quality score within each tier
        high_quality.sort(key=lambda x: x['quality_score'], reverse=True)
        medium_quality.sort(key=lambda x: x['quality_score'], reverse=True)
        low_quality.sort(key=lambda x: x['quality_score'], reverse=True)

        return {
            'high_quality': high_quality[:max_sources],
            'medium_quality': medium_quality[:max_sources],
            'low_quality': low_quality[:max_sources],
            'analysis_summary': {
                'total_sources_analyzed': len(quality_scores),
                'high_quality_count': len(high_quality),
                'medium_quality_count': len(medium_quality),
                'low_quality_count': len(low_quality),
                'average_quality_score': statistics.mean([m['total_score'] for m in quality_scores.values()]) if quality_scores else 0
            }
        }

    def _get_processing_recommendation(self, metrics: Dict[str, Any]) -> str:
        """Get processing recommendation based on quality metrics."""
        score = metrics['total_score']
        completeness = metrics['completeness_rate']
        relevance = metrics['relevance_rate']

        if score >= 80:
            return "Priority: Full LLM processing + content enhancement"
        elif score >= 70:
            return "High: Full LLM processing"
        elif score >= 50:
            return "Medium: LLM processing + consider custom parser"
        elif completeness > 0.5:
            return "Low: Title-based filtering first, then selective LLM processing"
        else:
            return "Very Low: Title-only filtering, minimal LLM processing"

    def track_source_performance_over_time(self, source_id: int, days_back: int = 30) -> Dict[str, Any]:
        """Track source performance trends over time.

        Args:
            source_id: Database ID of the source
            days_back: Number of days to look back

        Returns:
            Dictionary with trend analysis
        """
        # This would be implemented with time-series analysis
        # For now, return basic trend data
        current_score = self.calculate_source_quality_score(source_id, 7)
        previous_score = self.calculate_source_quality_score(source_id, days_back)

        if not current_score:
            return {'error': 'No recent data available'}

        trend = 'stable'
        change = 0
        if previous_score:
            change = current_score['total_score'] - previous_score['total_score']
            if change > 10:
                trend = 'improving'
            elif change < -10:
                trend = 'declining'

        return {
            'source_id': source_id,
            'current_score': current_score['total_score'],
            'previous_score': previous_score['total_score'] if previous_score else None,
            'score_change': change,
            'trend': trend,
            'current_articles': current_score['total_articles'],
            'previous_articles': previous_score['total_articles'] if previous_score else 0,
            'recommendation': self._get_trend_recommendation(trend, change)
        }

    def _get_trend_recommendation(self, trend: str, change: float) -> str:
        """Get recommendation based on performance trend."""
        if trend == 'improving':
            return f"Source quality improving (+{change:.1f} points). Consider increased priority."
        elif trend == 'declining':
            return f"Source quality declining ({change:.1f} points). Review source relevance."
        else:
            return "Source quality stable. Current priority appropriate."


def print_source_quality_report() -> None:
    """Print a comprehensive source quality report."""
    tracker = SourceQualityTracker()
    recommendations = tracker.get_source_recommendations()

    print("\n" + "="*80)
    print("SOURCE QUALITY TRACKING REPORT")
    print("="*80)

    summary = recommendations['analysis_summary']
    print(f"Total Sources Analyzed: {summary['total_sources_analyzed']}")
    print(f"High Quality (>70): {summary['high_quality_count']} sources")
    print(f"Medium Quality (40-70): {summary['medium_quality_count']} sources")
    print(f"Low Quality (<40): {summary['low_quality_count']} sources")
    print(f"Average Quality Score: {summary['average_quality_score']:.1f}/100")
    print()

    # High Quality Sources
    if recommendations['high_quality']:
        print("🌟 HIGH QUALITY SOURCES (Priority Processing)")
        print("-" * 80)
        for source in recommendations['high_quality']:
            print(f"• {source['source_name']} (Score: {source['quality_score']:.1f})")
            print(f"  {source['source_url']}")
            print(f"  Avg Content: {source['avg_content_length']:.0f} chars | Articles: {source['total_articles']}")
            print(f"  Recommendation: {source['recommendation']}")
            print()

    # Medium Quality Sources
    if recommendations['medium_quality']:
        print("⚠️  MEDIUM QUALITY SOURCES (Selective Processing)")
        print("-" * 80)
        for source in recommendations['medium_quality']:
            print(f"• {source['source_name']} (Score: {source['quality_score']:.1f})")
            print(f"  {source['source_url']}")
            print(f"  Avg Content: {source['avg_content_length']:.0f} chars | Articles: {source['total_articles']}")
            print(f"  Recommendation: {source['recommendation']}")
            print()

    # Low Quality Sources
    if recommendations['low_quality']:
        print("📉 LOW QUALITY SOURCES (Title-based Filtering)")
        print("-" * 80)
        for source in recommendations['low_quality'][:5]:  # Show top 5 low quality
            print(f"• {source['source_name']} (Score: {source['quality_score']:.1f})")
            print(f"  {source['source_url']}")
            print(f"  Avg Content: {source['avg_content_length']:.0f} chars | Articles: {source['total_articles']}")
            print(f"  Recommendation: {source['recommendation']}")
            print()


if __name__ == "__main__":
    # Initialize database
    database.initialize_database()

    # Generate and print quality report
    print_source_quality_report()