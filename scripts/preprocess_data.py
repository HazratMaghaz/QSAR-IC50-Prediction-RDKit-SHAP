"""
Preprocess QSAR input data.

Input:
    data/sample_qsar_dataset.csv

Output:
    results/tables/clean_qsar_dataset.csv
"""

from pathlib import Path
import math
import pandas as pd

DATA_PATH = Path("data/sample_qsar_dataset.csv")
OUT_DIR = Path("results/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_COLUMNS = {"compound_id", "smiles", "ic50_uM"}


def ic50_um_to_pic50(ic50_um: float) -> float:
    """Convert IC50 in micromolar to pIC50."""
    if ic50_um <= 0:
        raise ValueError("IC50 must be greater than zero.")
    return 6 - math.log10(ic50_um)


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=["compound_id", "smiles", "ic50_uM"]).copy()
    df["ic50_uM"] = pd.to_numeric(df["ic50_uM"], errors="coerce")
    df = df.dropna(subset=["ic50_uM"])
    df = df[df["ic50_uM"] > 0].copy()

    if "pic50" not in df.columns:
        df["pic50"] = df["ic50_uM"].apply(ic50_um_to_pic50)

    df.to_csv(OUT_DIR / "clean_qsar_dataset.csv", index=False)
    print(f"Saved cleaned dataset: {OUT_DIR / 'clean_qsar_dataset.csv'}")
    print(df.head())


if __name__ == "__main__":
    main()
