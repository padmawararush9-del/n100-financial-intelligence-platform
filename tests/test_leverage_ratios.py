from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover
)


def test_debt_to_equity_normal():
    assert debt_to_equity(
        100,
        100,
        400
    ) == 0.2


def test_debt_to_equity_debt_free():
    assert debt_to_equity(
        0,
        100,
        500
    ) == 0


def test_high_leverage_flag():
    assert high_leverage_flag(
        6,
        "Technology"
    ) is True


def test_financials_not_flagged():
    assert high_leverage_flag(
        10,
        "Financials"
    ) is False


def test_icr_interest_zero():
    assert interest_coverage_ratio(
        100,
        50,
        0
    ) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) is True


def test_asset_turnover_zero_assets():
    assert asset_turnover(
        1000,
        0
    ) is None