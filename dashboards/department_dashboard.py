import streamlit as st
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "feature_store.csv"))
    return df


def show_department_dashboard():

    df = load_data()

    st.markdown("## 🏥 Department Performance Dashboard")

    dept_filter = st.selectbox(
        "Select Department",
        ["All"] + sorted(df["Department"].dropna().unique())
    )

    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    total_revenue = df["Billing_Amount"].sum()
    approved = df["Approved_Amount"].sum()
    leakage = total_revenue - approved
    leakage_rate = (leakage / total_revenue) * 100 if total_revenue != 0 else 0

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    c2.metric("Approved Claims", f"₹ {approved:,.0f}")
    c3.metric("Revenue Leakage", f"₹ {leakage:,.0f}")
    c4.metric("Leakage Rate", f"{leakage_rate:.2f}%")

    if leakage_rate > 10:
        st.warning("⚠ High leakage detected for selected department")

    st.divider()

    st.markdown("### 💰 Revenue by Department")

    dept = df.groupby("Department")["Billing_Amount"].sum().reset_index()

    fig = px.bar(
        dept.sort_values("Billing_Amount", ascending=False),
        x="Department",
        y="Billing_Amount",
        color="Billing_Amount",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📊 Claim Approval vs Denial")

    if "Denial_Flag" in df.columns:

        denial_summary = df["Denial_Flag"].value_counts().reset_index()
        denial_summary.columns = ["Denial_Flag", "Count"]

        fig2 = px.pie(
            denial_summary,
            names="Denial_Flag",
            values="Count",
            template="plotly_dark"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("### 📈 Billing vs Approved Amount")

    sample = df.sample(min(len(df),3000))

    fig3 = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        color="Department",
        opacity=0.6,
        template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📄 Department Data Sample"):
        st.dataframe(df.head(20))