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

        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700&display=swap');

        .stApp * {
            font-family: 'Manrope', sans-serif;
        }

        section.main > div.block-container {
            min-height: 88vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding-top: 0.6rem;
            padding-bottom: 0.6rem;
        }

        .login-panel{
            background: rgba(15, 23, 42, 0.64);
            border: 1px solid rgba(148, 163, 184, 0.30);
            border-radius: 16px;
            padding: 26px;
            box-shadow: 0px 16px 36px rgba(2, 6, 23, 0.40);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .login-eyebrow {
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #93c5fd;
            margin-bottom: 8px;
            text-align: center;
        }

        .login-title {
            font-size: 28px;
            font-weight: 700;
            color: #f8fafc;
            margin: 0;
            line-height: 1.2;
            text-align: center;
        }

        .login-subtitle {
            margin-top: 10px;
            margin-bottom: 22px;
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.5;
            text-align: center;
        }

        .support-panel {
            background: rgba(15, 23, 42, 0.50);
            border: 1px solid rgba(148, 163, 184, 0.28);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0px 12px 30px rgba(2, 6, 23, 0.35);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            height: 100%;
        }

        .support-title {
            color: #f8fafc;
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .support-text {
            color: #cbd5e1;
            font-size: 13px;
            line-height: 1.5;
            margin-bottom: 12px;
        }

        .credential-block {
            background: rgba(30, 41, 59, 0.62);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 12px;
            padding: 12px;
            margin-top: 10px;
        }

        .credential-title {
            color: #f1f5f9;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .credential-line {
            color: #cbd5e1;
            font-size: 12px;
            margin-bottom: 4px;
        }

        .credential-line code {
            color: #93c5fd;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(59, 130, 246, 0.35);
            border-radius: 6px;
            padding: 1px 6px;
        }

        .login-panel [data-testid="stTextInput"] input,
        .login-panel [data-testid="stSelectbox"] div[data-baseweb="select"] {
            min-height: 2.2rem;
            background: rgba(30, 41, 59, 0.58);
            border: 1px solid rgba(148, 163, 184, 0.30);
            color: #e2e8f0;
            border-radius: 10px;
        }

        .login-panel [data-testid="stFormSubmitButton"] button {
            margin-top: 8px;
            border-radius: 10px;
            font-weight: 700;
            height: 2.8rem;
        }

        .login-panel [data-testid="stMarkdownContainer"] p {
            color: #e2e8f0;
        }

        @media (max-width: 900px) {
            section.main > div.block-container {
                min-height: auto;
                display: block;
                padding-top: 1rem;
                padding-bottom: 1rem;
            }

            .login-panel,
            .support-panel {
                padding: 18px;
            }
            .login-title {
                font-size: 24px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    left_space, center_col, right_space = st.columns([0.08, 0.84, 0.08])
    with center_col:
        form_col, info_col = st.columns([1.25, 1.0], gap="large")

    with form_col:
        st.markdown(
            """
            <div class="login-panel">
            <div class="login-eyebrow">Secure Access</div>
            <h1 class="login-title">🏥 Hospital Revenue Intelligence</h1>
            <p class="login-subtitle">Sign in with your role-based credentials to continue to your dashboard.</p>
            """,
            unsafe_allow_html=True
        )

        # Keep form values stable after submit so department selection is reliable.
        with st.form("login_form"):
            st.markdown("**Username**")
            username = st.text_input(
                "Username",
                placeholder="e.g., admin or cardiology_head",
                label_visibility="collapsed",
                key="login_username"
            )
            st.markdown("**Password**")
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                label_visibility="collapsed",
                key="login_password"
            )

            st.markdown("**Department**")
            selected_department = st.selectbox(
                "Department",
                options=DEPARTMENTS,
                label_visibility="collapsed",
                key="dept_select"
            )

            login = st.form_submit_button("Sign In", use_container_width=True, type="primary")

        st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
        st.markdown(
            """
            <div class="support-panel">
              <div class="support-title">Quick Access Credentials</div>
              <div class="support-text">Use these accounts for testing and role-based views.</div>

              <div class="credential-block">
                <div class="credential-title">System Admin</div>
                <div class="credential-line">Username: <code>admin</code></div>
                <div class="credential-line">Password: <code>Admin@123</code></div>
                <div class="credential-line">Department: Any selection works</div>
              </div>

              <div class="credential-block">
                <div class="credential-title">Department Heads</div>
                <div class="credential-line"><code>cardiology_head</code> / <code>Cardiology@123</code></div>
                <div class="credential-line"><code>emergency_head</code> / <code>Emergency@123</code></div>
                <div class="credential-line"><code>medicine_head</code> / <code>Medicine@123</code></div>
                <div class="credential-line"><code>neurology_head</code> / <code>Neurology@123</code></div>
                <div class="credential-line"><code>orthopedics_head</code> / <code>Orthopedics@123</code></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if login:
        username = username.strip() if username else ""
        password = password.strip() if password else ""

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
