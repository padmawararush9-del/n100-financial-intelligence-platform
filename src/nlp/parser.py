
import os
import re
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
ANALYSIS_FILE = "data/analysis.xlsx"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

PARSED_FILE = os.path.join(OUTPUT_DIR, "analysis_parsed.csv")
FAILURE_FILE = os.path.join(OUTPUT_DIR, "parse_failures.csv")
DIVERGENCE_FILE = os.path.join(OUTPUT_DIR, "divergence_report.csv")

PATTERN = re.compile(r"(\d+)\s*Years?:?\s*(-?[\d.]+)%", re.IGNORECASE)

TARGET_COLUMNS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

RATIO_MAP = {
    "compounded_sales_growth": "revenue_cagr_5yr",
    "compounded_profit_growth": "pat_cagr_5yr",
    "roe": "return_on_equity_pct"
}

def load_analysis():
    return pd.read_excel(ANALYSIS_FILE, skiprows=1)

def parse_analysis(df):
    parsed = []
    failures = []

    for _, row in df.iterrows():
        cid = row["company_id"]

        for metric in TARGET_COLUMNS:
            value = row.get(metric)

            if pd.isna(value):
                failures.append({
                    "company_id": cid,
                    "metric_type": metric,
                    "original_text": None
                })
                continue

            m = PATTERN.search(str(value))

            if m:
                parsed.append({
                    "company_id": cid,
                    "metric_type": metric,
                    "period_years": int(m.group(1)),
                    "value_pct": float(m.group(2))
                })
            else:
                failures.append({
                    "company_id": cid,
                    "metric_type": metric,
                    "original_text": value
                })

    return pd.DataFrame(parsed), pd.DataFrame(failures)

def validate(parsed_df):
    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql("""
        SELECT company_id,
               year,
               revenue_cagr_5yr,
               pat_cagr_5yr,
               return_on_equity_pct
        FROM financial_ratios
    """, conn)

    conn.close()

    latest = (
        ratios.sort_values("year")
        .groupby("company_id")
        .tail(1)
    )

    divergences = []

    for _, row in parsed_df.iterrows():
        metric = row["metric_type"]

        if metric not in RATIO_MAP:
            continue

        ratio_col = RATIO_MAP[metric]

        company = latest[latest.company_id == row.company_id]

        if company.empty:
            continue

        computed = company.iloc[0][ratio_col]

        if pd.isna(computed):
            continue

        diff = abs(row.value_pct - computed)

        if diff > 5:
            divergences.append({
                "company_id": row.company_id,
                "metric_type": metric,
                "parsed_value": row.value_pct,
                "computed_value": computed,
                "difference_pct": round(diff,2)
            })

    return pd.DataFrame(divergences)

def main():
    print("Loading analysis...")
    df = load_analysis()

    print("Parsing...")
    parsed, failures = parse_analysis(df)

    parsed.to_csv(PARSED_FILE, index=False)
    failures.to_csv(FAILURE_FILE, index=False)

    print("Validating...")
    divergence = validate(parsed)
    divergence.to_csv(DIVERGENCE_FILE, index=False)

    print("="*40)
    print("Parsing Complete")
    print(f"Parsed Records     : {len(parsed)}")
    print(f"Failed Records     : {len(failures)}")
    print(f"Divergence Records : {len(divergence)}")
    print("="*40)

if __name__ == "__main__":
    main()
