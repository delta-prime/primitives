"""Confidence computation primitives.

Pure functions for computing claim and aggregate confidence scores.
"""

from __future__ import annotations

from enum import StrEnum
from functools import reduce


class SourceTier(StrEnum):
    """Source credibility tiers with associated weights."""

    AUTHORITATIVE = "authoritative"  # 1.0
    VALIDATED = "validated"  # 0.85
    COMMUNITY = "community"  # 0.6
    UNKNOWN = "unknown"  # 0.4

    @property
    def weight(self) -> float:
        return _TIER_WEIGHTS[self]


_TIER_WEIGHTS: dict[SourceTier, float] = {
    SourceTier.AUTHORITATIVE: 1.0,
    SourceTier.VALIDATED: 0.85,
    SourceTier.COMMUNITY: 0.6,
    SourceTier.UNKNOWN: 0.4,
}


def combined_confidence(
    raw_confidence: float,
    source_tier: SourceTier,
    corroboration_factor: float = 1.0,
    method_weight: float = 1.0,
) -> float:
    """Compute combined confidence for a single claim.

    Formula: source_tier * corroboration_factor * method_weight * raw_confidence

    Args:
        raw_confidence: Base confidence from extraction (0.0 - 1.0)
        source_tier: Credibility tier of the source
        corroboration_factor: Boost from corroborating evidence (default 1.0)
        method_weight: Weight based on extraction method (default 1.0)

    Returns:
        Combined confidence score (0.0 - 1.0)
    """
    result = source_tier.weight * corroboration_factor * method_weight * raw_confidence
    return min(max(result, 0.0), 1.0)


def noisy_or_aggregate(confidences: list[float], cap: float = 0.99) -> float:
    """Aggregate multiple confidence scores using noisy-OR.

    Formula: 1 - product(1 - c_i) for each confidence c_i

    This models independent evidence: each source has a chance of being
    correct, and we want the probability that at least one is correct.

    Args:
        confidences: List of individual confidence scores
        cap: Maximum return value (default 0.99)

    Returns:
        Aggregated confidence score, capped at `cap`
    """
    if not confidences:
        return 0.0

    # 1 - product(1 - c_i)
    complement_product = reduce(lambda acc, c: acc * (1 - c), confidences, 1.0)
    result = 1 - complement_product

    return min(result, cap)


def incremental_noisy_or(
    current_aggregate: float,
    new_confidence: float,
    cap: float = 0.99,
) -> float:
    """Incrementally update a noisy-OR aggregate with a new confidence.

    Equivalent to recomputing from scratch but O(1) instead of O(n).

    Formula: 1 - (1 - current) * (1 - new)

    Args:
        current_aggregate: Existing aggregated confidence
        new_confidence: New confidence to incorporate
        cap: Maximum return value (default 0.99)

    Returns:
        Updated aggregated confidence
    """
    result = 1 - (1 - current_aggregate) * (1 - new_confidence)
    return min(result, cap)
