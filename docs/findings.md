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

## Sources and Acknowledgements

The sources below are identified from the repository's dependency manifest,
implementation, and documentation. Links point to official project, package,
or model pages where available.

### AI Models

- **Meta NLLB-200 distilled 600M**
  - Link: [Model page](https://huggingface.co/facebook/nllb-200-distilled-600M)
  - Used through the Transformers library for English-to-French and
    English-to-Swahili translation round trips.
- **Multilingual MiniLM-L12-v2**
  (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`)
  - Link: [Model page](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
  - Used to encode the original English text and its English back-translation
    as sentence embeddings for semantic-similarity scoring.

### Python Libraries

- **Transformers**
  - Link: [Hugging Face Transformers documentation](https://huggingface.co/docs/transformers/)
  - Loads the NLLB tokenizer and sequence-to-sequence model and generates
    translations.
- **PyTorch**
  - Link: [PyTorch documentation](https://pytorch.org/docs/stable/)
  - Runs model inference, selects CUDA when available, and provides
    inference-mode execution.
- **Sentence Transformers**
  - Link: [Sentence Transformers documentation](https://www.sbert.net/)
  - Loads the multilingual embedding model and encodes sentence pairs.
- **NumPy**
  - Link: [NumPy documentation](https://numpy.org/doc/)
  - Computes the dot product of normalized embeddings for the similarity
    score.
- **pandas**
  - Link: [pandas documentation](https://pandas.pydata.org/docs/)
  - Reads the input and result CSV files, processes tabular data, and writes
    experiment results.
- **Matplotlib**
  - Link: [Matplotlib documentation](https://matplotlib.org/stable/)
  - Creates and saves the result charts.
- **Seaborn**
  - Link: [Seaborn documentation](https://seaborn.pydata.org/)
  - Provides chart styles and statistical plots for the visualizations.
- **scikit-learn**
  - Link: [scikit-learn documentation](https://scikit-learn.org/stable/)
  - Listed in `requirements.txt`; no direct import or use was found in the
    current implementation.

### Development Tools

- **Python**
  - Link: [Python](https://www.python.org/) and the
    [venv documentation](https://docs.python.org/3/library/venv.html)
  - The documented runtime for the pipeline and chart-generation scripts;
    the README specifies Python 3.10 or later and gives virtual-environment
    setup instructions.
- **pip**
  - Link: [pip documentation](https://pip.pypa.io/en/stable/)
  - The documented installer used to install dependencies from
    `requirements.txt`.

### Platforms

- **Hugging Face Hub**
  - Link: [Hugging Face](https://huggingface.co/)
  - Hosts the model checkpoints referenced by the code and from which
    Transformers and Sentence Transformers load them.
- **CUDA**
  - Link: [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-toolkit)
  - An optional GPU execution path: the translator uses CUDA when PyTorch
    reports it is available and otherwise uses the CPU. The repository does
    not establish which device was used to produce the checked-in results.
- **GitHub**
  - Link: [MeaningGuard repository](https://github.com/Joawyo/MeaningGuard)
  - Hosts the project repository and its source, documentation, dataset, and
    results.

### Documentation References

- **MeaningGuard methodology**
  - Link: [docs/methodology.md](./methodology.md)
  - Documents the translation workflow, models, similarity calculation,
    scoring formula, and risk thresholds used by this project.
- **MeaningGuard dataset description**
  - Link: [docs/dataset.md](./dataset.md)
  - Documents the project dataset and its creation and limitations.
- **MeaningGuard dataset**
  - Link: [data/meaningguard_dataset.csv](../data/meaningguard_dataset.csv)
  - The 125 manually created English examples used as pipeline input. The
    repository identifies this as a project-created dataset; no external
    dataset source was found.

### AI Assistance

No AI assistant use is identified in the repository contents, so no
assistant is credited here. Add an acknowledgement if project records
confirm an assistant was used.

### Documentation Credits to Add

Before this section, the repository named the models and summarized its
technology stack but did not provide official source links for the models or
libraries. Those source links are now recorded above. The dataset is
described as manually created, with no external dataset source identified.
The `scikit-learn` dependency is declared but has no direct use in the
current implementation; remove it from `requirements.txt` if it is not
needed, rather than describing it as an actively used library.
