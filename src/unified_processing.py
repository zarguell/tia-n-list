"""Unified LLM processing module for Tia N. List project.

This module handles AI processing of articles using the multi-provider LLM system,
using the storage provider abstraction to support multiple storage backends.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, timezone
import json

from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider
from .llm_registry import get_registry


class UnifiedProcessing:
    """Unified LLM processing system using storage provider abstraction."""

    def __init__(self, storage: StorageProvider = None, llm_registry=None):
        """Initialize processing with storage provider and LLM registry."""
        self.storage = storage or get_default_storage_provider()
        self.llm_registry = llm_registry or get_registry()

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
            articles = self.storage.get_unprocessed_articles(limit=50)
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
                'total_iocs': 0,
                'processing_time': 0,
                'articles': []
            }

        print(f"Processing {len(articles)} articles with LLM analysis...")

        # Process articles in batches
        all_results = []
        total_iocs = 0
        processed_count = 0
        rejected_count = 0

        start_time = datetime.now()

        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            print(f"\nProcessing batch {i//batch_size + 1}/{(len(articles) + batch_size - 1)//batch_size}")

            batch_results = self._process_article_batch(batch, dry_run)
            all_results.extend(batch_results)

            # Update statistics
            for result in batch_results:
                if result['status'] == 'processed':
                    processed_count += 1
                    total_iocs += result.get('ioc_count', 0)
                elif result['status'] == 'rejected':
                    rejected_count += 1

        processing_time = (datetime.now() - start_time).total_seconds()

        stats = {
            'total_articles': len(articles),
            'processed_articles': processed_count,
            'rejected_articles': rejected_count,
            'total_iocs': total_iocs,
            'processing_time': processing_time,
            'articles': all_results
        }

        print(f"\nProcessing completed:")
        print(f"  Articles processed: {processed_count}/{len(articles)}")
        print(f"  Articles rejected: {rejected_count}")
        print(f"  Total IOCs extracted: {total_iocs}")
        print(f"  Processing time: {processing_time:.2f} seconds")

        return stats

    def _process_article_batch(self, articles: List[Dict[str, Any]], dry_run: bool = False) -> List[Dict[str, Any]]:
        """Process a batch of articles.

        Args:
            articles: List of article data dictionaries.
            dry_run: If True, analyze without updating storage.

        Returns:
            List of processing results.
        """
        results = []

        for article in articles:
            result = {
                'article_id': article['id'],
                'title': article['title'],
                'source_id': article['source_id'],
                'status': 'pending',
                'error': None,
                'ioc_count': 0,
                'analysis': None,
                'iocs': []
            }

            try:
                # Get article content
                content = self._get_article_content(article)

                if not content or len(content.strip()) < 100:
                    result['status'] = 'rejected'
                    result['error'] = 'Insufficient content for analysis'
                    results.append(result)
                    continue

                print(f"  Processing: {article['title'][:60]}...")

                # Process with LLM
                analysis_result = self._analyze_article_with_llm(article, content)

                if not analysis_result:
                    result['status'] = 'rejected'
                    result['error'] = 'LLM analysis failed'
                    results.append(result)
                    continue

                # Extract IOCs
                iocs = analysis_result.get('iocs', [])
                result['ioc_count'] = len(iocs)
                result['analysis'] = analysis_result.get('analysis', {})
                result['iocs'] = iocs

                # Update storage (unless dry run)
                if not dry_run:
                    success = self.storage.process_article(
                        article_id=article['id'],
                        processed_content=analysis_result.get('processed_content', ''),
                        analysis=analysis_result.get('analysis', {}),
                        iocs=iocs,
                        processing_metadata={
                            'processed_at': datetime.now(datetime.UTC).isoformat(),
                            'llm_provider': analysis_result.get('llm_provider'),
                            'model': analysis_result.get('model'),
                            'processing_time': analysis_result.get('processing_time')
                        }
                    )

                    if success:
                        result['status'] = 'processed'
                    else:
                        result['status'] = 'error'
                        result['error'] = 'Failed to update storage'
                else:
                    result['status'] = 'processed'  # Assume success for dry run

            except Exception as e:
                result['status'] = 'error'
                result['error'] = str(e)
                print(f"    Error: {e}")

            results.append(result)

        return results

    def _get_article_content(self, article: Dict[str, Any]) -> str:
        """Get the best available content for an article.

        Args:
            article: Article data dictionary.

        Returns:
            Best available content string.
        """
        # Try full content first, then processed content, then raw content
        content_data = article.get('content', {})

        # Priority: full > processed > raw
        for content_type in ['full', 'processed', 'raw']:
            content = content_data.get(content_type, '')
            if content and len(content.strip()) > 100:
                return content

        return ''

    def _analyze_article_with_llm(self, article: Dict[str, Any], content: str) -> Optional[Dict[str, Any]]:
        """Analyze article content with LLM.

        Args:
            article: Article data dictionary.
            content: Article content to analyze.

        Returns:
            LLM analysis result or None if failed.
        """
        try:
            # Prepare analysis prompt
            analysis_prompt = self._build_analysis_prompt(article, content)

            # Get LLM response
            response = self.llm_registry.execute_with_fallback(
                'generate_text',
                prompt=analysis_prompt,
                max_tokens=2000,
                temperature=0.1
            )

            if not response:
                return None

            # Parse LLM response
            return self._parse_llm_response(response, article)

        except Exception as e:
            print(f"    LLM analysis error: {e}")
            return None

    def _build_analysis_prompt(self, article: Dict[str, Any], content: str) -> str:
        """Build analysis prompt for LLM.

        Args:
            article: Article data dictionary.
            content: Article content to analyze.

        Returns:
            Analysis prompt string.
        """
        # Truncate content if too long
        max_content_length = 3000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."

        prompt = f"""
You are a cybersecurity threat intelligence analyst. Analyze the following article for threats, vulnerabilities, and indicators of compromise.

ARTICLE TITLE: {article['title']}
SOURCE: {article['source_id']}
URL: {article['url']}

CONTENT:
{content}

Please provide:
1. A threat analysis summary (2-3 sentences)
2. Threat category (malware, phishing, vulnerability, data breach, etc.)
3. Key entities mentioned (threat actors, malware families, vulnerabilities, etc.)
4. MITRE ATT&CK techniques if applicable
5. Indicators of Compromise (IPs, domains, hashes, file names, etc.)
6. Relevance score (1-10, where 10 is highly relevant for security teams)

Respond in JSON format:
{{
    "summary": "Brief threat analysis summary",
    "threat_category": "category_name",
    "relevance_score": 8,
    "key_entities": ["entity1", "entity2"],
    "attack_techniques": ["T1190", "T1566"],
    "iocs": [
        {{"type": "domain", "value": "malicious-domain.com", "confidence": "high"}},
        {{"type": "ip", "value": "192.168.1.1", "confidence": "medium"}}
    ]
}}
"""
        return prompt

    def _parse_llm_response(self, response: str, article: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM response into structured format.

        Args:
            response: LLM response string.
            article: Original article data.

        Returns:
            Parsed analysis result.
        """
        try:
            # Try to parse as JSON
            if response.strip().startswith('{'):
                analysis_data = json.loads(response)

                # Validate required fields
                summary = analysis_data.get('summary', '')
                threat_category = analysis_data.get('threat_category', 'general')
                relevance_score = analysis_data.get('relevance_score', 5)
                key_entities = analysis_data.get('key_entities', [])
                attack_techniques = analysis_data.get('attack_techniques', [])
                iocs = analysis_data.get('iocs', [])

                # Clean and validate IOCs
                validated_iocs = []
                for ioc in iocs:
                    if isinstance(ioc, dict) and 'type' in ioc and 'value' in ioc:
                        # Basic IOC validation
                        ioc_type = ioc['type'].lower()
                        ioc_value = ioc['value'].strip()

                        if self._is_valid_ioc(ioc_type, ioc_value):
                            validated_iocs.append({
                                'type': ioc_type,
                                'value': ioc_value,
                                'confidence': ioc.get('confidence', 'medium'),
                                'context': f"Extracted from article: {article['title']}"
                            })

                return {
                    'processed_content': summary,
                    'analysis': {
                        'score': relevance_score * 10,  # Convert to 100-point scale
                        'relevance_score': relevance_score,
                        'threat_category': threat_category,
                        'summary': summary,
                        'key_entities': key_entities,
                        'ttps': attack_techniques
                    },
                    'iocs': validated_iocs
                }

        except json.JSONDecodeError:
            # Fallback: try to extract information from text response
            return self._parse_text_response(response, article)

        except Exception as e:
            print(f"    Response parsing error: {e}")
            return None

    def _parse_text_response(self, response: str, article: Dict[str, Any]) -> Dict[str, Any]:
        """Parse text-based LLM response.

        Args:
            response: LLM text response.
            article: Original article data.

        Returns:
            Parsed analysis result.
        """
        # Simple text parsing fallback
        lines = response.strip().split('\n')

        summary = ''
        relevance_score = 5

        # Try to extract summary and relevance from text
        for line in lines:
            line_lower = line.lower()
            if 'summary' in line_lower or 'analysis' in line_lower:
                summary = line.replace(':', '').strip()
            elif 'relevance' in line_lower or 'score' in line_lower:
                # Try to extract number
                import re
                numbers = re.findall(r'\d+', line)
                if numbers:
                    relevance_score = min(10, int(numbers[0]))

        return {
            'processed_content': summary or response[:200],
            'analysis': {
                'score': relevance_score * 10,
                'relevance_score': relevance_score,
                'threat_category': 'general',
                'summary': summary or response[:200],
                'key_entities': [],
                'ttps': []
            },
            'iocs': []
        }

    def _is_valid_ioc(self, ioc_type: str, ioc_value: str) -> bool:
        """Validate IOC format.

        Args:
            ioc_type: Type of IOC.
            ioc_value: IOC value.

        Returns:
            True if IOC appears valid, False otherwise.
        """
        ioc_type = ioc_type.lower()
        ioc_value = ioc_value.strip()

        if not ioc_value:
            return False

        # Basic validation by type
        if ioc_type == 'domain':
            return '.' in ioc_value and len(ioc_value) > 4
        elif ioc_type == 'ip':
            parts = ioc_value.split('.')
            return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
        elif ioc_type == 'hash':
            return len(ioc_value) in [32, 40, 64] and all(c in '0123456789abcdefABCDEF' for c in ioc_value)
        elif ioc_type == 'url':
            return ioc_value.startswith(('http://', 'https://'))
        elif ioc_type == 'email':
            return '@' in ioc_value and '.' in ioc_value.split('@')[-1]

        # Accept other types but with basic validation
        return len(ioc_value) > 2

    def process_single_article(self, article_id: str, dry_run: bool = False) -> Dict[str, Any]:
        """Process a single article.

        Args:
            article_id: ID of the article to process.
            dry_run: If True, analyze without updating storage.

        Returns:
            Processing result dictionary.
        """
        article = self.storage.get_article(article_id)
        if not article:
            return {
                'article_id': article_id,
                'success': False,
                'error': 'Article not found'
            }

        print(f"Processing single article: {article['title']}")

        result = self._process_article_batch([article], dry_run)

        if result:
            return {
                'article_id': article_id,
                'success': result[0]['status'] == 'processed',
                'status': result[0]['status'],
                'error': result[0].get('error'),
                'ioc_count': result[0].get('ioc_count', 0),
                'analysis': result[0].get('analysis'),
                'iocs': result[0].get('iocs', [])
            }
        else:
            return {
                'article_id': article_id,
                'success': False,
                'error': 'Processing failed'
            }

    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get current processing statistics."""
        return self.storage.get_statistics()

    def health_check(self) -> Dict[str, Any]:
        """Check the health of the processing system."""
        health = {
            "status": "healthy",
            "checks": {},
            "issues": []
        }

        try:
            # Check storage health
            storage_health = self.storage.health_check()
            health["checks"]["storage"] = storage_health["status"] == "healthy"

            if storage_health["status"] != "healthy":
                health["status"] = "degraded"
                health["issues"].extend(storage_health.get("issues", []))

            # Check LLM registry
            try:
                llm_info = self.llm_registry.get_provider_info()
                health["checks"]["llm_registry"] = True
                health["llm_provider"] = llm_info.get('primary_provider')
            except Exception as e:
                health["checks"]["llm_registry"] = False
                health["status"] = "degraded"
                health["issues"].append(f"LLM registry check failed: {e}")

        except Exception as e:
            health["status"] = "unhealthy"
            health["issues"].append(f"Health check failed: {e}")

        return health


# Global processing instance
unified_processing = UnifiedProcessing()


def main():
    """Main function for standalone execution."""
    print("Starting unified LLM processing...")

    stats = unified_processing.process_articles(
        batch_size=5,
        dry_run=False
    )

    print("\n=== PROCESSING SUMMARY ===")
    print(f"Articles processed: {stats['processed_articles']}/{stats['total_articles']}")
    print(f"Articles rejected: {stats['rejected_articles']}")
    print(f"Total IOCs extracted: {stats['total_iocs']}")
    print(f"Processing time: {stats['processing_time']:.2f} seconds")


if __name__ == "__main__":
    main()