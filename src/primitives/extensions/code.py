"""Code entity extensions for coding-context use cases.

These types are optional — only needed when the knowledge graph
tracks code artifacts (functions, modules, endpoints, etc.).
"""

from __future__ import annotations

from enum import StrEnum


class CodeEntityType(StrEnum):
    """Types of code entities."""

    MODULE = "module"
    FUNCTION = "function"
    FILE = "file"
    ENDPOINT = "endpoint"
    CONFIG = "config"
    PACKAGE = "package"
    PATTERN = "pattern"
    SERVICE = "service"


class CodeRelType(StrEnum):
    """Relationship types between code entities."""

    IMPORTS = "IMPORTS"
    CALLS = "CALLS"
    DEFINES = "DEFINES"
    CONFIGURES = "CONFIGURES"
    DEPENDS_ON = "DEPENDS_ON"
    IMPLEMENTS = "IMPLEMENTS"
    EXTENDS = "EXTENDS"
    EXPOSES = "EXPOSES"
    CONSUMES = "CONSUMES"
    TESTS = "TESTS"


ALL_CODE_ENTITY_TYPES: frozenset[str] = frozenset(t.value for t in CodeEntityType)
ALL_CODE_REL_TYPES: frozenset[str] = frozenset(r.value for r in CodeRelType)
