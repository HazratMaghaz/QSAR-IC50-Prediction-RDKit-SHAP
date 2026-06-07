"""
Predict pIC50 for new compounds.

Inputs:
    data/new_compounds.csv
    results/models/best_qsar_model.joblib

Output:
    results/tables/new_compound_predictions.csv
"""

from pathlib import Path
import joblib
import pandas as pd

from generate_descriptors import calculate_descriptors

NEW_PATH = Path("data/new_compounds.csv")
MODEL_PATH = Path("results/models/best_qsar_model.joblib")
OUT_DIR = Path("results/tables")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    features = bundle["features"]

    df = pd.read_csv(NEW_PATH)
    desc = df["smiles"].apply(calculate_descriptors).apply(pd.Series)
    out = pd.concat([df, desc], axis=1)
    out = out[out["valid_smiles"]].copy()

    out["predicted_pic50"] = model.predict(out[features])
    out["predicted_ic50_uM"] = 10 ** (6 - out["predicted_pic50"])

    out[["compound_id", "smiles", "predicted_pic50", "predicted_ic50_uM"]].to_csv(
        OUT_DIR / "new_compound_predictions.csv", index=False
    )

    print(out[["compound_id", "predicted_pic50", "predicted_ic50_uM"]])


if __name__ == "__main__":
    main()
