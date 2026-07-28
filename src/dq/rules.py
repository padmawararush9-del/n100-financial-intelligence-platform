def company_pk_unique(df):
    return df["id"].is_unique


def annual_pk_unique(df):
    return not df.duplicated(["company_id", "year"]).any()


def balance_sheet_balanced(total_assets, total_liabilities):
    return total_assets == total_liabilities


def opm_cross_check(opm_percentage, operating_profit, sales, tolerance=1):
    if sales == 0:
        return False

    calculated = (operating_profit / sales) * 100
    return abs(calculated - opm_percentage) <= tolerance


def positive_sales(sales):
    return sales > 0


def valid_year(year):
    return isinstance(year, int) and 1900 <= year <= 2100


def valid_ticker(ticker):
    if not isinstance(ticker, str):
        return False

    ticker = ticker.strip().upper()
    return 3 <= len(ticker) <= 12


def net_cash_check(net_cash_flow, cfo, cfi, cff, tolerance=10):
    return abs(net_cash_flow - (cfo + cfi + cff)) <= tolerance


def non_negative_fixed_assets(fixed_assets):
    return fixed_assets >= 0


def valid_tax_rate(tax):
    return 0 <= tax <= 60


def valid_dividend_payout(payout):
    return payout <= 200


def eps_sign_consistency(eps, net_profit):
    if net_profit > 0:
        return eps > 0
    return True


def coverage_check(years):
    return years >= 5