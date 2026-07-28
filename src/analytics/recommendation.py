import pandas as pd


def generate_recommendation(df):
    """
    Assign investment recommendations based on Composite Quality Score.
    """

    result = df.copy()

    def classify(score):
        if pd.isna(score):
            return pd.NA
        elif score >= 40:
            return "Strong Buy"
        elif score >= 30:
            return "Buy"
        elif score >= 20:
            return "Hold"
        elif score >= 10:
            return "Watchlist"
        else:
            return "Avoid"

    result["recommendation"] = (
        result["composite_quality_score"]
        .apply(classify)
    )

    return result