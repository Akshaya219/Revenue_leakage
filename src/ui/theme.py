def apply_theme():

    import streamlit as st

    st.markdown(
        """
        <style>

        :root {
            --app-bg-top: #020617;
            --app-bg-bottom: #0f172a;
            --surface: rgba(15, 23, 42, 0.52);
            --surface-2: rgba(30, 41, 59, 0.48);
            --text-primary: #e2e8f0;
            --text-muted: #94a3b8;
            --border: rgba(148, 163, 184, 0.28);
            --accent: #3b82f6;
            --accent-2: #2563eb;
        }

        /* MAIN APP BACKGROUND */
        .stApp {
            background: linear-gradient(180deg, var(--app-bg-top), var(--app-bg-bottom));
            color: var(--text-primary);
        }

        /* SIDEBAR */
        section[data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            box-shadow: 8px 0 22px rgba(2, 6, 23, 0.35);
        }

        /* SIDEBAR TEXT */
        section[data-testid="stSidebar"] * {
            color: var(--text-primary);
        }

        /* METRIC CARDS */
        div[data-testid="metric-container"] {
            background: var(--surface);
            border: 1px solid var(--border);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 12px 28px rgba(2, 6, 23, 0.35);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            transition: transform 0.2s ease;
        }

        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
            border: 1px solid #60a5fa;
        }

        /* BUTTON STYLE */
        .stButton button {
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.92), rgba(29, 78, 216, 0.92));
            color: white;
            border-radius: 10px;
            height: 2.6em;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.2s ease;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0px 4px 14px rgba(59,130,246,0.35);
        }

        /* INPUT BOX */
        .stTextInput input {
            background-color: var(--surface-2);
            color: var(--text-primary);
            border-radius: 8px;
            border: 1px solid var(--border);
            min-height: 2.2rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* SELECT BOX */
        .stSelectbox div[data-baseweb="select"] {
            background-color: var(--surface-2);
            border-radius: 8px;
            min-height: 2.2rem;
            border: 1px solid var(--border);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        /* DATAFRAME STYLE */
        .stDataFrame {
            background-color: var(--surface-2);
            border-radius: 10px;
            border: 1px solid var(--border);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }

        [data-testid="stExpander"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
        }

        /* HEADINGS */
        h1, h2, h3, h4 {
            color: var(--text-primary);
            font-weight: 600;
        }

        p, label, span, div {
            color: var(--text-primary);
        }

        /* DIVIDERS */
        hr {
            border-color: var(--border);
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )