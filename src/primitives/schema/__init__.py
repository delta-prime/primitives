"""Schema primitives: node types, edge types, layers."""

from primitives.protocols import Layer

__all__ = ["Layer", "NodeType", "EdgeType"]


class NodeType:
    """Node type constants."""

    # Memory layer
    DOCUMENT = "Document"
    PASSAGE = "Passage"
    UTTERANCE = "Utterance"
    EVENT = "Event"

    # Knowledge layer
    CLAIM = "Claim"
    FACT = "Fact"

    # Wisdom layer
    BELIEF = "Belief"
    PATTERN = "Pattern"
    COMMITMENT = "Commitment"

    # Intelligence layer
    REASONING_CHAIN = "ReasoningChain"
    QUERY_CONTEXT = "QueryContext"

    # Registry
    ENTITY = "Entity"
    PREDICATE = "Predicate"
    AGENT = "Agent"


class EdgeType:
    """Edge type constants."""

    # Provenance
    DERIVED_FROM = "DERIVED_FROM"
    CITES = "CITES"
    SUPERSEDES = "SUPERSEDES"
    PROMOTED_FROM = "PROMOTED_FROM"
    CRYSTALLIZED_INTO = "CRYSTALLIZED_INTO"

    # Structure
    MEMBER_OF = "MEMBER_OF"
    PART_OF = "PART_OF"
    BELONGS_TO = "BELONGS_TO"

    # Entity resolution
    MENTIONS = "MENTIONS"
    USES_PREDICATE = "USES_PREDICATE"

    # Synthesis
    SYNTHESIZED_FROM = "SYNTHESIZED_FROM"
    COVERS = "COVERS"

    # Agent
    DECLARED_BY = "DECLARED_BY"
