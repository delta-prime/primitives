"""Fingerprint primitives: content hashing and dedup keys.

Used for idempotent MERGEs and detecting duplicate content.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def content_fingerprint(content: str, algorithm: str = "sha256") -> str:
    """Compute a fingerprint for text content.

    Args:
        content: The text to fingerprint
        algorithm: Hash algorithm (default sha256)

    Returns:
        Hex-encoded hash
    """
    h = hashlib.new(algorithm)
    h.update(content.encode("utf-8"))
    return h.hexdigest()


def spo_fingerprint(
    subject_id: str,
    predicate: str,
    object_id: str | None = None,
    object_literal: str | None = None,
) -> str:
    """Compute fingerprint for a (subject, predicate, object) triple.

    Used as MERGE key for :Fact nodes to ensure one Fact per unique triple.

    Args:
        subject_id: Subject entity ID
        predicate: Predicate/relationship type
        object_id: Object entity ID (if entity reference)
        object_literal: Object literal value (if not entity reference)

    Returns:
        sha256 hex fingerprint
    """
    obj = object_id if object_id is not None else f"lit:{object_literal}"
    canonical = f"{subject_id}|{predicate}|{obj}"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def claim_fingerprint(
    subject: str,
    predicate: str,
    object_value: str,
    source_passage_id: str,
) -> str:
    """Compute fingerprint for a Claim.

    Includes source_passage_id to distinguish same triple from different sources.

    Args:
        subject: Subject text or ID
        predicate: Predicate text
        object_value: Object text or ID
        source_passage_id: Source passage ID

    Returns:
        sha256 hex fingerprint
    """
    canonical = f"{subject}|{predicate}|{object_value}|{source_passage_id}"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def json_fingerprint(data: dict[str, Any] | list[Any]) -> str:
    """Compute fingerprint for JSON-serializable data.

    Uses sorted keys for determinism.

    Args:
        data: Dict or list to fingerprint

    Returns:
        sha256 hex fingerprint
    """
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
