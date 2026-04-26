"""Epistemology primitives: confidence, promotion, supersession.

All functions here are pure and deterministic. No LLM calls happen
at adjudication time.
"""

from primitives.epistemology.confidence import (
    SourceTier,
    combined_confidence,
    noisy_or_aggregate,
)
from primitives.epistemology.promotion import (
    PromotionRule,
    should_promote_r1,
    should_promote_r2,
)
from primitives.epistemology.supersession import (
    ContradictionResult,
    detect_contradiction,
    should_supersede,
)

__all__ = [
    "SourceTier",
    "combined_confidence",
    "noisy_or_aggregate",
    "PromotionRule",
    "should_promote_r1",
    "should_promote_r2",
    "ContradictionResult",
    "detect_contradiction",
    "should_supersede",
]
