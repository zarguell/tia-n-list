#!/usr/bin/env python3
"""
Integrated Dynamic Content Generation Test

Tests the integration of title and tag generation for blog posts.
This demonstrates how both systems would work together in the blog workflow.
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import date
from src.title_generator import TitleGenerator
from src.tag_generator import TagGenerator
from src.json_storage import JSONStorage


def test_integrated_generation():
    """Test integrated title and tag generation."""
    print("🎯 TESTING INTEGRATED DYNAMIC CONTENT GENERATION")
    print("=" * 60)

    # Initialize components
    storage = JSONStorage()
    title_generator = TitleGenerator(storage)
    tag_generator = TagGenerator(storage)

    # Get articles for today
    target_date = date.today()
    articles = storage.get_articles_by_date_range(
        start_date=target_date,
        end_date=target_date,
        status='processed'
    )

    if not articles:
        print("❌ No processed articles found for today")
        return

    # Sort by score
    articles.sort(key=lambda x: x.get('score', 0), reverse=True)
    print(f"📊 Found {len(articles)} processed articles for {target_date}")

    # Generate title
    print(f"\n🎯 DYNAMIC TITLE GENERATION")
    print("-" * 40)
    title = title_generator.generate_title(articles, target_date)
    print(f"Generated Title: {title}")

    # Generate tags
    print(f"\n🏷️  DYNAMIC TAG GENERATION")
    print("-" * 40)
    tags = tag_generator.generate_tags_for_date(target_date, limit=12)
    hugo_tags = tag_generator.format_tags_for_hugo(tags)
    print(f"Generated Tags: {', '.join(hugo_tags)}")

    # Show tag breakdown
    print(f"\n📊 TAG BREAKDOWN:")
    category_breakdown = {}
    for tag in tags:
        category = tag['category']
        if category not in category_breakdown:
            category_breakdown[category] = []
        category_breakdown[category].append(tag['tag'])

    category_icons = {
        'technical': '🔧',
        'malware_families': '🦠',
        'threat_actors': '🎭',
        'vendors': '🏢',
        'industries': '🏭',
        'severity': '⚠️'
    }

    for category, tag_list in category_breakdown.items():
        icon = category_icons.get(category, '🏷️')
        print(f"   {icon} {category.replace('_', ' ').title()}: {', '.join(tag_list)}")

    # Generate Hugo front matter example
    print(f"\n📝 HUGO FRONT MATTER EXAMPLE:")
    print("-" * 40)
    print("---")
    print(f"title: \"{title}\"")
    print("date: 2025-10-29T10:00:00Z")
    print("draft: false")
    print("author: \"Tia N. List\"")
    print("tags: [")
    for i, tag in enumerate(hugo_tags):
        comma = "," if i < len(hugo_tags) - 1 else ""
        print(f"  \"{tag}\"{comma}")
    print("]")
    print("categories: [\"Cybersecurity\", \"Threat Intelligence\"]")
    print("---")

    # Show content themes
    print(f"\n🎯 CONTENT THEMES ANALYSIS:")
    print("-" * 40)
    themes = title_generator._analyze_articles_for_themes(articles)

    theme_icons = {
        'critical_vulnerabilities': '🚨',
        'threat_actors': '🎭',
        'major_vendors': '🏢',
        'industries': '🏭',
        'malware_families': '🦠',
        'attack_types': '⚔️',
        'severity_indicators': '📊'
    }

    for theme_type, items in themes.items():
        if items:
            icon = theme_icons.get(theme_type, '📋')
            theme_name = theme_type.replace('_', ' ').title()
            print(f"   {icon} {theme_name}: {', '.join(items[:5])}")

    print(f"\n✅ INTEGRATED GENERATION COMPLETE")
    print("=" * 60)
    print(f"📈 Ready for Hugo blog post generation!")
    print(f"🔗 All components working together successfully")


def test_content_quality_metrics():
    """Test content quality metrics for generated content."""
    print(f"\n📊 CONTENT QUALITY METRICS")
    print("=" * 40)

    storage = JSONStorage()
    title_generator = TitleGenerator(storage)
    tag_generator = TagGenerator(storage)

    # Get title statistics
    title_stats = title_generator.get_title_statistics()
    print(f"📝 Title Generator Stats:")
    print(f"   Recent titles: {title_stats['recent_titles_count']}")
    print(f"   Cache status: {title_stats['cache_status']}")

    # Get tag statistics
    tag_stats = tag_generator.get_tag_statistics()
    print(f"\n🏷️  Tag Generator Stats:")
    print(f"   Taxonomy categories: {len(tag_stats['taxonomy_categories'])}")
    print(f"   Total patterns: {tag_stats['total_patterns']}")
    print(f"   Supported categories:")
    for category, info in tag_stats['supported_categories'].items():
        print(f"     • {category}: {info['pattern_count']} patterns (weight: {info['weight']})")


if __name__ == "__main__":
    test_integrated_generation()
    test_content_quality_metrics()