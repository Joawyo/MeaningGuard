"""Semantic similarity helpers for MeaningGuard."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


# Use the same multilingual embedding model previously configured in the pipeline.
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# Cache the model so it is loaded once and reused for all sentence comparisons.
@lru_cache(maxsize=1)
def load_similarity_model() -> SentenceTransformer:
    """Load and return the project's multilingual sentence embedding model."""
    return SentenceTransformer(MODEL_NAME)


# Embed two sentences and calculate cosine similarity from their normalized vectors.
def semantic_similarity(
    sentence_a: str,
    sentence_b: str,
    model: SentenceTransformer | None = None,
) -> float:
    """Return cosine similarity in the range [-1, 1] for two sentences."""
    if not isinstance(sentence_a, str) or not isinstance(sentence_b, str):
        raise TypeError("Both sentences must be strings")
    if not sentence_a.strip() or not sentence_b.strip():
        raise ValueError("Both sentences must contain non-whitespace text")

    if model is None:
        model = load_similarity_model()

    embeddings = model.encode(
        [sentence_a, sentence_b],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    cosine_score = float(np.dot(embeddings[0], embeddings[1]))
    # Clamp floating-point noise while preserving the full cosine range.
    return max(-1.0, min(1.0, cosine_score))


# Provide an alternate descriptive name for callers that prefer it.
calculate_similarity = semantic_similarity


__all__ = [
    "MODEL_NAME",
    "load_similarity_model",
    "semantic_similarity",
    "calculate_similarity",
]
