import pandas as pd
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("data/nifty100.db")

# Read cashflow table
cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)


def get_sign(value):
    if value > 0:
        return "+"
    elif value < 0:
        return "-"
    else:
        return "0"


def classify_pattern(cfo, cfi, cff):

    signs = (
        get_sign(cfo),
        get_sign(cfi),
        get_sign(cff)
    )

    if signs == ("+", "-", "-"):
        return "Reinvestor"

    elif signs == ("+", "+", "-"):
        return "Liquidating Assets"

    elif signs == ("-", "+", "+"):
        return "Distress Signal"

    elif signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    elif signs == ("+", "+", "+"):
        return "Cash Accumulator"

    elif signs == ("-", "-", "-"):
        return "Pre-Revenue"

    elif signs == ("+", "-", "+"):
        return "Mixed"

    return "Other"


# Create sign columns
cashflow["cfo_sign"] = cashflow[
    "operating_activity"
].apply(get_sign)

cashflow["cfi_sign"] = cashflow[
    "investing_activity"
].apply(get_sign)

cashflow["cff_sign"] = cashflow[
    "financing_activity"
].apply(get_sign)

# Create pattern labels
cashflow["pattern_label"] = cashflow.apply(
    lambda row: classify_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)

# Select required output columns
output = cashflow[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label"
    ]
]

# Save CSV
output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print(
    "capital_allocation.csv created successfully!"
)

conn.close()