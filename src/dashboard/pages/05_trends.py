import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Trend Analysis", layout="wide")

st.title("📈 Financial Trend Analysis")

# ----------------------------------------------------
# Database Connection
# ----------------------------------------------------

conn = sqlite3.connect("data/nifty100.db")

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
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

profit = (
    profit[profit["company_id"] == company_id]
    .sort_values("year")
)

balance = (
    balance[balance["company_id"] == company_id]
    .sort_values("year")
)

cashflow = (
    cashflow[cashflow["company_id"] == company_id]
    .sort_values("year")
)

# ----------------------------------------------------
# Revenue Trend
# ----------------------------------------------------

st.subheader("📊 Revenue Trend")

fig = px.line(
    profit,
    x="year",
    y="sales",
    markers=True,
    title="Revenue Over Years"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Net Profit Trend
# ----------------------------------------------------

st.subheader("💰 Net Profit Trend")

fig = px.line(
    profit,
    x="year",
    y="net_profit",
    markers=True,
    title="Net Profit Over Years"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Operating Cash Flow Trend
# ----------------------------------------------------

st.subheader("💵 Operating Cash Flow")

fig = px.line(
    cashflow,
    x="year",
    y="cash_from_operating_activity",
    markers=True,
    title="Operating Cash Flow"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Assets vs Liabilities
# ----------------------------------------------------

st.subheader("🏦 Assets vs Liabilities")

fig = px.bar(
    balance,
    x="year",
    y=[
        "total_assets",
        "total_liabilities"
    ],
    barmode="group",
    title="Assets vs Liabilities"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Financial Data Tables
# ----------------------------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Profit & Loss")
    st.dataframe(
        profit,
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("Balance Sheet")
    st.dataframe(
        balance,
        use_container_width=True,
        hide_index=True
    )

st.subheader("Cash Flow")

st.dataframe(
    cashflow,
    use_container_width=True,
    hide_index=True
)