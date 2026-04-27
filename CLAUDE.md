# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository

`primitives` — Open-source EAG (Epistemic Augmented Generation) primitives. Pure functions, schema definitions, and protocol interfaces. No storage backends, no LLM calls, no side effects.

Lives in the `delta-prime/` monorepo alongside `context-service/` (proprietary production backend).

## Naming Conventions

- **EAG** (Epistemic Augmented Generation) — the generation process
- **CITE** (Context In Tiered Epistemology) — the architecture and schema naming (e.g., `CITEEdgeType`)
- **Meta-Memory** — cross-cutting observability (provenance, time-travel, reflection)

The four cognitive layers: Memory → Knowledge → Wisdom → Intelligence.

## Stack

Python 3.12+ / Pydantic. No heavy dependencies — this is meant to be embedded. Canonical source: `pyproject.toml`.

## Commands

```bash
# Setup
just install-dev             # uv sync --all-extras
just sync                    # uv sync

# Quality
just lint                    # ruff check src tests
just typecheck               # mypy src
just format                  # ruff format + ruff check --fix
just check                   # lint + typecheck

# Tests
just test                    # pytest
uv run pytest tests/test_promotion.py -v
```

## Structure

```
src/primitives/
├── eag/                     # EAG-specific implementations
│   ├── epistemology/        # Confidence, promotion (R1/R2), supersession
│   ├── agents/              # AgentProtocol, ToolProtocol
│   └── queries/             # Cypher query helpers
├── schema/                  # CITE schema definitions
│   ├── labels.py            # Node labels (ALL_CITE_LABELS)
│   └── edges.py             # Edge types (CITEEdgeType, ALL_CITE_EDGES)
├── scoring/                 # Decay functions (Gaussian per-class)
├── taxonomy/                # Category definitions
├── protocols.py             # Abstract interfaces (KnowledgeStore, etc.)
├── shared/                  # Utilities (fingerprints, validators, cypher helpers)
└── extensions/              # Optional extensions (code.py for code entities)
```

## Specs

- `context/specs/01-paradigm.md` — EAG paradigm overview
- `context/specs/02-layers.md` — Four-layer model (Memory/Knowledge/Wisdom/Intelligence)
- `context/specs/03-transitions.md` — Layer transitions and promotion rules
- `context/specs/04-metacognition.md` — Meta-Memory and reflection
- `context/specs/06-epistemology.md` — Confidence math, supersession

## Key rules

1. **No side effects** — all functions are pure. No I/O, no network, no storage.
2. **No LLM calls** — adjudication is deterministic. LLM extraction lives in context-service.
3. Always invoke Python via `uv run`.
4. No emojis in code or docs.
5. Schema types use `CITE` prefix (e.g., `CITEEdgeType`), epistemology uses `EAG` module path.
6. Tests must pass before merge — run `just check`.

## Epistemology Quick Reference

```python
from primitives.eag.epistemology import (
    combined_confidence,      # raw_confidence * source_tier * corroboration
    noisy_or_aggregate,       # 1 - product(1 - c_i)
    should_promote_r1,        # Single authoritative source, confidence >= 0.7
    should_promote_r2,        # Multi-source corroboration, aggregate >= 0.8
    should_supersede,         # Dominance threshold (default 1.2x)
    detect_contradiction,     # Same (subject, predicate), different object
)

from primitives.schema import CITEEdgeType, ALL_CITE_LABELS
```
