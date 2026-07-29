from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm,
    roe,
    roce,
    roa
)


def test_net_profit_margin_normal():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(150, 1000) == 15.0


def test_opm_mismatch():
    result = check_opm(
        operating_profit=200,
        sales=1000,
        opm_percentage=15
    )

    assert "WARNING" in result


def test_roe_normal():
    assert roe(
        net_profit=200,
        equity_capital=100,
        reserves=900
    ) == 20.0


def test_roe_negative_equity():
    assert roe(
        net_profit=100,
        equity_capital=-100,
        reserves=50
    ) is None


def test_roce_normal():
    assert roce(
        operating_profit=300,
        equity_capital=500,
        reserves=500,
        borrowings=500
    ) == 20.0


def test_roa_zero_assets():
    assert roa(
        net_profit=100,
        total_assets=0
    ) is None