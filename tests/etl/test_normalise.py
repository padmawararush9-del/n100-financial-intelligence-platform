import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from scripts.normalizer import normalize_year


# ---------- Valid Formats ----------

def test_dec_2012():
    assert normalize_year("Dec 2012") == 2012


def test_mar_2014():
    assert normalize_year("Mar 2014") == 2014


def test_sep_2024():
    assert normalize_year("Sep 2024") == 2024


def test_plain_year():
    assert normalize_year("2020") == 2020


def test_integer_year():
    assert normalize_year(2019) == 2019


def test_year_with_spaces():
    assert normalize_year(" 2021 ") == 2021


def test_apr_1999():
    assert normalize_year("Apr 1999") == 1999


def test_jan_2000():
    assert normalize_year("Jan 2000") == 2000


def test_feb_1985():
    assert normalize_year("Feb 1985") == 1985


def test_oct_2018():
    assert normalize_year("Oct 2018") == 2018


# ---------- Null / Missing ----------

def test_none():
    assert normalize_year(None) is None


def test_nan():
    assert normalize_year(float("nan")) is None


# ---------- Invalid Inputs ----------

def test_empty_string():
    assert normalize_year("") is None


def test_short_string():
    assert normalize_year("123") is None


def test_random_text():
    assert normalize_year("abcd") is None


def test_special_characters():
    assert normalize_year("@@@@") is None

def test_month_without_year():
    assert normalize_year("Dec") is None


def test_year_with_suffix():
    assert normalize_year("2024AD") is None

def test_negative_number():
    assert normalize_year(-2024) is None


def test_float_input():
    assert normalize_year(2024.5) is None