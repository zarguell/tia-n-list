#!/usr/bin/env python3
"""Manual processing script for testing blog generation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import database

def manually_process_article():
    """Manually add processed_content to an article for testing."""

    # Initialize database
    database.initialize_database()

    # Get a processed article
    conn = database.get_connection()
    cursor = conn.execute('SELECT id, title, raw_content FROM articles WHERE status = "processed" LIMIT 1')
    article = cursor.fetchone()

    if not article:
        print("No processed articles found")
        return

    article_id, title, content = article
    print(f"Processing article: {title}")
    print(f"Content length: {len(content)} characters")

    # Create a simple summary for testing
    summary = f"""
This article discusses {title.lower()}.

Key Points:
- Important cybersecurity development
- Relevant for security professionals
- Requires attention and monitoring

Analysis: This content provides valuable threat intelligence that should be monitored for potential impact on security posture.

Recommendations: Security teams should review this information and consider appropriate defensive measures.
"""

    # Update the article with processed content and score
    cursor = conn.execute('''
        UPDATE articles
        SET processed_content = ?, score = 85
        WHERE id = ?
    ''', (summary, article_id))

    conn.commit()
    conn.close()

    print(f"✅ Article {article_id} updated with summary and score")
    print("Now you can run: python -m src.intelligent_blog_generator")

if __name__ == "__main__":
    manually_process_article()