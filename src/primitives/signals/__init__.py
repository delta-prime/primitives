"""Signal primitives: heat, freshness, priority.

Pure functions for computing knowledge signals that inform retrieval
ranking, lifecycle transitions, and work prioritization.
"""

from primitives.signals.heat import heat_score
from primitives.signals.freshness import freshness_score, decay_weight
from primitives.signals.priority import priority_score

__all__ = [
    "heat_score",
    "freshness_score",
    "decay_weight",
    "priority_score",
]
