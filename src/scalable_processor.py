"""Scalable LLM Processing Module

This module optimizes LLM processing for large feed volumes by integrating
with the tiered processing system and implementing efficient batching
strategies.
"""

import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from src import database, llm_client_multi, tiered_processor


class ScalableProcessor:
    """Optimized LLM processor for handling large feed volumes efficiently."""

    def __init__(self):
        self.llm_client = llm_client_multi.MultiLLMClient()
        self.tiered_processor = tiered_processor.TieredArticleProcessor(self.llm_client)

        # Processing configuration
        self.max_daily_articles = 100  # Maximum articles to process per day
        self.processing_batches = {
            'high_quality': 5,      # Batch size for high-quality sources
            'medium_quality': 3,    # Batch size for selective processing
            'title_analysis': 20    # Batch size for title analysis
        }

        # Rate limiting
        self.delays = {
            'between_batches': 2.0,   # Seconds between batches
            'between_articles': 0.5   # Seconds between individual articles
        }

    def process_daily_articles(self, max_articles: int = None) -> Dict[str, Any]:
        """Process articles using the optimized tiered approach.

        Args:
            max_articles: Maximum number of articles to process today

        Returns:
            Processing results and statistics
        """
        max_articles = max_articles or self.max_daily_articles

        print(f"🚀 Starting scalable LLM processing (max: {max_articles} articles)")

        # Get unprocessed articles
        all_articles = database.get_articles_by_status('fetched')

        if not all_articles:
            return {
                'success': True,
                'processed_count': 0,
                'skipped_count': 0,
                'processing_efficiency': 0,
                'overall_efficiency': 0,
                'cost_savings': 0,
                'message': 'No articles to process'
            }

        # Limit articles to prevent overload
        articles_to_process = all_articles[:max_articles]

        print(f"Found {len(all_articles)} total articles, processing {len(articles_to_process)}")

        # Use tiered processing to prioritize
        processing_results = self.tiered_processor.process_tiered_articles(
            articles_to_process,
            dry_run=False  # Actual processing
        )

        # Update database with processing decisions
        self._update_processing_decisions(processing_results)

        # Generate processing statistics
        stats = self._generate_processing_stats(processing_results, len(all_articles))

        return stats

    def _update_processing_decisions(self, results: Dict[str, Any]) -> None:
        """Update article statuses based on processing decisions.

        Args:
            results: Results from tiered processing
        """
        processed_count = 0
        skipped_count = 0

        # Mark processed articles
        for article in results.get('processed_articles', []):
            try:
                if article.get('processed', False):
                    database.update_article_status(article['id'], 'processed')
                    processed_count += 1
            except Exception as e:
                print(f"Error updating processed article {article.get('id')}: {e}")

        # Mark skipped articles as rejected to avoid reprocessing
        for article in results.get('skipped_articles', []):
            try:
                database.update_article_status(article['id'], 'rejected')
                skipped_count += 1
            except Exception as e:
                print(f"Error updating skipped article {article.get('id')}: {e}")

        print(f"✅ Updated {processed_count} articles as processed")
        print(f"⏭️  Marked {skipped_count} articles as rejected")

    def _generate_processing_stats(self, results: Dict[str, Any], total_available: int) -> Dict[str, Any]:
        """Generate comprehensive processing statistics.

        Args:
            results: Processing results
            total_available: Total articles available for processing

        Returns:
            Statistics dictionary
        """
        processed_count = len(results.get('processed_articles', []))
        skipped_count = len(results.get('skipped_articles', []))

        # Calculate efficiency metrics
        processing_efficiency = (processed_count / results['total_articles']) * 100 if results['total_articles'] > 0 else 0
        overall_efficiency = (processed_count / total_available) * 100 if total_available > 0 else 0

        # Estimate cost savings
        estimated_original_cost = total_available * 0.01  # Assume $0.01 per article
        estimated_optimized_cost = processed_count * 0.01
        cost_savings = estimated_original_cost - estimated_optimized_cost

        stats = {
            'success': True,
            'processed_count': processed_count,
            'skipped_count': skipped_count,
            'total_analyzed': results['total_articles'],
            'total_available': total_available,
            'processing_efficiency': processing_efficiency,
            'overall_efficiency': overall_efficiency,
            'cost_savings': cost_savings,
            'processing_plan': results.get('processing_plan', {}),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        return stats

    def batch_process_with_retry(self, articles: List[Dict[str, Any]], max_retries: int = 3) -> List[Dict[str, Any]]:
        """Process articles with intelligent retry logic.

        Args:
            articles: Articles to process
            max_retries: Maximum number of retry attempts

        Returns:
            Successfully processed articles
        """
        processed = []

        for article in articles:
            success = False
            attempts = 0

            while not success and attempts < max_retries:
                try:
                    # Use the existing processing logic
                    is_relevant = self.llm_client.is_relevant_article(article.get('title', ''), article.get('raw_content', ''))

                    if is_relevant:
                        # Extract IOCs and TTPs
                        iocs_result = self.llm_client.extract_iocs_and_ttps(
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
                        processed.append(article)
                        success = True

                    else:
                        # Mark as rejected
                        database.update_article_status(article['id'], 'rejected')
                        article['processed'] = False
                        processed.append(article)
                        success = True

                except Exception as e:
                    attempts += 1
                    if attempts < max_retries:
                        wait_time = 2 ** attempts  # Exponential backoff
                        print(f"Retry {attempts}/{max_retries} for article {article.get('id')} after {wait_time}s: {e}")
                        time.sleep(wait_time)
                    else:
                        print(f"Failed to process article {article.get('id')} after {max_retries} attempts: {e}")
                        article['processed'] = False
                        processed.append(article)

                # Rate limiting between articles
                if success:
                    time.sleep(self.delays['between_articles'])

        return processed

    def monitor_processing_health(self) -> Dict[str, Any]:
        """Monitor the health and performance of the processing system.

        Returns:
            Health metrics and recommendations
        """
        # Get recent processing statistics
        processed_articles = database.get_articles_by_status('processed')
        rejected_articles = database.get_articles_by_status('rejected')
        fetched_articles = database.get_articles_by_status('fetched')

        total_processed = len(processed_articles)
        total_rejected = len(rejected_articles)
        total_fetched = len(fetched_articles)

        # Calculate acceptance rate
        total_decided = total_processed + total_rejected
        acceptance_rate = (total_processed / total_decided) * 100 if total_decided > 0 else 0

        # Get source quality statistics
        quality_tracker = tiered_processor.source_quality.SourceQualityTracker()
        source_recommendations = quality_tracker.get_source_recommendations()

        health_metrics = {
            'total_articles_in_system': total_processed + total_rejected + total_fetched,
            'processed_articles': total_processed,
            'rejected_articles': total_rejected,
            'pending_articles': total_fetched,
            'acceptance_rate': acceptance_rate,
            'high_quality_sources': len(source_recommendations['high_quality']),
            'medium_quality_sources': len(source_recommendations['medium_quality']),
            'low_quality_sources': len(source_recommendations['low_quality']),
            'system_efficiency': acceptance_rate,  # Higher acceptance rate = better filtering
            'recommendations': self._generate_health_recommendations(acceptance_rate, source_recommendations)
        }

        return health_metrics

    def _generate_health_recommendations(self, acceptance_rate: float, source_recommendations: Dict[str, List[Dict[str, Any]]]) -> List[str]:
        """Generate health recommendations based on system metrics.

        Args:
            acceptance_rate: Percentage of articles accepted for processing
            source_recommendations: Source quality recommendations

        Returns:
            List of recommendations
        """
        recommendations = []

        if acceptance_rate < 20:
            recommendations.append("Low acceptance rate - consider adjusting title relevance thresholds")
        elif acceptance_rate > 80:
            recommendations.append("High acceptance rate - consider stricter filtering criteria")

        if len(source_recommendations['high_quality']) < 3:
            recommendations.append("Few high-quality sources - consider adding more premium cybersecurity feeds")

        if len(source_recommendations['low_quality']) > 10:
            recommendations.append("Many low-quality sources - consider removing or deprioritizing poor performing feeds")

        recommendations.append("Regular monitoring recommended to maintain optimal processing efficiency")

        return recommendations

    def print_health_report(self) -> None:
        """Print a comprehensive health report."""
        health = self.monitor_processing_health()

        print("\n" + "="*60)
        print("SCALABLE PROCESSOR HEALTH REPORT")
        print("="*60)

        print(f"📊 Article Statistics:")
        print(f"   Total Articles: {health['total_articles_in_system']}")
        print(f"   Processed: {health['processed_articles']}")
        print(f"   Rejected: {health['rejected_articles']}")
        print(f"   Pending: {health['pending_articles']}")
        print(f"   Acceptance Rate: {health['acceptance_rate']:.1f}%")

        print(f"\n🎯 Source Quality Distribution:")
        print(f"   High Quality: {health['high_quality_sources']} sources")
        print(f"   Medium Quality: {health['medium_quality_sources']} sources")
        print(f"   Low Quality: {health['low_quality_sources']} sources")

        print(f"\n💡 Recommendations:")
        for i, rec in enumerate(health['recommendations'], 1):
            print(f"   {i}. {rec}")

        print(f"\n✨ System Efficiency: {health['system_efficiency']:.1f}%")


def main():
    """Main function to run scalable processing."""
    print("Tia N. List - Scalable LLM Processor")
    print("Optimized processing for large feed volumes")

    # Initialize database and processor
    database.initialize_database()
    processor = ScalableProcessor()

    # Print health report first
    processor.print_health_report()

    # Run processing
    print(f"\n🔄 Starting optimized processing...")
    results = processor.process_daily_articles()

    if results['success']:
        print(f"\n✅ Processing completed successfully!")
        print(f"   Processed: {results['processed_count']} articles")
        print(f"   Skipped: {results['skipped_count']} articles")
        print(f"   Processing Efficiency: {results['processing_efficiency']:.1f}%")
        print(f"   Overall Efficiency: {results['overall_efficiency']:.1f}%")
        print(f"   Estimated Cost Savings: ${results['cost_savings']:.2f}")
    else:
        print(f"❌ Processing failed: {results.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()