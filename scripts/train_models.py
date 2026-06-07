"""
Train baseline QSAR machine learning models.

Input:
    results/tables/qsar_descriptors.csv

Outputs:
    results/tables/model_performance.csv
    results/tables/predictions_demo.csv
    results/models/best_qsar_model.joblib
    results/figures/predicted_vs_observed.png
"""

from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import ElasticNet, Ridge
from sklearn.ensemble import RandomForestRegressor

IN_PATH = Path("results/tables/qsar_descriptors.csv")
TABLE_DIR = Path("results/tables")
FIG_DIR = Path("results/figures")
MODEL_DIR = Path("results/models")
for path in [TABLE_DIR, FIG_DIR, MODEL_DIR]:
    path.mkdir(parents=True, exist_ok=True)

FEATURES = [
    "mol_wt",
    "logp",
    "hbd",
    "hba",
    "tpsa",
    "rotatable_bonds",
    "ring_count",
    "heavy_atom_count",
]
TARGET = "pic50"


def rmse(y_true, y_pred):
    return mean_squared_error(y_true, y_pred, squared=False)


def main() -> None:
    df = pd.read_csv(IN_PATH).dropna(subset=FEATURES + [TARGET])
    X = df[FEATURES]
    y = df[TARGET]

    # Small demo dataset: test split is only for demonstration.
    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X, y, df.index, test_size=0.25, random_state=42
    )

    models = {
        "Ridge": Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=1.0))]),
        "ElasticNet": Pipeline([("scaler", StandardScaler()), ("model", ElasticNet(alpha=0.05, l1_ratio=0.5, random_state=42))]),
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42, max_depth=4),
    }

    performance_rows = []
    best_name, best_model, best_mae = None, None, float("inf")

    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        try:
            cv_scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
            cv_mae = -cv_scores.mean()
        except Exception:
            cv_mae = None

        metrics = {
            "model": name,
            "test_r2": r2_score(y_test, pred),
            "test_mae": mean_absolute_error(y_test, pred),
            "test_rmse": rmse(y_test, pred),
            "cv_mae": cv_mae,
        }
        performance_rows.append(metrics)

        if metrics["test_mae"] < best_mae:
            best_name, best_model, best_mae = name, model, metrics["test_mae"]

    perf = pd.DataFrame(performance_rows)
    perf.to_csv(TABLE_DIR / "model_performance.csv", index=False)

    best_model.fit(X_train, y_train)
    final_pred = best_model.predict(X_test)

    pred_df = df.loc[test_idx, ["compound_id", "smiles", TARGET]].copy()
    pred_df["predicted_pic50"] = final_pred
    pred_df["absolute_error"] = (pred_df[TARGET] - pred_df["predicted_pic50"]).abs()
    pred_df.to_csv(TABLE_DIR / "predictions_demo.csv", index=False)

    joblib.dump({"model_name": best_name, "model": best_model, "features": FEATURES}, MODEL_DIR / "best_qsar_model.joblib")

    plt.figure(figsize=(6, 5))
    plt.scatter(y_test, final_pred)
    plt.xlabel("Observed pIC50")
    plt.ylabel("Predicted pIC50")
    plt.title(f"Predicted vs Observed pIC50 ({best_name})")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "predicted_vs_observed.png", dpi=300)
    plt.close()

    print("Model performance:")
    print(perf)
    print(f"Best model saved: {MODEL_DIR / 'best_qsar_model.joblib'}")


if __name__ == "__main__":
    main()
