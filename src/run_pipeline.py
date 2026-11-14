"""Run MeaningGuard English round-trip experiments for French and Swahili."""

from pathlib import Path
from typing import Any, Callable, List, Tuple

import pandas as pd

try:
    # Support importing this module as part of the src package.
    from .scoring import meaning_loss, risk_level
    from .similarity import load_similarity_model, semantic_similarity
    from .translate import (
        english_to_french,
        french_to_english,
        english_to_swahili,
        swahili_to_english,
    )
except ImportError:
    # Support running it directly with `python src/run_pipeline.py`.
    from scoring import meaning_loss, risk_level
    from similarity import load_similarity_model, semantic_similarity
    from translate import (
        english_to_french,
        french_to_english,
        english_to_swahili,
        swahili_to_english,
    )


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "meaningguard_dataset.csv"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTPUT_COLUMNS = [
    "id",
    "category",
    "language",
    "original_text",
    "translated_text",
    "back_translation",
    "similarity",
    "meaning_loss",
    "risk",
]


# Run one English-to-target-language round trip and save its scored rows.
def run_experiment(
    language: str,
    translate_to: Callable[[str], str],
    translate_back: Callable[[str], str],
    model: Any,
    input_path: Path = INPUT_PATH,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Translate, score, and save one language experiment's results."""
    input_path = Path(input_path)
    if output_path is None:
        output_path = RESULTS_DIR / f"{language.lower()}_results.csv"
    output_path = Path(output_path)

    dataset = pd.read_csv(input_path)
    required_columns = {"id", "category", "english_text"}
    missing_columns = required_columns.difference(dataset.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input CSV is missing required columns: {missing}")

    results: List[Tuple[object, str, str, str, str, str, float, float, str]] = []
    for row in dataset.itertuples(index=False):
        original_text = row.english_text
        if pd.isna(original_text):
            raise ValueError(f"Dataset row with id {row.id!r} has no english_text")
        original_text = str(original_text)

        translated_text = translate_to(original_text)
        back_translation = translate_back(translated_text)
        similarity = semantic_similarity(original_text, back_translation, model)
        loss = meaning_loss(similarity)
        risk = risk_level(loss)

        results.append(
            (
                row.id,
                row.category,
                language,
                original_text,
                translated_text,
                back_translation,
                similarity,
                loss,
                risk,
            )
        )

    results_df = pd.DataFrame(results, columns=OUTPUT_COLUMNS)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    return results_df


# Run both language experiments, write their separate CSVs, and combine the results.
def run_pipeline(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    """Create French, Swahili, and combined result CSV files."""
    input_path = Path(input_path)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    model = load_similarity_model()

    french_results = run_experiment(
        language="French",
        translate_to=english_to_french,
        translate_back=french_to_english,
        model=model,
        input_path=input_path,
        output_path=RESULTS_DIR / "french_results.csv",
    )
    swahili_results = run_experiment(
        language="Swahili",
        translate_to=english_to_swahili,
        translate_back=swahili_to_english,
        model=model,
        input_path=input_path,
        output_path=RESULTS_DIR / "swahili_results.csv",
    )

    # Keep the combined CSV's schema and column order consistent with each language CSV.
    final_results = pd.concat(
        [french_results, swahili_results], ignore_index=True
    ).reindex(columns=OUTPUT_COLUMNS)
    final_path = RESULTS_DIR / "final_results.csv"
    final_results.to_csv(final_path, index=False)
    return final_results


# Run both experiments when invoked as a script and report the output files.
if __name__ == "__main__":
    results = run_pipeline()
    print(f"Processed {len(results)} rows across French and Swahili experiments.")
    print(f"French results: {RESULTS_DIR / 'french_results.csv'}")
    print(f"Swahili results: {RESULTS_DIR / 'swahili_results.csv'}")
    print(f"Combined results: {RESULTS_DIR / 'final_results.csv'}")
