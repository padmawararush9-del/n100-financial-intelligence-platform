import streamlit as st
import pandas as pd
import sqlite3

st.title("🏢 Company Profile")

conn = sqlite3.connect("data/nifty100.db")

ranking = pd.read_sql("SELECT * FROM ranking_engine", conn)

companies = ranking["company_name"].sort_values().unique()

selected_company = st.selectbox(
    "Select a Company",
    companies
)

company = ranking[
    ranking["company_name"] == selected_company
].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Overall Rank",
    int(company["overall_rank"])
)

col2.metric(
    "Composite Score",
    round(company["composite_quality_score"],2)
)

col3.metric(
    "Recommendation",
    company["recommendation"]
)

st.divider()

st.subheader("Company Information")

st.dataframe(
    company.to_frame().T,
    use_container_width=True
)

conn.close()