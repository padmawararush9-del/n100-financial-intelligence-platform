import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Sector Analysis", layout="wide")

st.title("🏭 Sector Analysis Dashboard")

# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

ranking = pd.read_sql(
    "SELECT * FROM ranking_engine",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

# ----------------------------------------------------
# Merge Data
# ----------------------------------------------------

sector_df = ranking.merge(
    sectors,
    left_on="company_id",
    right_on="company_id",
    how="left"
)

# ----------------------------------------------------
# Sector Summary
# ----------------------------------------------------

summary = (
    sector_df.groupby("sector_name")
    .agg(
        Companies=("company_name", "count"),
        Avg_Score=("composite_quality_score", "mean"),
        Best_Rank=("overall_rank", "min")
    )
    .reset_index()
)

summary = summary.sort_values(
    "Avg_Score",
    ascending=False
)

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Sectors",
    len(summary)
)

c2.metric(
    "Total Companies",
    len(sector_df)
)

c3.metric(
    "Average Score",
    round(
        sector_df["composite_quality_score"].mean(),
        2
    )
)

st.divider()

# ----------------------------------------------------
# Sector Table
# ----------------------------------------------------

st.subheader("Sector Summary")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Average Score by Sector
# ----------------------------------------------------

st.subheader("📊 Average Composite Score")

fig = px.bar(
    summary,
    x="sector_name",
    y="Avg_Score",
    color="Avg_Score",
    text_auto=".2f",
    title="Average Composite Score by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Companies per Sector
# ----------------------------------------------------

st.subheader("🏢 Companies in Each Sector")

fig = px.pie(
    summary,
    names="sector_name",
    values="Companies",
    hole=0.45,
    title="Sector Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Sector Explorer
# ----------------------------------------------------

st.divider()

selected_sector = st.selectbox(
    "Select Sector",
    sorted(summary["sector_name"].dropna().unique())
)

sector_companies = sector_df[
    sector_df["sector_name"] == selected_sector
]

st.subheader(f"Companies in {selected_sector}")

st.dataframe(
    sector_companies[
        [
            "company_name",
            "overall_rank",
            "composite_quality_score",
            "recommendation"
        ]
    ].sort_values("overall_rank"),
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Score Comparison
# ----------------------------------------------------

fig = px.bar(
    sector_companies.sort_values("overall_rank"),
    x="company_name",
    y="composite_quality_score",
    color="recommendation",
    title=f"{selected_sector} Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)