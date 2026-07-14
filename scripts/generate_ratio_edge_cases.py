import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

companies = pd.read_sql(
    "SELECT id, roce_percentage, roe_percentage FROM companies",
    conn
)

ratios = pd.read_sql(
    """
    SELECT
        company_id,
        return_on_equity_pct
    FROM financial_ratios
    """,
    conn
)

log_lines = []

for _, company in companies.iterrows():

    company_id = company["id"]

    company_ratios = ratios[
        ratios["company_id"] == company_id
    ]

    if len(company_ratios) == 0:
        continue

    latest_roe = company_ratios[
        "return_on_equity_pct"
    ].dropna()

    if len(latest_roe) == 0:
        continue

    computed_roe = latest_roe.iloc[-1]

    source_roe = company["roe_percentage"]

    difference = abs(
        computed_roe - source_roe
    )

    if difference > 5:

        log_lines.append(
            f"{company_id} | ROE | "
            f"Computed={computed_roe:.2f} | "
            f"Source={source_roe:.2f} | "
            f"Diff={difference:.2f}"
        )

with open(
    "output/ratio_edge_cases.log",
    "w"
) as file:

    for line in log_lines:
        file.write(line + "\n")

print(
    f"{len(log_lines)} anomalies logged"
)

conn.close()