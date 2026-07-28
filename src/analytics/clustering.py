import os
import sqlite3
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

DB_PATH = "data/nifty100.db"
REPORT_DIR = "reports"
OUTPUT_DIR = "output"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def latest(df):
    """Return the latest record for each company."""
    if "year" not in df.columns:
        return df

    return (
        df.sort_values(["company_id", "year"])
        .groupby("company_id", as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )


def load_data():
    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        """,
        conn,
    )

    sectors = pd.read_sql(
        """
        SELECT
            company_id,
            broad_sector
        FROM sectors
        """,
        conn,
    )

    ratios = pd.read_sql(


        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )

    conn.close()

    ratios = latest(ratios)

    return companies, sectors, ratios


def prepare_dataframe():

    companies, sectors, ratios = load_data()

    features = [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct",
    ]

    df = companies.merge(
        sectors,
        on="company_id",
        how="left",
    )

    df = df.merge(
        ratios[features],
        on="company_id",
        how="left",
    )

    print("\nData Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isna().sum())

    return df

def run_clustering(df):

    feature_cols = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr",
        "operating_profit_margin_pct",
    ]

    # Sector median imputation
    for col in feature_cols:
        df[col] = df[col].fillna(
            df.groupby("broad_sector")[col].transform("median")
        )

    # Remaining missing values (if an entire sector was missing)
    imputer = SimpleImputer(strategy="median")
    df[feature_cols] = imputer.fit_transform(df[feature_cols])

    # Clip extreme outliers (1st and 99th percentile)
    for col in feature_cols:
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df[col] = df[col].clip(lower=lower, upper=upper)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[feature_cols])

    # KMeans
    kmeans = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10,
    )

    labels = kmeans.fit_predict(X_scaled)

    # Distance to assigned centroid
    distances = kmeans.transform(X_scaled)
    min_distance = np.min(distances, axis=1)

    df["cluster_id"] = labels
    df["distance_from_centroid"] = min_distance

    print("\nCluster Counts")
    print(df["cluster_id"].value_counts().sort_index())

    print("\nFeature Summary")
    print(df[feature_cols].describe())

    print("\nCompanies per Cluster")
    print(df.groupby("cluster_id")["company_name"].apply(list))

    return df, X_scaled


def generate_elbow_plot(X_scaled):

    inertias = []

    ks = range(2, 11)

    for k in ks:
        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10,
        )

        model.fit(X_scaled)

        inertias.append(model.inertia_)

    plt.figure(figsize=(8,5))

    plt.plot(ks, inertias, marker="o")

    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")

    plt.grid(True)

    plt.savefig(
        os.path.join(REPORT_DIR, "elbow_plot.png"),
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("\n✓ Elbow plot saved.")

def save_cluster_labels(df):

    cluster_names = {
        0: "Cluster 0",
        1: "Cluster 1",
        2: "Cluster 2",
        3: "Cluster 3",
        4: "Cluster 4",
    }

    output = df[
        [
            "company_id",
            "cluster_id",
            "distance_from_centroid",
        ]
    ].copy()

    output["cluster_name"] = output["cluster_id"].map(cluster_names)

    output = output[
        [
            "company_id",
            "cluster_id",
            "cluster_name",
            "distance_from_centroid",
        ]
    ]

    output.to_csv(
        os.path.join(OUTPUT_DIR, "cluster_labels.csv"),
        index=False,
    )

    print("✓ cluster_labels.csv saved.")



if __name__ == "__main__":

    df = prepare_dataframe()

    df, X_scaled = run_clustering(df)

    generate_elbow_plot(X_scaled)

    save_cluster_labels(df)