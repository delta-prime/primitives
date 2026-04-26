"""CAG Agent Protocol definitions.

Defines abstract interfaces for CAG agents and tools. Implementations
live in private repositories (context-service); this module provides
the protocol contract that implementations must follow.
"""

from primitives.cag.agents.base import (
    AgentConfig,
    AgentPhase,
    AgentProtocol,
    AgentResult,
    BudgetConfig,
    BudgetStatus,
    DepsProtocol,
)
from primitives.cag.agents.tools import (
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
