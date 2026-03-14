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
    core_metrics = pd.read_csv(os.path.join(DATA_DIR, "core_hospital_metrics.csv"))
    return df, forecast, core_metrics


def format_inr(num):
    num = float(num)
    if num >= 10000000:
        return f"₹ {num/10000000:.2f} Cr"
    if num >= 100000:
        return f"₹ {num/100000:.2f} L"
    return f"₹ {num:,.0f}"


def kpi_card(title,value,color):

    st.markdown(
        f"""
        <div style="
        background: linear-gradient(135deg,{color},#1e293b);
        padding:20px;
        border-radius:12px;
        text-align:center;
        ">
        <h4 style="margin:0">{title}</h4>
        <h2 style="margin:0">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_admin_dashboard():

    df, forecast, core_metrics = load_data()

    df["Claim_Submission_Date"] = pd.to_datetime(df["Claim_Submission_Date"], errors="coerce")
    df = df.dropna(subset=["Claim_Submission_Date"])

    st.markdown("## 🧭 Executive Revenue Overview")

    filters = st.columns(2)

    dept_filter = filters[0].selectbox(
        "Department",
        ["All"] + sorted(df["Department"].dropna().unique())
    )

    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    total_revenue = df["Billing_Amount"].sum()
    approved_revenue = df["Approved_Amount"].sum()
    leakage = total_revenue - approved_revenue
    leakage_percent = (leakage / total_revenue) * 100 if total_revenue != 0 else 0

    k1,k2,k3,k4 = st.columns(4)

    with k1:
        kpi_card("Total Revenue", format_inr(total_revenue), "#6366f1")

    with k2:
        kpi_card("Approved Revenue", format_inr(approved_revenue), "#22c55e")

    with k3:
        kpi_card("Revenue Leakage", format_inr(leakage), "#ef4444")

    with k4:
        kpi_card("Leakage Rate", f"{leakage_percent:.2f}%", "#f59e0b")

    if leakage_percent > 10:
        st.error("⚠ High revenue leakage detected")

    st.divider()

    st.markdown("### 📈 Revenue Trend")

    trend = df.groupby(
        df["Claim_Submission_Date"].dt.to_period("M")
    )["Billing_Amount"].sum().reset_index()

    trend["Month"] = trend["Claim_Submission_Date"].astype(str)

    fig = px.line(
        trend,
        x="Month",
        y="Billing_Amount",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### 🔮 Revenue Forecast")

    fig_forecast = px.line(
        forecast,
        x="Month",
        y="Forecasted_Revenue",
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig_forecast,use_container_width=True)

    st.divider()

    st.markdown("### 🏥 Core Hospital Financial Metrics")

    denial_rate = core_metrics["Denial_Rate"][0]
    collection_efficiency = core_metrics["Average_Collection_Efficiency"][0]
    revenue_realization = core_metrics["Average_Revenue_Realization_Rate"][0]
    claim_processing_time = core_metrics["Average_Claim_Processing_Time"][0]

    m1,m2,m3,m4 = st.columns(4)

    m1.metric("Denial Rate", f"{denial_rate:.2f}%")
    m2.metric("Collection Efficiency", f"{collection_efficiency:.2f}%")
    m3.metric("Revenue Realization", f"{revenue_realization:.2f}%")
    m4.metric("Claim Processing Time", f"{claim_processing_time:.1f} Days")

    st.divider()

    st.markdown("### 🏬 Department Leakage Analysis")

    dept = df.copy()
    dept["Leakage"] = dept["Billing_Amount"] - dept["Approved_Amount"]

    dept_summary = dept.groupby("Department").agg({
        "Billing_Amount":"sum",
        "Leakage":"sum"
    }).reset_index()

    dept_summary["Leakage_Rate"] = (
        dept_summary["Leakage"] /
        dept_summary["Billing_Amount"].replace(0,pd.NA)
    ) * 100

    fig_dept = px.bar(
        dept_summary.sort_values("Leakage_Rate",ascending=False),
        x="Department",
        y="Leakage_Rate",
        color="Leakage_Rate",
        template="plotly_dark",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig_dept,use_container_width=True)

    st.markdown("### 🔍 Claim Behavior Analysis")

    sample = df.sample(min(len(df),3000))

    fig_claim = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        color="Denial_Flag",
        opacity=0.6,
        template="plotly_dark"
    )

    st.plotly_chart(fig_claim,use_container_width=True)

    with st.expander("📄 Claim Data Sample"):
        st.dataframe(df.head(20))