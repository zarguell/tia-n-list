"""JSON-based LLM processing module for Tia N. List project.

This module handles AI processing of articles using the multi-provider LLM system,
storing results in JSON format for better git tracking and version control.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, timezone
import json

from .json_storage import JSONStorage
from .llm_client_multi import MultiLLMClient


class JSONProcessing:
    """JSON-based LLM processing system."""

    def __init__(self, storage: JSONStorage = None, llm_client: MultiLLMClient = None):
        """Initialize processing with JSON storage and LLM client."""
        self.storage = storage or JSONStorage()
        self.llm_client = llm_client or MultiLLMClient()

    def process_articles(self, article_ids: List[str] = None,
                        batch_size: int = 10,
                        dry_run: bool = False) -> Dict[str, Any]:
        """Process articles with LLM analysis and IOC extraction.

        Args:
            article_ids: List of article IDs to process. If None, process unprocessed articles.
            batch_size: Number of articles to process in each batch.
            dry_run: If True, analyze without updating storage.

        Returns:
            Dictionary with processing statistics.
        """
        # Get articles to process
        if article_ids is None:
            articles = self._get_unprocessed_articles(limit=50)
        else:
            articles = []
            for article_id in article_ids:
                article = self.storage.get_article(article_id)
                if article:
                    articles.append(article)

        if not articles:
            return {
                'total_articles': 0,
                'processed_articles': 0,
                'rejected_articles': 0,
                'failed_articles': 0,
                'batches_processed': 0,
                'articles': []
            }

        print(f"Starting LLM processing for {len(articles)} articles...")

        stats = {
            'total_articles': len(articles),
            'processed_articles': 0,
            'rejected_articles': 0,
            'failed_articles': 0,
            'batches_processed': 0,
            'articles': []
        }

        # Process articles in batches
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            batch_results = self._process_article_batch(batch, dry_run=dry_run)

            # Update statistics
            stats['processed_articles'] += batch_results['processed']
            stats['rejected_articles'] += batch_results['rejected']
            stats['failed_articles'] += batch_results['failed']
            stats['batches_processed'] += 1
            stats['articles'].extend(batch_results['articles'])

            print(f"Batch {i//batch_size + 1}: {batch_results['processed']} processed, "
                  f"{batch_results['rejected']} rejected, {batch_results['failed']} failed")

        print(f"Processing completed:")
        print(f"  Total articles: {stats['total_articles']}")
        print(f"  Successfully processed: {stats['processed_articles']}")
        print(f"  Rejected (not relevant): {stats['rejected_articles']}")
        print(f"  Failed (errors): {stats['failed_articles']}")

        return stats

    def process_single_article(self, article_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Process a single article.

        Args:
            article_id: ID of the article to process.
            dry_run: If True, analyze without updating storage.

        Returns:
            Dictionary with processing results for this article.
        """
        article = self.storage.get_article(article_id)
        if not article:
            return {
                'article_id': article_id,
                'success': False,
                'error': 'Article not found'
            }

        print(f"Processing single article: {article['title']} ({article_id})")

        # Get best available content
        content = article.get("content", {})
        article_content = content.get("full") or content.get("raw", "")

        if not article_content.strip():
            return {
                'article_id': article_id,
                'success': False,
                'error': 'No content available for processing'
            }

        try:
            # Perform relevance filtering and analysis
            processed_data = self._analyze_article(article, article_content)

            if dry_run:
                return {
                    'article_id': article_id,
                    'success': True,
                    'dry_run': True,
                    'processed_data': processed_data
                }

            # Store results
            success = self._store_processing_results(article_id, processed_data)

            return {
                'article_id': article_id,
                'success': success,
                'processed_data': processed_data
            }

        except Exception as e:
            print(f"Error processing article {article_id}: {e}")
            return {
                'article_id': article_id,
                'success': False,
                'error': str(e)
            }

    def enhance_articles_content(self, article_ids: List[str] = None,
                               max_articles: int = 50) -> Dict[str, Any]:
        """Enhance articles with full web content before processing.

        Args:
            article_ids: List of article IDs to enhance. If None, enhance fetched articles.
            max_articles: Maximum number of articles to enhance.

        Returns:
            Dictionary with enhancement statistics.
        """
        # Get articles that need content enhancement
        if article_ids is None:
            articles = self._get_articles_for_enhancement(limit=max_articles)
        else:
            articles = []
            for article_id in article_ids:
                article = self.storage.get_article(article_id)
                if article and self._needs_content_enhancement(article):
                    articles.append(article)

        if not articles:
            return {
                'total_articles': 0,
                'enhanced_articles': 0,
                'failed_articles': 0,
                'articles': []
            }

        print(f"Starting content enhancement for {len(articles)} articles...")

        from .content_fetcher import fetch_article_content

        stats = {
            'total_articles': len(articles),
            'enhanced_articles': 0,
            'failed_articles': 0,
            'articles': []
        }

        for article in articles:
            try:
                print(f"Enhancing content for: {article['title'][:50]}...")

                # Fetch full content
                result = fetch_article_content(article['url'])

                if result and result.get('success') and result.get('content'):
                    # Update article with enhanced content
                    success = self.storage.enhance_article_content(
                        article_id=article['id'],
                        full_content=result['content'],
                        fetch_method=result.get('method', 'unknown')
                    )

                    if success:
                        stats['enhanced_articles'] += 1
                        print(f"  ✅ Enhanced {len(result['content'])} characters")
                    else:
                        stats['failed_articles'] += 1
                        print(f"  ❌ Failed to store enhanced content")
                else:
                    stats['failed_articles'] += 1
                    print(f"  ❌ Failed to fetch content")

                stats['articles'].append({
                    'article_id': article['id'],
                    'title': article['title'],
                    'success': result.get('success', False) if result else False,
                    'content_length': len(result.get('content', '')) if result else 0
                })

            except Exception as e:
                stats['failed_articles'] += 1
                print(f"  ❌ Error enhancing content: {e}")

        print(f"Content enhancement completed:")
        print(f"  Total articles: {stats['total_articles']}")
        print(f"  Successfully enhanced: {stats['enhanced_articles']}")
        print(f"  Failed: {stats['failed_articles']}")

        return stats

    def _get_unprocessed_articles(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get articles that haven't been processed yet."""
        # Get recent articles that are still in 'fetched' status
        recent_articles = self.storage.get_recent_articles(days=3, status="fetched", limit=limit)
        return recent_articles

    def _get_articles_for_enhancement(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get articles that need content enhancement."""
        recent_articles = self.storage.get_recent_articles(days=3, status="fetched", limit=limit)
        return [a for a in recent_articles if self._needs_content_enhancement(a)]

    def _needs_content_enhancement(self, article: Dict[str, Any]) -> bool:
        """Check if article needs content enhancement."""
        content = article.get("content", {})

        # Needs enhancement if no full content and raw content is short
        has_full_content = bool(content.get("full", "").strip())
        raw_content = content.get("raw", "")

        return not has_full_content and len(raw_content) < 2000

    def _process_article_batch(self, articles: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
        """Process a batch of articles."""
        batch_stats = {
            'processed': 0,
            'rejected': 0,
            'failed': 0,
            'articles': []
        }

        # Prepare batch data for LLM processing
        batch_data = []
        for article in articles:
            content = article.get("content", {})
            article_content = content.get("full") or content.get("raw", "")

            if article_content.strip():
                batch_data.append({
                    'id': article['id'],
                    'title': article['title'],
                    'content': article_content[:2000],  # Limit content for processing
                    'url': article['url']
                })

        if not batch_data:
            return batch_stats

        try:
            # Perform batch relevance filtering and analysis
            analysis_results = self._batch_analyze_articles(batch_data)

            # Process results
            for i, article in enumerate(articles):
                if i < len(analysis_results):
                    result = analysis_results[i]

                    article_result = {
                        'article_id': article['id'],
                        'title': article['title'],
                        'success': False,
                        'status': 'unknown'
                    }

                    try:
                        if result.get('is_relevant', False):
                            # Article is relevant, extract IOCs and store
                            if not dry_run:
                                success = self._store_processing_results(article['id'], result)
                                article_result['success'] = success
                            else:
                                article_result['success'] = True
                                article_result['dry_run'] = True

                            article_result['status'] = 'processed'
                            batch_stats['processed'] += 1
                        else:
                            # Article is not relevant
                            if not dry_run:
                                self.storage.update_article(article['id'], status='rejected')

                            article_result['status'] = 'rejected'
                            batch_stats['rejected'] += 1

                        article_result['analysis'] = {
                            'relevance_score': result.get('relevance_score', 0),
                            'threat_category': result.get('threat_category'),
                            'score': result.get('score', 0)
                        }

                    except Exception as e:
                        batch_stats['failed'] += 1
                        article_result['error'] = str(e)

                    batch_stats['articles'].append(article_result)

        except Exception as e:
            print(f"Error processing batch: {e}")
            # Mark all as failed
            for article in articles:
                batch_stats['failed'] += 1
                batch_stats['articles'].append({
                    'article_id': article['id'],
                    'title': article['title'],
                    'success': False,
                    'error': 'Batch processing failed'
                })

        return batch_stats

    def _analyze_article(self, article: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Analyze a single article with LLM."""
        # Prepare analysis prompt
        prompt = self._create_analysis_prompt(article['title'], content)

        try:
            response = self.llm_client.generate_structured(
                prompt=prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "is_relevant": {"type": "boolean"},
                        "relevance_score": {"type": "number", "minimum": 0, "maximum": 100},
                        "threat_category": {
                            "type": "string",
                            "enum": ["malware", "phishing", "vulnerability", "data-breach",
                                   "network-security", "ransomware", "supply-chain", "other"]
                        },
                        "score": {"type": "number", "minimum": 0, "maximum": 100},
                        "summary": {"type": "string"},
                        "key_entities": {"type": "array", "items": {"type": "string"}},
                        "ttps": {"type": "array", "items": {"type": "string"}},
                        "processed_content": {"type": "string"},
                        "iocs": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "value": {"type": "string"},
                                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                                    "context": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["is_relevant", "relevance_score"]
                }
            )

            return response if response else {"is_relevant": False, "relevance_score": 0}

        except Exception as e:
            print(f"LLM analysis error: {e}")
            return {"is_relevant": False, "relevance_score": 0, "error": str(e)}

    def _batch_analyze_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple articles in batch."""
        # Prepare batch prompt
        batch_prompt = self._create_batch_analysis_prompt(articles)

        try:
            response = self.llm_client.generate_structured(
                prompt=batch_prompt,
                schema={
                    "type": "object",
                    "properties": {
                        "articles": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "is_relevant": {"type": "boolean"},
                                    "relevance_score": {"type": "number", "minimum": 0, "maximum": 100},
                                    "threat_category": {"type": "string"},
                                    "score": {"type": "number", "minimum": 0, "maximum": 100},
                                    "summary": {"type": "string"},
                                    "key_entities": {"type": "array", "items": {"type": "string"}},
                                    "ttps": {"type": "array", "items": {"type": "string"}},
                                    "iocs": {"type": "array", "items": {"type": "object"}}
                                }
                            }
                        }
                    }
                }
            )

            if response and 'articles' in response:
                return response['articles']
            else:
                # Fallback: process individually
                results = []
                for article in articles:
                    result = self._analyze_article(article, article['content'])
                    result['id'] = article['id']
                    results.append(result)
                return results

        except Exception as e:
            print(f"Batch analysis error: {e}")
            # Fallback: return all as not relevant
            return [{"id": a['id'], "is_relevant": False, "relevance_score": 0} for a in articles]

    def _store_processing_results(self, article_id: str, processed_data: Dict[str, Any]) -> bool:
        """Store processing results in JSON storage."""
        try:
            # Extract IOCs
            iocs = processed_data.get('iocs', [])

            # Prepare analysis data
            analysis = {
                'score': processed_data.get('score', 0),
                'relevance_score': processed_data.get('relevance_score', 0),
                'threat_category': processed_data.get('threat_category'),
                'summary': processed_data.get('summary'),
                'key_entities': processed_data.get('key_entities', []),
                'ttps': processed_data.get('ttps', [])
            }

            # Prepare processed content
            processed_content = processed_data.get('processed_content', '')

            # Prepare processing metadata
            processing_metadata = {
                'processed_at': datetime.now(timezone.utc).isoformat() + "Z",
                'llm_provider': getattr(self.llm_client, 'current_provider', 'unknown'),
                'processing_method': 'json_processing'
            }

            # Store results
            success = self.storage.process_article(
                article_id=article_id,
                processed_content=processed_content,
                analysis=analysis,
                iocs=iocs,
                processing_metadata=processing_metadata
            )

            return success

        except Exception as e:
            print(f"Error storing processing results for {article_id}: {e}")
            return False

    def _create_analysis_prompt(self, title: str, content: str) -> str:
        """Create analysis prompt for single article."""
        return f"""Analyze this cybersecurity article for relevance and extract threat intelligence.

TITLE: {title}

CONTENT: {content[:3000]}

Please analyze and provide:
1. Relevance assessment (is this cybersecurity-related?)
2. Relevance score (0-100)
3. Threat category if applicable
4. Quality score (0-100)
5. Brief summary
6. Key entities mentioned
7. Tactics, techniques, and procedures (TTPs)
8. Processed content (cleaned, key information only)
9. Any indicators of compromise (IOCs) found

Focus on actionable threat intelligence and security insights."""

    def _create_batch_analysis_prompt(self, articles: List[Dict[str, Any]]) -> str:
        """Create batch analysis prompt for multiple articles."""
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"""
Article {i}:
ID: {article['id']}
Title: {article['title']}
Content: {article['content'][:1500]}
---
"""

        return f"""Analyze these {len(articles)} cybersecurity articles for relevance and extract threat intelligence.

{articles_text}

For each article, provide:
1. Relevance assessment (is this cybersecurity-related?)
2. Relevance score (0-100)
3. Threat category if applicable
4. Quality score (0-100)
5. Brief summary
6. Key entities mentioned
7. Tactics, techniques, and procedures (TTPs)
8. Any indicators of compromise (IOCs) found

Focus on actionable threat intelligence and security insights."""


# Global processing instance
processor = JSONProcessing()


def main():
    """Main function for standalone execution."""
    print("Starting JSON-based LLM processing...")

    # First enhance content
    enhancement_stats = processor.enhance_articles_content(max_articles=20)
    print(f"Content enhancement: {enhancement_stats}")

    # Then process articles
    processing_stats = processor.process_articles(batch_size=5)
    print(f"Processing completed: {processing_stats}")


if __name__ == "__main__":
    main()