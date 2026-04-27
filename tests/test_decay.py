"""Tests for decay scoring primitives."""

import math

from primitives.scoring.decay import compute_effective_importance


class TestComputeEffectiveImportance:
    def test_zero_age_no_decay(self):
        result = compute_effective_importance(
            base_importance=0.9,
            decay_rate=0.01,
            age_days=0.0,
        )
        assert result == 0.9

    def test_pinned_bypasses_decay(self):
        result = compute_effective_importance(
            base_importance=0.9,
            decay_rate=0.1,
            age_days=100.0,
            pinned=True,
        )
        assert result == 0.9

    def test_decay_reduces_importance(self):
        result = compute_effective_importance(
            base_importance=0.9,
            decay_rate=0.01,
            age_days=30.0,
        )
        assert result < 0.9
        assert result > 0.0

    def test_exponential_decay_formula(self):
        base = 0.8
        rate = 0.05
        age = 10.0

        result = compute_effective_importance(base, rate, age)
        expected = base * math.exp(-rate * age)

        assert abs(result - expected) < 1e-10

    def test_higher_decay_rate_faster_decline(self):
        slow_decay = compute_effective_importance(0.9, 0.01, 30.0)
        fast_decay = compute_effective_importance(0.9, 0.1, 30.0)

        assert fast_decay < slow_decay

    def test_standard_decay_classes(self):
        base = 0.9
        age = 30.0

        ephemeral = compute_effective_importance(base, 0.1, age)
        standard = compute_effective_importance(base, 0.01, age)
        durable = compute_effective_importance(base, 0.002, age)

        assert ephemeral < standard < durable

    def test_very_old_content_approaches_zero(self):
        result = compute_effective_importance(
            base_importance=0.9,
            decay_rate=0.1,
            age_days=365.0,
        )
        assert result < 0.001

    def test_zero_decay_rate_no_change(self):
        result = compute_effective_importance(
            base_importance=0.9,
            decay_rate=0.0,
            age_days=100.0,
        )
        assert result == 0.9
