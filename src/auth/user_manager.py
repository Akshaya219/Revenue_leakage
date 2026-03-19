import sqlite3

try:
    from .db import get_connection, create_users_table
    from .security import hash_password
except ImportError:
    from auth.db import get_connection, create_users_table
    from auth.security import hash_password

def create_user(username, email, password, role, two_factor=False):
    conn = None
    try:
        if not username or not email or not password or not role:
            return False, "username, email, password, and role are required"

        create_users_table()
        conn = get_connection()
        cursor = conn.cursor()

        hashed = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (username,email,password_hash,role,two_factor_enabled)
            VALUES (?,?,?,?,?)
            """,
            (username, email, hashed, role, int(two_factor))
        )

        conn.commit()
        return True, "user created"
    except sqlite3.IntegrityError as exc:
        return False, f"user already exists or duplicate email: {exc}"
    except (sqlite3.Error, RuntimeError) as exc:
        return False, f"failed to create user: {exc}"
    finally:
        if conn is not None:
            conn.close()