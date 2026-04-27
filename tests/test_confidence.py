"""Tests for confidence computation primitives."""

from primitives.cag.epistemology.confidence import (
    SourceTier,
    combined_confidence,
    incremental_noisy_or,
    noisy_or_aggregate,
)


class TestSourceTier:
    def test_tier_weights(self):
        assert SourceTier.AUTHORITATIVE.weight == 1.0
        assert SourceTier.VALIDATED.weight == 0.85
        assert SourceTier.COMMUNITY.weight == 0.6
        assert SourceTier.UNKNOWN.weight == 0.4

    def test_tier_values(self):
        assert SourceTier.AUTHORITATIVE.value == "authoritative"
        assert SourceTier.VALIDATED.value == "validated"


class TestCombinedConfidence:
    def test_authoritative_full_confidence(self):
        result = combined_confidence(
            raw_confidence=1.0,
            source_tier=SourceTier.AUTHORITATIVE,
        )
        assert result == 1.0

    def test_unknown_tier_reduces_confidence(self):
        result = combined_confidence(
            raw_confidence=1.0,
            source_tier=SourceTier.UNKNOWN,
        )
        assert result == 0.4

    def test_corroboration_boost(self):
        base = combined_confidence(
            raw_confidence=0.5,
            source_tier=SourceTier.AUTHORITATIVE,
        )
        boosted = combined_confidence(
            raw_confidence=0.5,
            source_tier=SourceTier.AUTHORITATIVE,
            corroboration_factor=1.5,
        )
        assert boosted == base * 1.5

    def test_method_weight(self):
        result = combined_confidence(
            raw_confidence=0.8,
            source_tier=SourceTier.AUTHORITATIVE,
            method_weight=0.5,
        )
        assert result == 0.4

    def test_caps_at_one(self):
        result = combined_confidence(
            raw_confidence=1.0,
            source_tier=SourceTier.AUTHORITATIVE,
            corroboration_factor=2.0,
        )
        assert result == 1.0

    def test_floors_at_zero(self):
        result = combined_confidence(
            raw_confidence=-0.5,
            source_tier=SourceTier.AUTHORITATIVE,
        )
        assert result == 0.0


class TestNoisyOrAggregate:
    def test_empty_list(self):
        assert noisy_or_aggregate([]) == 0.0

    def test_single_confidence(self):
        assert noisy_or_aggregate([0.7]) == 0.7

    def test_two_confidences(self):
        result = noisy_or_aggregate([0.5, 0.5])
        assert result == 0.75

    def test_multiple_high_confidences_approach_cap(self):
        result = noisy_or_aggregate([0.9, 0.9, 0.9])
        assert result == 0.99

    def test_custom_cap(self):
        result = noisy_or_aggregate([0.9, 0.9, 0.9], cap=0.95)
        assert result == 0.95

    def test_zero_confidence_no_contribution(self):
        assert noisy_or_aggregate([0.7, 0.0]) == 0.7

    def test_formula_correctness(self):
        confidences = [0.6, 0.4, 0.3]
        expected = 1 - (0.4 * 0.6 * 0.7)
        assert abs(noisy_or_aggregate(confidences) - expected) < 1e-10


class TestIncrementalNoisyOr:
    def test_from_zero(self):
        result = incremental_noisy_or(0.0, 0.5)
        assert result == 0.5

    def test_incremental_matches_batch(self):
        confidences = [0.5, 0.6, 0.7]
        batch_result = noisy_or_aggregate(confidences)

        incremental = 0.0
        for c in confidences:
            incremental = incremental_noisy_or(incremental, c)

        assert abs(incremental - batch_result) < 1e-10

    def test_caps_at_limit(self):
        result = incremental_noisy_or(0.95, 0.9, cap=0.99)
        assert result == 0.99

    def test_custom_cap(self):
        result = incremental_noisy_or(0.9, 0.9, cap=0.95)
        assert result == 0.95
