"""Priority signal primitives.

Priority is the composite signal used for work ordering: which nodes
should the Custodian visit next?
"""

from __future__ import annotations

import math
from datetime import datetime


def priority_score(
    heat: float,
    freshness: float,
    confidence: float,
    age_days: float,
) -> float:
    """Compute priority score for work ordering.

    Formula: heat * (1 - freshness) * (1 - confidence) * age_boost

    Interpretation:
    - Hot nodes rise (frequently used = worth maintaining)
    - Stale nodes rise (not recently visited = may need update)
    - Low-confidence nodes rise (uncertain = worth re-evaluating)
    - Older nodes get a boost (logarithmic age factor)

    Args:
        heat: Heat score in [0, 1]
        freshness: Freshness score in [0, 1]
        confidence: Confidence score in [0, 1]
        age_days: Age of node in days

    Returns:
        Priority score (unbounded, higher = process sooner)
    """
    staleness = 1 - freshness
    uncertainty = 1 - confidence
    age_boost = math.log(age_days + 1) + 1  # +1 so new nodes aren't zeroed

    return heat * staleness * uncertainty * age_boost


def priority_from_node(
    heat: float,
    updated_at: datetime,
    confidence: float,
    created_at: datetime,
    now: datetime,
    freshness_half_life: float = 30.0,
) -> float:
    """Convenience wrapper computing priority from node data.

    Args:
        heat: Pre-computed heat score
        updated_at: When node was last updated
        confidence: Node confidence score
        created_at: When node was created
        now: Current timestamp
        freshness_half_life: Half-life for freshness decay

    Returns:
        Priority score
    """
    from primitives.signals.freshness import freshness_score

    freshness = freshness_score(updated_at, now, freshness_half_life)
    age_days = (now - created_at).total_seconds() / 86400

    return priority_score(heat, freshness, confidence, age_days)
