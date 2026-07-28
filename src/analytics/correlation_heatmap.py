import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "data/nifty100.db"
REPORT_DIR = "reports"

os.makedirs(REPORT_DIR, exist_ok=True)


def latest(df):
    return (
        df.sort_values(["company_id", "year"])
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )


conn = sqlite3.connect(DB_PATH)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn,
)

conn.close()

ratios = latest(ratios)

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

corr = ratios[kpis].corr(method="pearson")

plt.figure(figsize=(10, 8))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
)

plt.title("Correlation Matrix")

plt.tight_layout()

output_path = os.path.join(
    REPORT_DIR,
    "correlation_heatmap.png"
)

plt.savefig(
    output_path,
    dpi=300,
)

plt.close()

print(f"✓ Correlation heatmap saved to {output_path}")