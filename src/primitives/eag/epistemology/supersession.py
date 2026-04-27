"""Supersession primitives.

Pure functions for detecting contradictions and determining supersession.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ContradictionResult(StrEnum):
    """Possible outcomes of contradiction detection."""

    NO_CONTRADICTION = "no_contradiction"
    NEW_SUPERSEDES_OLD = "new_supersedes_old"
    OLD_SUPERSEDES_NEW = "old_supersedes_new"
    UNRESOLVED = "unresolved"  # Neither dominates


@dataclass
class FactForSupersession:
    """Minimal fact data needed for supersession decision."""

    id: str
    subject_id: str
    predicate: str
    object_id: str | None
    object_literal: str | None
    confidence: float


@dataclass
class SupersessionDecision:
    """Result of supersession evaluation."""

    result: ContradictionResult
    winner_id: str | None = None
    loser_id: str | None = None
    reason: str | None = None


def detect_contradiction(
    fact_a: FactForSupersession,
    fact_b: FactForSupersession,
) -> bool:
    """Detect if two facts contradict each other.

    Contradiction: same (subject_id, predicate) but different object.

    Args:
        fact_a: First fact
        fact_b: Second fact

    Returns:
        True if the facts contradict
    """
    if fact_a.subject_id != fact_b.subject_id:
        return False

    if fact_a.predicate != fact_b.predicate:
        return False

    # Same subject and predicate - check if objects differ
    a_object = fact_a.object_id or fact_a.object_literal
    b_object = fact_b.object_id or fact_b.object_literal

    return a_object != b_object


def should_supersede(
    existing: FactForSupersession,
    incoming: FactForSupersession,
    dominance_threshold: float = 1.2,
) -> SupersessionDecision:
    """Determine if one fact should supersede another.

    Rules:
    - If incoming.confidence >= threshold * existing.confidence: incoming wins
    - If existing.confidence >= threshold * incoming.confidence: existing wins
    - Otherwise: unresolved contradiction, both remain

    Args:
        existing: The existing fact in the graph
        incoming: The new fact being promoted
        dominance_threshold: Confidence ratio required to supersede (default 1.2)

    Returns:
        SupersessionDecision with winner/loser or unresolved status
    """
    if not detect_contradiction(existing, incoming):
        return SupersessionDecision(
            result=ContradictionResult.NO_CONTRADICTION,
            reason="Facts do not contradict (different subject or predicate)",
        )

    incoming_dominates = incoming.confidence >= dominance_threshold * existing.confidence
    existing_dominates = existing.confidence >= dominance_threshold * incoming.confidence

    if incoming_dominates:
        return SupersessionDecision(
            result=ContradictionResult.NEW_SUPERSEDES_OLD,
            winner_id=incoming.id,
            loser_id=existing.id,
            reason=f"Incoming confidence {incoming.confidence:.2f} >= {dominance_threshold}x existing {existing.confidence:.2f}",
        )

    if existing_dominates:
        return SupersessionDecision(
            result=ContradictionResult.OLD_SUPERSEDES_NEW,
            winner_id=existing.id,
            loser_id=incoming.id,
            reason=f"Existing confidence {existing.confidence:.2f} >= {dominance_threshold}x incoming {incoming.confidence:.2f}",
        )

    return SupersessionDecision(
        result=ContradictionResult.UNRESOLVED,
        reason=f"Neither dominates: existing={existing.confidence:.2f}, incoming={incoming.confidence:.2f}, threshold={dominance_threshold}x",
    )
