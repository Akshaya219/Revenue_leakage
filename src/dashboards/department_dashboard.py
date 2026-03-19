import streamlit as st
import pandas as pd
import plotly.express as px
import os

try:
    from auth.access_control import verify_department_access_to_data, get_user_department
except ImportError:
    from access_control import verify_department_access_to_data, get_user_department

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "feature_store.csv"))
    return df


def show_department_dashboard():
    """
    Department Head Dashboard - Shows only data for the user's department
    Enforces strict access control to prevent cross-department data access
    """
    
    df = load_data()
    user_department = get_user_department()

    st.markdown(f"## 🏥 {user_department} Department Performance Dashboard")
    
    st.markdown(
        f"""
        <div style="background:rgba(15,23,42,0.58); padding:12px; border-radius:6px; border-left:4px solid #3b82f6; margin-bottom:20px; color:#bfdbfe; border:1px solid rgba(59,130,246,0.42); box-shadow:0px 10px 24px rgba(2,6,23,0.34); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);">
        <b>🔒 Restricted Access:</b> You can only view data for the <b>{user_department}</b> department.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter data to only show user's department
    df_filtered = df[df["Department"] == user_department].copy()

    if df_filtered.empty:
        st.warning(f"No data available for {user_department} department.")
        return

    # Key Metrics
    total_revenue = df_filtered["Billing_Amount"].sum()
    approved = df_filtered["Approved_Amount"].sum()
    leakage = total_revenue - approved
    leakage_rate = (leakage / total_revenue) * 100 if total_revenue != 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    c2.metric("Approved Claims", f"₹ {approved:,.0f}")
    c3.metric("Revenue Leakage", f"₹ {leakage:,.0f}")
    c4.metric("Leakage Rate", f"{leakage_rate:.2f}%")

    if leakage_rate > 10:
        st.warning("⚠️ High leakage detected for your department")

    st.divider()

    # Department-specific metrics
    st.markdown(f"### 💰 {user_department} Revenue Overview")

    col1, col2 = st.columns(2)

    with col1:
        # Claims by status
        if "Denial_Flag" in df_filtered.columns:
            denial_counts = df_filtered["Denial_Flag"].value_counts().reset_index()
            denial_counts.columns = ["Status", "Count"]

            fig_denial = px.pie(
                denial_counts,
                names="Status",
                values="Count",
                title=f"Claims Status - {user_department}",
                template="plotly_dark",
                color_discrete_map={1: "#ef4444", 0: "#10b981"}
            )
            st.plotly_chart(fig_denial, use_container_width=True)

    with col2:
        # Billing vs Approved
        summary_data = pd.DataFrame({
            "Category": ["Billing Amount", "Approved Amount"],
            "Amount": [total_revenue, approved]
        })
        
        fig_summary = px.bar(
            summary_data,
            x="Category",
            y="Amount",
            title=f"Billing vs Approved - {user_department}",
            template="plotly_dark",
            color="Amount"
        )
        st.plotly_chart(fig_summary, use_container_width=True)

    st.divider()

    # Detailed Analysis
    st.markdown(f"### 📊 Claims Analysis - {user_department}")

    sample_size = min(len(df_filtered), 3000)
    sample = df_filtered.sample(sample_size) if len(df_filtered) > 1 else df_filtered

    fig_scatter = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        hover_data=["Department"],
        title=f"Billing vs Approved Amount (Sample of {sample_size} records)",
        template="plotly_dark",
        opacity=0.6,
        color_discrete_sequence=["#3b82f6"]
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.divider()

    # Department Data
    st.markdown(f"### 📄 {user_department} Department Data")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.text(f"Showing {len(df_filtered)} records from {user_department} department")
    with col2:
        if st.button("📥 Download Data"):
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{user_department}_revenue_data.csv",
                mime="text/csv"
            )

    st.dataframe(df_filtered.head(20), use_container_width=True)

    # Additional metrics by category if available
    st.divider()
    st.markdown(f"### 📈 Detailed Breakdown - {user_department}")
    
    if "Service_Type" in df_filtered.columns:
        service_breakdown = df_filtered.groupby("Service_Type").agg({
            "Billing_Amount": "sum",
            "Approved_Amount": "sum"
        }).reset_index()
        
        service_breakdown["Leakage"] = service_breakdown["Billing_Amount"] - service_breakdown["Approved_Amount"]
        
        fig_service = px.bar(
            service_breakdown,
            x="Service_Type",
            y=["Billing_Amount", "Approved_Amount"],
            title=f"Revenue by Service Type - {user_department}",
            template="plotly_dark",
            barmode="group"
        )
        st.plotly_chart(fig_service, use_container_width=True)
        
        st.dataframe(service_breakdown, use_container_width=True)