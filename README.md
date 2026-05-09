# ARSA Variant Pathogenicity Predictor

A two-part machine learning project connecting genetic mutations to a rare childhood disease, with predictions submitted to the **CAGI 7 international blind challenge**.

**Self-test AUC: 0.953 &nbsp;|&nbsp; 2,491 ARSA variants predicted &nbsp;|&nbsp; Berkeley C146 · Spring 2026**

---

## How the Project Works

This project has two sequential tasks:

```
TASK 1 — Train a pathogenicity classifier
─────────────────────────────────────────────────────────────────
 Input:  13,464 human genetic variants from ClinVar (many genes)
         each scored by 17 existing computational tools
 Label:  clinically classified as Pathogenic or Benign
 Model:  Random Forest meta-predictor
 Output: P(pathogenic) — probability a variant causes disease
 Eval:   Held-out self-test set → AUC 0.953, PR-AUC 0.806

         ↓  apply trained model to ARSA-specific variants

TASK 2 — Submit ARSA stability predictions to CAGI 7
─────────────────────────────────────────────────────────────────
 Input:  2,491 possible mutations in the ARSA gene
 Output: stability_score = 1 − P(pathogenic)
         (higher score = more stable protein = more benign)
 Eval:   Scored by CAGI 7 against real lab stability measurements
         the model never saw (Kendall's τ rank correlation)
```

**Why does `1 − P(pathogenic)` approximate stability?**  
Unstable proteins are preferentially degraded by the cell — so destabilization and pathogenicity are correlated. The conversion is an approximation: some variants are pathogenic *without* destabilizing the protein (e.g. they disrupt catalysis while still folding correctly). Those will be systematically mis-ranked, and that's a known limitation of this approach.

**Why does this matter?**  
ARSA produces an enzyme that breaks down fatty deposits in the brain. When ARSA is broken, those deposits accumulate and destroy the myelin sheath, causing **Metachromatic Leukodystrophy (MLD)** — a rare, fatal disease in young children. A gene therapy (Lenmeldy, ~$4.25M/patient) can prevent the disease, but *only before symptoms appear*. Accurate variant prediction is what makes early intervention possible.

---

## Key Files

| | |
|--|--|
| [`notebooks/analysis.ipynb`](notebooks/analysis.ipynb) | Full pipeline — EDA → classifier training → ARSA predictions |
| [`results/stability_predictions.tsv`](results/stability_predictions.tsv) | CAGI 7 submission: 2,491 ARSA variants with stability scores |
| [`data/`](data/README.md) | All input datasets with column descriptions |

---

## Task 1 Results — Pathogenicity Classifier

<img src="figures/roc_pr_curves.png" width="680"/>

| Model | AUC | PR-AUC |
|---|---|---|
| **Random Forest (ours)** | **0.953** | **0.806** |
| CADD (best single tool) | 0.954 | 0.853 |
| AlphaMissense | 0.939 | 0.656 |

The meta-predictor combines 17 tools via Random Forest (GridSearchCV, 5-fold stratified CV). Training CV AUC was 0.992 — the gap to 0.953 on self-test reflects circular training: several component tools were themselves trained on ClinVar, inflating CV scores.

<img src="figures/feature_importances.png" width="560"/>

AlphaMissense and CADD dominate. Conservation scores (phastCons, phyloP) add little once variant-level predictors are present.

---

## Task 2 Results — ARSA Stability Predictions

<img src="figures/arsa_predictions_histogram.png" width="560"/>

2,491 ARSA variants predicted. ~55% fall below the severe MLD clinical threshold (stability < 0.572). The figure below plots predicted vs. experimental stability on the 344 labeled ARSA variants used for orientation checks — points in the lower-right are stable proteins the model incorrectly flags as pathogenic (the known failure mode of the 1−P mapping).

<img src="figures/creative_figure.png" width="580"/>

---

## Run It

```bash
git clone https://github.com/ramjhawar-alt/arsa-variant-predictor.git
cd arsa-variant-predictor
pip install -r requirements.txt
jupyter notebook notebooks/analysis.ipynb
```

Full pipeline takes ~15 minutes (grid searches).

---

## Stack

Python 3.13 · scikit-learn 1.8 · pandas 3.0 · numpy 2.4 · scipy 1.17 · matplotlib · seaborn
