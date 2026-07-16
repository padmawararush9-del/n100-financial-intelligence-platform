import pandas as pd
import yaml


def load_config(config_path):

    with open(config_path, "r") as file:
        return yaml.safe_load(file)


def apply_filters(df, config):

    filtered = df.copy()

    # ROE
    if "roe_min" in config:
        filtered = filtered[
            filtered["return_on_equity_pct"]
            >= config["roe_min"]
        ]

    # Debt to Equity
    if "de_max" in config:

        non_financials = filtered[
            filtered["broad_sector"] != "Financials"
        ]

        financials = filtered[
            filtered["broad_sector"] == "Financials"
        ]

        non_financials = non_financials[
            non_financials["debt_to_equity"]
            <= config["de_max"]
        ]

        filtered = pd.concat(
            [non_financials, financials]
        )

    # Free Cash Flow
    if "fcf_min" in config:
        filtered = filtered[
            filtered["free_cash_flow_cr"]
            >= config["fcf_min"]
        ]

    # Revenue CAGR
    if "revenue_cagr_5yr_min" in config:
        filtered = filtered[
            filtered["revenue_cagr_5yr"]
            >= config["revenue_cagr_5yr_min"]
        ]

    # PAT CAGR
    if "pat_cagr_5yr_min" in config:
        filtered = filtered[
            filtered["pat_cagr_5yr"]
            >= config["pat_cagr_5yr_min"]
        ]

    # OPM
    if "opm_min" in config:
        filtered = filtered[
            filtered["operating_profit_margin_pct"]
            >= config["opm_min"]
        ]

    # P/E
    if "pe_max" in config:
        filtered = filtered[
            filtered["pe_ratio"]
            <= config["pe_max"]
        ]

    # P/B
    if "pb_max" in config:
        filtered = filtered[
            filtered["pb_ratio"]
            <= config["pb_max"]
        ]

    # Dividend Yield
    if "dividend_yield_min" in config:
        filtered = filtered[
            filtered["dividend_yield_pct"]
            >= config["dividend_yield_min"]
        ]

    # Interest Coverage
    if "icr_min" in config:

        filtered = filtered[
            (
                filtered["interest_coverage"]
                >= config["icr_min"]
            )
            |
            (
                filtered["icr_label"]
                == "Debt Free"
            )
        ]

    # Market Cap
    if "market_cap_min" in config:
        filtered = filtered[
            filtered["market_cap_crore"]
            >= config["market_cap_min"]
        ]

    # Asset Turnover
    if "asset_turnover_min" in config:
        filtered = filtered[
            filtered["asset_turnover"]
            >= config["asset_turnover_min"]
        ]

    # Composite Score Sorting
    filtered = filtered.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    def apply_filters(df):

    filtered = df[
        (df["return_on_equity_pct"] > 15)
        &
        (
            (df["debt_to_equity"] < 1)
            |
            (df["broad_sector"] == "Financials")
        )
    ]

    filtered = filtered.sort_values(
        by="composite_quality_score",
        ascending=False
    )

    return filtered