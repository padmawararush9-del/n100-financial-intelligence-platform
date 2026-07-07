def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = Net Profit / Sales * 100
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = Operating Profit / Sales * 100
    """

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm(operating_profit, sales, opm_percentage):
    """
    Compare calculated OPM with stored OPM
    """

    calculated = operating_profit_margin(
        operating_profit,
        sales
    )

    if calculated is None:
        return None

    difference = abs(
        calculated - opm_percentage
    )

    if difference > 1:
        return (
            f"WARNING: OPM mismatch "
            f"({difference:.2f}%)"
        )

    return "OK"


def roe(net_profit, equity_capital, reserves):
    """
    Return on Equity
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(
        (net_profit / equity) * 100,
        2
    )


def roce(
    operating_profit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed
    """

    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (operating_profit / capital_employed) * 100,
        2
    )


def roa(net_profit, total_assets):
    """
    Return on Assets
    """

    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )


# ==========================
# DAY 09 FUNCTIONS
# ==========================

def debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0

    equity = (
        equity_capital
        + reserves
    )

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )


def high_leverage_flag(
    debt_equity,
    sector
):
    """
    High leverage warning
    """

    if (
        debt_equity is not None
        and debt_equity > 5
        and sector != "Financials"
    ):
        return True

    return False


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return round(
        (
            operating_profit
            + other_income
        ) / interest,
        2
    )


def icr_label(
    interest
):
    """
    Debt free label
    """

    if interest == 0:
        return "Debt Free"

    return None


def icr_warning(
    icr
):
    """
    Interest coverage warning
    """

    if (
        icr is not None
        and icr < 1.5
    ):
        return True

    return False


def net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return (
        borrowings
        - investments
    )


def asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )