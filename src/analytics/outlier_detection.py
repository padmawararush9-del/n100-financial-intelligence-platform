import os
import sqlite3
import pandas as pd
from scipy.stats import zscore

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def latest(df):
    return (
        df.sort_values(["company_id", "year"])
        .groupby("company_id")
        .tail(1)
        .reset_index(drop=True)
    )


conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql(
    """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    """,
    conn,
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn,
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn,
)

conn.close()

ratios = latest(ratios)

df = companies.merge(
    sectors,
    on="company_id",
)

df = df.merge(
    ratios,
    on="company_id",
)

metrics = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]

outliers = []

for sector, group in df.groupby("broad_sector"):

    temp = group.copy()

    for metric in metrics:

        temp[f"{metric}_z"] = zscore(
            temp[metric],
            nan_policy="omit",
        )

    for _, row in temp.iterrows():

        flags = []

        for metric in metrics:

            z = row[f"{metric}_z"]

            if pd.notna(z) and abs(z) > 3:
                flags.append(metric)

        if flags:

            outliers.append(
                {
                    "company_id": row["company_id"],
                    "company_name": row["company_name"],
                    "broad_sector": sector,
                    "flagged_metrics": ", ".join(flags),
                }
            )

outliers = pd.DataFrame(outliers)

outliers.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "outlier_report.csv",
    ),
    index=False,
)

print(f"Outliers Found: {len(outliers)}")
print("✓ outlier_report.csv generated.")