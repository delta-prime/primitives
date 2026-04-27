"""CAG edge types organized by function."""

from __future__ import annotations

from enum import StrEnum


class CAGEdgeType(StrEnum):
    """All CAG edge types."""

    # Provenance edges (transition outputs)
    DERIVED_FROM = "DERIVED_FROM"
    EXTRACTED_FROM = "EXTRACTED_FROM"
    SUPERSEDES = "SUPERSEDES"
    SYNTHESIZED_FROM = "SYNTHESIZED_FROM"
    PROMOTED_FROM = "PROMOTED_FROM"
    CRYSTALLIZED_INTO = "CRYSTALLIZED_INTO"
    DECLARED_BY = "DECLARED_BY"

    # Semantic structure edges
    MENTIONS = "MENTIONS"
    USES_PREDICATE = "USES_PREDICATE"
    CAUSES = "CAUSES"
    CORROBORATES = "CORROBORATES"
    REFERENCES = "REFERENCES"

    # Clustering edges
    MEMBER_OF = "MEMBER_OF"
    COVERS = "COVERS"


# Edge sets by function
PROVENANCE_EDGES: frozenset[str] = frozenset({
    CAGEdgeType.DERIVED_FROM,
    CAGEdgeType.EXTRACTED_FROM,
    CAGEdgeType.SUPERSEDES,
    CAGEdgeType.SYNTHESIZED_FROM,
    CAGEdgeType.PROMOTED_FROM,
    CAGEdgeType.CRYSTALLIZED_INTO,
    CAGEdgeType.DECLARED_BY,
})

SEMANTIC_EDGES: frozenset[str] = frozenset({
    CAGEdgeType.MENTIONS,
    CAGEdgeType.USES_PREDICATE,
    CAGEdgeType.CAUSES,
    CAGEdgeType.CORROBORATES,
    CAGEdgeType.REFERENCES,
})

CLUSTERING_EDGES: frozenset[str] = frozenset({
    CAGEdgeType.MEMBER_OF,
    CAGEdgeType.COVERS,
})

ALL_CAG_EDGES: frozenset[str] = PROVENANCE_EDGES | SEMANTIC_EDGES | CLUSTERING_EDGES
