#!/usr/bin/env python3
"""
Train and compare QSAR regression models across precomputed fingerprint datasets.

Input:
    data/legacy_fingerprints/*.csv

Each CSV is expected to contain:
    - pIC50 column as target
    - fingerprint columns as features

Outputs:
    results/tables/fingerprint_model_metrics.csv
    results/figures/best_model_predicted_vs_actual.png
    results/figures/model_comparison_by_fingerprint.png
    results/models/best_qsar_model.joblib
"""

from __future__ import annotations

import argparse
from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.linear_model import ElasticNet, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


warnings.filterwarnings("ignore")


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def load_fingerprint_dataset(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)

    if "pIC50" not in df.columns:
        raise ValueError(f"{path.name} does not contain a pIC50 column.")

    df = df.dropna().drop_duplicates()
    y = df["pIC50"].astype(float)
    X = df.drop(columns=["pIC50"])

    # Keep numeric columns only.
    X = X.select_dtypes(include=[np.number])

    # Remove constant columns.
    nunique = X.nunique()
    X = X.loc[:, nunique > 1]

    return X, y


def get_models(random_state: int = 42) -> dict[str, object]:
    return {
        "Ridge": Pipeline([
            ("scaler", StandardScaler()),
            ("model", Ridge(alpha=1.0)),
        ]),
        "ElasticNet": Pipeline([
            ("scaler", StandardScaler()),
            ("model", ElasticNet(alpha=0.01, l1_ratio=0.5, max_iter=10000, random_state=random_state)),
        ]),
        "RandomForest": RandomForestRegressor(
            n_estimators=300,
            random_state=random_state,
            n_jobs=-1,
            min_samples_leaf=2,
        ),
        "ExtraTrees": ExtraTreesRegressor(
            n_estimators=300,
            random_state=random_state,
            n_jobs=-1,
            min_samples_leaf=2,
        ),
        "GradientBoosting": GradientBoostingRegressor(random_state=random_state),
    }


def evaluate_file(path: Path, results_dir: Path, random_state: int = 42) -> tuple[list[dict], dict]:
    X, y = load_fingerprint_dataset(path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=random_state
    )

    rows = []
    best = {
        "r2": -np.inf,
        "model": None,
        "model_name": None,
        "dataset": path.name,
        "X_test": X_test,
        "y_test": y_test,
        "y_pred": None,
        "feature_names": list(X.columns),
    }

    for model_name, model in get_models(random_state).items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        row = {
            "fingerprint_file": path.name,
            "model": model_name,
            "n_samples": int(len(y)),
            "n_features": int(X.shape[1]),
            "r2": r2_score(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred),
            "rmse": rmse(y_test, y_pred),
        }
        rows.append(row)

        if row["r2"] > best["r2"]:
            best.update({
                "r2": row["r2"],
                "model": model,
                "model_name": model_name,
                "X_test": X_test,
                "y_test": y_test,
                "y_pred": y_pred,
                "feature_names": list(X.columns),
            })

    return rows, best


def plot_best_predicted_vs_actual(best: dict, figures_dir: Path) -> None:
    y_test = best["y_test"]
    y_pred = best["y_pred"]

    plt.figure(figsize=(7, 6))
    plt.scatter(y_test, y_pred, alpha=0.75)
    min_val = min(float(np.min(y_test)), float(np.min(y_pred)))
    max_val = max(float(np.max(y_test)), float(np.max(y_pred)))
    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")
    plt.xlabel("Actual pIC50")
    plt.ylabel("Predicted pIC50")
    plt.title(f"Best QSAR Model: {best['model_name']} on {best['dataset']}")
    plt.tight_layout()
    plt.savefig(figures_dir / "best_model_predicted_vs_actual.png", dpi=300)
    plt.close()


def plot_model_comparison(metrics: pd.DataFrame, figures_dir: Path) -> None:
    top = metrics.sort_values("r2", ascending=False).head(15).copy()
    top["label"] = top["fingerprint_file"].str.replace(".csv", "", regex=False) + " | " + top["model"]

    plt.figure(figsize=(10, 7))
    plt.barh(top["label"][::-1], top["r2"][::-1])
    plt.xlabel("Test R2")
    plt.ylabel("Fingerprint + Model")
    plt.title("Top QSAR Model Performance")
    plt.tight_layout()
    plt.savefig(figures_dir / "model_comparison_by_fingerprint.png", dpi=300)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/legacy_fingerprints")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    results_dir = Path(args.results_dir)
    figures_dir = results_dir / "figures"
    tables_dir = results_dir / "tables"
    models_dir = results_dir / "models"

    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    all_rows = []
    global_best = {"r2": -np.inf}

    for csv_file in sorted(input_dir.glob("*.csv")):
        print(f"Training models for: {csv_file.name}")
        rows, best = evaluate_file(csv_file, results_dir, args.random_state)
        all_rows.extend(rows)

        if best["r2"] > global_best["r2"]:
            global_best = best

    metrics = pd.DataFrame(all_rows).sort_values("r2", ascending=False)
    metrics.to_csv(tables_dir / "fingerprint_model_metrics.csv", index=False)

    joblib.dump(global_best["model"], models_dir / "best_qsar_model.joblib")

    pd.DataFrame({
        "actual_pIC50": global_best["y_test"],
        "predicted_pIC50": global_best["y_pred"],
    }).to_csv(tables_dir / "best_model_predictions.csv", index=False)

    plot_best_predicted_vs_actual(global_best, figures_dir)
    plot_model_comparison(metrics, figures_dir)

    print("\nBest model")
    print("----------")
    print(f"Dataset: {global_best['dataset']}")
    print(f"Model:   {global_best['model_name']}")
    print(f"R2:      {global_best['r2']:.4f}")
    print(f"\nSaved metrics to: {tables_dir / 'fingerprint_model_metrics.csv'}")


if __name__ == "__main__":
    main()
