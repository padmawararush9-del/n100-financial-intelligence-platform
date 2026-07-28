import os
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"
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

clusters = pd.read_csv(
    os.path.join(OUTPUT_DIR, "cluster_labels.csv")
)

df = ratios.merge(
    clusters,
    on="company_id",
    how="inner",
)

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]

mean_profile = (
    df.groupby("cluster_name")[features]
    .mean()
    .round(2)
)

median_profile = (
    df.groupby("cluster_name")[features]
    .median()
    .round(2)
)

with pd.ExcelWriter(
    os.path.join(REPORT_DIR, "cluster_profile.xlsx")
) as writer:

    mean_profile.to_excel(
        writer,
        sheet_name="Mean"
    )

    median_profile.to_excel(
        writer,
        sheet_name="Median"
    )

print("✓ Cluster profile generated.")