import streamlit as st
import pandas as pd
import plotly.express as px
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "feature_store.csv"))
    forecast = pd.read_csv(os.path.join(DATA_DIR, "revenue_forecast.csv"))
    return df, forecast


def show_analyst_dashboard():

    df, forecast = load_data()

    st.markdown("## 🧠 Data Analytics & ML Insights")

    filters = st.columns(2)

    dept_filter = filters[0].selectbox(
        "Department",
        ["All"] + sorted(df["Department"].dropna().unique())
    )

    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    total_claims = len(df)
    denied_claims = df["Denial_Flag"].sum() if "Denial_Flag" in df.columns else 0
    anomaly_count = df["Anomaly_Flag"].sum() if "Anomaly_Flag" in df.columns else 0

    c1,c2,c3 = st.columns(3)

    c1.metric("Total Claims", total_claims)
    c2.metric("Denied Claims", denied_claims)
    c3.metric("Detected Anomalies", anomaly_count)

    st.divider()

    st.markdown("### 🔮 Revenue Forecast Model")

    fig = px.line(
        forecast,
        x="Month",
        y="Forecasted_Revenue",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📉 Claim Approval Behavior")

    sample = df.sample(min(len(df),3000))

    fig_claim = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        color="Denial_Flag",
        opacity=0.6,
        template="plotly_dark"
    )

    st.plotly_chart(fig_claim, use_container_width=True)

    st.divider()

    st.markdown("### 🚨 Anomaly Detection Distribution")

    if "Anomaly_Flag" in df.columns:

        anomaly_counts = df["Anomaly_Flag"].value_counts().reset_index()
        anomaly_counts.columns = ["Anomaly_Flag", "Count"]

        fig_anomaly = px.bar(
            anomaly_counts,
            x="Anomaly_Flag",
            y="Count",
            color="Anomaly_Flag",
            template="plotly_dark",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(fig_anomaly, use_container_width=True)

    st.divider()

    st.markdown("### 🏥 Department Revenue Patterns")

    dept_summary = df.groupby("Department")["Billing_Amount"].sum().reset_index()

    fig_dept = px.bar(
        dept_summary.sort_values("Billing_Amount", ascending=False),
        x="Department",
        y="Billing_Amount",
        template="plotly_dark",
        color="Billing_Amount"
    )

    st.plotly_chart(fig_dept, use_container_width=True)

    with st.expander("📄 Sample Data"):
        st.dataframe(df.head(20))