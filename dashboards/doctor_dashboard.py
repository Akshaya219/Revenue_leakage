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


def show_doctor_dashboard():

    df = load_data()

    st.markdown("## 👨‍⚕️ Doctor Performance Dashboard")

    proc_filter = st.selectbox(
        "Procedure Code",
        ["All"] + sorted(df["Procedure_Code"].dropna().unique())
    )

    if proc_filter != "All":
        df = df[df["Procedure_Code"] == proc_filter]

    total_billing = df["Billing_Amount"].sum()
    total_approved = df["Approved_Amount"].sum()
    procedures = df["Procedure_Code"].nunique()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Billing Value", f"₹ {total_billing:,.0f}")
    c2.metric("Approved Amount", f"₹ {total_approved:,.0f}")
    c3.metric("Unique Procedures", procedures)

    st.divider()

    st.markdown("### 🏥 Procedure Revenue Distribution")

    proc = df.groupby("Procedure_Code")["Billing_Amount"].sum().reset_index()

    fig = px.bar(
        proc.sort_values("Billing_Amount", ascending=False),
        x="Procedure_Code",
        y="Billing_Amount",
        color="Billing_Amount",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 📊 Billing vs Approved Comparison")

    sample = df.sample(min(len(df),3000))

    fig2 = px.scatter(
        sample,
        x="Billing_Amount",
        y="Approved_Amount",
        color="Procedure_Code",
        opacity=0.6,
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("### 📈 Procedure Frequency")

    freq = df["Procedure_Code"].value_counts().reset_index()
    freq.columns = ["Procedure_Code","Count"]

    fig3 = px.bar(
        freq,
        x="Procedure_Code",
        y="Count",
        color="Count",
        template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("📄 Sample Data"):
        st.dataframe(df.head(20))