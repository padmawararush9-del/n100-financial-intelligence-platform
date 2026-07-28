import os
import sqlite3
import pandas as pd

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUT_XLSX = os.path.join(OUTPUT_DIR, "cashflow_intelligence.xlsx")
DISTRESS_CSV = os.path.join(OUTPUT_DIR, "distress_alerts.csv")


def latest(df):
    return (
        df.sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )


def load_tables():
    conn = sqlite3.connect(DB_PATH)

    cash = pd.read_sql("SELECT * FROM cashflow", conn)
    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    bal = pd.read_sql("SELECT * FROM balancesheet", conn)
    ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
    comp = pd.read_sql(
        "SELECT id AS company_id, company_name FROM companies", conn
    )
    sectors = pd.read_sql(
        "SELECT company_id, broad_sector FROM sectors", conn
    )

    conn.close()

    return cash, pnl, bal, ratios, comp, sectors


def cfo_quality(cash, pnl):

    merged = cash.merge(
        pnl[["company_id", "year", "net_profit"]],
        on=["company_id", "year"],
        how="left",
    )

    merged["ratio"] = (
        merged["operating_activity"]
        / merged["net_profit"].replace(0, pd.NA)
    )

    avg = (
        merged.groupby("company_id", as_index=False)["ratio"]
        .mean()
        .rename(columns={"ratio": "cfo_quality_score"})
    )

    def label(v):
        if pd.isna(v):
            return "Unknown"
        elif v > 1:
            return "High Quality"
        elif v >= 0.5:
            return "Moderate"
        else:
            return "Accrual Risk"

    avg["cfo_quality_label"] = avg["cfo_quality_score"].apply(label)

    return avg


def build_report():

    cash, pnl, bal, ratios, comp, sectors = load_tables()

    latest_cash = latest(cash)
    latest_pnl = latest(pnl)
    latest_bal = latest(bal)
    latest_ratios = latest(ratios)

    report = comp.merge(sectors, on="company_id", how="left")

    report = report.merge(
        cfo_quality(cash, pnl),
        on="company_id",
        how="left",
    )

    report = report.merge(
        latest_cash[
            [
                "company_id",
                "operating_activity",
                "investing_activity",
                "financing_activity",
            ]
        ],
        on="company_id",
        how="left",
    )

    report = report.merge(
        latest_pnl[
            [
                "company_id",
                "sales",
                "net_profit",
            ]
        ],
        on="company_id",
        how="left",
    )

    report = report.merge(
        latest_bal[
            [
                "company_id",
                "borrowings",
            ]
        ],
        on="company_id",
        how="left",
    )

    report = report.merge(
        latest_ratios[
            [
                "company_id",
                "free_cash_flow_cr",
            ]
        ],
        on="company_id",
        how="left",
    )

    report["capex_intensity_pct"] = (
        report["investing_activity"].abs()
        / report["sales"].replace(0, pd.NA)
    ) * 100

    def capex_label(v):
        if pd.isna(v):
            return "Unknown"
        elif v < 3:
            return "Asset Light"
        elif v <= 8:
            return "Moderate"
        else:
            return "Capital Intensive"

    report["capex_label"] = report["capex_intensity_pct"].apply(capex_label)

    report["fcf_conversion_pct"] = (
        report["free_cash_flow_cr"]
        / report["net_profit"].replace(0, pd.NA)
    ) * 100

    report["fcf_cagr_5yr"] = pd.NA

    report["distress_flag"] = (
        (report["operating_activity"] < 0)
        & (report["financing_activity"] > 0)
    )

           # Previous year's borrowings
    prev_borrow = (
        bal.sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .agg(prev_borrowings=("borrowings", "last"))
    )

    report = report.merge(
        prev_borrow,
        on="company_id",
        how="left",
    )

    report["deleveraging_flag"] = (
        report["borrowings"] < report["prev_borrowings"]
    )
    

    def allocation(row):

        if row["distress_flag"]:
            return "Distress Signal"

        if row["deleveraging_flag"]:
            return "Debt Reduction"

        if row["capex_label"] == "Capital Intensive":
            return "Reinvestor"

        return "Balanced"

    report["capital_allocation_label"] = report.apply(
        allocation,
        axis=1,
    )
    final_cols = [
        "company_id",
        "company_name",
        "broad_sector",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity_pct",
        "capex_label",
        "fcf_cagr_5yr",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label",
    ]

    report[final_cols].rename(
        columns={
            "broad_sector": "sector"
        }
    ).to_excel(
        OUT_XLSX,
        index=False,
    )

    distress = report.loc[
        report["distress_flag"],
        [
            "company_id",
            "company_name",
            "operating_activity",
            "financing_activity",
            "net_profit",
        ],
    ].rename(
        columns={
            "operating_activity": "CFO",
            "financing_activity": "CFF",
            "net_profit": "latest_net_profit",
        }
    )

    distress.to_csv(
        DISTRESS_CSV,
        index=False,
    )

    print("Cash Flow Intelligence Generated")
    print(OUT_XLSX)
    print(DISTRESS_CSV)


if __name__ == "__main__":
    build_report()