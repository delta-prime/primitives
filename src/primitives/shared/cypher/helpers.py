"""Cypher helper utilities.

Safe parameter handling and label/property sanitization.
"""

from __future__ import annotations

import re
from typing import Any

# Valid Cypher identifier pattern
_IDENTIFIER_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def sanitize_label(label: str) -> str:
    """Sanitize a node label for safe use in Cypher.

    Labels must be valid identifiers. Invalid labels raise ValueError.

    Args:
        label: The label to sanitize

    Returns:
        The label if valid

    Raises:
        ValueError: If label contains invalid characters
    """
    if not _IDENTIFIER_PATTERN.match(label):
        raise ValueError(f"Invalid Cypher label: {label!r}")
    return label


def sanitize_property(prop: str) -> str:
    """Sanitize a property name for safe use in Cypher.

    Property names must be valid identifiers. Invalid names raise ValueError.

    Args:
        prop: The property name to sanitize

    Returns:
        The property name if valid

    Raises:
        ValueError: If property name contains invalid characters
    """
    if not _IDENTIFIER_PATTERN.match(prop):
        raise ValueError(f"Invalid Cypher property name: {prop!r}")
    return prop


def param_dict(**kwargs: Any) -> dict[str, Any]:
    """Create a parameter dict for Cypher queries.

    Filters out None values to avoid "null" in optional parameters.

    Args:
        **kwargs: Parameter name-value pairs

    Returns:
        Dict with None values removed
    """
    return {k: v for k, v in kwargs.items() if v is not None}
