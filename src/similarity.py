"""Semantic similarity helpers for MeaningGuard."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


# Keep the embedding model consistent with the one previously used in run_pipeline.py.
MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


# Load one shared model instance so repeated comparisons avoid reloading weights.
@lru_cache(maxsize=1)
def load_similarity_model() -> SentenceTransformer:
    """Load and return the project's multilingual sentence embedding model."""
    return SentenceTransformer(MODEL_NAME)


# Encode two sentences and calculate cosine similarity from their embeddings.
def semantic_similarity(
    sentence_a: str,
    sentence_b: str,
    model: SentenceTransformer | None = None,
) -> float:
    """Return cosine similarity in the range [0, 1] for two sentences.

    Similarity is computed from normalized sentence embeddings. Since cosine
    similarity can be negative, the result is clamped to [0, 1] as requested.
    """
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
    return max(0.0, min(1.0, cosine_score))


# Provide a descriptive alias for callers that prefer an explicit function name.
calculate_similarity = semantic_similarity


__all__ = ["MODEL_NAME", "load_similarity_model", "semantic_similarity", "calculate_similarity"]
