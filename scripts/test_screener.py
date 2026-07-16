import sqlite3
import pandas as pd

from src.screener.engine import (
    load_config,
    apply_filters
)

conn = sqlite3.connect(
    "data/nifty100.db"
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

config = load_config(
    "config/screener_config.yaml"
)

result = apply_filters(
    ratios,
    config
)

print(result.head())
print(len(result))