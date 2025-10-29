#!/usr/bin/env python3
"""Generate enhanced blog posts using the JSON-based system with dynamic titles and tags."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.enhanced_json_blog_generator import EnhancedJSONBlogGenerator
from datetime import date

def main():
    """Main enhanced blog generation function."""
    print("🚀 Generating enhanced blog post with dynamic titles and tags...")

    # Read environment variables for feature control
    use_dynamic_titles = os.getenv('USE_DYNAMIC_TITLES', 'true').lower() == 'true'
    use_dynamic_tags = os.getenv('USE_DYNAMIC_TAGS', 'true').lower() == 'true'

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

        if features_used:
            print(f"🎯 Features used: {', '.join(features_used)}")

        if result.get('generated_tags_count'):
            print(f"🏷️  Tags generated: {result['generated_tags_count']}")
    else:
        print("⚠️ Blog generation completed with fallback mode")

if __name__ == "__main__":
    main()