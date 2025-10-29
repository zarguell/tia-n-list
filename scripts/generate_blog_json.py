#!/usr/bin/env python3
"""Generate blog posts using the JSON-based system."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.json_blog_generator import JSONBlogGenerator
from datetime import date

def main():
    """Main blog generation function."""
    print("📝 Generating JSON-based blog post...")

    generator = JSONBlogGenerator()
    result = generator.generate_daily_summary(target_date=date.today(), use_intelligent_synthesis=False)

    print(f"Blog generation completed: {result['success']}")

    if result.get('filepath'):
        print(f"✅ Blog post generated: {result['filepath']}")
        print(f"Content length: {result.get('content_length', 0)} characters")
    else:
        print("⚠️ Blog generation completed with fallback mode")

if __name__ == "__main__":
    main()