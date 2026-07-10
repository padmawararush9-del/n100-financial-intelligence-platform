def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    FCF = CFO + CFI
    """

    return (
        operating_activity
        + investing_activity
    )


def cfo_quality_score(
    cfo,
    pat
):
    """
    CFO / PAT
    """

    if pat == 0:
        return None

    score = cfo / pat

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales
):
    """
    abs(CFI) / Sales * 100
    """

    if sales == 0:
        return None

    intensity = (
        abs(investing_activity)
        / sales
    ) * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(intensity, 2), label


def fcf_conversion_rate(
    fcf,
    operating_profit
):
    """
    FCF / Operating Profit * 100
    """

    if operating_profit == 0:
        return None

    return round(
        (fcf / operating_profit) * 100,
        2
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=None
):
    """
    8-pattern classifier
    """

    signs = (
        "+" if cfo > 0 else "-",
        "+" if cfi > 0 else "-",
        "+" if cff > 0 else "-"
    )

    if signs == ("+", "-", "-"):

        if (
            cfo_pat_ratio is not None
            and cfo_pat_ratio > 1
        ):
            return "Shareholder Returns"

        return "Reinvestor"

    if signs == ("+", "+", "-"):
        return "Liquidating Assets"

    if signs == ("-", "+", "+"):
        return "Distress Signal"

    if signs == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if signs == ("+", "+", "+"):
        return "Cash Accumulator"

    if signs == ("-", "-", "-"):
        return "Pre-Revenue"

    if signs == ("+", "-", "+"):
        return "Mixed"

    return "Other"