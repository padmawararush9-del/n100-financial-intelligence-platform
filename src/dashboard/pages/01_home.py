import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("🏠 Home Dashboard")

conn = sqlite3.connect("data/nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
ranking = pd.read_sql("SELECT * FROM ranking_engine", conn)

conn.close()

total_companies = companies["company_name"].nunique()
avg_score = ranking["composite_quality_score"].mean()
strong_buy = (ranking["recommendation"] == "Strong Buy").sum()
buy = (ranking["recommendation"] == "Buy").sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Companies", total_companies)
c2.metric("Average Score", f"{avg_score:.2f}")
c3.metric("Strong Buy", strong_buy)
c4.metric("Buy", buy)

st.divider()

st.subheader("🏆 Top 10 Ranked Companies")

top10 = (
    ranking
    .sort_values("overall_rank")
    .head(10)
)

st.dataframe(
    top10[
        [
            "company_name",
            "overall_rank",
            "composite_quality_score",
            "recommendation"
        ]
    ],
    use_container_width=True
)
st.divider()

st.subheader("📊 Recommendation Distribution")

recommendation_count = (
    ranking["recommendation"]
    .value_counts()
    .reset_index()
)

recommendation_count.columns = ["Recommendation", "Count"]

fig = px.pie(
    recommendation_count,
    names="Recommendation",
    values="Count",
    hole=0.45,
    title="Recommendation Breakdown"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Composite Quality Score Distribution")

fig = px.histogram(
    ranking,
    x="composite_quality_score",
    nbins=20,
    title="Composite Quality Score"
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("🏆 Top 10 Companies")

fig = px.bar(
    top10,
    x="company_name",
    y="composite_quality_score",
    color="recommendation",
    title="Top Companies by Composite Score"
)

st.plotly_chart(fig, use_container_width=True)