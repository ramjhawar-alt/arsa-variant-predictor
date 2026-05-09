# ARSA Variant Pathogenicity Predictor

A machine learning model that predicts whether a genetic mutation in the **ARSA gene** is likely to cause **Metachromatic Leukodystrophy (MLD)** — a rare, fatal childhood disease. The model is trained on 13,000+ clinically classified variants from across the human genome, learns to output a probability of pathogenicity, and then converts that to a protein stability score (`1 − P(pathogenic)`) which was submitted to the **CAGI 7 international blind challenge** to be scored against real lab measurements the model never saw.

**Self-test AUC: 0.953 &nbsp;|&nbsp; 2,491 ARSA variants predicted &nbsp;|&nbsp; Berkeley C146 · Spring 2026**

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
