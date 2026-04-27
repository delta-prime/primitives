"""EAG Agent Protocol definitions.

Defines abstract interfaces for EAG agents and tools. Implementations
live in private repositories (context-service); this module provides
the protocol contract that implementations must follow.
"""

from primitives.eag.agents.base import (
    AgentConfig,
    AgentPhase,
    AgentProtocol,
    AgentResult,
    BudgetConfig,
    BudgetStatus,
    DepsProtocol,
)
from primitives.eag.agents.tools import (
    ToolDefinition,
    ToolProtocol,
    ToolResult,
)

__all__ = [
    "AgentConfig",
    "AgentPhase",
    "AgentProtocol",
    "AgentResult",
    "BudgetConfig",
    "BudgetStatus",
    "DepsProtocol",
    "ToolDefinition",
    "ToolProtocol",
    "ToolResult",
]
