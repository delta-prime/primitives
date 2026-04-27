"""Tests for supersession primitives."""

from primitives.cag.epistemology.supersession import (
    ContradictionResult,
    FactForSupersession,
    detect_contradiction,
    should_supersede,
)


def make_fact(
    id: str = "fact-1",
    subject_id: str = "subj-1",
    predicate: str = "has_value",
    object_id: str | None = "obj-1",
    object_literal: str | None = None,
    confidence: float = 0.8,
) -> FactForSupersession:
    return FactForSupersession(
        id=id,
        subject_id=subject_id,
        predicate=predicate,
        object_id=object_id,
        object_literal=object_literal,
        confidence=confidence,
    )


class TestDetectContradiction:
    def test_same_fact_no_contradiction(self):
        fact_a = make_fact()
        fact_b = make_fact(id="fact-2")

        assert detect_contradiction(fact_a, fact_b) is False

    def test_different_subject_no_contradiction(self):
        fact_a = make_fact(subject_id="subj-1")
        fact_b = make_fact(subject_id="subj-2", object_id="obj-2")

        assert detect_contradiction(fact_a, fact_b) is False

    def test_different_predicate_no_contradiction(self):
        fact_a = make_fact(predicate="has_value")
        fact_b = make_fact(predicate="belongs_to", object_id="obj-2")

        assert detect_contradiction(fact_a, fact_b) is False

    def test_same_subject_predicate_different_object_contradicts(self):
        fact_a = make_fact(object_id="obj-1")
        fact_b = make_fact(id="fact-2", object_id="obj-2")

        assert detect_contradiction(fact_a, fact_b) is True

    def test_literal_vs_literal_contradiction(self):
        fact_a = make_fact(object_id=None, object_literal="value-1")
        fact_b = make_fact(id="fact-2", object_id=None, object_literal="value-2")

        assert detect_contradiction(fact_a, fact_b) is True

    def test_literal_vs_object_contradiction(self):
        fact_a = make_fact(object_id="obj-1", object_literal=None)
        fact_b = make_fact(id="fact-2", object_id=None, object_literal="value-1")

        assert detect_contradiction(fact_a, fact_b) is True


class TestShouldSupersede:
    def test_no_contradiction_returns_no_contradiction(self):
        existing = make_fact(subject_id="subj-1")
        incoming = make_fact(id="fact-2", subject_id="subj-2")

        decision = should_supersede(existing, incoming)

        assert decision.result == ContradictionResult.NO_CONTRADICTION
        assert decision.winner_id is None
        assert decision.loser_id is None

    def test_incoming_dominates(self):
        existing = make_fact(confidence=0.5, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.9, object_id="obj-2")

        decision = should_supersede(existing, incoming)

        assert decision.result == ContradictionResult.NEW_SUPERSEDES_OLD
        assert decision.winner_id == "fact-2"
        assert decision.loser_id == "fact-1"

    def test_existing_dominates(self):
        existing = make_fact(confidence=0.9, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.5, object_id="obj-2")

        decision = should_supersede(existing, incoming)

        assert decision.result == ContradictionResult.OLD_SUPERSEDES_NEW
        assert decision.winner_id == "fact-1"
        assert decision.loser_id == "fact-2"

    def test_unresolved_when_close_confidences(self):
        existing = make_fact(confidence=0.8, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.85, object_id="obj-2")

        decision = should_supersede(existing, incoming)

        assert decision.result == ContradictionResult.UNRESOLVED
        assert decision.winner_id is None
        assert decision.loser_id is None

    def test_custom_threshold(self):
        existing = make_fact(confidence=0.8, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.85, object_id="obj-2")

        decision = should_supersede(existing, incoming, dominance_threshold=1.05)

        assert decision.result == ContradictionResult.NEW_SUPERSEDES_OLD

    def test_boundary_exactly_at_threshold(self):
        existing = make_fact(confidence=0.5, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.6, object_id="obj-2")

        decision = should_supersede(existing, incoming, dominance_threshold=1.2)

        assert decision.result == ContradictionResult.NEW_SUPERSEDES_OLD

    def test_reason_includes_confidences(self):
        existing = make_fact(confidence=0.5, object_id="obj-1")
        incoming = make_fact(id="fact-2", confidence=0.9, object_id="obj-2")

        decision = should_supersede(existing, incoming)

        assert "0.9" in decision.reason
        assert "0.5" in decision.reason
