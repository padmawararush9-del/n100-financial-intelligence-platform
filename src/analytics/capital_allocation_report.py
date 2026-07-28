
import os
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

REPORT_XLSX = os.path.join(OUTPUT_DIR, "capital_allocation_report.xlsx")
SUMMARY_CSV = os.path.join(OUTPUT_DIR, "allocation_summary.csv")
GRADES_CSV = os.path.join(OUTPUT_DIR, "allocation_grades.csv")


def latest(df):
    if "year" in df.columns:
        return (
            df.sort_values(["company_id", "year"])
            .groupby("company_id", as_index=False)
            .tail(1)
            .reset_index(drop=True)
        )
    return df


def load():
    conn = sqlite3.connect(DB_PATH)
    companies = pd.read_sql("SELECT id AS company_id, company_name FROM companies", conn)
    sectors = pd.read_sql("SELECT company_id,broad_sector FROM sectors", conn)
    cash = pd.read_sql("SELECT * FROM cashflow", conn)
    bal = pd.read_sql("SELECT * FROM balancesheet", conn)
    ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    conn.close()
    return companies, sectors, cash, bal, ratios, pnl


def shareholder_score(row):
    score = 0
    if row.get("dividend_yield_pct", 0) > 2:
        score += 40
    if row.get("free_cash_flow_cr", 0) > 0:
        score += 30
    if row.get("net_profit", 0) > 0:
        score += 30
    return score


def grade(score):
    if score >= 90: return "A+"
    if score >= 80: return "A"
    if score >= 70: return "B"
    if score >= 60: return "C"
    if score >= 50: return "D"
    return "F"


def build():
    companies, sectors, cash, bal, ratios, pnl = load()

    cash = latest(cash)
    bal_latest = latest(bal)
    ratios = latest(ratios)
    pnl = latest(pnl)

    rows = []

    for company_id, grp in (
        bal.sort_values(["company_id", "year"])
        .groupby("company_id")
    ):

        if len(grp) >= 2:
            prev = grp.iloc[-2]["borrowings"]
        else:
            prev = grp.iloc[-1]["borrowings"]

        rows.append(
            {
                "company_id": company_id,
                "prev_borrowings": prev,
            }
        )

    prev_borrow = pd.DataFrame(rows)

    df = companies.merge(sectors, on="company_id", how="left")
    df = df.merge(cash, on="company_id", how="left")
    df = df.merge(bal_latest[["company_id", "borrowings"]], on="company_id", how="left")
    df = df.merge(prev_borrow, on="company_id", how="left")
    df = df.merge(ratios, on="company_id", how="left")
    df = df.merge(pnl[["company_id", "net_profit"]], on="company_id", how="left")

    df["reinvestment_ratio"] = (
        df["investing_activity"].abs() /
        df["operating_activity"].replace(0, pd.NA)
    )

    def reinvestment_style(v):
        if pd.isna(v):
            return "Unknown"
        if v > 0.80:
            return "Aggressive Growth"
        if v >= 0.40:
            return "Balanced Growth"
        return "Cash Conserving"

    df["reinvestment_style"] = df["reinvestment_ratio"].apply(reinvestment_style)

    df["deleveraging"] = (
        (df["financing_activity"] < 0) &
        (df["borrowings"] < df["prev_borrowings"])
    )

    df["shareholder_score"] = df.apply(shareholder_score, axis=1)

    df["cash_retention_ratio"] = (
        df["operating_activity"] /
        (df["investing_activity"].abs() + 1)
    )

    def allocation_style(r):
        if r["reinvestment_ratio"] > 0.80:
            return "Growth Focused"
        if r["deleveraging"]:
            return "Debt Reduction"
        if r["shareholder_score"] >= 70:
            return "Shareholder Friendly"
        if r["cash_retention_ratio"] > 2:
            return "Cash Hoarder"
        return "Balanced"

    df["allocation_style"] = df.apply(allocation_style, axis=1)

    df["allocation_score"] = (
        (df["shareholder_score"] * 0.4)
        + (df["reinvestment_ratio"].fillna(0).clip(0,1) * 20)
        + (df["deleveraging"].astype(int) * 20)
        + ((df["free_cash_flow_cr"] > 0).astype(int) * 20)
    )

    df["grade"] = df["allocation_score"].apply(grade)

    report = df[[
        "company_name",
        "broad_sector",
        "reinvestment_ratio",
        "reinvestment_style",
        "shareholder_score",
        "cash_retention_ratio",
        "allocation_style",
        "allocation_score",
        "grade"
    ]].rename(columns={"broad_sector":"sector"})

    report.to_excel(REPORT_XLSX, index=False)

    report.groupby("allocation_style").size().reset_index(name="companies").to_csv(
        SUMMARY_CSV, index=False
    )

    report[["company_name", "grade"]].to_csv(GRADES_CSV, index=False)

    print("Generated:")
    print(REPORT_XLSX)
    print(SUMMARY_CSV)
    print(GRADES_CSV)


if __name__ == "__main__":
    build()
