#!/usr/bin/env python3
"""
Test script for dynamic tag generation functionality.
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datetime import date
from src.tag_generator import TagGenerator
from src.json_storage import JSONStorage


def test_tag_generator():
    """Test tag generation with sample data."""
    print("🏷️  TESTING DYNAMIC TAG GENERATION")
    print("=" * 50)

    # Initialize tag generator
    storage = JSONStorage()
    tag_generator = TagGenerator(storage)

    # Print tag generator statistics
    stats = tag_generator.get_tag_statistics()
    print(f"📊 Tag Generator Configuration:")
    print(f"   Taxonomy categories: {', '.join(stats['taxonomy_categories'])}")
    print(f"   Total patterns: {stats['total_patterns']}")
    print(f"   Vendor mappings: {stats['vendor_mappings']}")
    print(f"   Industry mappings: {stats['industry_mappings']}")
    print()

    # Get articles for testing
    print("📊 Getting articles for testing...")
    articles = storage.get_articles_by_date_range(
        start_date=date(2025, 10, 28),
        end_date=date(2025, 10, 29),
        status='processed'
    )

    if not articles:
        print("❌ No processed articles found")
        return

    print(f"✅ Found {len(articles)} processed articles")

    # Sort by score and use top articles
    articles.sort(key=lambda x: x.get('score', 0), reverse=True)
    print(f"📈 Top article scores: {[a.get('score', 0) for a in articles[:5]]}")

    # Test tag generation
    print(f"\n🎯 Generating tags for {len(articles)} articles...")
    tags = tag_generator.extract_tags_from_articles(articles[:10], limit=15)

    if tags:
        print(f"✅ Generated {len(tags)} tags:")
        for i, tag in enumerate(tags, 1):
            category_icon = {
                'technical': '🔧',
                'malware_families': '🦠',
                'threat_actors': '🎭',
                'vendors': '🏢',
                'industries': '🏭',
                'severity': '⚠️'
            }.get(tag['category'], '🏷️')

            print(f"   {i:2d}. {category_icon} {tag['tag']} ({tag['category']}) - Confidence: {tag['confidence']:.2f}, Count: {tag['count']}")
            if tag['sources'] and len(tag['sources']) <= 3:
                print(f"       Sources: {', '.join(tag['sources'])}")

        print(f"\n🏷️  Hugo-formatted tags:")
        hugo_tags = tag_generator.format_tags_for_hugo(tags)
        print(f"   {', '.join(hugo_tags)}")

        # Test tag distribution by category
        print(f"\n📊 Tag distribution by category:")
        category_counts = {}
        for tag in tags:
            category = tag['category']
            category_counts[category] = category_counts.get(category, 0) + 1

        for category, count in category_counts.items():
            percentage = (count / len(tags)) * 100
            print(f"   {category}: {count} tags ({percentage:.1f}%)")

    else:
        print("❌ No tags generated")

    print("\n🎉 Tag generation test completed!")


def test_pattern_matching():
    """Test pattern matching with sample text."""
    print("\n" + "=" * 50)
    print("🧪 TESTING PATTERN MATCHING")
    print("=" * 50)

    tag_generator = TagGenerator()

    # Test text with various security indicators
    test_text = """
    Critical CVE-2025-24893 vulnerability allows remote code execution in Microsoft Windows.
    LockBit ransomware gang targets healthcare industry with new attacks.
    APT29 threat actors using spear phishing techniques against government agencies.
    Google Chrome zero-day vulnerability actively exploited in the wild.
    Apache Struts vulnerability leads to data breaches in finance sector.
    """

    print("📝 Test text:")
    print(test_text.strip())

    print(f"\n🔍 Extracting tags from test text...")
    tags = tag_generator._extract_pattern_tags(test_text.lower())

    if tags:
        print(f"✅ Extracted {len(tags)} tags:")
        for i, tag in enumerate(tags, 1):
            category_icon = {
                'technical': '🔧',
                'malware_families': '🦠',
                'threat_actors': '🎭',
                'vendors': '🏢',
                'industries': '🏭',
                'severity': '⚠️'
            }.get(tag['category'], '🏷️')

            print(f"   {i:2d}. {category_icon} {tag['tag']} ({tag['category']}) - Confidence: {tag['confidence']:.2f}")
    else:
        print("❌ No tags extracted")

    print("\n🧪 Pattern matching test completed!")


if __name__ == "__main__":
    test_tag_generator()
    test_pattern_matching()