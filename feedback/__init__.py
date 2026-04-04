"""
Feedback Abstraction Module

This module provides interfaces for formatting and generating feedback
from benchmark results that can be consumed by AI code agents.

Example:
    >>> from feedback import FeedbackFormatter, TextFeedback
    >>>
    >>> formatter = TextFeedback()
    >>> feedback = formatter.format(benchmark_results)
    >>> formatter.write(Path("./last_brief.txt"), feedback)
"""

from .base import FeedbackFormatter, FeedbackData
from .text import TextFeedbackFormatter, JsonFeedbackFormatter
from .anonymize import anonymize_feedback_data

__all__ = [
    "FeedbackFormatter",
    "FeedbackData",
    "TextFeedbackFormatter",
    "JsonFeedbackFormatter",
    "anonymize_feedback_data",
]
