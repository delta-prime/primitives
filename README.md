# primitives

EAG reference implementation — hot-swappable knowledge management primitives for AI agent context systems.

## What This Is

`primitives` is the open-source layer of the EAG (Epistemic Augmented Generation) architecture. It implements the pure, deterministic parts: epistemology math, scoring signals, schema definitions, and the protocol interfaces that the service layer depends on.

**Scope: what's in this library**

| Module | What it provides |
|--------|-----------------|
| `primitives.epistemology` | Confidence math, contradiction detection, promotion rules (R1/R2), corroboration, provenance invariant checks |
| `primitives.scoring` | Decay and freshness scoring formulas (Gaussian per-class decay) |
| `primitives.schema` | Node type definitions, `PersistenceLayer` enum, edge type catalogue |
| `primitives.protocols` | `KnowledgeStore`, `LifecycleManager`, `SignalProvider`, `ProvenanceTracker` interfaces |
| `primitives.shared` | Shared utilities across modules |
| `primitives.eag` | EAG-specific implementation of the protocols |

**Scope: what is NOT in this library (proprietary service layer)**

- Custodian workers — promotion, synthesis, revision scheduling
- Extraction prompts and LLM orchestration
- Heat-PPR scoring (ambient access-recency, Redis-backed)
- Graph + vector write paths and backend integrations
- Storage backends (Memgraph, Qdrant, Redis, Postgres)
- REST API and MCP interface
- Dagster pipelines and sensor logic

## EAG Paradigm

CAG splits knowledge persistence into four layers, each with distinct semantics:

| Layer | Semantics | Examples |
|-------|-----------|----------|
| Memory | Experiences that fade (Gaussian decay) | Passages, events, utterances |
| Knowledge | Facts that persist until contradicted | Claims, promoted Facts |
| Wisdom | Beliefs that revise on evidence shift | Patterns, Commitments |
| Intelligence | Ephemeral reasoning (session-scoped) | Reasoning chains |

All adjudication is deterministic — no LLM calls at decision time.

See `context/` for full paradigm documentation.

## Installation

```bash
pip install delta-prime-primitives
```

Or from source:

```bash
git clone https://github.com/delta-prime/primitives
cd primitives
pip install -e ".[dev]"
```

## Usage

### Epistemology

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

### Scoring

```python
from primitives.scoring import compute_effective_importance

# Gaussian decay — returns effective importance after age_days
importance = compute_effective_importance(
    base_importance=0.9,
    decay_rate=0.01,   # class-specific; ephemeral=0.1, standard=0.01, durable=0.002
    age_days=30.0,
)
```

Heat-PPR scores (ambient access-recency) are computed by the service layer and stored in Redis. They are not part of this library.

### Protocol injection

```python
from primitives.protocols import KnowledgeStore, Scope
from primitives.eag import EAGKnowledgeStore  # or your own implementation

# Inject at startup
store: KnowledgeStore = EAGKnowledgeStore(graph_client, vector_client)

# Product code uses the protocol interface only
result = await store.ingest(content, metadata, scope)
nodes = await store.query("what do we know about X?", scope)
```

### Swapping implementations

```python
# Current paradigm
from primitives.eag import EAGKnowledgeStore

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
