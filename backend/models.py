"""Database models and connection for screenshot search."""
import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

DATABASE_PATH = "screenshots.db"


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initialize the database schema."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                filepath TEXT NOT NULL,
                metadata JSON,
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def get_screenshot_by_filename(filename: str) -> Optional[Dict[str, Any]]:
    """Get a screenshot by filename."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM screenshots WHERE filename = ?", (filename,)
        ).fetchone()
        if row:
            return dict(row)
        return None


def get_all_screenshots() -> List[Dict[str, Any]]:
    """Get all screenshots from the database."""
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM screenshots ORDER BY indexed_at DESC").fetchall()
        return [dict(row) for row in rows]


def insert_screenshot(filename: str, filepath: str, metadata: Dict[str, Any]) -> int:
    """Insert a new screenshot into the database."""
    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO screenshots (filename, filepath, metadata, indexed_at)
            VALUES (?, ?, ?, ?)
            """,
            (filename, filepath, json.dumps(metadata), datetime.now().isoformat())
        )
        conn.commit()
        return cursor.lastrowid


def delete_screenshot(filename: str):
    """Delete a screenshot from the database."""
    with get_db() as conn:
        conn.execute("DELETE FROM screenshots WHERE filename = ?", (filename,))
        conn.commit()


def get_all_screenshots_metadata() -> List[Dict[str, Any]]:
    """Get all screenshots with parsed metadata for search."""
    screenshots = get_all_screenshots()
    result = []
    for screenshot in screenshots:
        parsed_metadata = json.loads(screenshot['metadata']) if screenshot['metadata'] else {}
        result.append({
            'id': screenshot['id'],
            'filename': screenshot['filename'],
            'filepath': screenshot['filepath'],
            'metadata': parsed_metadata,
            'indexed_at': screenshot['indexed_at']
        })
    return result

