"""Persona module for Tia N. List project.

This module handles the Tia N. List persona including joke fetching
and content formatting to maintain consistent brand voice.
"""

import requests
from typing import Dict, Any, Optional, List
from src import database


def fetch_joke_of_the_day() -> Optional[str]:
    """Fetch a random joke from the official joke API.

    Returns:
        Joke text or None if fetching fails.
    """
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=10)
        response.raise_for_status()

        joke_data = response.json()

        # Combine setup and punchline
        setup = joke_data.get('setup', '')
        punchline = joke_data.get('punchline', '')

        if setup and punchline:
            return f"{setup} {punchline}"
        elif punchline:
            return punchline
        elif setup:
            return setup

        return "Why don't scientists trust atoms? Because they make up everything!"

    except Exception as e:
        print(f"Error fetching joke: {e}")
        return None


def format_article_summary(title: str, content: str, score: int) -> str:
    """Format article summary in Tia N. List persona.

    Args:
        title: Article title.
        content: Article content.
        score: Relevance score (0-100).

    Returns:
        Formatted article summary.
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
        articles = database.get_top_articles(limit)

        # Add source names and format for display
        formatted_articles = []
        for article in articles:
            # Get source name
            sources = database.get_all_sources()
            source_name = "Unknown Source"
            for source in sources:
                if source['id'] == article['source_id']:
                    source_name = source['name']
                    break

            formatted_articles.append({
                'title': article['title'],
                'source': source_name,
                'url': article['url'],
                'score': article['score'],
                'summary': article['summary'] or 'No summary available'
            })

        return formatted_articles

    except Exception as e:
        print(f"Error getting top articles: {e}")
        return []


def add_joke_to_content(content: str) -> str:
    """Add a joke to content in Tia's style.

    Args:
        content: Original content.

    Returns:
        Content with joke appended.
    """
    joke = fetch_joke_of_the_day()

    if joke:
        # Add joke as a postscript with separator
        return f"{content}\n\n---\n\n📝 **Today's Cybersecurity Wisdom:**\n{joke}\n\n---"
    else:
        # Fallback if joke fetching fails
        return f"{content}\n\n---\n\n📝 **Today's Cybersecurity Wisdom:**\nWhy did the cybersecurity researcher cross the road? Because he was looking for vulnerabilities!\n\n---"