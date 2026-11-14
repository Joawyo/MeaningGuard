# MeaningGuard Methodology

## Project Overview

MeaningGuard evaluates meaning preservation in English-to-language-to-English
translation round trips. It compares each English source sentence with its
English back-translation using a multilingual sentence-embedding model, then
converts the similarity score to a meaning-loss score and risk category.

The current pipeline evaluates French and Swahili. Its implementation is in
[`src/run_pipeline.py`](../src/run_pipeline.py), with translation, similarity,
and scoring helpers in [`src/translate.py`](../src/translate.py),
[`src/similarity.py`](../src/similarity.py), and
[`src/scoring.py`](../src/scoring.py).

## Dataset Creation

The pipeline reads `data/meaningguard_dataset.csv`, which contains 125 English
examples and three fields: `id`, `category`, and `english_text`. The dataset
has five categories—literal, idiom, sarcasm, slang, and indirect speech—with
25 examples in each category.

The 125 sentences were manually created and balanced across the five
categories. Formal category annotation guidelines and independent review or
validation procedures are not documented. See
[`docs/dataset.md`](./dataset.md) for the dataset structure and limitations.

The pipeline checks that the `id`, `category`, and `english_text` columns are
present and stops with an error if an example has no English text.

## Translation Workflow

For each English example, the pipeline performs an English-to-target-language
translation. The target languages are French (`fra_Latn`) and Swahili
(`swh_Latn`), using English (`eng_Latn`) as the source language code.

Both translation directions use
[`facebook/nllb-200-distilled-600M`](../src/translate.py). The tokenizer is
configured with the source language, and generation is directed to the target
language with its language token. The implementation uses PyTorch inference
mode and selects CUDA when available, otherwise CPU. A shared translator
instance is cached and reused.

## Back Translation Process

Each target-language translation is translated back to English using the same
NLLB-200 model. The pipeline therefore produces, for every source example, an
English source, a target-language translation, and an English
back-translation. Meaning loss is assessed by comparing the source with the
back-translation, not by comparing the source directly with the
target-language text.

## Semantic Similarity Measurement

The source and back-translation are encoded using
`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`. The model
returns normalized sentence embeddings. Their dot product gives the cosine
similarity, which is clamped to the valid cosine range `[-1, 1]` to handle
floating-point error, then mapped to `[0, 1]`:

```text
normalized_similarity = (cosine_similarity + 1) / 2
```

Thus, `1` represents the highest similarity on this normalized scale and `0`
the lowest. This is an automated embedding-based proxy for semantic
preservation; it is not a human evaluation.

## Meaning Loss Score Formula

The pipeline calculates the meaning-loss score as:

```text
Meaning Loss Score = (1 - normalized_similarity) × 100
```

The result ranges from `0` to `100`: lower scores indicate greater embedding
similarity between the source and back-translation, while higher scores
indicate less similarity. Because the similarity is first mapped from
`[-1, 1]` to `[0, 1]`, the score is based on that normalized value.

## Risk Classification

Each meaning-loss score is assigned a risk category using the thresholds in
[`src/scoring.py`](../src/scoring.py):

| Meaning-loss score | Risk |
|---|---|
| Below 20 | Low |
| 20 to below 40 | Medium |
| 40 or above | High |

These are the project's operational thresholds. The repository does not
document external calibration or validation of the thresholds against human
judgments or downstream harm.

## Experimental Procedure

The pipeline loads the similarity model once, then runs the full dataset
through the French experiment and the Swahili experiment. For each example in
each experiment, it records the ID, category, language, source text,
translation, back-translation, normalized similarity, meaning-loss score,
and risk category.

This produces 125 observations per language and 250 language-specific
observations in total. The two language observations for a given source
example share the same source text, so they are paired evaluations rather
than independent source examples.

After each language experiment completes, its results are written to
`results/french_results.csv` or `results/swahili_results.csv`. Once both
experiments finish, their rows are concatenated and written to
`results/final_results.csv`. The combined file retains the same columns as
the language-specific files. Analyses of these results are descriptive unless
additional statistical tests or human evaluations are performed.
