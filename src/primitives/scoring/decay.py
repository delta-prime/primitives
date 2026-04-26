"""Decay scoring for context importance."""

from __future__ import annotations

import math


def compute_effective_importance(
    base_importance: float,
    decay_rate: float,
    age_days: float,
    pinned: bool = False,
) -> float:
    """Compute effective importance with exponential decay.

    Args:
        base_importance: Initial importance score (0.0 to 1.0)
        decay_rate: Decay constant (higher = faster decay)
        age_days: Age of the content in days
        pinned: If True, bypass decay entirely

    Returns:
        Decayed importance score
    """
    if pinned:
        return base_importance
    return base_importance * math.exp(-decay_rate * age_days)
