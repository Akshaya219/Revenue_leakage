import streamlit as st

from dashboards.admin_dashboard import show_admin_dashboard
from dashboards.finance_dashboard import show_finance_dashboard
from dashboards.analyst_dashboard import show_analyst_dashboard
from dashboards.department_dashboard import show_department_dashboard
from dashboards.doctor_dashboard import show_doctor_dashboard

from auth.db import create_users_table, migrate_add_department_column
from auth.login_page import login_screen
from auth.user_manager import initialize_default_users
from auth.access_control import require_authentication, get_user_department, show_department_info
from ui.theme import apply_theme

st.set_page_config(
    page_title="Hospital Revenue Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

try:
    create_users_table()
    migrate_add_department_column()
    # Initialize default users on first run
    initialize_default_users()
except Exception as exc:
    st.error(f"❌ Authentication database initialization failed: {exc}")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()

try:
    require_authentication()
    role = st.session_state["role"]
    user = st.session_state["user"]["username"]
    department = st.session_state.get("department", "Unknown")
except KeyError:
    st.session_state.clear()
    st.error("❌ Session data is invalid. Please log in again.")
    st.stop()

with st.sidebar:

    st.markdown(
        """
        <h2 style='text-align:center;'>🏥 Hospital Revenue Intelligence</h2>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Display different info based on role
    role = st.session_state.get("role", "Unknown")
    department = st.session_state.get("department", "Unknown")
    user = st.session_state["user"]["username"]
    
    if role == "admin":
        st.markdown(
            f"""
            <div style="
            background:rgba(69, 26, 3, 0.46);
            padding:15px;
            border-radius:10px;
            margin-bottom:20px;
            border:1px solid rgba(245, 158, 11, 0.45);
            border-left:4px solid #f59e0b;
            box-shadow:0px 10px 24px rgba(2, 6, 23, 0.38);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            color:#fde68a;
            ">
            <b>👨‍💼 Admin User:</b> {user}<br>
            <b>🔑 Access Level:</b> System Administrator<br>
            <b>📊 Visible Data:</b> All Departments
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="
            background:rgba(15, 23, 42, 0.58);
            padding:15px;
            border-radius:10px;
            margin-bottom:20px;
            border:1px solid rgba(148, 163, 184, 0.30);
            box-shadow:0px 10px 24px rgba(2, 6, 23, 0.38);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            color:#e2e8f0;
            ">
            <b>👤 User:</b> {user}<br>
            <b>🏢 Department:</b> {department}<br>
            <b>📊 Role:</b> {role.replace('_', ' ').title()}
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown(
    """
    <h1 style='font-size:36px;'>🏥 Hospital Revenue Intelligence Platform</h1>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

if role == "admin":
    st.markdown(f"### 👨‍💼 Welcome, System Administrator")
    st.warning("🔑 You have full system access to all departments and administrative functions.")
    show_admin_dashboard()

elif role == "finance_manager":
    show_finance_dashboard()

elif role == "data_analyst":
    show_analyst_dashboard()

elif role == "department_head":
    st.markdown(f"### Welcome, {department} Department Head")
    st.info(f"👋 You can only view revenue and metrics for the **{department}** department.")
    show_department_dashboard()

elif role == "doctor":
    show_doctor_dashboard()

else:
    st.error(f"❌ Role '{role}' is not recognized. Please contact your administrator.")