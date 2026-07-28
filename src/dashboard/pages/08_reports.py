import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(
    page_title="Valuation Dashboard",
    layout="wide"
)

st.title("💎 Valuation Dashboard")

# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

# ----------------------------------------------------
# Company Selection
# ----------------------------------------------------

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"].sort_values()
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

df = financial[
    financial["company_id"] == company_id
].sort_values("year")

latest = df.iloc[-1]

# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "P/E Ratio",
    round(latest["price_to_earnings"],2)
)

c2.metric(
    "P/B Ratio",
    round(latest["price_to_book"],2)
)

c3.metric(
    "ROE",
    round(latest["roe"],2)
)

c4.metric(
    "ROCE",
    round(latest["roce"],2)
)

st.divider()

# ----------------------------------------------------
# P/E Trend
# ----------------------------------------------------

st.subheader("📈 Price to Earnings Ratio")

fig = px.line(
    df,
    x="year",
    y="price_to_earnings",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# P/B Trend
# ----------------------------------------------------

st.subheader("🏦 Price to Book Ratio")

fig = px.line(
    df,
    x="year",
    y="price_to_book",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# ROE Trend
# ----------------------------------------------------

st.subheader("💰 Return on Equity")

fig = px.bar(
    df,
    x="year",
    y="roe",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# ROCE Trend
# ----------------------------------------------------

st.subheader("🏭 Return on Capital Employed")

fig = px.bar(
    df,
    x="year",
    y="roce",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Financial Table
# ----------------------------------------------------

st.divider()

st.subheader("Valuation Metrics")

st.dataframe(
    df[
        [
            "year",
            "price_to_earnings",
            "price_to_book",
            "roe",
            "roce"
        ]
    ],
    use_container_width=True,
    hide_index=True
)