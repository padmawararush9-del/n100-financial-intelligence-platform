import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Peer Comparison", layout="wide")

st.title("👥 Peer Comparison Dashboard")

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("data/nifty100.db")

ranking = pd.read_sql(
    "SELECT * FROM ranking_engine",
    conn
)

conn.close()

# -----------------------------
# Company Selection
# -----------------------------
companies = sorted(ranking["company_name"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

company = ranking[
    ranking["company_name"] == selected_company
].iloc[0]

peer_group = company["peer_group_name"]

peer_df = ranking[
    ranking["peer_group_name"] == peer_group
].sort_values("peer_rank")

# -----------------------------
# Company Details
# -----------------------------
st.subheader(f"Peer Group : {peer_group}")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Overall Rank",
    int(company["overall_rank"])
)

c2.metric(
    "Peer Rank",
    int(company["peer_rank"])
)

c3.metric(
    "Composite Score",
    round(company["composite_quality_score"],2)
)

st.divider()

# -----------------------------
# Peer Table
# -----------------------------
st.subheader("Peer Companies")

st.dataframe(
    peer_df[
        [
            "company_name",
            "peer_rank",
            "overall_rank",
            "composite_quality_score",
            "recommendation"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Comparison Chart
# -----------------------------
st.subheader("Composite Score Comparison")

fig = px.bar(
    peer_df,
    x="company_name",
    y="composite_quality_score",
    color="recommendation",
    text="peer_rank",
    title="Peer Group Comparison"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Composite Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Best Company
# -----------------------------
best = peer_df.iloc[0]

st.success(
    f"🏆 Highest Ranked Company in this Peer Group: "
    f"{best['company_name']} "
    f"(Score: {best['composite_quality_score']:.2f})"
)