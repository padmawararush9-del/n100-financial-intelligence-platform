from src.dq.rules import (
    company_pk_unique,
    annual_pk_unique,
    balance_sheet_balanced,
    opm_cross_check,
    positive_sales,
    valid_year,
    valid_ticker,
    net_cash_check,
    non_negative_fixed_assets,
    valid_tax_rate,
    valid_dividend_payout,
    eps_sign_consistency,
    coverage_check
)

import pandas as pd


# ---------- Company PK ----------

def test_company_pk_unique():
    df = pd.DataFrame({"id": [1, 2, 3]})
    assert company_pk_unique(df)


def test_company_pk_duplicate():
    df = pd.DataFrame({"id": [1, 2, 2]})
    assert not company_pk_unique(df)


# ---------- Annual PK ----------

def test_annual_pk_unique():
    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2023, 2024]
    })
    assert annual_pk_unique(df)


def test_annual_pk_duplicate():
    df = pd.DataFrame({
        "company_id": [1, 1],
        "year": [2023, 2023]
    })
    assert not annual_pk_unique(df)


# ---------- Balance Sheet ----------

def test_balance_sheet_balanced():
    assert balance_sheet_balanced(1000, 1000)


def test_balance_sheet_unbalanced():
    assert not balance_sheet_balanced(1000, 900)


# ---------- OPM ----------

def test_opm_cross_check_ok():
    assert opm_cross_check(20, 200, 1000)


def test_opm_cross_check_fail():
    assert not opm_cross_check(10, 200, 1000)


# ---------- Sales ----------

def test_positive_sales():
    assert positive_sales(100)


def test_negative_sales():
    assert not positive_sales(-10)


# ---------- Year ----------

def test_valid_year():
    assert valid_year(2024)


def test_invalid_year():
    assert not valid_year(1800)


# ---------- Ticker ----------

def test_valid_ticker():
    assert valid_ticker("INFY")


def test_invalid_ticker():
    assert not valid_ticker("A")


# ---------- Net Cash ----------

def test_net_cash_check():
    assert net_cash_check(100, 50, 30, 20)


def test_net_cash_check_fail():
    assert not net_cash_check(50, 50, 30, 20)


# ---------- Fixed Assets ----------

def test_non_negative_fixed_assets():
    assert non_negative_fixed_assets(10)


def test_negative_fixed_assets():
    assert not non_negative_fixed_assets(-1)


# ---------- Tax ----------

def test_valid_tax_rate():
    assert valid_tax_rate(30)


def test_invalid_tax_rate():
    assert not valid_tax_rate(80)


# ---------- Dividend ----------

def test_valid_dividend():
    assert valid_dividend_payout(50)


def test_invalid_dividend():
    assert not valid_dividend_payout(250)


# ---------- EPS ----------

def test_eps_consistency():
    assert eps_sign_consistency(5, 100)


def test_eps_inconsistency():
    assert not eps_sign_consistency(-5, 100)


# ---------- Coverage ----------

def test_coverage_check():
    assert coverage_check(5)


def test_coverage_check_fail():
    assert not coverage_check(3)
    