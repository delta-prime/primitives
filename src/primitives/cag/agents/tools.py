"""Tool protocol definitions for CAG agents.

Tools are functions that agents call to read state, commit artifacts, or
signal completion. Each tool call updates the budget and may mutate the
dependency container.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel, ConfigDict

from primitives.cag.agents.base import BudgetStatus, DepsProtocol

DepsT = TypeVar("DepsT", bound=DepsProtocol, contravariant=True)
ResultT = TypeVar("ResultT", covariant=True)


class ToolResult(BaseModel):
    """Base class for tool results. All results carry budget status."""

    model_config = ConfigDict(extra="forbid")

    budget_status: BudgetStatus


class ToolDefinition(BaseModel):
    """Metadata describing a tool for schema generation."""

    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    parameters_schema: dict[str, Any]
    result_schema: dict[str, Any]


@runtime_checkable
class ToolProtocol(Protocol[DepsT]):
    """Protocol for CAG agent tools.

    Tools are async callables that receive a context (containing deps)
    and arguments, returning a result that includes budget status.
    """

    @property
    def name(self) -> str:
        """Tool name as exposed to the agent."""
        ...

    @property
    def description(self) -> str:
        """Description shown to the agent."""
        ...

    @property
    def definition(self) -> ToolDefinition:
        """Full tool definition for schema generation."""
        ...

    @abstractmethod
    async def __call__(
        self,
        deps: DepsT,
        **kwargs: Any,
    ) -> ToolResult:
        """Execute the tool.

        Implementations should:
        1. Perform the operation (read, commit, etc.)
        2. Update deps.seen_node_ids if nodes were returned
        3. Rebuild the budget status
        4. Return a result with the updated budget
        """
        ...
