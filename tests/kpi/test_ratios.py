import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm,
    roe,
    roce,
    roa,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover
)


# ---------- Net Profit Margin ----------

def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.00


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


# ---------- Operating Profit Margin ----------

def test_operating_profit_margin():
    assert operating_profit_margin(250, 1000) == 25.00


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(100, 0) is None


# ---------- Check OPM ----------

def test_check_opm_ok():
    assert check_opm(250, 1000, 25.0) == "OK"


def test_check_opm_warning():
    assert "WARNING" in check_opm(250, 1000, 20.0)


def test_check_opm_none():
    assert check_opm(100, 0, 10) is None


# ---------- ROE ----------

def test_roe():
    assert roe(200, 500, 500) == 20.00


def test_roe_zero_equity():
    assert roe(100, 0, 0) is None


# ---------- ROCE ----------

def test_roce():
    assert roce(300, 500, 300, 200) == 30.00


def test_roce_zero_capital():
    assert roce(100, 0, 0, 0) is None


# ---------- ROA ----------

def test_roa():
    assert roa(150, 1000) == 15.00


def test_roa_zero_assets():
    assert roa(100, 0) is None


# ---------- Debt to Equity ----------

def test_debt_to_equity():
    assert debt_to_equity(500, 500, 500) == 0.50


def test_debt_to_equity_zero_debt():
    assert debt_to_equity(0, 500, 500) == 0


def test_debt_to_equity_zero_equity():
    assert debt_to_equity(100, 0, 0) is None


# ---------- High Leverage ----------

def test_high_leverage_true():
    assert high_leverage_flag(6, "IT") is True


def test_high_leverage_financials():
    assert high_leverage_flag(6, "Financials") is False


# ---------- Interest Coverage ----------

def test_interest_coverage_ratio():
    assert interest_coverage_ratio(100, 20, 40) == 3.00


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(100, 20, 0) is None


# ---------- ICR ----------

def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_label_none():
    assert icr_label(50) is None


def test_icr_warning_true():
    assert icr_warning(1.2) is True


def test_icr_warning_false():
    assert icr_warning(3.5) is False


# ---------- Net Debt ----------

def test_net_debt():
    assert net_debt(500, 150) == 350


# ---------- Asset Turnover ----------

def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.00


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None