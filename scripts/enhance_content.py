#!/usr/bin/env python3
"""Content enhancement script for Tia N. List project.

This script enhances RSS articles by fetching full content from URLs
using the modular content fetching system.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src import database
from src.content_fetcher import fetch_article_content


def enhance_articles(limit: int = 10, dry_run: bool = False) -> dict:
    """Enhance articles with short RSS content by fetching full content.

    Args:
        limit: Maximum number of articles to enhance.
        dry_run: If True, don't actually update the database.

    Returns:
        Dictionary with enhancement statistics.
    """
    # Get articles that need content enhancement
    articles = database.get_articles_needing_content_enhancement(limit)

    if not articles:
        return {
            'total_articles': 0,
            'enhanced': 0,
            'failed': 0,
            'skipped': 0,
            'articles': []
        }

    print(f"Found {len(articles)} articles needing content enhancement")

    stats = {
        'total_articles': len(articles),
        'enhanced': 0,
        'failed': 0,
        'skipped': 0,
        'articles': []
    }

    for article in articles:
        article_id = article['id']
        title = article['title'][:50] + "..." if len(article['title']) > 50 else article['title']
        current_length = len(article.get('raw_content', ''))

        print(f"\nProcessing: {title}")
        print(f"  Current content length: {current_length} chars")

        # Fetch full content
        result = fetch_article_content(article['url'])

        if result['success']:
            new_content = result['content']
            new_length = len(new_content)
            method = result['method']

            # Check if content is actually better
            if new_length > current_length * 1.5:  # At least 50% improvement
                print(f"  ✅ Enhanced with {method}: {current_length} → {new_length} chars")

                if not dry_run:
                    success = database.update_article_content(article_id, new_content, method)
                    if success:
                        stats['enhanced'] += 1
                    else:
                        stats['failed'] += 1
                        print(f"  ❌ Failed to update database")
                else:
                    print(f"  🧪 DRY RUN: Would update with {method}")
                    stats['enhanced'] += 1

                stats['articles'].append({
                    'id': article_id,
                    'title': title,
                    'old_length': current_length,
                    'new_length': new_length,
                    'method': method,
                    'improvement': new_length - current_length
                })
            else:
                print(f"  ⏭️ Skipped: Not enough improvement ({current_length} → {new_length})")
                stats['skipped'] += 1
        else:
            print(f"  ❌ Failed to fetch content: {result['error']}")
            stats['failed'] += 1

    return stats


def print_summary(stats: dict) -> None:
    """Print enhancement summary.

    Args:
        stats: Statistics dictionary from enhance_articles().
    """
    print(f"\n{'='*50}")
    print("CONTENT ENHANCEMENT SUMMARY")
    print(f"{'='*50}")
    print(f"Total articles processed: {stats['total_articles']}")
    print(f"Successfully enhanced: {stats['enhanced']}")
    print(f"Failed to enhance: {stats['failed']}")
    print(f"Skipped (no improvement): {stats['skipped']}")

    if stats['articles']:
        print(f"\nTop improvements:")
        # Sort by improvement amount
        sorted_articles = sorted(stats['articles'], key=lambda x: x['improvement'], reverse=True)
        for article in sorted_articles[:5]:
            print(f"  {article['title']}")
            print(f"    {article['old_length']} → {article['new_length']} chars (+{article['improvement']})")
            print(f"    Method: {article['method']}")


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Enhance article content with full web scraping")
    parser.add_argument("--limit", type=int, default=10, help="Maximum articles to enhance")
    parser.add_argument("--dry-run", action="store_true", help="Don't update database, just show what would happen")
    parser.add_argument("--source", choices=['rss', 'scraped'], help="Filter by content source")

    args = parser.parse_args()

    # Initialize database
    database.initialize_database()

    if args.source:
        # Show articles by content source
        articles = database.get_articles_by_content_source(args.source, args.limit)
        print(f"Found {len(articles)} articles with content_source='{args.source}'")
        for article in articles:
            title = article['title'][:50] + "..." if len(article['title']) > 50 else article['title']
            print(f"  {title} ({len(article.get('raw_content', ''))} chars)")
        return

    # Run content enhancement
    print("Starting content enhancement...")
    stats = enhance_articles(limit=args.limit, dry_run=args.dry_run)

    # Print summary
    print_summary(stats)

    if stats['enhanced'] > 0 and not args.dry_run:
        print(f"\n✅ Successfully enhanced {stats['enhanced']} articles!")
        print("These articles are now ready for improved LLM processing.")
    elif args.dry_run:
        print(f"\n🧪 DRY RUN: Would have enhanced {stats['enhanced']} articles.")
        print("Run without --dry-run to actually update the database.")


if __name__ == "__main__":
    main()