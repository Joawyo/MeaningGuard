# Dataset Overview

MeaningGuard uses a manually created dataset of 125 English sentences to
explore how different kinds of language are preserved in machine-translation
round trips. The examples are evenly distributed across five categories, with
25 sentences per category. Each sentence is translated into French and
Swahili, producing 250 language-specific translation observations.

The dataset is intended for a small exploratory project, not as a
representative sample of everyday language or a benchmark of translation
quality.

# Dataset Structure

The source file is [`data/meaningguard_dataset.csv`](../data/meaningguard_dataset.csv)
and contains one row per English sentence:

| Column | Description |
|---|---|
| `id` | Identifier for the source sentence |
| `category` | Language category assigned to the sentence |
| `english_text` | English sentence used as the translation input |

Translation outputs and evaluation scores are stored separately in the CSV
files under [`results/`](../results/).

# Categories

Each category has 25 examples:

## Literal

Direct, primarily literal statements used as a comparison group.

## Idiom

Expressions whose intended meaning is not necessarily the literal meaning of
their individual words.

## Slang

Informal or colloquial expressions, including language whose meaning may
depend on community or context.

## Sarcasm

Statements where the intended meaning may differ from or contrast with the
literal wording.

## Indirect Speech

Statements that communicate a request, opinion, or intention indirectly
rather than stating it explicitly.

# Dataset Creation Process

The 125 English sentences were manually created and assigned to the five
categories, with 25 sentences in each category. This balanced construction
allows the project to compare category averages using the same number of
source examples per category. Each source sentence is then used in both the
French and Swahili experiments.

# Limitations

- **Limited dataset size:** With 25 examples per category, the dataset
  provides only a small sample. Results may be sensitive to the wording and
  selection of individual sentences.
- **Hand-crafted examples:** Manually created sentences may not reflect the
  frequency, diversity, or context of language use in real-world
  communication.
- **Category subjectivity:** Categories such as sarcasm, slang, and indirect
  speech can overlap, and reasonable annotators may classify some examples
  differently. The project does not document formal annotation guidelines
  or independent label review.

These limitations mean that findings should be interpreted as exploratory
and should not be generalized to all text, speakers, or translation
scenarios.

# Future Dataset Expansion

Future versions could expand the number and diversity of examples per
category, document category definitions and labeling decisions, and obtain
independent review from multiple annotators. The dataset could also include
context where needed to disambiguate intent, cover more varieties of English,
and add other language categories and translation target languages. A larger,
carefully documented dataset would support more robust comparisons and
evaluation against human judgments.
