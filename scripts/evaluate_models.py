"""
Create a simple model-performance bar plot.

Input:
    results/tables/model_performance.csv

Output:
    results/figures/model_mae_comparison.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PERF_PATH = Path("results/tables/model_performance.csv")
FIG_DIR = Path("results/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    perf = pd.read_csv(PERF_PATH)
    perf = perf.sort_values("test_mae")

    plt.figure(figsize=(7, 4))
    plt.bar(perf["model"], perf["test_mae"])
    plt.ylabel("Test MAE")
    plt.title("QSAR model comparison")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "model_mae_comparison.png", dpi=300)
    plt.close()

    print(f"Saved: {FIG_DIR / 'model_mae_comparison.png'}")


if __name__ == "__main__":
    main()
