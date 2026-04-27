"""EAG lifecycle manager: promotion, contradiction, supersession, decay."""

from __future__ import annotations

from abc import abstractmethod
from typing import Any

from primitives.eag.epistemology import (
    ClaimForPromotion,
    FactForSupersession,
    detect_contradiction,
    should_promote_r1,
    should_promote_r2,
)
from primitives.protocols import (
    DecayResult,
    KnowledgeNode,
    PromoteResult,
    Scope,
    SupersedeResult,
)


class EAGLifecycleManager:
    """EAG implementation of lifecycle transitions.

    should_promote and detect_contradiction are pure, synchronous predicates
    backed by the epistemology module. promote/supersede/decay are abstract
    because they require a storage backend.
    """

    def should_promote(self, node: KnowledgeNode) -> tuple[bool, str]:
        """Return (should_promote, reason) without mutating state.

        Tries R1 first (single authoritative source); falls back to R2
        (multi-source corroboration) when additional claim metadata is present
        in node.metadata["claims"].
        """
        raw_confidence: float = node.metadata.get("raw_confidence", node.confidence)
        source_tier_value: str = node.metadata.get("source_tier", "")

        from primitives.eag.epistemology.confidence import SourceTier

        try:
            source_tier = SourceTier(source_tier_value)
        except ValueError:
            source_tier = SourceTier.UNKNOWN

        single_claim = ClaimForPromotion(
            fingerprint=node.metadata.get("fingerprint", node.id),
            combined_confidence=node.confidence,
            source_tier=source_tier,
            raw_confidence=raw_confidence,
        )

        r1 = should_promote_r1(single_claim)
        if r1.should_promote:
            return True, r1.reason

        raw_claims: list[dict[str, Any]] = node.metadata.get("claims", [])
        if len(raw_claims) >= 2:
            claims = [
                ClaimForPromotion(
                    fingerprint=c.get("fingerprint", node.id),
                    combined_confidence=c.get("combined_confidence", 0.0),
                    source_tier=SourceTier(str(c.get("source_tier", SourceTier.UNKNOWN))),
                    raw_confidence=c.get("raw_confidence", 0.0),
                )
                for c in raw_claims
            ]
            r2 = should_promote_r2(claims)
            if r2.should_promote:
                return True, r2.reason
            return False, r2.reason

        return False, r1.reason

    def detect_contradiction(
        self, node_a: KnowledgeNode, node_b: KnowledgeNode
    ) -> tuple[bool, str | None]:
        """Return (contradicts, explanation) without mutating state."""
        fact_a = FactForSupersession(
            id=node_a.id,
            subject_id=node_a.metadata.get("subject_id", node_a.id),
            predicate=node_a.metadata.get("predicate", ""),
            object_id=node_a.metadata.get("object_id"),
            object_literal=node_a.metadata.get("object_literal", node_a.content),
            confidence=node_a.confidence,
        )
        fact_b = FactForSupersession(
            id=node_b.id,
            subject_id=node_b.metadata.get("subject_id", node_b.id),
            predicate=node_b.metadata.get("predicate", ""),
            object_id=node_b.metadata.get("object_id"),
            object_literal=node_b.metadata.get("object_literal", node_b.content),
            confidence=node_b.confidence,
        )

        contradicts = detect_contradiction(fact_a, fact_b)
        if contradicts:
            return True, (
                f"Nodes {node_a.id!r} and {node_b.id!r} share "
                f"(subject={fact_a.subject_id!r}, predicate={fact_a.predicate!r}) "
                "but differ on object"
            )
        return False, None

    @abstractmethod
    async def promote(self, node_id: str, scope: Scope) -> PromoteResult:
        """Promote node to the next layer. Requires a storage backend."""
        ...

    @abstractmethod
    async def supersede(
        self,
        old_id: str,
        new_id: str,
        reason: str,
        scope: Scope,
    ) -> SupersedeResult:
        """Mark old_id as superseded by new_id. Requires a storage backend."""
        ...

    @abstractmethod
    async def decay(self, scope: Scope, threshold: float) -> DecayResult:
        """Apply decay to nodes below threshold. Requires a storage backend."""
        ...
