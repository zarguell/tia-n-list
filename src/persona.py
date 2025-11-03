"""Persona module for Tia N. List project.

This module handles the Tia N. List persona and content formatting
to maintain consistent professional brand voice for executive audience.
"""

from typing import Dict, Any, List
from datetime import date
from .storage_provider import StorageProvider
from .storage_registry import get_default_storage_provider


def format_article_summary(title: str, content: str, score: int) -> str:
    """Format article summary in Tia N. List persona for executive audience.

    Args:
        title: Article title.
        content: Article content.
        score: Relevance score (0-100).

    Returns:
        Professionally formatted article summary with relevance indicators
        and executive-appropriate insights.
    """
    # Add Tia's signature based on relevance
    relevance_emoji = "🔴" if score < 30 else "🟡" if score < 70 else "🟢" if score < 90 else "🟢"

    # Add a personal touch
    personal_note = ""
    if score >= 80:
        personal_note = "\n\n*Tia's take: This is critical intelligence that organizations should act on immediately.*"
    elif score >= 60:
        personal_note = "\n\n*Tia's note: Interesting development worth monitoring for defensive measures.*"

    return f"""
{relevance_emoji} **{title}**

{content[:300]}...
{personal_note}

---
*Relevance Score: {score}/100* | Tia N. List*"""


def get_top_articles_for_summary(limit: int = 5) -> List[Dict[str, Any]]:
    """Get top articles for daily summary generation.

    Args:
        limit: Maximum number of articles to include.

    Returns:
        List of top scoring articles.
    """
    try:
        storage = get_default_storage_provider()
        articles = storage.get_articles_by_date_range(
            start_date=date.today(),
            end_date=date.today(),
            status="processed"
        )

        # Sort by score and take top articles
        articles.sort(key=lambda x: x.get('analysis', {}).get('score', 0), reverse=True)
        top_articles = articles[:limit]

        # Add source names and format for display
        formatted_articles = []
        for article in top_articles:
            # Get source name from sources
            sources = storage.get_all_sources()
            source_name = "Unknown Source"
            for source in sources:
                if source['id'] == article.get('source_id'):
                    source_name = source['name']
                    break

            formatted_articles.append({
                'title': article.get('title', 'No title'),
                'source': source_name,
                'url': article.get('url', ''),
                'score': article.get('analysis', {}).get('score', 0),
                'summary': article.get('analysis', {}).get('summary', 'No summary available')
            })

        return formatted_articles

    except Exception as e:
        print(f"Error getting top articles: {e}")
        return []


