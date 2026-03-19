"""
Department-based Access Control
Enforces authorization rules for accessing department data
"""

import streamlit as st
from typing import Optional, Callable


def require_authentication() -> bool:
    """
    Check if user is authenticated.
    Redirects to login if not.
    """
    if "authenticated" not in st.session_state or not st.session_state.get("authenticated"):
        st.error("❌ You must be logged in to access this page")
        st.stop()
    return True


def require_department_access(allowed_departments: list) -> bool:
    """
    Check if user has access to their department.
    
    Args:
        allowed_departments: List of departments user can access
        
    Returns:
        True if user has access, False otherwise (shows error and stops)
    """
    require_authentication()
    
    user_dept = st.session_state.get("department")
    
    if user_dept not in allowed_departments:
        st.error(
            f"❌ **Access Denied**: Your department ({user_dept}) does not have "
            f"access to this resource. Contact your administrator."
        )
        st.stop()
    
    return True


def get_user_department() -> Optional[str]:
    """Get current user's department"""
    return st.session_state.get("department")


def get_user_role() -> Optional[str]:
    """Get current user's role"""
    return st.session_state.get("role")


def get_current_user() -> Optional[dict]:
    """Get current user information"""
    return st.session_state.get("user")


def verify_department_access_to_data(data_department: str) -> bool:
    """
    Verify if current user can access data from a specific department.
    
    Args:
        data_department: Department of the data being accessed
        
    Returns:
        True if access allowed, False otherwise
    """
    user_dept = get_user_department()
    
    if user_dept != data_department:
        return False
    
    return True


def filter_data_by_department(df, department_column: str = "Department") -> object:
    """
    Filter DataFrame to only show data for user's department.
    
    Args:
        df: Pandas DataFrame to filter
        department_column: Column name containing department info
        
    Returns:
        Filtered DataFrame
    """
    require_authentication()
    user_dept = get_user_department()
    
    if department_column in df.columns:
        df = df[df[department_column] == user_dept]
    
    return df


def show_access_denied(resource_name: str = "resource", department: str = None):
    """
    Display a formatted access denied message.
    
    Args:
        resource_name: Name of the resource being accessed
        department: Department that was attempted to be accessed
    """
    st.error(
        f"❌ **Access Denied**\n\n"
        f"You are not authorized to access {resource_name}. "
        f"You can only view data from your department: **{get_user_department()}**"
    )


def show_department_info():
    """
    Display user's department information in sidebar.
    """
    with st.sidebar:
        user_dept = get_user_department()
        user_name = st.session_state.get("user", {}).get("username", "Unknown")
        
        st.markdown(
            f"""
            <div style="background:#1e293b; padding:15px; border-radius:10px;">
            <b>👤 User:</b> {user_name}<br>
            <b>🏢 Department:</b> {user_dept}<br>
            <b>📊 Access Level:</b> Department Head
            </div>
            """,
            unsafe_allow_html=True
        )


def is_department_administrator() -> bool:
    """Check if user is a department administrator"""
    return get_user_role() == "department_head"


def check_department_access_for_records(records: list, 
                                       department_field: str = "Department") -> list:
    """
    Filter a list of records to only include those from user's department.
    
    Args:
        records: List of dictionaries/records to filter
        department_field: Field name containing department info
        
    Returns:
        Filtered list of records
    """
    user_dept = get_user_department()
    
    return [
        record for record in records 
        if record.get(department_field) == user_dept
    ]
