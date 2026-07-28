from pathlib import Path
import pandas as pd
import pytest

from scripts.loader import load_excel, load_all_datasets


def test_load_excel_returns_dataframe(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    file = tmp_path / "sample.xlsx"
    df.to_excel(file, index=False)

    result = load_excel(file)

    assert isinstance(result, pd.DataFrame)


def test_load_excel_row_count(tmp_path):
    df = pd.DataFrame({"A": [1, 2, 3]})
    file = tmp_path / "sample.xlsx"
    df.to_excel(file, index=False)

    result = load_excel(file)

    assert len(result) == 3


def test_load_excel_column_names(tmp_path):
    df = pd.DataFrame({"Col1": [1], "Col2": [2]})
    file = tmp_path / "sample.xlsx"
    df.to_excel(file, index=False)

    result = load_excel(file)

    assert list(result.columns) == ["Col1", "Col2"]


def test_load_all_datasets_single_file(tmp_path):
    df = pd.DataFrame({"A": [1]})
    df.to_excel(tmp_path / "one.xlsx", index=False)

    datasets = load_all_datasets(tmp_path)

    assert "one" in datasets


def test_load_all_datasets_multiple_files(tmp_path):
    pd.DataFrame({"A": [1]}).to_excel(tmp_path / "one.xlsx", index=False)
    pd.DataFrame({"B": [2]}).to_excel(tmp_path / "two.xlsx", index=False)

    datasets = load_all_datasets(tmp_path)

    assert len(datasets) == 2


def test_load_all_datasets_returns_dict(tmp_path):
    pd.DataFrame({"A": [1]}).to_excel(tmp_path / "one.xlsx", index=False)

    datasets = load_all_datasets(tmp_path)

    assert isinstance(datasets, dict)


def test_dataset_keys_are_file_stems(tmp_path):
    pd.DataFrame({"A": [1]}).to_excel(tmp_path / "financials.xlsx", index=False)

    datasets = load_all_datasets(tmp_path)

    assert "financials" in datasets


def test_dataset_values_are_dataframes(tmp_path):
    pd.DataFrame({"A": [1]}).to_excel(tmp_path / "financials.xlsx", index=False)

    datasets = load_all_datasets(tmp_path)

    assert isinstance(datasets["financials"], pd.DataFrame)


def test_empty_directory_returns_empty_dict(tmp_path):
    datasets = load_all_datasets(tmp_path)

    assert datasets == {}


def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_excel("does_not_exist.xlsx")