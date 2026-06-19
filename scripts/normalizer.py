"""
Data normalization functions for
N100 Financial Intelligence Platform.
"""

import pandas as pd


def normalize_year(year):
    """
    Convert year values to YYYY format.

    Examples:
    Dec 2012 -> 2012
    Mar 2014 -> 2014
    """

    if pd.isna(year):
        return None

    year = str(year)

    if len(year) >= 4:
        return int(year[-4:])

    return None


def normalize_ticker(ticker):
    """
    Standardize company ticker.
    """

    if pd.isna(ticker):
        return None

    return (
        str(ticker)
        .upper()
        .replace(".NS", "")
        .replace(".NSE", "")
        .strip()
    )


def normalize_dataframe(df):
    """
    Apply normalization to common columns.
    """

    if "year" in df.columns:
        df["year"] = df["year"].apply(normalize_year)

    if "company_id" in df.columns:
        df["company_id"] = df["company_id"].apply(normalize_ticker)

    return df


if __name__ == "__main__":

    sample = pd.DataFrame(
        {
            "company_id": ["abb", "tcs.ns", " axisbank "],
            "year": ["Dec 2012", "Mar 2014", "Sep 2024"],
        }
    )

    print("Before:")
    print(sample)

    sample = normalize_dataframe(sample)

    print("\nAfter:")
    print(sample)