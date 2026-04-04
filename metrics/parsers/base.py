"""Abstract base class for agent log parsers."""

from __future__ import annotations

from abc import ABC, abstractmethod

from metrics.models import IterationMetrics


class BaseAgentParser(ABC):
    """Parse agent stdout from iteration JSON into structured metrics."""

    @abstractmethod
    def parse_iteration(self, iter_data: dict) -> IterationMetrics:
        """Parse a single iteration log dict into IterationMetrics."""
        ...

    @abstractmethod
    def supports_agent(self, agent_name: str) -> bool:
        """Return True if this parser handles the given agent type."""
        ...
