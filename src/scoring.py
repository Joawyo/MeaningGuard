"""Meaning-loss scoring utilities for MeaningGuard."""


def meaning_loss(similarity: float) -> float:
    """Convert cosine similarity to a meaning-loss score from 0 to 200.

    Cosine similarity is expected to be in the range [-1, 1]. A similarity of
    1 indicates no measured loss, while lower similarity yields a higher score.
    """
    if not isinstance(similarity, (int, float)) or isinstance(similarity, bool):
        raise TypeError("similarity must be a number")
    if not -1 <= similarity <= 1:
        raise ValueError("similarity must be between -1 and 1")

    return (1 - similarity) * 100


def risk_level(score: float) -> str:
    """Map a meaning-loss score to Low, Medium, or High risk.

    Scores below 20 are Low, scores from 20 up to (but not including) 40
    are Medium, and scores of 40 or higher are High.
    """
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise TypeError("score must be a number")
    if score < 0:
        raise ValueError("score must not be negative")

    if score < 20:
        return "Low"
    if score < 40:
        return "Medium"
    return "High"


__all__ = ["meaning_loss", "risk_level"]
