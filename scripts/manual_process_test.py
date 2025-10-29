#!/usr/bin/env python3
"""Manual script to create some processed articles for testing."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import database

def create_test_processed_articles():
    """Create some test processed articles for blog generation testing."""

    # Initialize database
    database.initialize_database()

    # Get some recent articles
    conn = database.get_connection()
    cursor = conn.execute('''
        SELECT id, title, raw_content, url
        FROM articles
        WHERE status = 'rejected'
        ORDER BY created_at DESC
        LIMIT 5
    ''')

    articles = cursor.fetchall()

    if not articles:
        print("No rejected articles found")
        return

    print(f"Found {len(articles)} rejected articles to manually process:")

    for article in articles:
        article_id, title, content, url = article

        print(f"\nProcessing article {article_id}: {title[:50]}...")

        # Create a simple summary for testing
        summary = f"""
This article discusses important cybersecurity developments related to {title.lower()}.

Key Points:
- Significant security implications for organizations
- Requires attention from security professionals
- Potential impact on current threat landscape

Analysis: This content provides valuable threat intelligence that should be monitored for potential impact on security posture.

Recommendations: Security teams should review this information and consider appropriate defensive measures and monitoring strategies.
        """.strip()

        # Create some sample IOCs
        sample_iocs = [
            {"type": "domain", "value": "malicious-example.com", "confidence": "high"},
            {"type": "ip_address", "value": "192.168.1.100", "confidence": "medium"}
        ]

        # Update the article with processed content and score
        cursor = conn.execute('''
            UPDATE articles
            SET processed_content = ?,
                summary = ?,
                score = 85,
                status = 'processed'
            WHERE id = ?
        ''', (summary, summary, article_id))

        # Add IOCs
        for ioc in sample_iocs:
            conn.execute('''
                INSERT INTO iocs (article_id, type, value, confidence)
                VALUES (?, ?, ?, ?)
            ''', (article_id, ioc['type'], ioc['value'], ioc['confidence']))

        print(f"  ✅ Updated article {article_id}")

    conn.commit()
    conn.close()

    print(f"\n✅ Manually processed {len(articles)} articles for testing")
    print("Now you can run: PYTHONPATH=. python -m src.intelligent_blog_generator")

if __name__ == "__main__":
    create_test_processed_articles()