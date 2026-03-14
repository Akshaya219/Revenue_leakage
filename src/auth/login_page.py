import streamlit as st
from auth.login import authenticate_user


def login_screen():

    st.markdown(
        """
        <style>

        .login-container{
            background:#1e293b;
            padding:40px;
            border-radius:12px;
            width:350px;
            margin:auto;
            margin-top:120px;
            box-shadow:0px 4px 20px rgba(0,0,0,0.5);
        }

        .login-title{
            text-align:center;
            font-size:26px;
            font-weight:600;
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
        """,
        unsafe_allow_html=True
    )

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login = st.button("Login", use_container_width=True)

    if login:

        user = authenticate_user(username, password)

        if user:

            st.session_state["user"] = user
            st.session_state["role"] = user["role"]
            st.session_state["authenticated"] = True

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)