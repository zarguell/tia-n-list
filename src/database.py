"""Database module for Tia N. List project.

This module provides functions to interact with SQLite database,
including schema initialization and CRUD operations for sources,
articles, and IOCs.
"""

import sqlite3
import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


# Database file path
DB_PATH = Path("tia_n_list.db")


def get_connection() -> sqlite3.Connection:
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Initialize the database with required tables."""
    conn = get_connection()

    try:
        # Create sources table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                last_fetched DATETIME
            )
        """)

        # Create articles table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                guid TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                raw_content TEXT,
                processed_content TEXT,
                summary TEXT,
                score INTEGER,
                status TEXT DEFAULT 'fetched',
                published_at DATETIME,
                content_source TEXT DEFAULT 'rss',
                content_fetch_method TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (source_id) REFERENCES sources (id)
            )
        """)

        # Create IOCs table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS iocs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                value TEXT NOT NULL,
                confidence TEXT DEFAULT 'medium',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        """)

        # Run migrations for existing databases
        _run_migrations(conn)

        conn.commit()
    finally:
        conn.close()


def _run_migrations(conn: sqlite3.Connection) -> None:
    """Run database migrations for schema updates."""
    try:
        # Check if content_source column exists
        cursor = conn.execute("PRAGMA table_info(articles)")
        columns = [column[1] for column in cursor.fetchall()]

        # Add content_source column if it doesn't exist
        if 'content_source' not in columns:
            conn.execute("ALTER TABLE articles ADD COLUMN content_source TEXT DEFAULT 'rss'")
            print("Added content_source column to articles table")

        # Add content_fetch_method column if it doesn't exist
        if 'content_fetch_method' not in columns:
            conn.execute("ALTER TABLE articles ADD COLUMN content_fetch_method TEXT")
            print("Added content_fetch_method column to articles table")

    except sqlite3.Error as e:
        print(f"Migration failed: {e}")


def add_source(name: str, url: str) -> int:
    """Add a new source to the database.

    Args:
        name: Name of the source.
        url: URL of the RSS/Atom feed.

    Returns:
        int: ID of the inserted source.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            "INSERT OR REPLACE INTO sources (name, url) VALUES (?, ?)",
            (name, url)
        )
        conn.commit()
        return cursor.lastrowid or 0
    finally:
        conn.close()


def get_all_sources() -> List[Dict[str, Any]]:
    """Get all sources from the database.

    Returns:
        List of dictionaries representing sources.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            SELECT id, name, url, last_fetched
            FROM sources
            ORDER BY name
            """
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_source_last_fetched(source_id: int) -> None:
    """Update the last_fetched timestamp for a source."""
    conn = get_connection()

    try:
        cursor = conn.execute(
            "UPDATE sources SET last_fetched = CURRENT_TIMESTAMP WHERE id = ?",
            (source_id,)
        )
        conn.commit()
    finally:
        conn.close()


def add_articles(articles: List[Dict[str, Any]]) -> List[int]:
    """Add multiple articles to the database.

    Args:
        articles: List of article dictionaries with keys:
                 source_id, guid, title, url, raw_content

    Returns:
        List[int]: IDs of inserted articles.
    """
    if not articles:
        return []

    conn = get_connection()

    try:
        cursor = conn.executemany(
            """
            INSERT OR IGNORE INTO articles
            (source_id, guid, title, url, raw_content, status)
            VALUES (?, ?, ?, ?, ?, 'fetched')
            """,
            [(a['source_id'], a['guid'], a['title'], a['url'], a.get('raw_content', ''))
                 for a in articles]
        )
        conn.commit()
        return [row[0] for row in cursor.execute("SELECT last_insert_rowid()")]
    finally:
        conn.close()


def get_article_by_id(article_id: int) -> Optional[Dict[str, Any]]:
    """Get a single article by ID.

    Args:
        article_id: ID of the article to retrieve.

    Returns:
        Dictionary representing the article or None.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            SELECT * FROM articles WHERE id = ?
            """,
            (article_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_articles_by_status(status: str) -> List[Dict[str, Any]]:
    """Get articles by their status.

    Args:
        status: Status to filter by ('fetched', 'processed', 'published', etc.)

    Returns:
        List of articles with the specified status.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            SELECT * FROM articles WHERE status = ? ORDER BY created_at DESC
            """,
            (status,)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_articles_by_source_id(source_id: int, days_back: int = 7) -> List[Dict[str, Any]]:
    """Get articles from a specific source within the last N days.

    Args:
        source_id: Database ID of the source
        days_back: Number of days to look back (default: 7)

    Returns:
        List of articles from the specified source.
    """
    conn = get_connection()

    cutoff_date = (datetime.datetime.now(datetime.timezone.utc) -
                   datetime.timedelta(days=days_back)).isoformat()

    try:
        cursor = conn.execute(
            """
            SELECT a.*, s.name as source_name, s.url as source_url
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            WHERE a.source_id = ? AND a.created_at >= ?
            ORDER BY a.created_at DESC
            """,
            (source_id, cutoff_date)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_article_status(article_id: int, status: str) -> None:
    """Update the status of an article."""
    conn = get_connection()

    try:
        conn.execute(
            "UPDATE articles SET status = ? WHERE id = ?",
            (status, article_id)
        )
        conn.commit()
    finally:
        conn.close()


def update_article_processed_content(article_id: int, processed_content: str, summary: str, score: int) -> None:
    """Update the processed content, summary, and score of an article."""
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            UPDATE articles
            SET processed_content = ?, summary = ?, score = ?, status = 'processed'
            WHERE id = ?
            """,
            (processed_content, summary, score, article_id)
        )
        conn.commit()
    finally:
        conn.close()


def get_top_articles(limit: int = 10) -> List[Dict[str, Any]]:
    """Get top articles by score.

    Args:
        limit: Maximum number of articles to return.

    Returns:
        List of top scoring articles.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            SELECT a.*, s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            WHERE a.status = 'processed' AND a.score IS NOT NULL
            ORDER BY a.score DESC, a.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def add_iocs(iocs: List[Dict[str, Any]]) -> List[int]:
    """Add multiple IOCs to the database.

    Args:
        iocs: List of IOC dictionaries with keys:
                 article_id, type, value, confidence

    Returns:
        List[int]: IDs of inserted IOCs.
    """
    if not iocs:
        return []

    conn = get_connection()
    inserted_ids = []

    try:
        for ioc in iocs:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO iocs
                (article_id, type, value, confidence)
                VALUES (?, ?, ?, ?)
                """,
                (ioc['article_id'], ioc['type'], ioc['value'], ioc.get('confidence', 'medium'))
            )
            if cursor.rowcount > 0:  # Only add ID if actually inserted (not ignored)
                inserted_ids.append(cursor.lastrowid)

        conn.commit()
        return inserted_ids
    finally:
        conn.close()


def get_iocs_by_article_id(article_id: int) -> List[Dict[str, Any]]:
    """Get IOCs associated with a specific article.

    Args:
        article_id: ID of the article.

    Returns:
        List of IOCs for the article.
    """
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            SELECT * FROM iocs WHERE article_id = ?
            """,
            (article_id,)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def update_article_content(article_id: int, new_content: str, fetch_method: str) -> bool:
    """Update an article's raw content with scraped content.

    Args:
        article_id: ID of the article to update.
        new_content: New content to replace raw_content.
        fetch_method: Method used to fetch content ('website_specific', 'trafilatura', 'beautifulsoup').

    Returns:
        True if update was successful, False otherwise.
    """
    conn = get_connection()
    try:
        conn.execute(
            """
            UPDATE articles
            SET raw_content = ?,
                content_source = 'scraped',
                content_fetch_method = ?,
                status = 'fetched'  -- Reset to fetched for reprocessing
            WHERE id = ?
            """,
            (new_content, fetch_method, article_id)
        )
        conn.commit()
        return conn.total_changes > 0
    except sqlite3.Error as e:
        print(f"Error updating article content: {e}")
        return False
    finally:
        conn.close()


def get_articles_by_content_source(content_source: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get articles by content source type.

    Args:
        content_source: 'rss' or 'scraped'.
        limit: Maximum number of articles to return.

    Returns:
        List of articles with the specified content source.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT a.*, s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            WHERE a.content_source = ?
            ORDER BY a.created_at DESC
            LIMIT ?
            """,
            (content_source, limit)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_articles_needing_content_enhancement(limit: int = 20) -> List[Dict[str, Any]]:
    """Get articles that have short RSS content and could benefit from scraping.

    Args:
        limit: Maximum number of articles to return.

    Returns:
        List of articles with short content that could be enhanced.
    """
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT a.*, s.name as source_name
            FROM articles a
            JOIN sources s ON a.source_id = s.id
            WHERE a.content_source = 'rss'
            AND LENGTH(a.raw_content) < 500
            AND a.url IS NOT NULL
            ORDER BY a.created_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    finally:
        conn.close()