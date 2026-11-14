"""Run the MeaningGuard English-French round-trip evaluation pipeline."""

from pathlib import Path
from typing import List, Tuple

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

try:
    # Support importing this module as part of the src package.
    from .scoring import meaning_loss, risk_level
    from .translate import english_to_french, french_to_english
except ImportError:
    # Support running it directly with `python src/run_pipeline.py`.
    from scoring import meaning_loss, risk_level
    from translate import english_to_french, french_to_english


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "meaningguard_dataset.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "french_results.csv"
SIMILARITY_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# Load a multilingual sentence-embedding model once for all similarity comparisons.
def load_similarity_model() -> SentenceTransformer:
    """Load and return the multilingual model used to embed sentences."""
    return SentenceTransformer(SIMILARITY_MODEL_NAME)


# Embed the original and back-translated sentences and compare their vectors.
def semantic_similarity(
    original_text: str, back_translation: str, model: SentenceTransformer
) -> float:
    """Return cosine similarity between two sentences' multilingual embeddings."""
    embeddings = model.encode(
        [original_text, back_translation],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    return float(cosine_similarity(embeddings[0:1], embeddings[1:2])[0, 0])


# Execute the English -> French -> English workflow for every dataset row.
def run_pipeline(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
) -> pd.DataFrame:
    """Translate, score, and save the dataset; return the results DataFrame."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    dataset = pd.read_csv(input_path)

    required_columns = {"id", "category", "english_text"}
    missing_columns = required_columns.difference(dataset.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Input CSV is missing required columns: {missing}")

    model = load_similarity_model()
    results: List[Tuple[object, str, str, str, str, float, float, str]] = []

    for row in dataset.itertuples(index=False):
        original_text = getattr(row, "english_text")
        if pd.isna(original_text):
            raise ValueError(f"Dataset row with id {row.id!r} has no english_text")
        original_text = str(original_text)

        translated_text = english_to_french(original_text)
        back_translation = french_to_english(translated_text)
        similarity = semantic_similarity(original_text, back_translation, model)
        loss = meaning_loss(similarity)
        risk = risk_level(loss)

        results.append(
            (
                row.id,
                row.category,
                original_text,
                translated_text,
                back_translation,
                similarity,
                loss,
                risk,
            )
        )

    output_columns = [
        "id",
        "category",
        "original_text",
        "translated_text",
        "back_translation",
        "similarity",
        "meaning_loss",
        "risk",
    ]
    results_df = pd.DataFrame(results, columns=output_columns)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    return results_df


# Run the workflow when invoked as a script and report the output location.
if __name__ == "__main__":
    results = run_pipeline()
    print(f"Processed {len(results)} rows. Results saved to {OUTPUT_PATH}")
