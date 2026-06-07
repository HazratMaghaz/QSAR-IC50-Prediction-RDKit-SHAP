# Legacy QSAR Learning Dataset and Code Mapping

This folder integrates QSAR learning materials that were originally created during self-study. The goal is not to publish raw learning files as-is, but to refactor their useful parts into a cleaner, reproducible QSAR portfolio workflow.

## What was added

### Fingerprint datasets

The `data/legacy_fingerprints/` folder contains precomputed molecular fingerprint datasets. Each file has:

- `pIC50` as the target variable
- fingerprint bits/counts as input features
- 987 compounds/rows in each dataset

These files are useful for machine-learning model training and fingerprint-method comparison.

### Legacy reference notebooks

The original notebooks are placed in:

```text
notebooks/legacy_reference/
```

They are kept only as reference material.

### Legacy R scripts

The original R modeling scripts are placed in:

```text
archive/legacy_r_models/
```

They are kept for learning history. The main public workflow should use the cleaned Python scripts and notebooks.

## Clean project direction

The cleaned workflow should focus on:

1. Loading the fingerprint datasets
2. Comparing different fingerprint feature sets
3. Training machine-learning regression models for pIC50 prediction
4. Evaluating R2, MAE, and RMSE
5. Selecting the best fingerprint/model pair
6. Generating predicted-vs-actual plots
7. Running applicability domain analysis using a Williams plot
8. Saving final metrics and figures

## Important limitation

These fingerprint datasets do not include original SMILES strings. Therefore, they are suitable for ML model training and fingerprint comparison, but not for molecule drawing or new descriptor recalculation unless the original SMILES dataset is also available.
