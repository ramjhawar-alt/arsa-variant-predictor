# Data Directory

All feature scores come from **dbNSFP v4.9a** (released 8 August 2024), a database that pre-computes functional impact scores for every possible amino acid–changing single-nucleotide variant in the human exome.

Labels (pathogenic / benign) come from **ClinVar** under ACMG/AMP classification guidelines.

---

## Files

### `training_variants.tsv`
~13,000 ClinVar missense variants used to train the meta-predictor. Each row is one variant with 17 feature scores and a binary label (`Y`: 0 = benign/likely-benign, 1 = pathogenic/likely-pathogenic).

Class balance: ~12,144 benign / 1,320 pathogenic (~9:1 ratio).

### `test_variants.tsv`
2,000 ClinVar variants classified **after** the training cutoff — used exactly once for the final generalization estimate. Never used during training or hyperparameter tuning.

### `arsa_sample_labeled.tsv`
344 ARSA missense variants with experimental measurements from the CAGI 7 dataset:
- `stability_score_48hr` — protein stability at 48 hours (wildtype ≈ 0.784; severe MLD threshold < 0.572)
- `CDS percent WT activity` — enzymatic activity as percent of wildtype
- All 17 dbNSFP feature scores

### `arsa_snv_features.tsv`
2,491 SNV-accessible ARSA missense variants — the prediction targets. These are the ~2,000 amino acid substitutions reachable from the reference codon by a single base change. dbNSFP does not cover multi-nucleotide variants (MNVs), which is why coverage is ~2,000 out of ~8,867 total possible ARSA missense changes.

### `arsa_submission_template.tsv`
Blank CAGI 7 submission template listing all 2,491 target variants with empty score and SD columns.

### `gene_annotations.tsv`
Per-gene annotations joined by Ensembl gene ID: GO biological process, GO molecular function, GO cellular component, pathway membership (KEGG, ConsensusPathDB), disease associations, and function descriptions. Not used as model features directly.

---

## Feature Column Descriptions

| Column | What it measures | Direction |
|--------|-----------------|-----------|
| `CADD_raw` | Combined annotation-dependent depletion (ensemble) | ↑ = more damaging |
| `DANN_score` | Deep neural network trained on CADD's data | ↑ = more damaging |
| `Eigen-raw_coding` | Unsupervised spectral approach | ↑ = more damaging |
| `Eigen-PC-raw_coding` | PC-corrected Eigen score | ↑ = more damaging |
| `FATHMM_score` | Functional analysis via hidden Markov model | ↓ = more damaging |
| `GERP++_RS` | Evolutionary constraint (rejected substitutions) | ↑ = more constrained |
| `PROVEAN_score` | Protein variation effect analyzer | ↓ = more damaging |
| `Polyphen2_HVAR_score` | PolyPhen-2 HumVar score | ↑ = more damaging |
| `SIFT_score` | Sequence-based tolerance prediction | ↓ = more damaging |
| `VEST4_score` | Variant effect scoring tool v4 | ↑ = more damaging |
| `phastCons100way_vertebrate` | Conservation across 100 vertebrate genomes | ↑ = more conserved |
| `phastCons470way_mammalian` | Conservation across 470 mammalian genomes | ↑ = more conserved |
| `phyloP100way_vertebrate` | Phylogenetic p-value, 100 vertebrates | ↑ = more conserved |
| `phyloP470way_mammalian` | Phylogenetic p-value, 470 mammals | ↑ = more conserved |
| `gnomAD_exomes_AF` | Population allele frequency (gnomAD v4) | ↑ = more common = likely benign |
| `AlphaMissense_score` | Google DeepMind structure-based predictor | ↑ = more damaging |
| `ESM1b_score` | Meta protein language model (ESM-1b) | ↓ = more damaging |

Missing values are encoded as `'.'` in the raw dbNSFP files; the loading function replaces them with `NaN`.
