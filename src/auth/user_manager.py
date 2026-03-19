"""User management with department-based access and role assignment."""

import sqlite3
from typing import List, Dict, Optional, Tuple, Any

try:
    from .db import get_connection, create_users_table
    from .security import hash_password
except ImportError:
    from auth.db import get_connection, create_users_table
    from auth.security import hash_password


DEPARTMENTS = [
    "Cardiology",
    "Emergency",
    "General Medicine",
    "Neurology",
    "Orthopedics"
]

ADMIN_DEPARTMENT = "Admin"
AVAILABLE_ROLES = ["admin", "department_head", "finance_manager", "data_analyst", "doctor"]


def create_user(
    username: str,
    email: str,
    password: str,
    role: str,
    department: str = "General",
    two_factor: bool = False
) -> Tuple[bool, str]:
    """Create new user with department and role assignment.
    
    Args:
        username: Unique username
        email: User email
        password: Plain text password (bcrypt hashed)
        role: User role (admin, department_head, etc)
        department: Assigned department
        two_factor: Enable 2FA flag
        
    Returns:
        (success: bool, message: str)
    """
    conn = None
    try:
        if not username or not email or not password or not role:
            return False, "username, email, password, and role are required"

        # Allow "Admin" for admin role, otherwise validate against DEPARTMENTS
        valid_departments = DEPARTMENTS + [ADMIN_DEPARTMENT]
        if department not in valid_departments:
            return False, f"Invalid department. Valid departments: {', '.join(valid_departments)}"

        create_users_table()
        conn = get_connection()
        cursor = conn.cursor()

        hashed = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role, department, two_factor_enabled)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, email, hashed, role, department, int(two_factor))
        )

        conn.commit()
        return True, f"User created successfully"
    except sqlite3.IntegrityError as exc:
        return False, f"User already exists or duplicate email: {exc}"
    except (sqlite3.Error, RuntimeError) as exc:
        return False, f"Failed to create user: {exc}"
    finally:
        if conn is not None:
            conn.close()


def initialize_default_users() -> bool:
    """Create default 6 accounts (1 admin + 5 dept heads) on first run.
    
    Returns:
        True if users created, False if already exist
    """
    conn = None
    try:
        create_users_table()
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if users already exist
        cursor.execute("SELECT COUNT(*) as count FROM users")
        count = cursor.fetchone()["count"]
        
        if count > 0:
            return False
        
        default_users = [
            {
                "username": "admin",
                "email": "admin@hospital.com",
                "password": "Admin@123",
                "department": "Admin",
                "role": "admin"
            },
            {
                "username": "cardiology_head",
                "email": "head.cardiology@hospital.com",
                "password": "Cardiology@123",
                "department": "Cardiology",
                "role": "department_head"
            },
            {
                "username": "emergency_head",
                "email": "head.emergency@hospital.com",
                "password": "Emergency@123",
                "department": "Emergency",
                "role": "department_head"
            },
            {
                "username": "medicine_head",
                "email": "head.medicine@hospital.com",
                "password": "Medicine@123",
                "department": "General Medicine",
                "role": "department_head"
            },
            {
                "username": "neurology_head",
                "email": "head.neurology@hospital.com",
                "password": "Neurology@123",
                "department": "Neurology",
                "role": "department_head"
            },
            {
                "username": "orthopedics_head",
                "email": "head.orthopedics@hospital.com",
                "password": "Orthopedics@123",
                "department": "Orthopedics",
                "role": "department_head"
            }
        ]
        
        for user in default_users:
            try:
                create_user(
                    username=user["username"],
                    email=user["email"],
                    password=user["password"],
                    role=user.get("role", "department_head"),
                    department=user["department"]
                )
            except Exception as e:
                print(f"Could not create user {user['username']}: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error initializing default users: {e}")
        return False
    finally:
        if conn:
            conn.close()


def get_user_by_username(username: str) -> Optional[Dict]:
    """Get user details by username"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, username, email, role, department, two_factor_enabled
            FROM users
            WHERE username = ?
            """,
            (username,)
        )
        
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
        
    except sqlite3.Error as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn:
            conn.close()


def get_all_users() -> List[Dict[str, Any]]:
    """Get all users from database.
    
    Returns:
        List of user dicts ordered by department, then username
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, role, department, created_at FROM users ORDER BY department, username"
        )
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_users_by_department(department: str) -> List[Dict[str, Any]]:
    """Get all users assigned to a specific department.
    
    Args:
        department: Department name to filter by
        
    Returns:
        List of user dicts in that department
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, role, department, created_at FROM users WHERE department = ? ORDER BY username",
            (department,)
        )
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching department users: {e}")
        return []
    finally:
        if conn:
            conn.close()


def update_user_password(username: str, new_password: str) -> bool:
    """Update user's password with bcrypt hash.
    
    Args:
        username: User to update
        new_password: New password (will be hashed)
        
    Returns:
        True if successful, False otherwise
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(new_password), username)
        )
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        if conn:
            conn.close()


def delete_user(username: str) -> bool:
    """Delete user from system (admin only).
    
    Args:
        username: Username to delete
        
    Returns:
        True if user deleted, False otherwise
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        if conn:
            conn.close()