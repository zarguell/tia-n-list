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
from src.workflow_config import get_workflow_config
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
        config = get_workflow_config()

        # Get and validate configuration
        min_content_length, default_score = _get_and_validate_config(config)

        print(f"📋 Using min_content_length={min_content_length}, default_score={default_score}")

        # Get today's articles
        articles = storage.get_articles_by_date_range(start_date=date.today(), end_date=date.today())
        print(f'Found {len(articles)} articles to filter')

        if not articles:
            print("ℹ️  No articles found for today")
            return 0

        # Process articles for relevance
        relevant_count = _process_articles_for_relevance(
            articles, storage, registry, min_content_length, default_score
        )

        print(f'✅ Processed {relevant_count} relevant articles')
        return relevant_count

    except Exception as e:
        print(f"❌ Error in simple article processing: {e}")
        return 1


def _get_and_validate_config(config) -> tuple[int, int]:
    """Get and validate configuration values with sensible defaults."""
    workflow_settings = config.get_workflow_settings()
    min_content_length = _validate_config_value(
        workflow_settings.get('min_content_length', 200),
        'min_content_length', 200, positive=True
    )
    default_score = _validate_config_value(
        workflow_settings.get('default_article_score', 50),
        'default_score', 50, positive=False
    )
    return min_content_length, default_score


def _validate_config_value(value, name: str, default: int, positive: bool = False) -> int:
    """Validate a configuration value and return a safe default if invalid."""
    try:
        int_value = int(value)
        if positive and int_value <= 0:
            print(f"⚠️  Invalid {name}: {int_value}, using default {default}")
            return default
        if not positive and int_value < 0:
            print(f"⚠️  Invalid {name}: {int_value}, using default {default}")
            return default
        return int_value
    except (ValueError, TypeError):
        print(f"⚠️  Invalid {name} type, using default {default}")
        return default


def _process_articles_for_relevance(articles, storage, registry,
                                  min_content_length: int, default_score: int) -> int:
    """Process articles for relevance filtering."""
    relevant_count = 0

    for article in articles:
        if _is_article_suitable_for_processing(article, min_content_length):
            if _process_single_article(article, storage, registry, default_score):
                relevant_count += 1

    return relevant_count


def _is_article_suitable_for_processing(article, min_content_length: int) -> bool:
    """Check if article has sufficient content for processing."""
    content = (
        article.get('content', {}).get('raw', '') or
        article.get('content', {}).get('processed', '')
    )
    return len(content) > min_content_length


def _process_single_article(article, storage, registry, default_score: int) -> bool:
    """Process a single article for relevance."""
    try:
        is_relevant = registry.execute_with_fallback(
            'is_relevant_article',
            article=article
        )

        if is_relevant:
            storage.update_article_status(
                article.get('id') or article.get('guid'),
                'processed',
                {'score': default_score, 'processed_at': date.today().isoformat()}
            )
            return True

        return False

    except Exception as e:
        print(f"Warning: Failed to process article {article.get('id', 'unknown')}: {e}")
        return False


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