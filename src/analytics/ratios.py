def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = Net Profit / Sales * 100
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    OPM = Operating Profit / Sales * 100
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
        (operating_profit /
         capital_employed) * 100,
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