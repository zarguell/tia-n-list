#!/usr/bin/env python3
"""
Enhanced blog generation script with dynamic titles and tags.

This script replaces the basic blog generation with our enhanced system
that includes dynamic title generation and intelligent tag extraction.
"""

import sys
import os
import argparse
from datetime import date, timedelta

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.enhanced_json_blog_generator import EnhancedJSONBlogGenerator


def main():
    """Main enhanced blog generation function."""
    parser = argparse.ArgumentParser(description='Generate enhanced blog posts with dynamic titles and tags')
    parser.add_argument('--date', type=str, help='Date to generate for (YYYY-MM-DD format). Defaults to today.')
    parser.add_argument('--no-dynamic-title', action='store_true', help='Disable dynamic title generation')
    parser.add_argument('--no-dynamic-tags', action='store_true', help='Disable dynamic tag generation')
    parser.add_argument('--no-intelligent-synthesis', action='store_true', help='Disable intelligent synthesis')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode with verbose output')

    args = parser.parse_args()

    # Parse target date
    if args.date:
        try:
            target_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"❌ Invalid date format: {args.date}. Use YYYY-MM-DD format.")
            sys.exit(1)
    else:
        target_date = date.today()

    # Parse options
    use_dynamic_title = not args.no_dynamic_title
    use_dynamic_tags = not args.no_dynamic_tags
    use_intelligent_synthesis = not args.no_intelligent_synthesis

    print("🚀 ENHANCED BLOG GENERATION")
    print("=" * 60)
    print(f"📅 Target Date: {target_date.isoformat()}")
    print(f"🎯 Dynamic Titles: {'✅' if use_dynamic_title else '❌'}")
    print(f"🏷️  Dynamic Tags: {'✅' if use_dynamic_tags else '❌'}")
    print(f"🧠 Intelligent Synthesis: {'✅' if use_intelligent_synthesis else '❌'}")
    print()

    # Initialize enhanced generator
    generator = EnhancedJSONBlogGenerator()

    # Print system status in test mode
    if args.test_mode:
        stats = generator.get_generation_statistics()
        print("🔍 SYSTEM STATUS")
        print("-" * 30)
        print(f"Title Generator: {'✅ Available' if stats['title_generator_available'] else '❌ Unavailable'}")
        print(f"Tag Generator: {'✅ Available' if stats['tag_generator_available'] else '❌ Unavailable'}")

        if stats['title_generator_stats']:
            title_stats = stats['title_generator_stats']
            print(f"Title Cache Size: {title_stats.get('recent_titles_count', 0)}")

        if stats['tag_generator_stats']:
            tag_stats = stats['tag_generator_stats']
            print(f"Tag Patterns: {tag_stats.get('total_patterns', 0)}")
            print(f"Tag Categories: {len(tag_stats.get('taxonomy_categories', []))}")
        print()

    # Generate blog post
    print("📝 GENERATING BLOG POST")
    print("-" * 30)
    result = generator.generate_daily_summary(
        target_date=target_date,
        use_intelligent_synthesis=use_intelligent_synthesis,
        use_dynamic_title=use_dynamic_title,
        use_dynamic_tags=use_dynamic_tags
    )

    # Print results
    print(f"\n📊 GENERATION RESULTS")
    print("-" * 30)
    print(f"Success: {'✅' if result['success'] else '❌'}")
    print(f"Fallback Mode: {'✅' if result.get('fallback_mode') else '❌'}")

    if result.get('filepath'):
        print(f"Generated File: {result['filepath']}")

    # Print feature usage
    print(f"\n🎯 FEATURE USAGE")
    print("-" * 30)
    print(f"Dynamic Title Used: {'✅' if result.get('dynamic_title_used') else '❌'}")
    print(f"Dynamic Tags Used: {'✅' if result.get('dynamic_tags_used') else '❌'}")
    print(f"Intelligent Synthesis Used: {'✅' if result.get('intelligent_synthesis_used') else '❌'}")

    # Print content statistics
    if result.get('content_length'):
        print(f"\n📈 CONTENT STATISTICS")
        print("-" * 30)
        print(f"Content Length: {result['content_length']:,} characters")
        print(f"Articles Processed: {result.get('total_articles', 0)}")
        print(f"IOCs Found: {result.get('total_iocs', 0)}")
        print(f"Unique Sources: {result.get('unique_sources', 0)}")

    if result.get('generated_tags_count'):
        print(f"Tags Generated: {result['generated_tags_count']}")

    # Print generation method
    if result.get('generation_method'):
        method = result['generation_method'].title()
        print(f"Generation Method: {method}")

    # Print error if any
    if result.get('error'):
        print(f"\n⚠️  WARNING")
        print("-" * 30)
        print(f"Error: {result['error']}")

    print(f"\n🎉 Enhanced blog generation completed!")


if __name__ == "__main__":
    main()