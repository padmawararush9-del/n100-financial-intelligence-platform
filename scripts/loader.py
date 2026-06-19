from pathlib import Path
import pandas as pd

SPECIAL_FILES = {
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
}


def load_excel(file_path):
    file_path = Path(file_path)

    if file_path.name in SPECIAL_FILES:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path)

    return df


def load_all_datasets(data_dir):
    datasets = {}

    for file in Path(data_dir).glob("*.xlsx"):
        datasets[file.stem] = load_excel(file)

    return datasets


if __name__ == "__main__":

    datasets = load_all_datasets(
        "../data/raw"
    )

    for name, df in datasets.items():

        print(
            f"{name}: {df.shape}"
        )