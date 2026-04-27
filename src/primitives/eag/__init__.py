"""EAG (Epistemic Augmented Generation) implementation.

Four-layer cognitive architecture: Memory -> Knowledge -> Wisdom -> Intelligence.
Implements the protocol interfaces with EAG-specific semantics.
"""

# Epistemology exports
from primitives.eag.epistemology import (
    ClaimForPromotion,
    ContradictionResult,
    PromotionDecision,
    PromotionRule,
    SourceTier,
    SupersessionDecision,
    combined_confidence,
    detect_contradiction,
    incremental_noisy_or,
    noisy_or_aggregate,
    should_promote_r1,
    should_promote_r2,
    should_supersede,
)

# Store/lifecycle implementations will be added here
# from primitives.eag.store import EAGKnowledgeStore
# from primitives.eag.lifecycle import EAGLifecycleManager

__all__ = [
    # Epistemology
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
    "detect_contradiction",
    "should_supersede",
    "SupersessionDecision",
    # Implementations (TODO)
    # "EAGKnowledgeStore",
    # "EAGLifecycleManager",
]
