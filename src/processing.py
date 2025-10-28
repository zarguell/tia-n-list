"""Content processing module for Tia N. List project.

This module handles filtering, de-duplication, relevance scoring, and extraction
of IOCs and TTPs from articles using Google Gemini LLM.
"""

import json
from src import database, llm_client_multi


def filter_articles_for_relevance() -> None:
    """Filter articles for relevance using multi-provider LLM client in batches.

    Retrieves all articles with 'fetched' status, analyzes them for relevance,
    and updates their status to 'processed' or 'rejected'.
    """
    print("Starting article relevance filtering...")

    # Get fetched articles
    fetched_articles = database.get_articles_by_status('fetched')

    if not fetched_articles:
        print("No articles to filter")
        return

    print(f"Found {len(fetched_articles)} articles to analyze")

    # Initialize multi-provider LLM client
    try:
        client = llm_client_multi.MultiLLMClient()
        provider_info = client.get_provider_info()
        print(f"Using primary provider: {provider_info['primary_provider']}")
        if provider_info['fallback_provider']:
            print(f"Fallback provider: {provider_info['fallback_provider']}")
    except Exception as e:
        print(f"Error initializing LLM client: {e}")
        return

    print("Using batch processing for efficiency...")

    try:
        # Process articles in batches
        batch_results = client.batch_filter_articles(fetched_articles, batch_size=10)

        processed_count = 0
        rejected_count = 0

        # Update articles based on batch results
        for result in batch_results:
            article_id = result.get('article_id')

            # Find the corresponding article
            article = next((a for a in fetched_articles if a['id'] == article_id), None)
            if not article:
                print(f"Warning: Could not find article {article_id}")
                continue

            if result.get('is_relevant', False):
                # Update article with processed content and score
                database.update_article_processed_content(
                    article['id'],
                    article['raw_content'] or "",
                    result.get('reasoning', 'No reasoning provided'),
                    result.get('relevance_score', 50)  # Default score if not provided
                )
                processed_count += 1
                print(f"  ✓ {article['title'][:40]}... (score: {result.get('relevance_score', 50)})")
            else:
                # Mark as rejected
                database.update_article_status(article['id'], 'rejected')
                rejected_count += 1
                print(f"  ✗ {article['title'][:40]}... - {result.get('reasoning', 'No reasoning provided')}")

    except Exception as e:
        print(f"Error in batch processing: {e}")
        print("Falling back to individual processing...")

        # Fallback to individual processing
        processed_count = 0
        rejected_count = 0

        for article in fetched_articles:
            print(f"Analyzing: {article['title'][:50]}...")
            try:
                analysis = client.is_relevant_article(
                    article['title'],
                    article['raw_content'] or ""
                )

                if analysis.get('is_relevant', False):
                    database.update_article_processed_content(
                        article['id'],
                        article['raw_content'] or "",
                        analysis.get('reasoning', 'No reasoning provided'),
                        analysis.get('relevance_score', 50)
                    )
                    processed_count += 1
                    print(f"  ✓ Relevant (score: {analysis.get('relevance_score', 50)})")
                else:
                    database.update_article_status(article['id'], 'rejected')
                    rejected_count += 1
                    print(f"  ✗ Rejected: {analysis.get('reasoning', 'No reasoning provided')}")

            except Exception as e:
                print(f"  ✗ Error analyzing article: {e}")
                database.update_article_status(article['id'], 'rejected')
                rejected_count += 1

    print("\nFiltering complete:")
    print(f"  Processed: {processed_count}")
    print(f"  Rejected: {rejected_count}")


def extract_iocs_and_ttps() -> None:
    """Extract IOCs and TTPs from processed articles.

    Retrieves all articles with 'processed' status, analyzes them with multi-provider LLM
    to extract indicators and techniques, stores IOCs in database.
    """
    print("Starting IOC/TTP extraction...")

    # Get processed articles
    processed_articles = database.get_articles_by_status('processed')

    if not processed_articles:
        print("No processed articles to analyze")
        return

    print(f"Found {len(processed_articles)} processed articles to analyze")

    # Initialize multi-provider LLM client
    try:
        client = llm_client_multi.MultiLLMClient()
        provider_info = client.get_provider_info()
        print(f"Using primary provider: {provider_info['primary_provider']}")
        if provider_info['fallback_provider']:
            print(f"Fallback provider: {provider_info['fallback_provider']}")
    except Exception as e:
        print(f"Error initializing LLM client: {e}")
        return

    total_iocs = 0
    total_ttps = 0

    for article in processed_articles:
        print(f"Extracting from: {article['title'][:50]}...")

        try:
            # Extract structured data using Pro model
            extraction = client.extract_iocs_and_ttps(
                article['title'],
                article['raw_content'] or ""
            )

            # Store IOCs
            iocs = extraction.get('iocs', [])
            if iocs:
                ioc_list = [
                    {
                        'article_id': article['id'],
                        'type': ioc.get('type', 'unknown'),
                        'value': ioc.get('value', ''),
                        'confidence': ioc.get('confidence', 'medium')
                    }
                    for ioc in iocs
                ]

                inserted_ioc_ids = database.add_iocs(ioc_list)
                total_iocs += len(inserted_ioc_ids)
                print(f"  ✓ Found {len(ioc_list)} IOCs")

            # Store TTPs (for now, store in processed_content as JSON)
            ttps = extraction.get('ttps', [])
            if ttps:
                total_ttps += len(ttps)
                ttp_data = {
                    'ttps': ttps,
                    'extracted_at': article.get('created_at')
                }

                # Update article with TTP data
                database.update_article_processed_content(
                    article['id'],
                    f"{article['processed_content'] or ''}\n\n## Tactics, Techniques, and Procedures\n\n```json\n{json.dumps(ttps, indent=2)}\n```",
                    article.get('summary', ''),
                    article.get('score', 0)
                )
                print(f"  ✓ Found {len(ttps)} TTPs")

        except Exception as e:
            print(f"  ✗ Error extracting from article: {e}")

    print("\nExtraction complete:")
    print(f"  Total IOCs: {total_iocs}")
    print(f"  Total TTPs: {total_ttps}")


def process_new_articles() -> None:
    """Process new articles through filtering and extraction pipeline."""
    print("Starting full article processing pipeline...")

    # Step 1: Filter for relevance
    filter_articles_for_relevance()

    # Step 2: Extract IOCs and TTPs
    extract_iocs_and_ttps()

    print("\nProcessing pipeline complete!")


if __name__ == "__main__":
    process_new_articles()