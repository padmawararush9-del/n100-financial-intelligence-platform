from src.analytics.cashflow import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern
)


def test_fcf():
    assert free_cash_flow(
        100,
        -40
    ) == 60


def test_cfo_quality_high():
    assert (
        cfo_quality_score(
            120,
            100
        )
        == "High Quality"
    )


def test_cfo_quality_moderate():
    assert (
        cfo_quality_score(
            75,
            100
        )
        == "Moderate"
    )


def test_cfo_quality_accrual():
    assert (
        cfo_quality_score(
            20,
            100
        )
        == "Accrual Risk"
    )


def test_pat_zero():
    assert (
        cfo_quality_score(
            100,
            0
        )
        is None
    )


def test_capex_intensity():
    _, label = capex_intensity(
        -200,
        1000
    )

    assert (
        label
        == "Capital Intensive"
    )


def test_fcf_conversion():
    assert (
        fcf_conversion_rate(
            100,
            200
        )
        == 50.0
    )


def test_reinvestor_pattern():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -30,
            0.8
        )
        == "Reinvestor"
    )


def test_shareholder_returns():
    assert (
        capital_allocation_pattern(
            100,
            -50,
            -30,
            1.2
        )
        == "Shareholder Returns"
    )


def test_distress_signal():
    assert (
        capital_allocation_pattern(
            -100,
            50,
            50
        )
        == "Distress Signal"
    )