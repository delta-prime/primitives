"""Heat signal primitives.

Heat represents usage-based temperature: frequently retrieved nodes are hot,
rarely retrieved nodes are cold.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class RetrievalEvent:
    """A single retrieval event for heat computation."""

    timestamp: datetime
    weight: float = 1.0  # Can weight by query importance


def heat_score(
    events: list[RetrievalEvent],
    now: datetime,
    half_life_days: float = 7.0,
    cap: float = 1.0,
) -> float:
    """Compute heat score from retrieval events.

    Uses exponential decay: recent retrievals contribute more than old ones.

    Args:
        events: List of retrieval events
        now: Current timestamp
        half_life_days: Days until a retrieval's contribution halves
        cap: Maximum heat score (default 1.0)

    Returns:
        Heat score in [0, cap]
    """
    if not events:
        return 0.0

    decay_constant = math.log(2) / half_life_days
    total = 0.0

    for event in events:
        age_days = (now - event.timestamp).total_seconds() / 86400
        if age_days < 0:
            continue  # Future event, ignore
        contribution = event.weight * math.exp(-decay_constant * age_days)
        total += contribution

    # Normalize: at half_life_days with 1 event/day, heat approaches ~1.44
    # Scale so that steady-state with 1 event/day = 1.0
    normalized = total / (1 / decay_constant)

    return min(normalized, cap)


def heat_from_count(
    retrieval_count: int,
    last_retrieved_at: datetime | None,
    now: datetime,
    half_life_days: float = 7.0,
) -> float:
    """Simplified heat from count + last retrieval time.

    Use when full event history isn't available.

    Args:
        retrieval_count: Total retrieval count
        last_retrieved_at: Timestamp of most recent retrieval
        now: Current timestamp
        half_life_days: Decay half-life

    Returns:
        Approximate heat score in [0, 1]
    """
    if retrieval_count == 0 or last_retrieved_at is None:
        return 0.0

    age_days = (now - last_retrieved_at).total_seconds() / 86400
    if age_days < 0:
        age_days = 0

    decay_constant = math.log(2) / half_life_days
    recency_factor = math.exp(-decay_constant * age_days)

    # Log scale for count, capped contribution
    count_factor = min(math.log(retrieval_count + 1) / math.log(100), 1.0)

    return recency_factor * count_factor
