"""
Optional SHAP analysis for the saved QSAR model.

Input:
    results/models/best_qsar_model.joblib
    results/tables/qsar_descriptors.csv

Output:
    results/figures/shap_summary.png

Note:
    SHAP works best with tree models. For non-tree pipelines, this script
    uses a generic explainer and may be slower.
"""

from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt

try:
    import shap
except ImportError as exc:
    raise ImportError("Install shap first: pip install shap") from exc

MODEL_PATH = Path("results/models/best_qsar_model.joblib")
DATA_PATH = Path("results/tables/qsar_descriptors.csv")
FIG_DIR = Path("results/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    features = bundle["features"]

    df = pd.read_csv(DATA_PATH).dropna(subset=features)
    X = df[features]

    explainer = shap.Explainer(model.predict, X)
    shap_values = explainer(X)

    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shap_summary.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Saved: {FIG_DIR / 'shap_summary.png'}")


if __name__ == "__main__":
    main()
