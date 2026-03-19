"""Database connection and schema management."""

import sqlite3
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection() -> sqlite3.Connection:
    """Get SQLite database connection with Row factory.
    
    Returns:
        SQLite connection object
        
    Raises:
        RuntimeError: If database connection fails
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as exc:
        raise RuntimeError(f"Database connection failed at {DB_PATH}: {exc}") from exc


def create_users_table() -> None:
    """Create users table if it doesn't exist.
    
    Raises:
        RuntimeError: If table creation fails
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT NOT NULL,
                department TEXT NOT NULL,
                two_factor_enabled INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as exc:
        raise RuntimeError(f"Failed to create users table: {exc}") from exc
    finally:
        if conn:
            conn.close()


def migrate_add_department_column() -> None:
    """Add department column to users table if needed."""
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = {column[1] for column in cursor.fetchall()}
        
        if "department" not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN department TEXT DEFAULT 'General'")
            conn.commit()
    except sqlite3.Error:
        pass  # Silently ignore if column already exists
    finally:
        if conn:
            conn.close()