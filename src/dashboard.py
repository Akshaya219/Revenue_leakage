import streamlit as st

from dashboards.admin_dashboard import show_admin_dashboard
from dashboards.finance_dashboard import show_finance_dashboard
from dashboards.analyst_dashboard import show_analyst_dashboard
from dashboards.department_dashboard import show_department_dashboard
from dashboards.doctor_dashboard import show_doctor_dashboard

from auth.db import create_users_table
from auth.login_page import login_screen
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
except Exception as exc:
    st.error(f"Authentication database initialization failed: {exc}")
    st.stop()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login_screen()
    st.stop()

try:
    role = st.session_state["role"]
    user = st.session_state["user"]["username"]
except KeyError:
    st.session_state.clear()
    st.error("Session data is invalid. Please log in again.")
    st.stop()

with st.sidebar:

    st.markdown(
        """
        <h2 style='text-align:center;'>🏥 Hospital Revenue Intelligence</h2>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f"""
        <div style="
        background:#1e293b;
        padding:15px;
        border-radius:10px;
        margin-bottom:20px;
        ">
        <b>User:</b> {user}<br>
        <b>Role:</b> {role}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown(
    """
    <h1 style='font-size:36px;'>Hospital Revenue Intelligence Platform</h1>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

if role == "admin":
    show_admin_dashboard()

elif role == "finance_manager":
    show_finance_dashboard()

elif role == "data_analyst":
    show_analyst_dashboard()

elif role == "department_head":
    show_department_dashboard()

elif role == "doctor":
    show_doctor_dashboard()

else:
    st.error("Role not recognized")