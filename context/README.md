# CAG — Cognitive Augmented Generation

Reference documentation for the CAG paradigm implemented in this library.

## What is CAG

CAG (Cognitive Augmented Generation) is a four-layer cognitive architecture for AI agents. Information flows through distinct persistence regimes:

- **Memory** — experiences that fade (Gaussian decay)
- **Knowledge** — facts that persist until contradicted (indefinite supersession)
- **Wisdom** — beliefs that revise on evidence shift (evidence-gated revision)
- **Intelligence** — ephemeral reasoning (session-scoped)

Unlike RAG, CAG adjudicates (via a Custodian), tracks provenance, supports supersession, and shapes itself around usage (heat). Extraction produces structured claims; the epistemology library is deterministic.

Source: arxiv:2604.11364v1 — *The Missing Knowledge Layer in Cognitive Architectures for AI Agents*.

## What this library provides

`primitives` implements the open, deterministic parts of CAG:

- **Epistemology** — confidence math, contradiction detection, promotion rules (R1/R2), corroboration. Pure functions, no LLM at decision time.
- **Signals** — heat, freshness, priority scoring formulas.
- **Schema** — node type definitions, `PersistenceLayer` enum, edge catalogue.
- **Protocols** — `KnowledgeStore`, `LifecycleManager`, `SignalProvider`, `ProvenanceTracker`.
- **Shared utilities** — used across modules.

What is NOT in this library (proprietary to the service layer):

- Custodian workers (promotion, synthesis, revision scheduling)
- Extraction prompts and LLM orchestration
- Graph + vector write paths
- Storage backends (Memgraph, Qdrant, Redis, Postgres)
- API and MCP interface

## Specs index

| Doc | Contents |
|-----|----------|
| [specs/01-paradigm.md](specs/01-paradigm.md) | Why CAG, the category error in RAG, when CAG pays off |
| [specs/02-layers.md](specs/02-layers.md) | KMWI layer semantics, node types, scoring formulas |
| [specs/03-transitions.md](specs/03-transitions.md) | Transition catalogue (T1-T9), execution rules, provenance |
| [specs/06-epistemology.md](specs/06-epistemology.md) | Deterministic primitives: confidence, contradiction, corroboration, provenance invariants |

## Reading order

1. [01-paradigm.md](specs/01-paradigm.md) — what and why
2. [02-layers.md](specs/02-layers.md) — KMWI taxonomy
3. [03-transitions.md](specs/03-transitions.md) — architecture lives here
4. [06-epistemology.md](specs/06-epistemology.md) — deterministic primitives (maps directly to this library's API)
