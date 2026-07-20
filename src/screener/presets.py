import pandas as pd


def quality_compounder(df):
    """
    Quality Compounder:
    ROE > 15%
    D/E < 1
    FCF > 0
    Revenue CAGR 5yr > 10%
    """

    result = df[
        (df["return_on_equity_pct"] > 15) &
        (df["debt_to_equity"] < 1) &
        (df["free_cash_flow_cr"] > 0) &
        (df["revenue_cagr_5yr"] > 10)
    ]

    result = result.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return result
    


def value_pick(df):
    """
    Value Pick:
    P/E < 20
    P/B < 3
    D/E < 2
    Dividend Yield > 1%
    """

    result = df[
        (df["pe_ratio"] < 20) &
        (df["pb_ratio"] < 3) &
        (df["debt_to_equity"] < 2) &
        (df["dividend_yield_pct"] > 1)
    ]

    return result.sort_values(
        by="pe_ratio",
        ascending=True
    )


def growth_accelerator(df):
    """
    Growth Accelerator:
    PAT CAGR 5yr > 20%
    Revenue CAGR 5yr > 15%
    D/E < 2
    """

    result = df[
        (df["pat_cagr_5yr"] > 20) &
        (df["revenue_cagr_5yr"] > 15) &
        (df["debt_to_equity"] < 2)
    ]

    return result.sort_values(
        by="pat_cagr_5yr",
        ascending=False
    )


def dividend_champion(df):
    """
    Dividend Champion:
    Dividend Yield > 2%
    Dividend Payout < 60%
    Free Cash Flow > 0
    """

    result = df[
        (df["dividend_yield_pct"] > 3.5) &
        (df["dividend_payout"] < 60) &
        (df["free_cash_flow_cr"] > 500)
    ]

    return result.sort_values(
        by="dividend_yield_pct",
        ascending=False
    )

def debt_free_bluechip(df):
    """
    Debt-Free Blue Chip:
    Debt/Equity = 0
    ROE > 12%
    Sales > 5000 Cr
    """

    result = df[
        (df["debt_to_equity"] == 0) &
        (df["return_on_equity_pct"] > 12) &
        (df["sales"] > 5000)
    ]

    return result.sort_values(
        by="return_on_equity_pct",
        ascending=False
    )


def turnaround_watch(df):
    """
    Turnaround Watch (adapted)

    Revenue CAGR 5yr > 10%
    Free Cash Flow > 0
    Debt/Equity < 1.5
    """

    result = df[
        (df["revenue_cagr_5yr"] > 10) &
        (df["free_cash_flow_cr"] > 0) &
        (df["debt_to_equity"] < 1.5)
    ]

    return result.sort_values(
        by="revenue_cagr_5yr",
        ascending=False
    )