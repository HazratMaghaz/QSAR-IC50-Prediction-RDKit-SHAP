## Legacy Fingerprint QSAR Workflow

This project also includes a cleaned integration of self-learning QSAR fingerprint datasets.

The folder `data/legacy_fingerprints/` contains 12 precomputed fingerprint datasets with `pIC50` as the activity endpoint. These datasets are used to compare multiple fingerprint representations and machine-learning models.

Run the fingerprint-model comparison workflow:

```bash
python scripts/train_fingerprint_qsar_models.py
```

Then generate an applicability-domain diagnostic plot:

```bash
python scripts/applicability_domain.py
```

Main outputs:

| Output | Description |
|---|---|
| `results/tables/fingerprint_model_metrics.csv` | Model performance across fingerprint datasets |
| `results/tables/best_model_predictions.csv` | Actual vs predicted pIC50 for the best model |
| `results/figures/best_model_predicted_vs_actual.png` | Predicted-vs-actual plot |
| `results/figures/model_comparison_by_fingerprint.png` | Top fingerprint/model comparison plot |
| `results/figures/williams_plot_demo.png` | Applicability-domain style diagnostic plot |

The original learning notebooks and R scripts are kept separately as reference files, while the main workflow is refactored into clean Python scripts.
