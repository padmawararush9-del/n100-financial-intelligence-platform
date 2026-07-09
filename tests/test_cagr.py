from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr,
    check_data_availability
)


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert flag is None
    assert value is not None


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        50,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -50,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        100,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_data():

    value, flag = check_data_availability(
        3,
        5
    )

    assert value is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():

    value, flag = revenue_cagr(
        100,
        150,
        3
    )

    assert flag is None


def test_pat_cagr():

    value, flag = pat_cagr(
        100,
        200,
        5
    )

    assert flag is None


def test_eps_cagr():

    value, flag = eps_cagr(
        10,
        20,
        5
    )

    assert flag is None


def test_valid_data_availability():

    value, flag = check_data_availability(
        10,
        5
    )

    assert value is True
    assert flag is None