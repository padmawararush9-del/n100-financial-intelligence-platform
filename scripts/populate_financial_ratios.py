import sqlite3
import pandas as pd

conn = sqlite3.connect("data/nifty100.db")

pl = pd.read_sql(
    """
    SELECT *
    FROM profitandloss
    """,
    conn
)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)


def calculate_cagr(start_value, end_value, years=5):

    if start_value <= 0:
        return None

    if end_value <= 0:
        return None

    return round(
        (
            (
                end_value / start_value
            ) ** (1 / years) - 1
        ) * 100,
        2
    )


updates = []

for company in pl["company_id"].unique():

    company_df = (
        pl[
            pl["company_id"] == company
        ]
        .reset_index(drop=True)
    )

    for i in range(len(company_df)):

        revenue_cagr = None
        pat_cagr = None
        eps_cagr = None

        if i >= 5:

            current = company_df.iloc[i]
            previous = company_df.iloc[i - 5]

            revenue_cagr = calculate_cagr(
                previous["sales"],
                current["sales"]
            )

            pat_cagr = calculate_cagr(
                previous["net_profit"],
                current["net_profit"]
            )

            eps_cagr = calculate_cagr(
                previous["eps"],
                current["eps"]
            )

            quality_score = 0

            if revenue_cagr is not None:
                quality_score += revenue_cagr

            if pat_cagr is not None:
                quality_score += pat_cagr

            if eps_cagr is not None:
                quality_score += eps_cagr

            quality_score = round(
                quality_score / 3,
                2
            )

            updates.append(
                (
                    revenue_cagr,
                    pat_cagr,
                    eps_cagr,
                    quality_score,
                    current["company_id"],
                    current["year"]
                )
            )


cursor = conn.cursor()

cursor.executemany(
    """
    UPDATE financial_ratios
    SET
        revenue_cagr_5yr = ?,
        pat_cagr_5yr = ?,
        eps_cagr_5yr = ?,
        composite_quality_score = ?
    WHERE company_id = ?
      AND year = ?
    """,
    updates
)

conn.commit()

count = pd.read_sql(
    """
    SELECT COUNT(*)
    AS rows_loaded
    FROM financial_ratios
    """,
    conn
)

print(count)

print(
    f"Updated {len(updates)} records"
)

conn.close()