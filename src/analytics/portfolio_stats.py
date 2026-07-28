import os
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def latest(df):
    """Return the latest financial ratios for each company."""
    return (
        df.sort_values(["company_id", "year"])
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )


# Connect to database
conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn,
)

conn.close()

ratios = latest(ratios)

# KPIs to summarize
kpis = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "dividend_payout_ratio_pct",
    "composite_quality_score",
]

stats = []

for col in kpis:
    series = ratios[col].dropna()

    stats.append({
        "KPI": col,
        "P10": series.quantile(0.10),
        "P25": series.quantile(0.25),
        "P50": series.quantile(0.50),
        "P75": series.quantile(0.75),
        "P90": series.quantile(0.90),
        "Mean": series.mean(),
        "Std": series.std(),
    })

portfolio_stats = pd.DataFrame(stats)

portfolio_stats = portfolio_stats.round(2)

output_path = os.path.join(
    OUTPUT_DIR,
    "portfolio_stats.csv"
)

portfolio_stats.to_csv(
    output_path,
    index=False,
)

print(f"✓ Portfolio statistics saved to {output_path}")
print(portfolio_stats)