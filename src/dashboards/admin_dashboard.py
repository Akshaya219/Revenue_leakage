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
        background: linear-gradient(135deg,{color},rgba(15,23,42,0.62));
        border:1px solid rgba(148,163,184,0.30);
        padding:20px;
        border-radius:12px;
        text-align:center;
        box-shadow:0px 12px 28px rgba(2,6,23,0.36);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        color:#f8fafc;
        ">
        <h4 style="margin:0">{title}</h4>
        <h2 style="margin:0">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_admin_dashboard():
    """
    System Administrator Dashboard
    View all department data, hospital-wide metrics, and manage the system
    """

    df, forecast, core_metrics = load_data()

    df["Claim_Submission_Date"] = pd.to_datetime(df["Claim_Submission_Date"], errors="coerce")
    df = df.dropna(subset=["Claim_Submission_Date"])

    st.markdown(
        """
        <div style="background:rgba(69,26,3,0.46); padding:15px; border-radius:10px; border-left:4px solid #f59e0b; margin-bottom:20px; border:1px solid rgba(245,158,11,0.45); box-shadow:0px 10px 24px rgba(2,6,23,0.38); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);">
        <b style="font-size:16px;color:#fde68a;">👨‍💼 SYSTEM ADMINISTRATOR DASHBOARD</b><br>
        <span style="color:#fcd34d;font-size:13px;">Full access to all departments and system management</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## 🧭 Hospital-Wide Revenue Overview")

    filters = st.columns(3)

    dept_filter = filters[0].selectbox(
        "Filter by Department",
        ["All Departments (System-Wide View)"] + sorted(df["Department"].dropna().unique()),
        key="dept_filter_admin"
    )

    show_all = dept_filter == "All Departments (System-Wide View)"
    
    if not show_all:
        df = df[df["Department"] == dept_filter]

    total_revenue = df["Billing_Amount"].sum()
    approved_revenue = df["Approved_Amount"].sum()
    leakage = total_revenue - approved_revenue
    leakage_percent = (leakage / total_revenue) * 100 if total_revenue != 0 else 0

    # Display header based on scope
    if show_all:
        st.info("📊 **Viewing Hospital-Wide Data** - All departments included")
    else:
        st.info(f"🔍 **Filtered View** - Showing {dept_filter} department only")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Total Revenue", format_inr(total_revenue), "#6366f1")

    with k2:
        kpi_card("Approved Revenue", format_inr(approved_revenue), "#22c55e")

    with k3:
        kpi_card("Revenue Leakage", format_inr(leakage), "#ef4444")

    with k4:
        kpi_card("Leakage Rate", f"{leakage_percent:.2f}%", "#f59e0b")

    if leakage_percent > 10:
        st.error("⚠️ High revenue leakage detected - Immediate action required")

    st.divider()

    # Admin Control Panel
    st.markdown("### ⚙️ System Administration Panel")
    
    admin_col1, admin_col2, admin_col3 = st.columns(3)
    
    with admin_col1:
        st.markdown(
            """
            <div style="background:rgba(15,23,42,0.58); padding:15px; border-radius:8px; text-align:center; border:1px solid rgba(148,163,184,0.30); box-shadow:0px 10px 24px rgba(2,6,23,0.34); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color:#e2e8f0;">
            <b>👥 User Management</b><br>
            <small>Manage department heads & staff</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with admin_col2:
        st.markdown(
            """
            <div style="background:rgba(15,23,42,0.58); padding:15px; border-radius:8px; text-align:center; border:1px solid rgba(148,163,184,0.30); box-shadow:0px 10px 24px rgba(2,6,23,0.34); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color:#e2e8f0;">
            <b>📋 Audit Logs</b><br>
            <small>Track system activity</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with admin_col3:
        st.markdown(
            """
            <div style="background:rgba(15,23,42,0.58); padding:15px; border-radius:8px; text-align:center; border:1px solid rgba(148,163,184,0.30); box-shadow:0px 10px 24px rgba(2,6,23,0.34); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); color:#e2e8f0;">
            <b>⚡ System Health</b><br>
            <small>Monitor performance</small>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("### 📈 Revenue Trend (All Departments)")

    trend = df.groupby(
        df["Claim_Submission_Date"].dt.to_period("M")
    )["Billing_Amount"].sum().reset_index()

    trend["Month"] = trend["Claim_Submission_Date"].astype(str)

    fig = px.line(
        trend,
        x="Month",
        y="Billing_Amount",
        markers=True,
        template="plotly_dark",
        title="Hospital-Wide Revenue Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🔮 Revenue Forecast")

    fig_forecast = px.line(
        forecast,
        x="Month",
        y="Forecasted_Revenue",
        markers=True,
        template="plotly_dark",
        title="Hospital Revenue Forecast"
    )

    st.plotly_chart(fig_forecast, use_container_width=True)

    st.divider()

    st.markdown("### 🏥 Core Hospital Financial Metrics")

    denial_rate = core_metrics["Denial_Rate"][0]
    collection_efficiency = core_metrics["Average_Collection_Efficiency"][0]
    revenue_realization = core_metrics["Average_Revenue_Realization_Rate"][0]
    claim_processing_time = core_metrics["Average_Claim_Processing_Time"][0]

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Denial Rate", f"{denial_rate:.2f}%", delta="-0.5%" if denial_rate > 15 else "+0.1%")
    m2.metric("Collection Efficiency", f"{collection_efficiency:.2f}%", delta="+1.2%")
    m3.metric("Revenue Realization", f"{revenue_realization:.2f}%", delta="+0.8%")
    m4.metric("Claim Processing Time", f"{claim_processing_time:.1f} Days", delta="-0.5 Days")

    st.divider()

    st.markdown("### 🏬 Department-wise Leakage Analysis")

    dept_data = df.copy()
    dept_data["Leakage"] = dept_data["Billing_Amount"] - dept_data["Approved_Amount"]

    dept_summary = dept_data.groupby("Department").agg({
        "Billing_Amount": "sum",
        "Approved_Amount": "sum",
        "Leakage": "sum"
    }).reset_index()

    dept_summary["Leakage_Rate"] = (
        dept_summary["Leakage"] /
        dept_summary["Billing_Amount"].replace(0, pd.NA)
    ) * 100

    # Revenue comparison
    col1, col2 = st.columns(2)
    
    with col1:
        fig_dept_leakage = px.bar(
            dept_summary.sort_values("Leakage_Rate", ascending=False),
            x="Department",
            y="Leakage_Rate",
            color="Leakage_Rate",
            template="plotly_dark",
            color_continuous_scale="Reds",
            title="Leakage Rate by Department"
        )
        st.plotly_chart(fig_dept_leakage, use_container_width=True)
    
    with col2:
        fig_dept_revenue = px.bar(
            dept_summary.sort_values("Billing_Amount", ascending=False),
            x="Department",
            y="Billing_Amount",
            color="Approved_Amount",
            template="plotly_dark",
            title="Billing vs Approved by Department",
            barmode="group"
        )
        st.plotly_chart(fig_dept_revenue, use_container_width=True)

    st.markdown("### 📊 Department Summary Table")
    
    summary_display = dept_summary.copy()
    summary_display.columns = ["Department", "Total Billing", "Approved Amount", "Leakage", "Leakage Rate %"]
    summary_display["Total Billing"] = summary_display["Total Billing"].apply(format_inr)
    summary_display["Approved Amount"] = summary_display["Approved Amount"].apply(format_inr)
    summary_display["Leakage"] = summary_display["Leakage"].apply(format_inr)
    summary_display["Leakage Rate %"] = summary_display["Leakage Rate %"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(summary_display, use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("### 🔍 Claim Behavior Analysis")

    sample = df.sample(min(len(df), 3000))

    fig_claim = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        color="Denial_Flag",
        opacity=0.6,
        template="plotly_dark",
        title="Claim Billing vs Approved Amounts"
    )

    st.plotly_chart(fig_claim, use_container_width=True)

    with st.expander("📄 Full Dataset Sample (Admin View)"):
        st.dataframe(df.head(50), use_container_width=True)