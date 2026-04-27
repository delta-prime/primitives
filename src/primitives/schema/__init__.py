"""CITE schema definitions: node labels, edge types, layer taxonomy.

Single source of truth for graph structure. Import from here, not string literals.
"""

from primitives.schema.edges import (
    ALL_CITE_EDGES,
    CLUSTERING_EDGES,
    PROVENANCE_EDGES,
    SEMANTIC_EDGES,
    CITEEdgeType,
)
from primitives.schema.labels import (
    ALL_CITE_LABELS,
    AUDIT_LABELS,
    CONTENT_LABELS,
    INTELLIGENCE_LABELS,
    KNOWLEDGE_LABELS,
    MEMORY_LABELS,
    REGISTRY_LABELS,
    WISDOM_LABELS,
    AuditLabel,
    IntelligenceLabel,
    KnowledgeLabel,
    MemoryLabel,
    PersistenceLayer,
    RegistryLabel,
    WisdomLabel,
    layer_for_label,
)

__all__ = [
    # Edges
    "CITEEdgeType",
    "PROVENANCE_EDGES",
    "SEMANTIC_EDGES",
    "CLUSTERING_EDGES",
    "ALL_CITE_EDGES",
    # Layers
    "PersistenceLayer",
    # Labels by layer
    "MemoryLabel",
    "KnowledgeLabel",
    "WisdomLabel",
    "IntelligenceLabel",
    "RegistryLabel",
    "AuditLabel",
    # Label sets
    "MEMORY_LABELS",
    "KNOWLEDGE_LABELS",
    "WISDOM_LABELS",
    "INTELLIGENCE_LABELS",
    "REGISTRY_LABELS",
    "AUDIT_LABELS",
    "ALL_CITE_LABELS",
    "CONTENT_LABELS",
    # Utilities
    "layer_for_label",
]
