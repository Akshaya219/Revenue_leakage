"""User authentication with credential and department verification."""

import sqlite3
from typing import Dict, Optional

try:
    from .db import get_connection, create_users_table
    from .security import verify_password
except ImportError:
    from auth.db import get_connection, create_users_table
    from auth.security import verify_password


def authenticate_user(
    username: str,
    password: str,
    department: Optional[str] = None
) -> Optional[Dict]:
    """Authenticate user with credentials and optional department verification.
    
    Args:
        username: User's login username
        password: User's login password
        department: Optional department to verify (for dept heads)
        
    Returns:
        User dictionary with id, username, email, role, department on success
        None if authentication fails
    """
    if not username or not password:
        return None

    conn: Optional[sqlite3.Connection] = None
    try:
        create_users_table()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, role, department, password_hash, two_factor_enabled FROM users WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()
    except (sqlite3.Error, RuntimeError):
        return None
    finally:
        if conn:
            conn.close()

    if user is None or not verify_password(password, user["password_hash"]):
        return None

    # Verify department match for department heads
    if department and user["department"] != department:
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "department": user["department"],
        "two_factor_enabled": user["two_factor_enabled"]
    }