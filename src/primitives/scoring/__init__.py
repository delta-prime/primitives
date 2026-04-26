"""Scoring primitives: decay, freshness, and priority calculations."""

from primitives.scoring.decay import compute_effective_importance

__all__ = [
    "compute_effective_importance",
]
