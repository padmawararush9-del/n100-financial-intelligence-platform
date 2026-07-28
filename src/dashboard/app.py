import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Nifty100 Financial Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("📈 Nifty100 Dashboard")
st.sidebar.markdown("---")
st.sidebar.success("Navigation")

st.sidebar.markdown("""
### Dashboard Modules

🏠 Home

🏢 Company Profile

🔍 Stock Screener

👥 Peer Comparison

📈 Trend Analysis

🏭 Sector Analysis

💰 Capital Allocation

💎 Valuation Dashboard
""")

st.sidebar.markdown("---")
st.sidebar.info(
    "Built using Streamlit, SQLite, Pandas & Plotly"
)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Nifty100 Financial Intelligence Dashboard")
st.write("An interactive financial analytics dashboard for Nifty100 companies.")

# -----------------------------
# Load Database
# -----------------------------
with st.spinner("Loading data..."):

    conn = sqlite3.connect("data/nifty100.db")

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    ranking = pd.read_sql(
        "SELECT * FROM ranking_engine",
        conn
    )

    conn.close()

if ranking.empty:
    st.error("No ranking data found.")
    st.stop()

# -----------------------------
# KPI Cards
# -----------------------------
total_companies = companies["company_name"].nunique()

avg_score = ranking["composite_quality_score"].mean()

strong_buy = (
    ranking["recommendation"] == "Strong Buy"
).sum()

buy = (
    ranking["recommendation"] == "Buy"
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Companies",
    total_companies
)

col2.metric(
    "Average Score",
    f"{avg_score:.2f}"
)

col3.metric(
    "Strong Buy",
    strong_buy
)

col4.metric(
    "Buy",
    buy
)

st.divider()

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:

    recommendation_chart = (
        ranking["recommendation"]
        .value_counts()
        .reset_index()
    )

    recommendation_chart.columns = [
        "Recommendation",
        "Count"
    ]

    fig = px.pie(
        recommendation_chart,
        names="Recommendation",
        values="Count",
        hole=0.45,
        title="Recommendation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.histogram(
        ranking,
        x="composite_quality_score",
        nbins=20,
        title="Composite Quality Score Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Top Companies
# -----------------------------
st.subheader("🏆 Top 10 Companies")

top10 = (
    ranking
    .sort_values("overall_rank")
    .head(10)
)

fig = px.bar(
    top10,
    x="company_name",
    y="composite_quality_score",
    color="recommendation",
    text="overall_rank",
    title="Top 10 Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    top10[
        [
            "company_name",
            "overall_rank",
            "peer_group_name",
            "composite_quality_score",
            "recommendation"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------------
# Download
# -----------------------------
csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Ranking Data",
    data=csv,
    file_name="ranking_engine.csv",
    mime="text/csv"
)

st.success("✅ Dashboard Loaded Successfully")