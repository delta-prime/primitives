"""Category definitions for context classification."""

from __future__ import annotations

from enum import StrEnum


class ContextCategory(StrEnum):
    """Categories of context for classification."""

    # Structural
    ARCHITECTURE = "architecture"
    CONVENTION = "convention"
    DEPENDENCY = "dependency"
    SCHEMA = "schema"

    # Decisional
    DECISION = "decision"
    TRADEOFF = "tradeoff"
    CONSTRAINT = "constraint"

    # Operational
    BUG = "bug"
    WORKAROUND = "workaround"
    ENVIRONMENT = "environment"
    OBSERVATION = "observation"

    # Instructional
    PREFERENCE = "preference"
    INSTRUCTION = "instruction"
    WORKFLOW = "workflow"


ALL_CATEGORIES: frozenset[str] = frozenset(c.value for c in ContextCategory)


def is_valid_category(category: str) -> bool:
    """Check if a category string is valid."""
    return category in ALL_CATEGORIES
