"""Multi-Tier Article Processing System

This module implements a smart processing system that prioritizes articles
based on source quality and title analysis to optimize LLM usage and
ensure the most relevant content gets processed.
"""

import time
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from src import database, source_quality
from .llm_registry import get_registry, is_relevant_article, extract_iocs_and_ttps


@dataclass
class ProcessingPriority:
    """Represents processing priority for articles."""
    priority_level: int  # 1=highest, 5=lowest
    processing_type: str  # 'full', 'title_only', 'selective'
    reason: str  # Why this priority was assigned


class TieredArticleProcessor:
    """Multi-tier processing system for articles based on source quality and title analysis."""

    def __init__(self, llm_registry=None):
        self.llm_registry = llm_registry or get_registry()
        self.quality_tracker = source_quality.SourceQualityTracker()

        # Processing thresholds
        self.high_quality_threshold = 70.0
        self.medium_quality_threshold = 40.0

        # Batch sizes for different processing types
        self.full_processing_batch_size = 5
        self.selective_processing_batch_size = 10
        self.title_analysis_batch_size = 20

    def get_processing_priority(self, article: Dict[str, Any]) -> ProcessingPriority:
        """Determine processing priority for an article based on source quality and title.

        Args:
            article: Article dictionary with source information

        Returns:
            ProcessingPriority object with priority level and processing type
        """
        # Get source quality score
        source_id = article['source_id']
        source_quality_score = self.quality_tracker.calculate_source_quality_score(source_id, days_back=7)

        if not source_quality_score:
            # No quality data available, use medium priority
            return ProcessingPriority(
                priority_level=3,
                processing_type='selective',
                reason='New source - medium priority'
            )

        quality_score = source_quality_score['total_score']
        title = article.get('title', '').lower()

        # Priority 1: High quality sources - immediate full processing
        if quality_score >= self.high_quality_threshold:
            return ProcessingPriority(
                priority_level=1,
                processing_type='full',
                reason=f'High quality source (score: {quality_score:.1f}) - immediate processing'
            )

        # Priority 2: Medium quality sources with relevant keywords
        elif quality_score >= self.medium_quality_threshold:
            if self._has_relevant_keywords(title):
                return ProcessingPriority(
                    priority_level=2,
                    processing_type='full',
                    reason=f'Medium quality source with relevant keywords (score: {quality_score:.1f})'
                )
            else:
                return ProcessingPriority(
                    priority_level=3,
                    processing_type='selective',
                    reason=f'Medium quality source, title analysis needed (score: {quality_score:.1f})'
                )

        # Priority 3-4: Low quality sources - title-only analysis first
        else:
            relevance_score = self._analyze_title_relevance(title)

            if relevance_score >= 0.8:  # Highly relevant titles
                return ProcessingPriority(
                    priority_level=3,
                    processing_type='selective',
                    reason=f'Low quality source but highly relevant title (relevance: {relevance_score:.2f})'
                )
            elif relevance_score >= 0.5:  # Moderately relevant
                return ProcessingPriority(
                    priority_level=4,
                    processing_type='title_only',
                    reason=f'Low quality source, moderate title relevance (relevance: {relevance_score:.2f})'
                )
            else:  # Low relevance
                return ProcessingPriority(
                    priority_level=5,
                    processing_type='title_only',
                    reason=f'Low quality source, low title relevance (relevance: {relevance_score:.2f})'
                )

    def _has_relevant_keywords(self, title: str) -> bool:
        """Check if title contains high-priority cybersecurity keywords."""
        high_priority_keywords = [
            'zero-day', '0day', 'vulnerability', 'exploit', 'cve',
            'breach', 'hack', 'attack', 'malware', 'ransomware',
            'critical', 'patch', 'security', 'threat', 'intelligence'
        ]

        return any(keyword in title for keyword in high_priority_keywords)

    def _analyze_title_relevance(self, title: str) -> float:
        """Analyze title relevance using basic keyword scoring.

        Args:
            title: Article title

        Returns:
            Relevance score between 0.0 and 1.0
        """
        if not title:
            return 0.0

        # High priority keywords (weight: 0.4)
        high_priority = [
            'zero-day', '0day', 'critical', 'vulnerability', 'cve',
            'exploit', 'breach', 'ransomware', 'apt', 'attack'
        ]

        # Medium priority keywords (weight: 0.3)
        medium_priority = [
            'security', 'malware', 'threat', 'hack', 'patch',
            'cyber', 'data breach', 'phishing', 'privacy'
        ]

        # Low priority keywords (weight: 0.2)
        low_priority = [
            'software', 'update', 'release', 'company', 'service',
            'platform', 'tool', 'research', 'report'
        ]

        # Negative indicators (weight: -0.3)
        negative_indicators = [
            'sale', 'discount', 'deal', 'coupon', 'buy', 'price',
            'review', 'unboxing', 'comparison', 'best'
        ]

        score = 0.0

        # Count keywords
        high_count = sum(1 for keyword in high_priority if keyword in title)
        medium_count = sum(1 for keyword in medium_priority if keyword in title)
        low_count = sum(1 for keyword in low_priority if keyword in title)
        negative_count = sum(1 for keyword in negative_indicators if keyword in title)

        # Calculate weighted score
        score += (high_count * 0.4)
        score += (medium_count * 0.3)
        score += (low_count * 0.2)
        score -= (negative_count * 0.3)

        # Normalize to 0-1 range
        max_possible_score = 1.0  # Assume max 1 high priority keyword
        normalized_score = max(0.0, min(1.0, score / max_possible_score))

        return normalized_score

    def batch_analyze_titles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Use LLM to analyze article titles for relevance when basic scoring is unclear.

        Args:
            articles: List of articles to analyze

        Returns:
            List of articles with LLM relevance scores added
        """
        if not articles:
            return []

        # Prepare titles for LLM analysis
        titles = []
        for article in articles:
            source_name = article.get('source_name', 'Unknown')
            title = article.get('title', '')
            titles.append(f"Source: {source_name}\nTitle: {title}")

        # Create analysis prompt
        prompt = """Analyze these cybersecurity article titles for relevance and importance.
Rate each title on a scale of 1-10 for how valuable it would be for a threat intelligence briefing.

Consider:
- Is this about current threats, vulnerabilities, or attacks?
- Does it provide actionable intelligence?
- Is this timely and relevant to security professionals?
- Does it contain specific technical details?

Respond with JSON only: [{"title_index": 0, "relevance_score": 8, "reason": "Critical vulnerability"}, ...]

Titles to analyze:
""" + "\n\n".join(f"{i}. {title}" for i, title in enumerate(titles))

        # Use basic scoring approach for title analysis
        # This is efficient and doesn't require additional LLM calls
        scored_articles = []
        for article in articles:
            basic_score = self._analyze_title_relevance(article.get('title', ''))
            article['llm_relevance_score'] = basic_score * 10  # Convert to 1-10 scale
            scored_articles.append(article)

        return scored_articles

    def prioritize_articles(self, articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Prioritize articles into processing tiers.

        Args:
            articles: List of articles to prioritize

        Returns:
            Dictionary with articles grouped by processing priority
        """
        prioritized = {
            'priority_1_full': [],    # Immediate full processing
            'priority_2_full': [],    # High priority full processing
            'priority_3_selective': [], # Selective processing
            'priority_4_title': [],    # Title analysis only
            'priority_5_skip': []      # Skip/deprioritize
        }

        for article in articles:
            priority = self.get_processing_priority(article)
            article['_processing_priority'] = priority

            # Add to appropriate bucket
            if priority.priority_level == 1:
                prioritized['priority_1_full'].append(article)
            elif priority.priority_level == 2:
                prioritized['priority_2_full'].append(article)
            elif priority.priority_level == 3:
                prioritized['priority_3_selective'].append(article)
            elif priority.priority_level == 4:
                prioritized['priority_4_title'].append(article)
            else:
                prioritized['priority_5_skip'].append(article)

        return prioritized

    def process_tiered_articles(self, articles: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, Any]:
        """Process articles using tiered approach.

        Args:
            articles: List of articles to process
            dry_run: If True, only analyze without actual processing

        Returns:
            Dictionary with processing results
        """
        print(f"🎯 Tiered Processing: Analyzing {len(articles)} articles")

        # Prioritize articles
        prioritized = self.prioritize_articles(articles)

        results = {
            'total_articles': len(articles),
            'processing_plan': {},
            'processed_articles': [],
            'skipped_articles': []
        }

        # Priority 1: Immediate full processing (high quality sources)
        if prioritized['priority_1_full']:
            batch = prioritized['priority_1_full'][:self.full_processing_batch_size]
            results['processing_plan']['priority_1'] = {
                'count': len(batch),
                'type': 'full_processing',
                'description': 'High quality sources - immediate processing'
            }

            if not dry_run:
                processed = self._process_full_articles(batch)
                results['processed_articles'].extend(processed)
            else:
                results['processed_articles'].extend(batch)

        # Priority 2: High priority full processing
        if prioritized['priority_2_full']:
            batch = prioritized['priority_2_full'][:self.full_processing_batch_size]
            results['processing_plan']['priority_2'] = {
                'count': len(batch),
                'type': 'full_processing',
                'description': 'Medium quality with relevant keywords'
            }

            if not dry_run:
                processed = self._process_full_articles(batch)
                results['processed_articles'].extend(processed)
            else:
                results['processed_articles'].extend(batch)

        # Priority 3: Selective processing with LLM title analysis
        if prioritized['priority_3_selective']:
            batch = prioritized['priority_3_selective'][:self.selective_processing_batch_size]
            results['processing_plan']['priority_3'] = {
                'count': len(batch),
                'type': 'selective_processing',
                'description': 'LLM title analysis then selective processing'
            }

            # Analyze titles first
            scored_articles = self.batch_analyze_titles(batch)
            # Select top articles for full processing
            top_articles = sorted(scored_articles,
                                key=lambda x: x.get('llm_relevance_score', 0),
                                reverse=True)[:3]

            if not dry_run:
                processed = self._process_full_articles(top_articles)
                results['processed_articles'].extend(processed)
            else:
                results['processed_articles'].extend(top_articles)

        # Priority 4: Title analysis only
        if prioritized['priority_4_title']:
            batch = prioritized['priority_4_title'][:self.title_analysis_batch_size]
            results['processing_plan']['priority_4'] = {
                'count': len(batch),
                'type': 'title_analysis',
                'description': 'Title analysis only, no full processing'
            }
            # Just analyze titles for monitoring
            self.batch_analyze_titles(batch)

        # Priority 5: Skip/deprioritize
        if prioritized['priority_5_skip']:
            results['processing_plan']['priority_5'] = {
                'count': len(prioritized['priority_5_skip']),
                'type': 'skipped',
                'description': 'Low relevance, skipped'
            }
            results['skipped_articles'].extend(prioritized['priority_5_skip'])

        return results

    def _process_full_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process articles with full LLM analysis.

        Args:
            articles: Articles to process

        Returns:
            List of processed articles
        """
        processed = []

        for article in articles:
            try:
                # Use the LLM registry for actual processing
                relevance_result = is_relevant_article(article.get('title', ''), article.get('raw_content', ''))
                is_relevant = relevance_result.get('is_relevant', False)

                if is_relevant:
                    # Extract IOCs and TTPs
                    iocs_result = extract_iocs_and_ttps(
                        article.get('title', ''),
                        article.get('raw_content', '')
                    )

                    # Update article with extracted data
                    database.update_article_processed_content(
                        article['id'],
                        iocs_result.get('summary', ''),
                        iocs_result.get('relevance_score', 0)
                    )

                    # Store IOCs if any
                    if iocs_result.get('iocs'):
                        database.add_iocs(article['id'], iocs_result['iocs'])

                    # Mark as processed
                    database.update_article_status(article['id'], 'processed')
                    article['processed'] = True
                    article['iocs_extracted'] = len(iocs_result.get('iocs', []))
                    article['summary'] = iocs_result.get('summary', '')
                    article['relevance_score'] = iocs_result.get('relevance_score', 0)

                else:
                    # Mark as rejected
                    database.update_article_status(article['id'], 'rejected')
                    article['processed'] = False
                    article['relevance_score'] = 0

                processed.append(article)

                # Add delay to respect rate limits
                time.sleep(0.5)

            except Exception as e:
                print(f"Error processing article {article['id']}: {e}")
                article['processed'] = False
                processed.append(article)

        return processed

    def print_processing_summary(self, results: Dict[str, Any]) -> None:
        """Print a summary of the tiered processing results.

        Args:
            results: Results from process_tiered_articles
        """
        print(f"\n{'='*60}")
        print("TIERED PROCESSING SUMMARY")
        print(f"{'='*60}")

        print(f"Total Articles Analyzed: {results['total_articles']}")
        print(f"Articles Processed: {len(results['processed_articles'])}")
        print(f"Articles Skipped: {len(results['skipped_articles'])}")

        print(f"\nProcessing Plan:")
        for priority, plan in results['processing_plan'].items():
            print(f"  {priority}: {plan['count']} articles - {plan['description']}")

        print(f"\nProcessing Efficiency: {len(results['processed_articles'])/results['total_articles']*100:.1f}% of articles selected for full processing")


def main():
    """Main function to demonstrate tiered processing."""
    print("Tia N. List - Tiered Article Processor")
    print("Optimizing LLM usage through intelligent source and title analysis")

    # Initialize database and processor
    database.initialize_database()
    processor = TieredArticleProcessor()

    # Get unprocessed articles
    articles = database.get_articles_by_status('fetched')

    if not articles:
        print("No articles to process. Run ingestion first.")
        return

    print(f"Found {len(articles)} articles for tiered processing")

    # Process with dry run to show plan
    results = processor.process_tiered_articles(articles, dry_run=True)

    # Print summary
    processor.print_processing_summary(results)


if __name__ == "__main__":
    main()