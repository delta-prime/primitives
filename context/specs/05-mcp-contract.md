# 05 — MCP Contract

> The agent-facing interface to the EAG architecture.

## Design Philosophy

The MCP surface uses **intent-based verbs** that reflect agent cognition, not system internals:

| Agent thinks | Agent says | System does |
|--------------|------------|-------------|
| "I observed this" | `remember` | Write to Memory |
| "I believe this is true" | `assert` | Write Claim to Knowledge |
| "I commit to this stance" | `commit` | Write Commitment to Wisdom |
| "I notice something about my thinking" | `reflect` | Write MetaObservation |

Agents speak in **intent**; the system handles **mechanics** (transitions, promotion, supersession).

## Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| Write (intent verbs) | `remember`, `assert`, `commit`, `reflect`, `link` | Create nodes/edges |
| Read | `query`, `get`, `graph` | Retrieve with filtering |
| Meta-memory | `provenance`, `history` | Introspect epistemic state |
| Intelligence | `reason` | Store reasoning chains |
| Silo | `silo_create`, `silo_list` | Tenancy management |

## Evidence Requirements

**Principle:** Knowledge-layer assertions require grounded evidence. Agents cannot hallucinate sources.

| Layer | Evidence required? | Grounding mechanism |
|-------|-------------------|---------------------|
| Memory | No | Memories ARE grounding |
| Knowledge | Yes | `DERIVED_FROM` edge to Memory node or validated URI |
| Wisdom | No | Derives from Knowledge via synthesis |
| Intelligence | No | Session-scoped, ephemeral |

### Evidence Formats

```
node:<uuid>     — Reference to existing Memory-layer node
https://...     — External URI (validated via evidence pipeline)
file://...      — Local file URI (for ingested sources)
```

### Source Types

| Type | Meaning |
|------|---------|
| `document` | Derived from ingested document/passage |
| `user` | Derived from user utterance |
| `external` | Derived from external URI |
| `agent` | Derived from agent's own reasoning chain |

## Agent Attribution

- **Implicit from auth** — The calling agent's identity is captured automatically
- **`observed_from`** — Optional override when reporting what others said
- **`DECLARED_BY`** — Commitments and reflections link to declaring agent

## Concurrency Model

Race conditions are resolved through:

1. **Deterministic IDs** — Content-based hashing (no timestamps in IDs)
2. **MERGE semantics** — Idempotent writes
3. **Agent-scoped nodes** — Commitments/reflections are per-agent, no conflict
4. **Custodian reconciliation** — Conflicting claims coexist until T2 supersession

## Core Tool Signatures

### context_remember

```
remember(silo_id, content, content_type?, metadata?, tags?, decay_class?, observed_from?)
  -> {node_id, layer: "memory", decay_class, created_at}
```

Decay classes: `ephemeral` (7d), `standard` (90d), `durable` (540d), `permanent` (5y)

### context_assert

```
assert(silo_id, claim, evidence, source_type, confidence?, metadata?, tags?, evidence_mode?)
  -> {node_id, layer: "knowledge", claim_type, evidence_status, evidence_nodes, created_at}
```

`claim` can be freeform string or structured SPO:
```
{subject: str, predicate: str, object: str, qualifiers?: dict}
```

`evidence_mode`:
- `sync` — Validate before accepting (default)
- `async` — Accept optimistically, validate in background

### context_commit

```
commit(silo_id, belief, about, confidence?, reasoning?, metadata?, tags?)
  -> {node_id, layer: "wisdom", declared_by, about_nodes, created_at}
```

`about` references the Knowledge-layer nodes this belief concerns.

### context_reflect

```
reflect(silo_id, observation, observation_type, about, confidence?, metadata?)
  -> {node_id, observation_type, about_nodes, created_at}
```

Observation types: `belief_change`, `confidence_shift`, `contradiction`, `uncertainty`, `correction`, `insight`

### context_query

```
query(silo_id, query, layers?, filters?, top_k?, include_superseded?, as_of?)
  -> {results, total_candidates, search_time_ms}
```

`as_of` enables time-travel queries.

### context_provenance

```
provenance(silo_id, node_id, max_depth?)
  -> {chain: [{node_id, layer, relationship, confidence}], root_sources}
```

Traces citation chain to Memory-layer sources.

### context_history

```
history(silo_id, subject?, node_id?)
  -> {timeline: [{node_id, content, valid_from, valid_to, superseded_by, reason, confidence}], current}
```

Shows belief/fact evolution via SUPERSEDES chain.

### context_reason

```
reason(silo_id, steps, conclusion?, evidence_used?, crystallizations?)
  -> {chain_id, layer: "intelligence", steps_count, crystallizations_queued, session_id}
```

Stores reasoning chains. Crystallizations queue claims for assertion.

## Relationship to Transitions

| MCP verb | Primary layer | Related transitions |
|----------|---------------|---------------------|
| `remember` | Memory | T8 (decay), T9 (hard-delete) |
| `assert` | Knowledge | T1 (extract from), T2 (supersede), T5 (promote to) |
| `commit` | Wisdom | T7 (commit) |
| `reflect` | Meta | (none — meta-observations don't transition) |
| `reason` | Intelligence | T5 (consensus), T6 (trace) |

The Custodian handles transitions; agents express intent through MCP verbs.

## Evidence Pipeline (Service Layer)

The context-service implements evidence validation:

```
URI -> Cache -> Allowlist -> Reachability -> [Fetch] -> [Ingest] -> Result
```

Configurable per-silo via `EvidencePolicy`:
- `allowlist` — Trusted domains (skip fetch)
- `auto_ingest` — Create Memory nodes from fetched content
- `require_reachable` — Reject if HEAD fails
- `cache_ttl` — Validation cache duration

## Invariants

I1. Every `:Claim` in Knowledge has at least one `DERIVED_FROM` edge to Memory or validated URI.

I2. Every `:Commitment` has exactly one `DECLARED_BY` edge to the authoring agent.

I3. Evidence node refs must resolve to existing nodes; dangling refs are rejected.

I4. `as_of` queries respect bi-temporal fields (`valid_from`, `valid_to`, `created_at`).

I5. Deterministic IDs ensure concurrent writes to same content converge to same node.
