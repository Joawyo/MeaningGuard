# MeaningGuard: Two-Minute Demo Script

**Format:** Screen recording with narration  
**Target length:** Approximately two minutes  
**Preparation:** Open the repository in a code editor or GitHub, and have
`data/meaningguard_dataset.csv`, `src/run_pipeline.py`,
`results/final_results.csv`, and the four charts in `visualizations/` ready to
show. Use the saved results for the walkthrough; running the full pipeline
live may take time because model checkpoints may need to load or download.

| Time | On screen | Narration |
|---|---|---|
| 0:00–0:15 | Show the repository root and briefly highlight `data/`, `src/`, `results/`, `visualizations/`, and `docs/`. | “This is MeaningGuard, a research prototype that studies how much meaning can shift during machine translation. The repository separates the dataset, pipeline code, results, visualizations, and project documentation.” |
| 0:15–0:32 | Open `data/meaningguard_dataset.csv`. Show the `id`, `category`, and `english_text` columns, then scroll to a few category rows. | “Our dataset has 125 manually created English sentences, evenly split across five categories: literal language, idioms, slang, sarcasm, and indirect speech. Each sentence is evaluated in both French and Swahili.” |
| 0:32–0:52 | Open `src/run_pipeline.py`. Point to the French and Swahili `run_experiment` calls and then the concatenation to `final_results.csv`. | “The pipeline translates each English sentence into the target language with NLLB-200, then translates it back into English. It runs once for French and once for Swahili, saves a CSV for each experiment, and combines them into one results file.” |
| 0:52–1:15 | Open `results/final_results.csv` and locate row ID 56, French. Highlight the source, translation, back-translation, similarity, loss, and risk fields. | “Here is one actual slang example. The source says, ‘No cap, this is the best dumpling place in the neighborhood.’ The French translation begins ‘Pas de cap,’ and its back-translation becomes, ‘It’s the best place for the pastry shop in the neighborhood.’ The original slang and the dumpling reference have shifted.” |
| 1:15–1:32 | Zoom in on the row’s `similarity`, `meaning_loss`, and `risk` values; optionally show the formula in `src/scoring.py`. | “The normalized similarity is about 0.760. Meaning loss is one minus similarity, times 100, giving about 23.981. Under the project’s current thresholds, that is Medium risk. It’s an automated comparison signal, not a human judgment.” |
| 1:32–1:48 | Show `category_loss.png`, `language_comparison.png`, `heatmap.png`, and `risk_distribution.png` in sequence. | “These charts summarize the dataset. Slang has the highest average category loss at 9.294, while literal language has the lowest at 3.316. Swahili averages 8.105, compared with 5.316 for French.” |
| 1:48–2:00 | End on `risk_distribution.png` or the README results table. | “Overall, 94.8 percent of results are Low risk, 5.2 percent Medium, and none High under the current cutoffs. MeaningGuard’s findings are exploratory: the dataset is small, and the scores need human evaluation before they can be treated as validated risk assessments.” |

## Recording Notes

- Keep the CSV view wide enough to show the full sample row and column names.
- Use the already generated charts and saved results to keep the recording
  within two minutes.
- The sample is from the existing French slang results; exact translations
  can vary if the translation model is rerun with different software or model
  versions.
- The `similarity` displayed in the output is normalized to `[0, 1]`, and the
  displayed meaning loss is rounded here for narration.
