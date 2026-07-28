import os
import sqlite3
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "data/nifty100.db"
OUTPUT_DIR = "output"
REPORT_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

styles = getSampleStyleSheet()

OUT_XLSX = os.path.join(OUTPUT_DIR, "portfolio_summary.xlsx")
OUT_STATS = os.path.join(OUTPUT_DIR, "portfolio_statistics.csv")
OUT_PDF = os.path.join(REPORT_DIR, "Portfolio_Summary.pdf")


def latest(df):
    if "year" not in df.columns:
        return df

    return (
        df.sort_values(["company_id", "year"])
          .groupby("company_id", as_index=False)
          .tail(1)
          .reset_index(drop=True)
    )


def load_data():
    conn = sqlite3.connect(DB_PATH)

    ranking = pd.read_sql("""
SELECT
    company_id,
    overall_rank,
    recommendation,
    composite_quality_score
FROM ranking_engine
""", conn)
    companies = pd.read_sql(
        "SELECT id AS company_id, company_name FROM companies",
        conn,
    )
    sectors = pd.read_sql(
        "SELECT company_id, broad_sector FROM sectors",
        conn,
    )
    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    conn.close()

    cash = (
        pd.read_excel("output/cashflow_intelligence.xlsx")
        if os.path.exists("output/cashflow_intelligence.xlsx")
        else pd.DataFrame()
    )

    allocation = (
        pd.read_excel("output/capital_allocation_report.xlsx")
        if os.path.exists("output/capital_allocation_report.xlsx")
        else pd.DataFrame()
    )

    pros = (
        pd.read_csv("output/pros_cons_generated.csv")
        if os.path.exists("output/pros_cons_generated.csv")
        else pd.DataFrame(columns=["type", "text"])
    )

    return (
        ranking,
        companies,
        sectors,
        ratios,
        cash,
        allocation,
        pros,
    )


def build():

    (
        ranking,
        companies,
        sectors,
        ratios,
        cash,
        allocation,
        pros,
    ) = load_data()

    ratios = latest(ratios)

    ratio_cols = [
        "company_id",
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "free_cash_flow_cr",
    ]

    ratio_cols = [c for c in ratio_cols if c in ratios.columns]

    report = companies.merge(
        ranking,
        on="company_id",
        how="left",
    )

    report = report.merge(
        sectors,
        on="company_id",
        how="left",
    )

    report = report.merge(
        ratios[ratio_cols],
        on="company_id",
        how="left",
    )

    report.to_excel(
        OUT_XLSX,
        index=False,
    )

    stats = {
        "Total Companies": len(report),
        "Average Quality Score": report["composite_quality_score"].mean()
        if "composite_quality_score" in report.columns
        else None,
        "Average ROE": report["return_on_equity_pct"].mean()
        if "return_on_equity_pct" in report.columns
        else None,
        "Average Revenue CAGR": report["revenue_cagr_5yr"].mean()
        if "revenue_cagr_5yr" in report.columns
        else None,
        "Average PAT CAGR": report["pat_cagr_5yr"].mean()
        if "pat_cagr_5yr" in report.columns
        else None,
        "Average Free Cash Flow": report["free_cash_flow_cr"].mean()
        if "free_cash_flow_cr" in report.columns
        else None,
    }

    pd.DataFrame(
        stats.items(),
        columns=["Metric", "Value"],
    ).to_csv(
        OUT_STATS,
        index=False,
    )

    doc = SimpleDocTemplate(OUT_PDF)
    story = []

    story.append(
        Paragraph(
            "<b>Nifty100 Portfolio Summary Report</b>",
            styles["Title"],
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Overall Statistics</b>",
            styles["Heading2"],
        )
    )

    for k, v in stats.items():
        story.append(
            Paragraph(
                f"{k}: {v}",
                styles["BodyText"],
            )
        )

    story.append(Spacer(1, 12))

    if "recommendation" in report.columns:

        story.append(
            Paragraph(
                "<b>Recommendation Summary</b>",
                styles["Heading2"],
            )
        )

        for rec, cnt in report["recommendation"].value_counts().items():
            story.append(
                Paragraph(
                    f"{rec}: {cnt}",
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            "<b>Top 10 Companies</b>",
            styles["Heading2"],
        )
    )

    if "overall_rank" in report.columns:

        top = report.sort_values("overall_rank").head(10)

        for _, row in top.iterrows():

            story.append(
                Paragraph(
                    f"{int(row['overall_rank'])}. "
                    f"{row['company_name']} "
                    f"({row.get('recommendation','N/A')})",
                    styles["BodyText"],
                )
            )

    story.append(Spacer(1, 12))

    if "broad_sector" in report.columns:

        story.append(
            Paragraph(
                "<b>Sector Summary</b>",
                styles["Heading2"],
            )
        )

        for sec, cnt in report["broad_sector"].value_counts(dropna=False).items():
            story.append(
                Paragraph(
                    f"{sec}: {cnt}",
                    styles["BodyText"],
                )
            )

    if not cash.empty and "cfo_quality_label" in cash.columns:

        story.append(Spacer(1, 12))
        story.append(
            Paragraph(
                "<b>Cash Flow Quality</b>",
                styles["Heading2"],
            )
        )

        for lbl, cnt in cash["cfo_quality_label"].value_counts().items():
            story.append(
                Paragraph(
                    f"{lbl}: {cnt}",
                    styles["BodyText"],
                )
            )

    if not allocation.empty and "allocation_style" in allocation.columns:

        story.append(Spacer(1, 12))
        story.append(
            Paragraph(
                "<b>Capital Allocation Styles</b>",
                styles["Heading2"],
            )
        )

        for lbl, cnt in allocation["allocation_style"].value_counts().items():
            story.append(
                Paragraph(
                    f"{lbl}: {cnt}",
                    styles["BodyText"],
                )
            )

    if not pros.empty:

        story.append(Spacer(1, 12))
        story.append(
            Paragraph(
                "<b>Most Common Pros</b>",
                styles["Heading2"],
            )
        )

        pro = pros[pros["type"] == "pro"]["text"].value_counts().head(5)

        for text, count in pro.items():
            story.append(
                Paragraph(
                    f"{text} ({count})",
                    styles["BodyText"],
                )
            )

        story.append(Spacer(1, 12))
        story.append(
            Paragraph(
                "<b>Most Common Cons</b>",
                styles["Heading2"],
            )
        )

        con = pros[pros["type"] == "con"]["text"].value_counts().head(5)

        for text, count in con.items():
            story.append(
                Paragraph(
                    f"{text} ({count})",
                    styles["BodyText"],
                )
            )

    doc.build(story)

    print("Generated:")
    print(OUT_XLSX)
    print(OUT_STATS)
    print(OUT_PDF)


if __name__ == "__main__":
    build()