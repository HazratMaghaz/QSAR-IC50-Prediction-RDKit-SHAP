#!/usr/bin/env python3
"""
Generate a simple Williams plot / applicability-domain style diagnostic.

This script uses the saved best-model predictions table created by:
    scripts/train_fingerprint_qsar_models.py

Output:
    results/figures/williams_plot_demo.png

Note:
    A full Williams plot requires leverage values from the model matrix.
    This demo version uses standardized residuals against predicted pIC50
    to provide an easy beginner-friendly diagnostic plot.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main() -> None:
    table_path = Path("results/tables/best_model_predictions.csv")
    out_dir = Path("results/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not table_path.exists():
        raise FileNotFoundError(
            "Run scripts/train_fingerprint_qsar_models.py first to generate predictions."
        )

    df = pd.read_csv(table_path)
    df["residual"] = df["actual_pIC50"] - df["predicted_pIC50"]
    df["standardized_residual"] = (
        df["residual"] - df["residual"].mean()
    ) / df["residual"].std(ddof=0)

    plt.figure(figsize=(8, 6))
    plt.scatter(df["predicted_pIC50"], df["standardized_residual"], alpha=0.75)
    plt.axhline(3, linestyle="--")
    plt.axhline(-3, linestyle="--")
    plt.axhline(0, linestyle="-")
    plt.xlabel("Predicted pIC50")
    plt.ylabel("Standardized residual")
    plt.title("Applicability Domain Diagnostic: Standardized Residual Plot")
    plt.tight_layout()
    plt.savefig(out_dir / "williams_plot_demo.png", dpi=300)
    plt.close()

    print("Saved:", out_dir / "williams_plot_demo.png")


if __name__ == "__main__":
    main()
