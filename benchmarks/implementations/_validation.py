"""
Shared output validation helpers for benchmark implementations.
"""

from typing import Iterable, Optional


def find_success_marker_line(output: str, markers: Iterable[str]) -> Optional[str]:
    """Return the first output line containing any success marker."""
    normalized = tuple(str(marker).strip().lower() for marker in markers if str(marker).strip())
    if not normalized:
        return None

    for raw_line in (output or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lowered = line.lower()
        if any(marker in lowered for marker in normalized):
            return line
    return None


def missing_success_marker_error(phase_name: str, markers: Iterable[str]) -> str:
    marker_text = ", ".join(str(marker) for marker in markers if str(marker).strip())
    return f"{phase_name} output lacks success markers: {marker_text}"
