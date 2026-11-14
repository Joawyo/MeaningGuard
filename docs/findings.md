# MeaningGuard Findings

## Research Question

How does meaning loss in English translation round trips vary across text
categories and between French and Swahili, and what proportion of translations
falls into each project-defined risk level?

## Dataset Summary

The analysis uses the 250 observations in `results/final_results.csv`. These
comprise 125 English-to-French-to-English translations and 125
English-to-Swahili-to-English translations. Each observation records a
category, a meaning-loss score, and a risk classification.

## Category Results

Mean meaning-loss scores by category are shown below. Higher scores indicate
lower semantic similarity between the original English text and its
back-translation.

| Category | Average meaning loss |
|---|---:|
| Slang | 9.294 |
| Idiom | 9.100 |
| Sarcasm | 6.542 |
| Indirect Speech | 5.300 |
| Literal | 3.316 |

Slang had the highest average loss, closely followed by idioms. Literal
examples had the lowest average loss.

## Language Comparison

| Translation language | Average meaning loss |
|---|---:|
| Swahili | 8.105 |
| French | 5.316 |

In this dataset, Swahili translations had a higher average meaning-loss score
than French translations. This is a descriptive comparison and does not by
itself establish a statistically significant or generalizable language
difference.

## Risk Distribution

| Risk level | Translations | Percentage |
|---|---:|---:|
| Low | 237 | 94.8% |
| Medium | 13 | 5.2% |
| High | 0 | 0.0% |

Low risk was the most common classification. The risk levels use
MeaningGuard's project-defined thresholds.

## Key Findings

- The dataset contains 250 translations, evenly divided between French and
  Swahili (125 each).
- Slang (9.294) and idioms (9.100) had the highest category-average meaning
  loss; literal examples had the lowest (3.316).
- Swahili's average meaning loss (8.105) exceeded French's (5.316).
- Most translations were classified as Low risk (94.8%); none were classified
  as High risk.

## Limitations

These results are descriptive and come from a finite project dataset. The
translation comparison uses back-translations and an automated
embedding-based similarity measure, which is a proxy for meaning preservation
and not a human assessment. The results may also reflect the specific
translation and embedding models used. No statistical significance testing,
confidence intervals, or human validation are reported here; the observed
differences should not be interpreted as causal or generalized beyond the
evaluated examples and languages.

## Threats to Validity

Several factors constrain the interpretation and generalizability of these
findings. First, the dataset contains only 125 source sentences, with 25
examples per category. This limited sample may not capture the diversity of
language use within each category, and observed averages may be sensitive to
the particular examples selected.

Second, semantic embedding similarity is an indirect proxy for meaning
preservation. Similarity scores may not reliably represent pragmatic intent,
tone, cultural context, or distinctions that are important to human readers.
Consequently, a higher or lower score should not be treated as a definitive
judgment of translation quality.

Third, the results have not been compared with judgments from fluent speakers
or other human evaluators. Without such evaluation, the validity of the
automated scores and their relationship to perceived meaning loss remain
uncertain. The project-defined risk thresholds likewise have not been
validated against human assessments.

Finally, the experiment covers only French and Swahili, using one
translation-model configuration. Results may differ for other languages,
language varieties, translation systems, or translation directions. The
language comparison should therefore be interpreted as specific to this
dataset and setup, not as evidence of general differences between languages.

## Conclusion

In the evaluated round trips, average meaning loss varied across categories
and languages: slang and idioms showed the largest category averages, while
literal text showed the smallest, and Swahili had a higher average than
French. Nearly all translations were assigned Low risk under the project's
thresholds, with no High-risk cases. These findings provide a useful
descriptive snapshot for the hackathon project, while further examples,
human evaluation, and statistical analysis would be needed to support broader
conclusions.
