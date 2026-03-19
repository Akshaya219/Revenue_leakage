import streamlit as st
from auth.login import authenticate_user
from auth.user_manager import DEPARTMENTS


def login_screen():
    """
    Department-based login page with department head and admin accounts
    """

    st.markdown(
        """
        <style>

        .login-container{
            background:#1e293b;
            padding:40px;
            border-radius:12px;
            width:400px;
            margin:auto;
            margin-top:80px;
            box-shadow:0px 4px 20px rgba(0,0,0,0.5);
        }

        .login-title{
            text-align:center;
            font-size:26px;
            font-weight:600;
            margin-bottom:10px;
            color:#fff;
        }

        .login-subtitle{
            text-align:center;
            font-size:14px;
            color:#94a3b8;
            margin-bottom:30px;
        }

        .info-box{
            background:#0f172a;
            border-left:4px solid #3b82f6;
            padding:12px;
            border-radius:6px;
            font-size:12px;
            color:#cbd5e1;
            margin-bottom:20px;
        }

        .admin-alert{
            background:#0f172a;
            border-left:4px solid #f59e0b;
            padding:12px;
            border-radius:6px;
            font-size:12px;
            color:#fcd34d;
            margin-bottom:20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="login-container">
        <div class="login-title">🏥 Hospital Revenue Intelligence</div>
        <div class="login-subtitle">Department Head & Admin Access Portal</div>
        """,
        unsafe_allow_html=True
    )

    # Use form to group inputs and prevent rerun on each field change
    with st.form("login_form", clear_on_submit=True):
        st.markdown("**Login Credentials**")
        username = st.text_input(
            "Username",
            placeholder="e.g., admin or cardiology_head",
            key="login_username"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        # Department selection (hidden for admin)
        st.markdown("**Select Department** (Department Heads only)")
        selected_department = st.selectbox(
            "Department",
            options=DEPARTMENTS,
            label_visibility="collapsed",
            key="dept_select"
        )

        login = st.form_submit_button("Login", use_container_width=True, type="primary")

    # Info boxes with credentials
    st.markdown(
        """
        <div class="admin-alert">
        <strong>⚡ System Admin:</strong><br>
        • Username: <code>admin</code><br>
        • Password: <code>Admin@123</code><br>
        <em>Ignore department selection - view all data</em>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-box">
        <strong>Department Heads:</strong><br>
        • Cardiology: cardiology_head / Cardiology@123<br>
        • Emergency: emergency_head / Emergency@123<br>
        • Medicine: medicine_head / Medicine@123<br>
        • Neurology: neurology_head / Neurology@123<br>
        • Orthopedics: orthopedics_head / Orthopedics@123
        </div>
        """,
        unsafe_allow_html=True
    )

    if login:
        if not username or not password:
            st.error("❌ Please enter both username and password")
            return

        try:
            # Check if this is admin login
            if username == "admin":
                # Admin authentication - don't check department
                user = authenticate_user(username, password, department="Admin")
            else:
                # Department head authentication - verify department
                user = authenticate_user(username, password, department=selected_department)
        except Exception as exc:
            st.error(f"❌ Authentication service error: {exc}")
            return

        if user:
            # For department heads, verify the department matches
            if user["role"] == "department_head" and user["department"] != selected_department:
                st.error(
                    f"❌ **Access Denied**: Your account is registered for the "
                    f"{user['department']} department. You cannot access the "
                    f"{selected_department} department. Please select the correct department."
                )
                return

            # Store user info in session
            st.session_state["user"] = user
            st.session_state["role"] = user["role"]
            st.session_state["department"] = user["department"]
            st.session_state["authenticated"] = True

            st.success("✅ Login successful! Redirecting...")
            st.rerun()

        else:
            st.error(
                "❌ Invalid credentials or department mismatch. "
                "Please verify your username, password, and selected department."
            )

    st.markdown("</div>", unsafe_allow_html=True)