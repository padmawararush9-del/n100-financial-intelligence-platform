import pandas as pd


def overall_rank(df):
    """
    Rank companies based on Composite Quality Score.
    """

    result = df.copy()

    result["overall_rank"] = pd.NA

    mask = result["composite_quality_score"].notna()

    result.loc[mask, "overall_rank"] = (
        result.loc[mask]
        .groupby("year")["composite_quality_score"]
        .rank(
            method="dense",
            ascending=False
        )
    )

    return result
def peer_rank(df):
    """
    Rank companies within each peer group for every financial year.
    """

    result = df.copy()

    result["peer_rank"] = pd.NA

    mask = result["composite_quality_score"].notna()

    result.loc[mask, "peer_rank"] = (
        result.loc[mask]
        .groupby(
            ["peer_group_name", "year"]
        )["composite_quality_score"]
        .rank(
            method="dense",
            ascending=False
        )
    )

    return result

def top_companies(df, year=None, n=10):
    """
    Return the top N companies by Composite Quality Score.
    """

    result = df.copy()

    if year is not None:
        result = result[result["year"] == year]

    result = result[result["composite_quality_score"].notna()]

    return (
        result.sort_values(
            "composite_quality_score",
            ascending=False
        ).head(n)
    )
def bottom_companies(df, year=None, n=10):
    """
    Return the bottom N companies by Composite Quality Score.
    """

    result = df.copy()

    if year is not None:
        result = result[result["year"] == year]

    result = result[result["composite_quality_score"].notna()]

    return (
        result.sort_values(
            "composite_quality_score",
            ascending=True
        ).head(n)
    )
def ranking_trend(df, company_id):
    """
    Return yearly ranking trend for a company.
    """

    result = (
        df[df["company_id"] == company_id]
        .sort_values("year")
    )

    return result[
        [
            "company_id",
            "year",
            "composite_quality_score",
            "overall_rank",
            "peer_rank"
        ]
    ]