import pandas as pd


def validate_companies(companies):
    failures = []

    duplicates = companies[
        companies["id"].duplicated()
    ]

    for _, row in duplicates.iterrows():
        failures.append([
            "DQ-01",
            "CRITICAL",
            row["id"],
            "Duplicate company ID"
        ])

    return failures


def validate_balance_sheet(balancesheet):
    failures = []

    invalid = balancesheet[
        balancesheet["total_assets"]
        != balancesheet["total_liabilities"]
    ]

    for _, row in invalid.iterrows():
        failures.append([
            "DQ-04",
            "WARNING",
            row["company_id"],
            "Assets not equal to liabilities"
        ])

    return failures


def validate_profit_and_loss(profitandloss):
    failures = []

    invalid_sales = profitandloss[
        profitandloss["sales"] <= 0
    ]

    for _, row in invalid_sales.iterrows():
        failures.append([
            "DQ-06",
            "WARNING",
            row["company_id"],
            "Sales less than or equal to zero"
        ])

    invalid_tax = profitandloss[
        (profitandloss["tax_percentage"] < 0)
        |
        (profitandloss["tax_percentage"] > 60)
    ]

    for _, row in invalid_tax.iterrows():
        failures.append([
            "DQ-11",
            "WARNING",
            row["company_id"],
            "Invalid tax percentage"
        ])

    return failures


def run_validation(
    companies,
    balancesheet,
    profitandloss
):
    failures = []

    failures.extend(
        validate_companies(companies)
    )

    failures.extend(
        validate_balance_sheet(
            balancesheet
        )
    )

    failures.extend(
        validate_profit_and_loss(
            profitandloss
        )
    )

    return pd.DataFrame(
        failures,
        columns=[
            "rule_id",
            "severity",
            "company_id",
            "issue"
        ]
    )