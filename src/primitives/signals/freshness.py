"""Freshness signal primitives.

Freshness represents recency: recently created/updated nodes are fresh,
old nodes are stale.
"""

from __future__ import annotations

import math
from datetime import datetime


def freshness_score(
    updated_at: datetime,
    now: datetime,
    half_life_days: float = 30.0,
) -> float:
    """Compute freshness score based on last update time.

    Args:
        updated_at: When the node was last updated
        now: Current timestamp
        half_life_days: Days until freshness halves

    Returns:
        Freshness in [0, 1] where 1 = just updated
    """
    age_days = (now - updated_at).total_seconds() / 86400
    if age_days < 0:
        return 1.0  # Future timestamp, treat as fresh

    decay_constant = math.log(2) / half_life_days
    return math.exp(-decay_constant * age_days)


def decay_weight(
    created_at: datetime,
    now: datetime,
    half_life_days: float = 30.0,
    floor: float = 0.1,
) -> float:
    """Compute retrieval weight decay for Memory-layer nodes.

    Memory-layer nodes (passages, events) decay over time. This weight
    is applied at retrieval to downrank old memories.

    Args:
        created_at: When the node was created
        now: Current timestamp
        half_life_days: Days until weight halves
        floor: Minimum weight (default 0.1)

    Returns:
        Weight in [floor, 1.0]
    """
    freshness = freshness_score(created_at, now, half_life_days)
    return max(freshness, floor)


def days_until_stale(
    updated_at: datetime,
    now: datetime,
    staleness_threshold: float = 0.1,
    half_life_days: float = 30.0,
) -> float:
    """Compute days until a node becomes stale.

    Args:
        updated_at: When the node was last updated
        now: Current timestamp
        staleness_threshold: Freshness below which node is stale
        half_life_days: Decay half-life

    Returns:
        Days until stale, or 0 if already stale
    """
    current_freshness = freshness_score(updated_at, now, half_life_days)
    if current_freshness <= staleness_threshold:
        return 0.0

    # Solve: threshold = exp(-k * t) for t
    # t = -ln(threshold) / k
    decay_constant = math.log(2) / half_life_days
    target_age = -math.log(staleness_threshold) / decay_constant

    current_age = (now - updated_at).total_seconds() / 86400
    return max(target_age - current_age, 0.0)
