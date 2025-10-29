#!/usr/bin/env python3
"""Enhanced content fetcher with robust timeout mechanisms for GitHub Actions."""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import signal
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from src.json_storage import JSONStorage
from src.json_processing import JSONProcessing


class ContentEnhancementTimeout(Exception):
    """Custom exception for content enhancement timeout."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise ContentEnhancementTimeout("Content enhancement timed out")


def enhance_single_article_with_timeout(processor, article_id, timeout_seconds=60):
    """Enhance a single article with timeout protection.

    Args:
        processor: JSONProcessing instance
        article_id: Article ID to enhance
        timeout_seconds: Maximum time to spend on this article

    Returns:
        Enhancement result or timeout error
    """
    def enhance_article():
        try:
            from src.content_fetcher import fetch_article_content
            article = processor.storage.get_article(article_id)
            if not article:
                return {'success': False, 'error': 'Article not found'}

            print(f"🔍 Enhancing: {article['title'][:50]}...")

            # Fetch content with timeout
            result = fetch_article_content(article['url'])

            if result and result.get('success') and result.get('content'):
                # Store enhanced content
                success = processor.storage.enhance_article_content(
                    article_id=article_id,
                    full_content=result['content'],
                    fetch_method=result.get('method', 'unknown')
                )
                if success:
                    print(f"  ✅ Enhanced {len(result['content'])} characters ({result.get('method', 'unknown')})")
                    return {
                        'success': True,
                        'article_id': article_id,
                        'content_length': len(result['content']),
                        'method': result.get('method', 'unknown')
                    }
                else:
                    print(f"  ❌ Failed to store enhanced content")
                    return {'success': False, 'article_id': article_id, 'error': 'Storage failed'}
            else:
                print(f"  ❌ Failed to fetch content: {result.get('error', 'Unknown error') if result else 'No result'}")
                return {'success': False, 'article_id': article_id, 'error': result.get('error', 'Unknown error') if result else 'No result'}

        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
            return {'success': False, 'article_id': article_id, 'error': str(e)}

    # Use thread-based timeout for better cross-platform compatibility
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(enhance_article)
        try:
            return future.result(timeout=timeout_seconds)
        except FutureTimeoutError:
            print(f"  ⏰ TIMEOUT after {timeout_seconds}s - skipping URL")
            return {'success': False, 'article_id': article_id, 'error': f'Timeout after {timeout_seconds}s'}


def main():
    """Enhanced content enhancement with timeout protection and progress tracking."""
    print("🚀 ENHANCED CONTENT ENHANCEMENT WITH TIMEOUTS")
    print("=" * 50)

    # Configuration
    MAX_ARTICLES = 50
    PER_ARTICLE_TIMEOUT = 45  # seconds per article
    OVERALL_TIMEOUT = 1800    # 30 minutes total

    start_time = time.time()

    # Set up signal handler for overall timeout
    def overall_timeout_handler(signum, frame):
        elapsed = time.time() - start_time
        raise ContentEnhancementTimeout(f"Overall content enhancement timed out after {elapsed:.1f}s")

    signal.signal(signal.SIGALRM, overall_timeout_handler)
    signal.alarm(OVERALL_TIMEOUT)

    try:
        processor = JSONProcessing()

        # Get articles needing enhancement
        articles = processor._get_articles_for_enhancement(limit=MAX_ARTICLES)

        if not articles:
            print("ℹ️  No articles need content enhancement")
            return

        print(f"📊 Found {len(articles)} articles to enhance")
        print(f"⏱️  Per-article timeout: {PER_ARTICLE_TIMEOUT}s")
        print(f"⏱️  Overall timeout: {OVERALL_TIMEOUT}s")
        print()

        stats = {
            'total_articles': len(articles),
            'enhanced_articles': 0,
            'failed_articles': 0,
            'timeout_articles': 0,
            'start_time': start_time,
            'articles': []
        }

        # Process articles with individual timeouts
        for i, article in enumerate(articles, 1):
            elapsed = time.time() - start_time
            remaining_time = OVERALL_TIMEOUT - elapsed

            if remaining_time <= 0:
                print(f"⏰ Overall timeout reached, stopping ({len(articles) - i + 1} articles remaining)")
                break

            print(f"[{i}/{len(articles)}] Article {article['id']} (elapsed: {elapsed:.1f}s, remaining: {remaining_time:.1f}s)")

            # Adjust per-article timeout based on remaining time
            article_timeout = min(PER_ARTICLE_TIMEOUT, remaining_time - 10)  # Leave 10s buffer

            result = enhance_single_article_with_timeout(
                processor,
                article['id'],
                timeout_seconds=article_timeout
            )

            if result['success']:
                stats['enhanced_articles'] += 1
            elif 'timeout' in result.get('error', '').lower():
                stats['timeout_articles'] += 1
            else:
                stats['failed_articles'] += 1

            stats['articles'].append(result)

        # Final summary
        total_elapsed = time.time() - start_time
        print("\n" + "=" * 50)
        print("📊 CONTENT ENHANCEMENT SUMMARY")
        print("=" * 50)
        print(f"⏱️  Total time: {total_elapsed:.1f}s")
        print(f"📰 Total articles: {stats['total_articles']}")
        print(f"✅ Successfully enhanced: {stats['enhanced_articles']}")
        print(f"❌ Failed (errors): {stats['failed_articles']}")
        print(f"⏰ Failed (timeouts): {stats['timeout_articles']}")

        success_rate = (stats['enhanced_articles'] / stats['total_articles']) * 100 if stats['total_articles'] > 0 else 0
        print(f"📈 Success rate: {success_rate:.1f}%")

        if stats['enhanced_articles'] > 0:
            print("\n🎉 Content enhancement completed successfully!")
            print(f"📝 Enhanced articles are ready for LLM processing")
        else:
            print("\n⚠️  No articles were enhanced")

        # Show failed articles for debugging
        failed_articles = [a for a in stats['articles'] if not a['success']]
        if failed_articles:
            print(f"\n🔍 Failed articles ({len(failed_articles)}):")
            for article in failed_articles[:5]:  # Show first 5
                error = article.get('error', 'Unknown error')[:50]
                print(f"  • {article['article_id']}: {error}")
            if len(failed_articles) > 5:
                print(f"  ... and {len(failed_articles) - 5} more")

    except ContentEnhancementTimeout as e:
        elapsed = time.time() - start_time
        print(f"\n⏰ CONTENT ENHANCEMENT TIMEOUT: {e}")
        print(f"   Processed for {elapsed:.1f}s before timeout")
        sys.exit(1)
    except KeyboardInterrupt:
        elapsed = time.time() - start_time
        print(f"\n🛑 Content enhancement interrupted by user (after {elapsed:.1f}s)")
        sys.exit(1)
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n💥 Unexpected error during content enhancement: {e}")
        print(f"   Occurred after {elapsed:.1f}s")
        sys.exit(1)
    finally:
        signal.alarm(0)  # Cancel the alarm


if __name__ == "__main__":
    main()