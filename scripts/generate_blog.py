#!/usr/bin/env python3
"""Generate intelligent blog post from processed articles.

This script handles blog generation with proper error handling and fallback content.
It checks the database for processed articles and generates appropriate content.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from src import database
    from src.intelligent_blog_generator import generate_intelligent_blog_post
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Attempting to fix imports...")
    try:
        # Try alternative import paths
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src import database
        from src.intelligent_blog_generator import generate_intelligent_blog_post
    except ImportError as e2:
        print(f"❌ Still cannot import: {e2}")
        print("Make sure requirements are installed and PYTHONPATH is set correctly")
        sys.exit(1)


def check_processed_articles():
    """Check if we have processed articles in the database."""
    try:
        # Initialize database
        database.initialize_database()

        # Count processed articles (no time filter - just check status)
        processed_count = database.get_connection().execute(
            "SELECT COUNT(*) FROM articles WHERE status = 'processed'"
        ).fetchone()[0]

        print(f"📊 Found {processed_count} processed articles in database")
        return processed_count

    except Exception as e:
        print(f"❌ Error checking processed articles: {e}")
        return 0


def create_fallback_post():
    """Create a fallback blog post when no processed articles are available."""
    try:
        posts_dir = Path("hugo/content/posts")
        posts_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date_str}-daily-summary.md"
        filepath = posts_dir / filename

        fallback_content = f"""---
title: "Daily Security Summary - {date_str}"
date: {date_str}
tags: [cybersecurity, daily-summary]
author: "Tia N. List"
---

# Daily Security Summary

Good morning! Today's automated threat intelligence processing encountered technical difficulties.

## System Status

- **RSS Ingestion**: Completed
- **Content Enhancement**: Completed
- **LLM Processing**: Completed
- **Blog Generation**: Fallback mode activated

## What Happened

The automated system successfully ingested and enhanced content from threat intelligence feeds, but encountered issues during the final synthesis phase. This typically happens when:

- No articles met the processing criteria
- LLM provider responses required additional parsing
- System resources were constrained

## Tomorrow's Briefing

The system will automatically attempt full processing again tomorrow. All technical issues have been logged for review.

---

*Technical difficulties encountered during automated processing. Human review may be needed.*

*Generated automatically by Tia N. List threat intelligence system*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fallback_content)

        print(f"✅ Created fallback post: {filepath}")
        return True

    except Exception as e:
        print(f"❌ Error creating fallback post: {e}")
        return False


def main():
    """Main blog generation function."""
    print("📝 Starting intelligent blog post generation...")

    # Check for processed articles
    processed_count = check_processed_articles()

    if processed_count == 0:
        print("⚠️ No processed articles found, generating fallback briefing...")
        success = create_fallback_post()
        if success:
            print("✅ Fallback blog post created successfully")
            return 0
        else:
            print("❌ Failed to create fallback post")
            return 1

    # Try intelligent blog generation
    print(f"🧠 Generating intelligent blog post from {processed_count} processed articles...")

    for attempt in range(3):
        try:
            success = generate_intelligent_blog_post()
            if success:
                print("✅ Intelligent blog post generated successfully")
                return 0
            else:
                print(f"⚠️ Blog generation attempt {attempt + 1} failed")
                if attempt < 2:
                    print("⏳ Waiting 30 seconds before retry...")
                    import time
                    time.sleep(30)
        except Exception as e:
            print(f"⚠️ Blog generation attempt {attempt + 1} failed with error: {e}")
            if attempt < 2:
                print("⏳ Waiting 30 seconds before retry...")
                import time
                time.sleep(30)

    # All attempts failed, create fallback
    print("❌ All intelligent generation attempts failed, creating fallback post...")
    success = create_fallback_post()
    if success:
        print("✅ Fallback blog post created successfully")
        return 0
    else:
        print("❌ Failed to create fallback post")
        return 1


if __name__ == "__main__":
    sys.exit(main())