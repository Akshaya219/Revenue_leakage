import sqlite3

try:
    from .db import get_connection, create_users_table
    from .security import verify_password
except ImportError:
    from auth.db import get_connection, create_users_table
    from auth.security import verify_password


def authenticate_user(username, password):
    if not username or not password:
        return None

    conn = None
    user = None
    try:
        # Ensure schema exists before querying.
        create_users_table()
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, username, email, role, password_hash, two_factor_enabled
            FROM users
            WHERE username=?
            """,
            (username,)
        )

        user = cursor.fetchone()
    except (sqlite3.Error, RuntimeError):
        return None
    finally:
        if conn is not None:
            conn.close()

    if user is None:
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "two_factor_enabled": user["two_factor_enabled"]
    }