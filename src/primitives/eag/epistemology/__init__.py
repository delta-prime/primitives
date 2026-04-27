"""Epistemology primitives: confidence, promotion, supersession.

All functions here are pure and deterministic. No LLM calls happen
at adjudication time.
"""

from primitives.eag.epistemology.confidence import (
    SourceTier,
    combined_confidence,
    incremental_noisy_or,
    noisy_or_aggregate,
)
from primitives.eag.epistemology.promotion import (
    ClaimForPromotion,
    PromotionDecision,
    PromotionRule,
    should_promote_r1,
    should_promote_r2,
)
from primitives.eag.epistemology.supersession import (
    ContradictionResult,
    FactForSupersession,
    SupersessionDecision,
    detect_contradiction,
    should_supersede,
)

__all__ = [
    "SourceTier",
    "combined_confidence",
    "noisy_or_aggregate",
    "incremental_noisy_or",
    "PromotionRule",
    "ClaimForPromotion",
    "PromotionDecision",
    "should_promote_r1",
    "should_promote_r2",
    "ContradictionResult",
    "FactForSupersession",
    "SupersessionDecision",
    "detect_contradiction",
    "should_supersede",
]
