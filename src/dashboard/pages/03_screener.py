import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("🔍 Stock Screener")

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
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

recommendation = st.sidebar.multiselect(
    "Recommendation",
    sorted(ranking["recommendation"].dropna().unique()),
    default=sorted(ranking["recommendation"].dropna().unique())
)

peer_group = st.sidebar.multiselect(
    "Peer Group",
    sorted(ranking["peer_group_name"].dropna().unique()),
    default=sorted(ranking["peer_group_name"].dropna().unique())
)

min_score = st.sidebar.slider(
    "Minimum Composite Score",
    min_value=0.0,
    max_value=float(ranking["composite_quality_score"].max()),
    value=0.0
)

company_search = st.text_input(
    "🔍 Search Company"
)

# -----------------------------
# Apply Filters
# -----------------------------
filtered = ranking.copy()

filtered = filtered[
    filtered["recommendation"].isin(recommendation)
]

filtered = filtered[
    filtered["peer_group_name"].isin(peer_group)
]

filtered = filtered[
    filtered["composite_quality_score"] >= min_score
]

if company_search:
    filtered = filtered[
        filtered["company_name"].str.contains(
            company_search,
            case=False,
            na=False
        )
    ]

# -----------------------------
# KPI Cards
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Companies Found", len(filtered))

if len(filtered) > 0:
    c2.metric(
        "Average Score",
        round(filtered["composite_quality_score"].mean(), 2)
    )

    c3.metric(
        "Best Rank",
        int(filtered["overall_rank"].min())
    )
else:
    c2.metric("Average Score", "0")
    c3.metric("Best Rank", "-")

st.divider()

# -----------------------------
# Results Table
# -----------------------------
st.subheader("Filtered Companies")

st.dataframe(
    filtered[
        [
            "company_name",
            "overall_rank",
            "peer_rank",
            "peer_group_name",
            "composite_quality_score",
            "recommendation"
        ]
    ].sort_values("overall_rank"),
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Results as CSV",
    data=csv,
    file_name="screened_stocks.csv",
    mime="text/csv"
)