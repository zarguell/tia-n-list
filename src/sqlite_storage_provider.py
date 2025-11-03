"""SQLite storage provider implementation for Tia N. List project.

This module implements the StorageProvider interface using SQLite database,
providing a traditional database backend option.

Note: This implementation is provided for completeness but the JSON
storage provider is the primary storage backend used by this project.
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid

from .storage_provider import StorageProvider


class SQLiteStorageProvider(StorageProvider):
    """SQLite-based storage provider implementing the StorageProvider interface."""

    def __init__(self, db_path: str = "data/threat_intelligence.db"):
        """Initialize SQLite storage with database path."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def initialize(self) -> None:
        """Initialize the storage provider."""
        with self._get_connection() as conn:
            # Create tables
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sources (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    last_fetched TIMESTAMP,
                    fetch_interval_hours INTEGER DEFAULT 1,
                    quality_score INTEGER DEFAULT 50,
                    active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                );

                CREATE TABLE IF NOT EXISTS articles (
                    id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    guid TEXT,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    published_at TIMESTAMP NOT NULL,
                    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'fetched',
                    content_raw TEXT,
                    content_full TEXT,
                    content_processed TEXT,
                    analysis_score REAL,
                    analysis_relevance_score REAL,
                    analysis_threat_category TEXT,
                    analysis_summary TEXT,
                    analysis_key_entities TEXT,  -- JSON array
                    analysis_ttps TEXT,  -- JSON array
                    content_source TEXT DEFAULT 'rss',
                    content_fetch_method TEXT,
                    processing_metadata TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES sources(id)
                );

                CREATE TABLE IF NOT EXISTS iocs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    article_id TEXT NOT NULL,
                    type TEXT NOT NULL,
                    value TEXT NOT NULL,
                    confidence TEXT,
                    context TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    process_date DATE NOT NULL,
                    FOREIGN KEY (article_id) REFERENCES articles(id)
                );

                CREATE INDEX IF NOT EXISTS idx_articles_source_id ON articles(source_id);
                CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status);
                CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);
                CREATE INDEX IF NOT EXISTS idx_iocs_article_id ON iocs(article_id);
                CREATE INDEX IF NOT EXISTS idx_iocs_process_date ON iocs(process_date);
            """)

    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return dictionary-like rows
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parse datetime string with robust error handling."""
        if not datetime_str:
            return datetime.utcnow()

        try:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return datetime.utcnow()

    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about stored data."""
        with self._get_connection() as conn:
            # Source statistics
            sources = conn.execute("SELECT COUNT(*) as total, SUM(CASE WHEN active THEN 1 ELSE 0 END) as active FROM sources").fetchone()

            # Article statistics
            article_stats = conn.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(CASE WHEN published_at >= datetime('now', '-7 days') THEN 1 END) as recent_7_days
                FROM articles
            """).fetchone()

            article_by_status = conn.execute("SELECT status, COUNT(*) as count FROM articles GROUP BY status").fetchall()
            article_by_source = conn.execute("SELECT source_id, COUNT(*) as count FROM articles GROUP BY source_id").fetchall()

            # IOC statistics
            ioc_stats = conn.execute("""
                SELECT
                    COUNT(*) as total,
                    COUNT(CASE WHEN extracted_at >= datetime('now', '-7 days') THEN 1 END) as recent_7_days
                FROM iocs
            """).fetchone()

            ioc_by_type = conn.execute("SELECT type, COUNT(*) as count FROM iocs GROUP BY type").fetchall()

        return {
            "sources": {
                "total": sources["total"],
                "active": sources["active"]
            },
            "articles": {
                "total": article_stats["total"],
                "by_status": {row["status"]: row["count"] for row in article_by_status},
                "by_source": {row["source_id"]: row["count"] for row in article_by_source},
                "recent_7_days": article_stats["recent_7_days"]
            },
            "iocs": {
                "total": ioc_stats["total"],
                "recent_7_days": ioc_stats["recent_7_days"],
                "by_type": {row["type"]: row["count"] for row in ioc_by_type}
            }
        }

    # Source Management Methods
    def add_source(self, name: str, url: str, **metadata) -> str:
        """Add a new RSS source configuration."""
        source_id = name.lower().replace(" ", "-").replace("/", "-")

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO sources
                (id, name, url, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (source_id, name, url, json.dumps(metadata) if metadata else None))

        return source_id

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Get source configuration by ID."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM sources WHERE id = ?", (source_id,)).fetchone()
            if row:
                source = dict(row)
                if source["metadata"]:
                    source["metadata"] = json.loads(source["metadata"])
                return source
        return None

    def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all configured sources."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM sources ORDER BY name").fetchall()
            sources = []
            for row in rows:
                source = dict(row)
                if source["metadata"]:
                    source["metadata"] = json.loads(source["metadata"])
                sources.append(source)
            return sources

    def update_source(self, source_id: str, **updates) -> bool:
        """Update source configuration."""
        if not updates:
            return False

        # Handle metadata separately
        metadata = updates.pop("metadata", None)

        set_clauses = []
        values = []

        for key, value in updates.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)

        if metadata is not None:
            set_clauses.append("metadata = ?")
            values.append(json.dumps(metadata))

        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(source_id)

        with self._get_connection() as conn:
            conn.execute(f"""
                UPDATE sources
                SET {', '.join(set_clauses)}
                WHERE id = ?
            """, values)

        return conn.total_changes > 0

    # Article Management Methods
    def add_article(self, source_id: str, guid: str, title: str, url: str,
                   published_at: datetime, raw_content: str = None, **metadata) -> str:
        """Add a new article to storage."""
        article_id = str(uuid.uuid4())

        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO articles
                (id, source_id, guid, title, url, published_at, content_raw, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (article_id, source_id, guid, title, url, published_at.isoformat(),
                  raw_content, json.dumps(metadata) if metadata else None))

        return article_id

    def get_article(self, article_id: str) -> Optional[Dict[str, Any]]:
        """Get article by ID."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
            if row:
                article = dict(row)
                # Parse JSON fields
                for field in ["analysis_key_entities", "analysis_ttps", "processing_metadata", "metadata"]:
                    if article[field]:
                        try:
                            article[field] = json.loads(article[field])
                        except json.JSONDecodeError:
                            article[field] = [] if field in ["analysis_key_entities", "analysis_ttps"] else {}
                return article
        return None

    def get_articles_by_source(self, source_id: str, limit: int = None,
                              status: str = None) -> List[Dict[str, Any]]:
        """Get articles from a specific source."""
        query = "SELECT * FROM articles WHERE source_id = ?"
        params = [source_id]

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY published_at DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            articles = []
            for row in rows:
                article = dict(row)
                # Parse JSON fields
                for field in ["analysis_key_entities", "analysis_ttps", "processing_metadata", "metadata"]:
                    if article[field]:
                        try:
                            article[field] = json.loads(article[field])
                        except json.JSONDecodeError:
                            article[field] = [] if field in ["analysis_key_entities", "analysis_ttps"] else {}
                articles.append(article)
            return articles

    def get_recent_articles(self, days: int = 7, status: str = "processed",
                           limit: int = None) -> List[Dict[str, Any]]:
        """Get recent articles within the specified date range."""
        query = """
            SELECT * FROM articles
            WHERE published_at >= datetime('now', '-{} days')
        """.format(days)

        params = []
        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY published_at DESC"

        if limit:
            query += " LIMIT ?"
            params.append(limit)

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            articles = []
            for row in rows:
                article = dict(row)
                # Parse JSON fields
                for field in ["analysis_key_entities", "analysis_ttps", "processing_metadata", "metadata"]:
                    if article[field]:
                        try:
                            article[field] = json.loads(article[field])
                        except json.JSONDecodeError:
                            article[field] = [] if field in ["analysis_key_entities", "analysis_ttps"] else {}
                articles.append(article)
            return articles

    def get_articles_by_date_range(self, start_date: date, end_date: date = None,
                                  status: str = None) -> List[Dict[str, Any]]:
        """Get articles within a specific date range."""
        if end_date is None:
            end_date = start_date

        query = """
            SELECT * FROM articles
            WHERE date(published_at) BETWEEN ? AND ?
        """
        params = [start_date.isoformat(), end_date.isoformat()]

        if status:
            query += " AND status = ?"
            params.append(status)

        query += " ORDER BY published_at DESC"

        with self._get_connection() as conn:
            rows = conn.execute(query, params).fetchall()
            articles = []
            for row in rows:
                article = dict(row)
                # Parse JSON fields
                for field in ["analysis_key_entities", "analysis_ttps", "processing_metadata", "metadata"]:
                    if article[field]:
                        try:
                            article[field] = json.loads(article[field])
                        except json.JSONDecodeError:
                            article[field] = [] if field in ["analysis_key_entities", "analysis_ttps"] else {}
                articles.append(article)
            return articles

    def update_article(self, article_id: str, **updates) -> bool:
        """Update article data."""
        if not updates:
            return False

        set_clauses = []
        values = []

        for key, value in updates.items():
            if key.startswith("analysis_") or key.startswith("content_") or key == "processing_metadata":
                if isinstance(value, (dict, list)):
                    set_clauses.append(f"{key} = ?")
                    values.append(json.dumps(value))
                else:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)

        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(article_id)

        with self._get_connection() as conn:
            conn.execute(f"""
                UPDATE articles
                SET {', '.join(set_clauses)}
                WHERE id = ?
            """, values)

        return conn.total_changes > 0

    def enhance_article_content(self, article_id: str, full_content: str,
                              fetch_method: str) -> bool:
        """Enhance article with full scraped content."""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE articles
                SET content_full = ?, content_source = 'enhanced', content_fetch_method = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (full_content, fetch_method, article_id))

        return conn.total_changes > 0

    def process_article(self, article_id: str, processed_content: str,
                       analysis: Dict[str, Any], iocs: List[Dict[str, Any]],
                       processing_metadata: Dict[str, Any]) -> bool:
        """Mark article as processed with analysis results."""
        with self._get_connection() as conn:
            # Update article
            conn.execute("""
                UPDATE articles
                SET status = 'processed',
                    content_processed = ?,
                    analysis_score = ?,
                    analysis_relevance_score = ?,
                    analysis_threat_category = ?,
                    analysis_summary = ?,
                    analysis_key_entities = ?,
                    analysis_ttps = ?,
                    processing_metadata = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                processed_content,
                analysis.get("score"),
                analysis.get("relevance_score"),
                analysis.get("threat_category"),
                analysis.get("summary"),
                json.dumps(analysis.get("key_entities", [])),
                json.dumps(analysis.get("ttps", [])),
                json.dumps(processing_metadata),
                article_id
            ))

            # Save IOCs
            process_date = datetime.utcnow().date()
            for ioc in iocs:
                conn.execute("""
                    INSERT INTO iocs
                    (article_id, type, value, confidence, context, process_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    article_id,
                    ioc.get("type"),
                    ioc.get("value"),
                    ioc.get("confidence"),
                    ioc.get("context"),
                    process_date.isoformat()
                ))

        return conn.total_changes > 0

    # IOC Management Methods
    def save_iocs_for_date(self, process_date: date, article_id: str,
                          iocs: List[Dict[str, Any]]) -> bool:
        """Save IOCs for a specific date."""
        with self._get_connection() as conn:
            for ioc in iocs:
                conn.execute("""
                    INSERT INTO iocs
                    (article_id, type, value, confidence, context, process_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    article_id,
                    ioc.get("type"),
                    ioc.get("value"),
                    ioc.get("confidence"),
                    ioc.get("context"),
                    process_date.isoformat()
                ))

        return True

    def get_iocs_by_date(self, target_date: date) -> List[Dict[str, Any]]:
        """Get all IOCs extracted on a specific date."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM iocs
                WHERE process_date = ?
                ORDER BY extracted_at DESC
            """, (target_date.isoformat(),)).fetchall()

            return [dict(row) for row in rows]

    def get_recent_iocs(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get IOCs from the last N days."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM iocs
                WHERE extracted_at >= datetime('now', '-{} days')
                ORDER BY extracted_at DESC
            """.format(days)).fetchall()

            return [dict(row) for row in rows]

    def get_article_iocs(self, article_id: str) -> List[Dict[str, Any]]:
        """Get all IOCs for a specific article."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM iocs
                WHERE article_id = ?
                ORDER BY extracted_at DESC
            """, (article_id,)).fetchall()

            return [dict(row) for row in rows]

    # Utility Methods
    def get_unprocessed_articles(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get articles that haven't been processed yet."""
        query = "SELECT * FROM articles WHERE status != 'processed' ORDER BY published_at DESC"

        if limit:
            query += f" LIMIT {limit}"

        with self._get_connection() as conn:
            rows = conn.execute(query).fetchall()
            articles = []
            for row in rows:
                article = dict(row)
                # Parse JSON fields
                for field in ["analysis_key_entities", "analysis_ttps", "processing_metadata", "metadata"]:
                    if article[field]:
                        try:
                            article[field] = json.loads(article[field])
                        except json.JSONDecodeError:
                            article[field] = [] if field in ["analysis_key_entities", "analysis_ttps"] else {}
                articles.append(article)
            return articles

    def health_check(self) -> Dict[str, Any]:
        """Check the health of the storage provider."""
        health = {
            "status": "healthy",
            "checks": {},
            "issues": []
        }

        try:
            # Check database connection
            with self._get_connection() as conn:
                # Test basic query
                conn.execute("SELECT 1").fetchone()
                health["checks"]["database_connection"] = True

                # Check tables exist
                tables = conn.execute("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name IN ('sources', 'articles', 'iocs')
                """).fetchall()

                table_names = [row[0] for row in tables]
                required_tables = ['sources', 'articles', 'iocs']

                for table in required_tables:
                    health["checks"][f"table_{table}"] = table in table_names
                    if table not in table_names:
                        health["status"] = "unhealthy"
                        health["issues"].append(f"Table {table} does not exist")

        except Exception as e:
            health["status"] = "unhealthy"
            health["issues"].append(f"Database health check failed: {e}")
            health["checks"]["database_connection"] = False

        return health