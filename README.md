# primitives

Hot-swappable knowledge management primitives for AI agent context systems.

## What This Is

A library of pure, deterministic primitives for building knowledge graphs that AI agents can read from and write to. Designed to be paradigm-agnostic: the product layer defines protocols (interfaces), this library implements them. Swap implementations without rewriting product code.

## Installation

```bash
pip install primitives
```

## Core Concepts

### Protocols

The library implements four core protocols (defined in your product repo):

- **KnowledgeStore**: Ingest, query, retrieve, delete
- **LifecycleManager**: Promote, supersede, decay
- **SignalProvider**: Heat, confidence, freshness, priority
- **ProvenanceTracker**: Derivation chains, citations

### Layers

Knowledge flows through four persistence layers:

| Layer | Semantics | Examples |
|-------|-----------|----------|
| Memory | Experiences that fade | Passages, events, utterances |
| Knowledge | Facts that persist until contradicted | Claims, facts |
| Wisdom | Beliefs that revise on evidence shift | Patterns, commitments |
| Intelligence | Ephemeral reasoning | Reasoning chains |

### Epistemology

All adjudication is deterministic. No LLM calls at decision time.

```python
from primitives.epistemology import (
    combined_confidence,
    noisy_or_aggregate,
    should_promote_r1,
    should_promote_r2,
    detect_contradiction,
    should_supersede,
)

# Per-claim confidence
cc = combined_confidence(
    raw_confidence=0.85,
    source_tier=SourceTier.AUTHORITATIVE,
)

# Aggregate across claims
aggregate = noisy_or_aggregate([0.7, 0.6, 0.5])  # -> 0.94

# Promotion decision
decision = should_promote_r2(claims)
if decision.should_promote:
    # Promote to Fact
    ...
```

### Signals

```python
from primitives.signals import heat_score, freshness_score, priority_score

heat = heat_score(retrieval_events, now)
fresh = freshness_score(updated_at, now)
priority = priority_score(heat, fresh, confidence, age_days)
```

## Usage

```python
from primitives.protocols import KnowledgeStore, Scope
from primitives.cag import CAGKnowledgeStore  # or your implementation

# Inject at startup
store: KnowledgeStore = CAGKnowledgeStore(graph_client, vector_client)

# Product code uses protocols only
result = await store.ingest(content, metadata, scope)
nodes = await store.query("what do we know about X?", scope)
```

## Swapping Implementations

```python
# Current paradigm
from primitives.cag import CAGKnowledgeStore

# Future paradigm (same interface)
from primitives.newparadigm import NewKnowledgeStore

# Product code unchanged
store = NewKnowledgeStore(graph_client, vector_client)
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type check
mypy src/primitives

# Lint
ruff check src/primitives
```

## License

MIT
