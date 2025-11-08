#!/usr/bin/env python3
"""
Simple article processing workflow for GitHub Actions.
Replaces inline Python code in workflow with dedicated module.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.storage_registry import get_default_storage_provider
from src.llm_registry import get_registry
from datetime import date


def process_simple_articles():
    """
    Process articles with simple relevance filtering.
    This replaces the complex processing pipeline with a streamlined approach.
    """
    print("🧠 Starting simple LLM processing (relevance filtering only)...")
    print(f"Using LLM provider: {os.getenv('LLM_PROVIDER', 'openrouter')}")
    print(f"📊 Processing articles for relevance (no complex IOC extraction)")

    try:
        storage = get_default_storage_provider()
        registry = get_registry()

        # Get today's articles
        articles = storage.get_articles_by_date_range(start_date=date.today(), end_date=date.today())
        print(f'Found {len(articles)} articles to filter')

        if not articles:
            print("ℹ️  No articles found for today")
            return 0

        # Filter for relevance using simple approach
        relevant_articles = []
        for article in articles:
            content = article.get('content', {}).get('raw', '') or article.get('content', {}).get('processed', '')
            if len(content) > 200:  # Basic quality check
                # Simple relevance check
                try:
                    is_relevant = registry.execute_with_fallback(
                        'is_relevant_article',
                        article=article
                    )
                    if is_relevant:
                        # Mark as processed
                        storage.update_article_status(
                            article.get('id') or article.get('guid'),
                            'processed',
                            {'score': 50, 'processed_at': date.today().isoformat()}
                        )
                        relevant_articles.append(article)
                except Exception as e:
                    print(f"Warning: Failed to process article {article.get('id', 'unknown')}: {e}")
                    continue

        print(f'✅ Processed {len(relevant_articles)} relevant articles')
        return len(relevant_articles)

    except Exception as e:
        print(f"❌ Error in simple article processing: {e}")
        return 1


def main():
    """Main entry point for simple article processing."""
    print("🚀 Simple Article Processing Workflow")
    print("=" * 50)

    result = process_simple_articles()

    if result == 0:
        print("\n✅ Simple processing completed successfully")
    elif result > 0:
        print(f"\n✅ Simple processing completed - {result} articles processed")
    else:
        print(f"\n❌ Simple processing failed")
        return 1

    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())