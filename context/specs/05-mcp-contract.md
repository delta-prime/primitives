# 05 — MCP Contract

> The agent-facing interface to the EAG architecture.

## Design Philosophy

The MCP surface uses **3 core tools** that map to fundamental operations:

| Operation | Tool | What it does |
|-----------|------|--------------|
| Write | `context_store` | Store to any layer (memory, knowledge, wisdom, intelligence, meta) |
| Read | `context_recall` | Retrieve via search, fetch, graph, history, or provenance |
| Link | `context_link` | Create relationships between nodes |

This minimal surface follows the "less is more" principle: agents learn 3 tools instead of 15, with layer/mode parameters providing the specificity. Skills (agent-side prompt templates) teach common patterns.

## Silo Tenancy

**`silo_id` is auto-derived from auth.** Agents never pass it explicitly.

The service derives `silo_id` deterministically from `org_id` in the auth context. This eliminates the friction of discovering and threading silo IDs through every call.

## Tool Surface

### context_store

Write content to any cognitive layer.

```
context_store(
  content: str,
  layer: str = "memory",       # memory | knowledge | wisdom | intelligence | meta
  evidence: list[str] | None,  # required for knowledge
  about: list[str] | None,     # required for wisdom, meta
  steps: list[dict] | None,    # required for intelligence
  tags: list[str] | None,
  session: str | None,
) -> {node_id, layer, created_at}
```

**Layer-specific requirements:**

| Layer | Required params | Creates |
|-------|-----------------|---------|
| memory | (none) | Memory node (decays) |
| knowledge | `evidence` | Claim (may promote to Fact) |
| wisdom | `about` | Belief/Commitment |
| intelligence | `steps` | ReasoningChain |
| meta | `about` | MetaObservation |

**Decay classes (memory layer only):** `ephemeral` (7d), `standard` (90d), `durable` (540d), `permanent` (5y)

### context_recall

Retrieve from epistemic memory with multiple modes.

```
context_recall(
  query: str,
  mode: str = "search",        # search | fetch | graph | history | provenance
  node_ids: list[str] | None,  # for fetch, history, provenance modes
  depth: int = 0,              # for graph mode (0 = flat, 1-3 = traversal)
  layers: list[str] | None,    # filter by layer
  top_k: int = 10,
  as_of: str | None,           # time-travel (ISO datetime)
) -> {results, mode, search_time_ms}
```

**Mode behavior:**

| Mode | Uses query | Uses node_ids | Returns |
|------|------------|---------------|---------|
| search | Yes | No | Semantic search results |
| fetch | No | Yes | Nodes by ID (cached, <20ms) |
| graph | Yes or node_ids | Optional | Subgraph traversal |
| history | No | Yes (one) | SUPERSEDES chain |
| provenance | No | Yes (one) | Citation chain to sources |

### context_link

Create typed relationships between nodes.

```
context_link(
  from_id: str,
  to_id: str,
  rel: str,                    # supports | contradicts | derives | supersedes | references
  weight: float = 1.0,
  note: str | None,
) -> {edge_id, rel, created_at}
```

## Skills

Skills are agent-side prompt templates that teach when and how to use the core tools. They are NOT MCP tools — they're patterns installed in the agent's system prompt.

**Core skills:**

| Skill | Trigger | Maps to |
|-------|---------|---------|
| observe | "remember this" | `context_store(layer="memory")` |
| learn | "I learned" | `context_store(layer="knowledge", evidence=[...])` |
| recall | "what do I know" | `context_recall(mode="search")` |
| trace | "why do I believe" | `context_recall(mode="provenance")` |
| reflect | "I notice a pattern" | `context_store(layer="meta", about=[...])` |
| reason | "let me think through" | `context_store(layer="intelligence", steps=[...])` |

Skills are distributed separately. See [skills/context-skills.md](../../../context-service/skills/context-skills.md).

## Evidence Requirements

**Principle:** Knowledge-layer writes require grounded evidence. Agents cannot hallucinate sources.

| Layer | Evidence required? | Grounding mechanism |
|-------|-------------------|---------------------|
| memory | No | Memories ARE grounding |
| knowledge | Yes | `DERIVED_FROM` edge to Memory node or validated URI |
| wisdom | No | Derives from Knowledge via synthesis |
| intelligence | No | Session-scoped, ephemeral |
| meta | No | References existing nodes via `about` |

### Evidence Formats

```
node:<uuid>     — Reference to existing Memory-layer node
https://...     — External URI (validated via evidence pipeline)
file://...      — Local file URI (for ingested sources)
```

## Agent Attribution

- **`agent_id`** — Auto-captured from auth context (defaults to `user:{user_id}`)
- **`session_id`** — Auto-derived from auth token or provided via header
- **`DECLARED_BY`** — Commitments and reflections link to declaring agent

## Concurrency Model

Race conditions are resolved through:

1. **Deterministic IDs** — Content-based hashing (no timestamps in IDs)
2. **MERGE semantics** — Idempotent writes
3. **Agent-scoped nodes** — Commitments/reflections are per-agent, no conflict
4. **Custodian reconciliation** — Conflicting claims coexist until T2 supersession

## Relationship to Transitions

| Tool + layer/mode | Primary layer | Related transitions |
|-------------------|---------------|---------------------|
| `context_store` layer=memory | Memory | T8 (decay), T9 (hard-delete) |
| `context_store` layer=knowledge | Knowledge | T1 (extract from), T2 (supersede), T5 (promote to) |
| `context_store` layer=wisdom | Wisdom | T7 (commit) |
| `context_store` layer=meta | Meta | (none — meta-observations don't transition) |
| `context_store` layer=intelligence | Intelligence | T5 (consensus), T6 (trace) |
| `context_recall` mode=provenance | (read) | T6 (trace) |

The Custodian handles transitions; agents express intent through MCP tools.

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

I6. `silo_id` is derived from auth; explicit silo params are rejected to prevent cross-tenant access.
