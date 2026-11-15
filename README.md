# MeaningGuard

MeaningGuard measures meaning loss during AI translation and highlights cases where a round\-trip translation may have lost important meaning. This research project compares English text with its English back\-translation after translation into French or Swahili.

## Project Overview

MeaningGuard explores how different types of language behave during AI translation. Each input passes through an English → target language → English workflow, and an embedding\-based similarity score estimates how closely the back\-translation preserves the original meaning. The similarity score is converted into a meaning\-loss value and a Low, Medium, or High risk category.

The current repository provides a batch analysis pipeline and visualizations. It does not include a deployed user\-facing warning interface.

## Problem Statement

Machine translation can preserve the general topic of a sentence while changing nuance, intent, or non\-literal meaning. Idioms, slang, sarcasm, and indirect speech may be especially sensitive to these shifts. MeaningGuard investigates whether a consistent round\-trip scoring workflow can help identify potential meaning loss for further review.

## Research Question

**Which types of language lose the most meaning during AI translation?**

## Core Innovation

MeaningGuard combines a multilingual translation model with semantic similarity scoring to provide a simple, comparable signal of meaning preservation. It evaluates examples across multiple language categories and target languages, then summarizes scores through category comparisons, language comparisons, and risk classifications.

The score is an automated screening signal, not a guarantee of correctness or a replacement for human review.

## Methodology

For each English dataset example, MeaningGuard:

1. Translates the text from English into French or Swahili using NLLB\-200.
2. Translates the result back into English using NLLB\-200.
3. Encodes the original and back\-translated English text using sentence\-transformers/paraphrase\-multilingual\-MiniLM\-L12\-v2.
4. Calculates normalized cosine similarity between the sentence embeddings.
5. Computes meaning loss and assigns a risk category.

The scoring formula is:

Meaning Loss = (1 \- similarity) × 100

Here, similarity is normalized to the range [0, 1]; lower similarity therefore produces a higher meaning\-loss score.

Risk levels are defined as:

Low:    < 20

Medium: 20–39.99

High:   40\+

These thresholds were defined for this project and have not yet been validated against human evaluations. They should be interpreted as an exploratory screening system rather than a definitive measurement of translation quality.

For additional details, see docs/methodology.md.

## Technology Stack

- **Translation:** Meta NLLB\-200 (facebook/nllb\-200\-distilled\-600M)
- **Semantic Similarity:** Sentence Transformers (sentence\-transformers/paraphrase\-multilingual\-MiniLM\-L12\-v2)
- **Machine Learning Runtime:** PyTorch and Transformers
- **Data Processing:** Python, pandas, and NumPy
- **Visualization:** Matplotlib and Seaborn

## Dataset Description

The pipeline uses data/meaningguard\_dataset.csv, which contains 125 English examples balanced across five categories:

| Category | Examples |
| --- | --- |
| Literal Language | 25 |
| Idiom | 25 |
| Sarcasm | 25 |
| Slang | 25 |
| Indirect Speech | 25 |

Each example contains:

- ID
- Category label
- English text

Both target\-language experiments use the same source examples, resulting in **250 total translation observations**:

- 125 French
- 125 Swahili

The dataset was manually created and evenly distributed across the five categories. Additional information is available in docs/dataset.md.

## Repository Structure

MeaningGuard/

├── data/

│   └── meaningguard\_dataset.csv

├── docs/

│   ├── dataset.md

│   ├── demo\_script.md

│   ├── findings.md

│   └── methodology.md

├── results/

│   ├── final\_results.csv

│   ├── french\_results.csv

│   └── swahili\_results.csv

├── src/

│   ├── run\_pipeline.py

│   ├── scoring.py

│   ├── similarity.py

│   └── translate.py

├── visualizations/

│   ├── category\_loss.png

│   ├── create\_charts.py

│   ├── heatmap.png

│   ├── language\_comparison.png

│   └── risk\_distribution.png

├── requirements.txt

└── README.md

## Installation

Use Python 3.10 or later.

Create and activate a virtual environment:

python \-m venv .venv

macOS / Linux:

source .venv/bin/activate

Windows PowerShell:

.\\.venv\\Scripts\\Activate.ps1

Install dependencies:

python \-m pip install \-r requirements.txt

The first run downloads model files, so an internet connection is required unless they have already been cached.

## Running the Pipeline

Run:

python src/run\_pipeline.py

This generates:

results/french\_results.csv

results/swahili\_results.csv

results/final\_results.csv

Each row contains:

- Original text
- Translation
- Back translation
- Similarity score
- Meaning\-loss score
- Risk classification

To regenerate visualizations:

python visualizations/create\_charts.py

## Visualizations

MeaningGuard generates:

- Average Meaning Loss by Category
- Average Meaning Loss by Language
- Risk Distribution
- Average Meaning Loss by Language and Category

All generated charts are stored in the visualizations/ folder.

## Results

The current experiment produced **250 translations**:

- 125 French
- 125 Swahili

### Average Meaning Loss by Category

| Category | Average Meaning Loss |
| --- | --- |
| Slang | 9.294 |
| Idiom | 9.100 |
| Sarcasm | 6.542 |
| Indirect Speech | 5.300 |
| Literal Language | 3.316 |

### Average Meaning Loss by Language

| Language | Average Meaning Loss |
| --- | --- |
| Swahili | 8.105 |
| French | 5.316 |

### Risk Distribution

| Risk Level | Count | Percentage |
| --- | --- | --- |
| Low | 237 | 94.8% |
| Medium | 13 | 5.2% |
| High | 0 | 0.0% |

### Key Findings

- Slang produced the highest average meaning loss.
- Literal language produced the lowest average meaning loss.
- Swahili showed higher meaning loss than French across every category in this dataset.
- Most translations remained in the Low\-Risk category.

Full analysis is available in docs/findings.md.

## Limitations

- Back translation is an indirect measure of meaning preservation and may reflect errors from either translation direction.
- Embedding similarity is an automated proxy and may not capture all forms of nuance, intent, or cultural context.
- The dataset is relatively small and consists of manually created examples.
- Only French and Swahili were evaluated.
- Only one translation model and one similarity model were tested.
- Risk thresholds have not been calibrated against human judgments.
- Findings are descriptive and should not be interpreted as statistically significant conclusions.

## Future Work

- Expand the dataset and document annotation guidelines.
- Add more languages and translation systems.
- Compare automated scores with native\-speaker evaluations.
- Calibrate risk thresholds using human judgments.
- Investigate statistical significance across categories.
- Build an interactive translation\-risk warning interface.

## AI Assistance

GitHub Copilot ([github.com/features/copilot](https://github.com/features/copilot))
provided code suggestions, debugging assistance, documentation support, and
repository review. Microsoft Copilot
([copilot.microsoft.com](https://copilot.microsoft.com/)) assisted with
project planning. These tools provided assistance only. The project author
created the dataset, ran the experiments, analyzed the results, and made all
final project decisions.

MeaningGuard is a solo research project created for the Veritas AI International High School Hackathon 2026.

### Repository

[https://github.com/Joawyo/MeaningGuard](https://github.com/Joawyo/MeaningGuard)
