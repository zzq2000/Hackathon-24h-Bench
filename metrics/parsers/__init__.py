"""Agent log parsers."""

from metrics.parsers.base import BaseAgentParser
from metrics.parsers.claude import ClaudeParser
from metrics.parsers.cline import ClineParser
from metrics.parsers.codex import CodexParser
from metrics.parsers.gemini import GeminiParser
from metrics.parsers.opencode import OpenCodeParser

PARSERS: list[BaseAgentParser] = [
    ClaudeParser(),
    ClineParser(),
    CodexParser(),
    GeminiParser(),
    OpenCodeParser(),
]


def get_parser(agent_name: str) -> BaseAgentParser | None:
    """Return the first parser that supports the given agent."""
    for p in PARSERS:
        if p.supports_agent(agent_name):
            return p
    return None

__all__ = [
    "BaseAgentParser",
    "ClaudeParser",
    "ClineParser",
    "CodexParser",
    "GeminiParser",
    "OpenCodeParser",
    "get_parser",
    "PARSERS",
]
