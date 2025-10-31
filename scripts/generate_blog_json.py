#!/usr/bin/env python3
"""Generate enhanced blog posts using the JSON-based system with dynamic titles and tags."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.enhanced_json_blog_generator import EnhancedJSONBlogGenerator
from src.two_tier_blog_generator import TwoTierBlogGenerator
from datetime import date

def main():
    """Main enhanced blog generation function."""
    print("🚀 Generating enhanced blog post with dynamic titles and tags...")

    # Read environment variables for feature control
    use_dynamic_titles = os.getenv('USE_DYNAMIC_TITLES', 'true').lower() == 'true'
    use_dynamic_tags = os.getenv('USE_DYNAMIC_TAGS', 'true').lower() == 'true'
    use_two_tier_analysis = os.getenv('USE_TWO_TIER_ANALYSIS', 'false').lower() == 'true'

    # Choose generator based on configuration
    if use_two_tier_analysis:
        print("🔄 Using Two-Tier Blog Generator...")
        generator = TwoTierBlogGenerator()
        result = generator.generate_daily_summary(
            target_date=date.today(),
            use_intelligent_synthesis=True,
            use_dynamic_title=use_dynamic_titles,
            use_dynamic_tags=use_dynamic_tags,
            use_two_tier_analysis=True
        )
    else:
        print("✨ Using Enhanced Blog Generator...")
        generator = EnhancedJSONBlogGenerator()
        result = generator.generate_daily_summary(
            target_date=date.today(),
            use_intelligent_synthesis=True,
            use_dynamic_title=use_dynamic_titles,
            use_dynamic_tags=use_dynamic_tags
        )

    print(f"Enhanced blog generation completed: {result['success']}")

    if result.get('filepath'):
        print(f"✅ Blog post generated: {result['filepath']}")
        print(f"Content length: {result.get('content_length', 0)} characters")

        # Print feature usage
        features_used = []
        if result.get('dynamic_title_used'):
            features_used.append("dynamic title")
        if result.get('dynamic_tags_used'):
            features_used.append("dynamic tags")
        if result.get('intelligent_synthesis_used'):
            features_used.append("intelligent synthesis")
        if result.get('two_tier_analysis_used'):
            features_used.append("two-tier analysis")

        if features_used:
            print(f"🎯 Features used: {', '.join(features_used)}")

        # Two-tier specific reporting
        if result.get('two_tier_analysis_used'):
            metadata = result.get('metadata', {})
            print(f"📊 Tier 1 success: {metadata.get('tier_1_success', False)}")
            print(f"📊 Tier 2 success: {metadata.get('tier_2_success', False)}")
            print(f"🔤 Tier 1 tokens: {metadata.get('tier_1_tokens', 0)}")
            print(f"🔤 Tier 2 tokens: {metadata.get('tier_2_tokens', 0)}")
            print(f"🔄 Fallback used: {metadata.get('fallback_used', False)}")

        if result.get('generated_tags_count'):
            print(f"🏷️  Tags generated: {result['generated_tags_count']}")
    else:
        print("⚠️ Blog generation completed with fallback mode")

if __name__ == "__main__":
    main()