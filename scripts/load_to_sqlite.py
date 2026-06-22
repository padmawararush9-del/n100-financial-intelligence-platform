import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "nifty100.db"
RAW_PATH = BASE_DIR / "data" / "raw"
OUTPUT_PATH = BASE_DIR / "output"

FILE_TABLE_MAP = {
    "companies.xlsx": "companies",
    "balancesheet.xlsx": "balancesheet",
    "profitandloss.xlsx": "profitandloss",
    "cashflow.xlsx": "cashflow",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "sectors.xlsx": "sectors",
    "stock_prices.xlsx": "stock_prices",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons"
}

SPECIAL_FILES = {
    "companies.xlsx",
    "balancesheet.xlsx",
    "profitandloss.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "analysis.xlsx"
}

conn = sqlite3.connect(DB_PATH)

audit_data = []

for file_name, table_name in FILE_TABLE_MAP.items():

    file_path = RAW_PATH / file_name

    print(f"\nLoading {file_name} -> {table_name}")

    if file_name in SPECIAL_FILES:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    audit_data.append(
        {
            "table_name": table_name,
            "rows_loaded": len(df)
        }
    )

    print(f"{len(df)} rows loaded")

audit_df = pd.DataFrame(audit_data)

audit_df.to_csv(
    OUTPUT_PATH / "load_audit.csv",
    index=False
)

print("\nLoad audit generated successfully")

conn.close()