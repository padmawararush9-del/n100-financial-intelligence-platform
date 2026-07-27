def compare_with_benchmark(df):
    """
    Compare each company's quality score with the benchmark
    company in its peer group.
    """

    result = df.copy()

    # Remove old columns if the function is called again
    result = result.drop(
        columns=["benchmark_score", "score_difference"],
        errors="ignore"
    )

    benchmark_scores = (
        result[
            (result["is_benchmark"] == 1) &
            (result["composite_quality_score"].notna())
        ][
            ["peer_group_name", "year", "composite_quality_score"]
        ]
        .rename(
            columns={
                "composite_quality_score": "benchmark_score"
            }
        )
        .drop_duplicates(
            subset=["peer_group_name", "year"]
        )
    )

    result = result.merge(
        benchmark_scores,
        on=["peer_group_name", "year"],
        how="left"
    )

    result["score_difference"] = (
        result["composite_quality_score"] -
        result["benchmark_score"]
    )

    return result