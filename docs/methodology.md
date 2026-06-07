# Methodology

This repository demonstrates a machine-learning QSAR workflow for IC50/pIC50 prediction.

## Workflow

1. Load compound identifiers, SMILES, and IC50 values.
2. Convert IC50 values to pIC50.
3. Validate SMILES strings.
4. Generate molecular descriptors using RDKit.
5. Train baseline regression models.
6. Evaluate models using R², MAE, and RMSE.
7. Save demo figures, tables, and the selected model.
8. Predict pIC50 for new compounds.
9. Optionally run SHAP analysis for model interpretation.

## Why pIC50?

IC50 values are often converted to pIC50 because pIC50 is easier for regression modeling and makes stronger activity correspond to larger values.

For IC50 in micromolar:

```text
pIC50 = 6 - log10(IC50_uM)
```
