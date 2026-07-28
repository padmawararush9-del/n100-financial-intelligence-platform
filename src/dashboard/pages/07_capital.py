import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Capital Allocation", layout="wide")

st.title("💰 Capital Allocation Dashboard")

# ----------------------------------------------------
# Database
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

# ----------------------------------------------------
# Latest KPIs
# ----------------------------------------------------

latest = df.iloc[-1]

c1, c2 = st.columns(2)

c1.metric(
    "FCF Conversion",
    round(latest["fcf_conversion_rate"],2)
)

c2.metric(
    "CFO Quality",
    round(latest["cfo_quality_score"],2)
)

c3, c4 = st.columns(2)

c3.metric(
    "CapEx Intensity",
    round(latest["capex_intensity"],2)
)

c4.metric(
    "Free Cash Flow",
    round(latest["free_cash_flow"],2)
)

st.divider()

# ----------------------------------------------------
# Free Cash Flow
# ----------------------------------------------------

st.subheader("💵 Free Cash Flow")

fig = px.line(
    df,
    x="year",
    y="free_cash_flow",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# FCF Conversion
# ----------------------------------------------------

st.subheader("📈 FCF Conversion Rate")

fig = px.bar(
    df,
    x="year",
    y="fcf_conversion_rate",
    text_auto=".2f"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# CFO Quality
# ----------------------------------------------------

st.subheader("🏦 CFO Quality Score")

fig = px.line(
    df,
    x="year",
    y="cfo_quality_score",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# CapEx Intensity
# ----------------------------------------------------

st.subheader("🏗 CapEx Intensity")

fig = px.bar(
    df,
    x="year",
    y="capex_intensity",
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

st.subheader("Capital Allocation Metrics")

st.dataframe(
    df[
        [
            "year",
            "free_cash_flow",
            "fcf_conversion_rate",
            "cfo_quality_score",
            "capex_intensity"
        ]
    ],
    use_container_width=True,
    hide_index=True
)