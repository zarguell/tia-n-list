#!/usr/bin/env python3
"""Feed Quality Analyzer

This script analyzes RSS feed quality without using custom content parsers.
It measures content length, article frequency, and other quality metrics
to help identify which feeds provide the best content out of the box.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import ingestion, database
import statistics
from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta


def analyze_feed_content_quality() -> Dict[str, Any]:
    """Analyze the content quality of all articles in the database.

    Returns:
        Dictionary with quality metrics by source.
    """
    # Get all articles with content
    articles = database.get_articles_by_status('fetched')

    if not articles:
        print("No articles found in database. Run ingestion first.")
        return {}

    # Get all sources for mapping
    all_sources = database.get_all_sources()
    source_by_id = {source['id']: source for source in all_sources}

    # Group articles by source
    source_stats = {}

    for article in articles:
        source_id = article['source_id']

        # Get source information from mapping
        source = source_by_id.get(source_id)
        if source:
            source_name = source['name']
            source_url = source['url']
        else:
            source_name = f"Source {source_id}"
            source_url = article.get('source_url', '')

        content_length = len(article.get('raw_content', ''))

        if source_id not in source_stats:
            source_stats[source_id] = {
                'source_name': source_name,
                'source_url': source_url,
                'articles': [],
                'total_articles': 0,
                'total_content_length': 0,
                'avg_content_length': 0,
                'min_content_length': float('inf'),
                'max_content_length': 0,
                'has_full_content': 0,  # Articles with >1000 chars
                'has_partial_content': 0,  # Articles with 100-1000 chars
                'has_headline_only': 0,  # Articles with <100 chars
                'quality_score': 0  # Will be calculated
            }

        stats = source_stats[source_id]
        stats['articles'].append({
            'title': article.get('title', ''),
            'url': article.get('url', ''),
            'content_length': content_length,
            'published_at': article.get('published_at')
        })
        stats['total_articles'] += 1
        stats['total_content_length'] += content_length
        stats['min_content_length'] = min(stats['min_content_length'], content_length)
        stats['max_content_length'] = max(stats['max_content_length'], content_length)

        # Categorize content quality
        if content_length > 1000:
            stats['has_full_content'] += 1
        elif content_length > 100:
            stats['has_partial_content'] += 1
        else:
            stats['has_headline_only'] += 1

    # Calculate averages and quality scores
    for source_id, stats in source_stats.items():
        if stats['total_articles'] > 0:
            stats['avg_content_length'] = stats['total_content_length'] / stats['total_articles']

            # Quality score calculation (0-100)
            # Factors: average content length, percentage of full content, consistency
            avg_length_score = min(stats['avg_content_length'] / 2000, 1.0) * 40  # Max 40 points
            full_content_ratio = stats['has_full_content'] / stats['total_articles']
            content_quality_score = full_content_ratio * 40  # Max 40 points

            # Consistency bonus (lower std dev = higher consistency)
            if stats['total_articles'] > 1:
                lengths = [a['content_length'] for a in stats['articles']]
                std_dev = statistics.stdev(lengths) if len(lengths) > 1 else 0
                consistency_score = max(0, 1 - (std_dev / stats['avg_content_length'])) * 20  # Max 20 points
            else:
                consistency_score = 10  # Neutral for single articles

            stats['quality_score'] = avg_length_score + content_quality_score + consistency_score

    return source_stats


def print_quality_analysis(source_stats: Dict[str, Any]) -> None:
    """Print a formatted analysis of feed quality.

    Args:
        source_stats: Dictionary with source quality metrics.
    """
    if not source_stats:
        return

    # Sort by quality score
    sorted_sources = sorted(source_stats.items(), key=lambda x: x[1]['quality_score'], reverse=True)

    print("\n" + "="*80)
    print("RSS FEED QUALITY ANALYSIS")
    print("="*80)
    print(f"Analyzing {sum(s['total_articles'] for s in source_stats.values())} articles from {len(source_stats)} sources")
    print()

    print("RANKING BY QUALITY SCORE:")
    print("-" * 80)
    print(f"{'Rank':<4} {'Source':<30} {'Score':<6} {'Articles':<9} {'Avg Length':<11} {'Full %':<7} {'Type':<15}")
    print("-" * 80)

    for rank, (source_id, stats) in enumerate(sorted_sources, 1):
        name = stats['source_name'][:28] + '..' if len(stats['source_name']) > 30 else stats['source_name']
        score = f"{stats['quality_score']:.1f}"
        articles = stats['total_articles']
        avg_len = f"{stats['avg_content_length']:.0f}"
        full_pct = f"{(stats['has_full_content'] / articles * 100):.0f}%" if articles > 0 else "0%"

        # Determine content type classification
        if stats['has_full_content'] / articles > 0.7:
            content_type = "Full Content"
        elif stats['has_partial_content'] / articles > 0.7:
            content_type = "Partial Content"
        else:
            content_type = "Headline Only"

        print(f"{rank:<4} {name:<30} {score:<6} {articles:<9} {avg_len:<11} {full_pct:<7} {content_type:<15}")

    print("\n" + "="*80)
    print("DETAILED ANALYSIS:")
    print("="*80)

    for rank, (source_id, stats) in enumerate(sorted_sources[:10], 1):  # Top 10 detailed
        print(f"\n{rank}. {stats['source_name']}")
        print(f"   URL: {stats['source_url']}")
        print(f"   Quality Score: {stats['quality_score']:.1f}/100")
        print(f"   Total Articles: {stats['total_articles']}")
        print(f"   Average Content Length: {stats['avg_content_length']:.0f} characters")
        print(f"   Content Range: {stats['min_content_length']:.0f} - {stats['max_content_length']:.0f} chars")
        print(f"   Full Content Articles (>1000 chars): {stats['has_full_content']} ({stats['has_full_content']/stats['total_articles']*100:.1f}%)")
        print(f"   Partial Content (100-1000 chars): {stats['has_partial_content']} ({stats['has_partial_content']/stats['total_articles']*100:.1f}%)")
        print(f"   Headline Only (<100 chars): {stats['has_headline_only']} ({stats['has_headline_only']/stats['total_articles']*100:.1f}%)")

        # Show sample articles if available
        if stats['articles']:
            sample = stats['articles'][0]
            print(f"   Sample Article: {sample['title'][:60]}{'...' if len(sample['title']) > 60 else ''}")
            print(f"   Content Length: {sample['content_length']} chars")

    # Summary statistics
    all_scores = [stats['quality_score'] for stats in source_stats.values()]
    print(f"\n" + "="*80)
    print("SUMMARY STATISTICS:")
    print("="*80)
    print(f"Total Sources Analyzed: {len(source_stats)}")
    print(f"Average Quality Score: {statistics.mean(all_scores):.1f}")
    print(f"Median Quality Score: {statistics.median(all_scores):.1f}")
    print(f"Highest Quality Score: {max(all_scores):.1f}")
    print(f"Lowest Quality Score: {min(all_scores):.1f}")

    # Categorize sources
    high_quality = len([s for s in source_stats.values() if s['quality_score'] > 70])
    medium_quality = len([s for s in source_stats.values() if 40 <= s['quality_score'] <= 70])
    low_quality = len([s for s in source_stats.values() if s['quality_score'] < 40])

    print(f"\nQuality Distribution:")
    print(f"  High Quality (>70): {high_quality} sources")
    print(f"  Medium Quality (40-70): {medium_quality} sources")
    print(f"  Low Quality (<40): {low_quality} sources")

    # Recommendations
    print(f"\nRECOMMENDATIONS:")
    print("-" * 40)
    print("• Prioritize high-quality sources for LLM processing")
    print("• Consider custom parsers for medium-quality sources")
    print("• Use title-only filtering for low-quality sources")
    print(f"• Top 3 sources for immediate processing: {', '.join(list(sorted_sources[:3][i][1]['source_name'] for i in range(3)))}")


def main():
    """Main function to run feed quality analysis."""
    print("Tia N. List - Feed Quality Analyzer")
    print("Analyzing RSS feed content quality without custom parsers...")

    # Initialize database
    database.initialize_database()

    # Analyze feed quality
    source_stats = analyze_feed_content_quality()

    # Print analysis
    print_quality_analysis(source_stats)

    print(f"\n✅ Feed quality analysis complete!")
    print(f"💡 Use this analysis to prioritize sources for LLM processing and custom parser development")


if __name__ == "__main__":
    main()