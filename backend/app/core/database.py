"""
SQLite database setup and connection management.
"""

import sqlite3
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from app.core.config import settings

# Database file path
DB_PATH = Path(settings.database_dir) / "buybuddy.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_db_connection() -> sqlite3.Connection:
    """
    Get a database connection.
    """
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


@contextmanager
def get_db():
    """
    Context manager for database connections.
    """
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """
    Initialize database tables.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Table: conversations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                assistant_response TEXT,
                structured_query TEXT,  -- JSON string
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table: products (cache)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price TEXT,
                link TEXT UNIQUE,
                platform TEXT,
                image TEXT,
                search_query TEXT,  -- The query that found this product
                cached_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table: searches (search history)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                query_text TEXT NOT NULL,
                structured_query TEXT,  -- JSON string
                num_results INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_link ON products(link)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_search_query ON products(search_query)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_searches_session ON searches(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_searches_timestamp ON searches(timestamp)")
        
        conn.commit()
        print(f"Database initialized at: {DB_PATH}")


# Initialize database on import
init_database()

