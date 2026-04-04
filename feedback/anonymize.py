"""
Benchmark Name Anonymization

Replaces real benchmark tool/client names with generic labels in feedback
destined for AI agents, preventing agents from gaming specific test tools.
Also sanitizes error messages to prevent leaking benchmark internals
(SQL queries, table names, connection strings, file paths, etc.).
"""

import hashlib
import re
from typing import Dict, Any, List, Optional

# Mapping from real benchmark/suite names to anonymous labels.
# Keys are lowercase canonical names; values are the replacement labels.
_TOOL_ALIASES: Dict[str, str] = {
    # Aggregate benchmark runners that wrap multiple inner suites
    "mq_bench": "messaging",
    "http_bench": "web",
    "redis_bench": "kv",
    # Message Queue suites
    "pika": "acceptance",
    "omq": "throughput",
    "perftest": "performance",
    # Database benchmarks
    "sysbench": "oltp",
    "tpcc": "transaction",
    "tpch": "analytical",
    # HTTP Server suites
    "cispa": "compliance",
    "tfb": "workload",
    "h1spec": "spec",
    # Redis KV Store suites
    "tcl": "conformance",
    "redis_benchmark": "perf",
    "ycsb": "appload",
    "memtier": "stress",
}

# Additional aliases for hyphenated/display forms that appear in error messages
# (e.g. "TPC-C: 4/8 workloads passed", "TPC-H query 3 did not complete").
_TEXT_ALIASES: Dict[str, str] = {
    "tpc-c": "transaction",
    "tpc-h": "analytical",
    "perf-test": "performance",
    "rabbitmq-perf-test": "performance",
    "redis-benchmark": "perf",
    "hammerdb": "driver",
    "techempower": "workload",
    "frameworkbenchmarks": "workload",
}

# Merge both maps for the regex; _TOOL_ALIASES is used for suite key lookups,
# while both are used for free-text replacement.
_ALL_ALIASES: Dict[str, str] = {**_TOOL_ALIASES, **_TEXT_ALIASES}

# Wrapper benchmark names are implementation details in suite keys such as
# "mq_bench:pika:connection". When an inner suite is present, drop the wrapper
# segment entirely so agent-facing briefs group by the anonymized suite family.
_DROPPED_WRAPPER_PREFIXES = {"mq_bench", "http_bench", "redis_bench"}

# Coarse suite families can remain visible in the agent-facing brief, but the
# fine-grained workload/rule identifiers under them should be replaced with
# stable opaque labels to avoid leaking benchmark internals.
_OPAQUE_SUFFIX_FAMILIES = {
    "acceptance": "case",
    "throughput": "case",
    "performance": "case",
    "compliance": "rule",
    "workload": "case",
    "spec": "case",
    "conformance": "case",
    "perf": "case",
    "appload": "case",
    "stress": "case",
}

# Pre-compiled pattern that matches any known tool name as a word boundary.
# Matches "pika", "Pika", "PIKA", "TPC-C", "tpc-h", "sysbench", etc.
_TOOL_RE = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in _ALL_ALIASES) + r')\b',
    re.IGNORECASE,
)

_OPAQUE_LABEL_RE = re.compile(r'^(?:case|rule)_[0-9a-f]{8}$')
_BRIEF_GROUP_RE = re.compile(
    r'^(?P<indent>\s{2})(?P<bench>[^:]+): '
    r'(?P<passed>\d+)/(?P<total>\d+) passed'
    r'(?: \[FAIL: (?P<failed>.+)\])?$'
)


def _replace_match(m: re.Match) -> str:
    """Replace a regex match with its anonymous alias, preserving case style."""
    original = m.group(0)
    alias = _ALL_ALIASES[original.lower()]
    if original.isupper():
        return alias.upper()
    if original[0].isupper():
        return alias.capitalize()
    return alias


def _opaque_suffix_label(family: str, suffix: str) -> str:
    """Return a stable opaque label for a workload/rule identifier."""
    prefix = _OPAQUE_SUFFIX_FAMILIES[family]
    digest = hashlib.sha1(f"{family}:{suffix}".encode("utf-8")).hexdigest()[:8]
    return f"{prefix}_{digest}"


def anonymize_name(name: str) -> str:
    """Anonymize a single suite/workload name.

    Handles both prefixed names ("pika:connection" -> "acceptance:connection")
    and nested names ("mq_bench:pika:connection" -> "acceptance:connection").
    """
    parts = [part.strip() for part in str(name).split(":")]
    if len(parts) > 1 and parts[0].lower() in _DROPPED_WRAPPER_PREFIXES:
        parts = parts[1:]

    if (
        len(parts) == 2
        and parts[0].lower() in _OPAQUE_SUFFIX_FAMILIES
        and _OPAQUE_LABEL_RE.match(parts[1])
    ):
        return ":".join(parts)

    anonymized_parts = [
        _TOOL_ALIASES.get(part.lower(), part)
        for part in parts
    ]
    if len(parts) > 1:
        family = anonymized_parts[0].lower()
        if family in _OPAQUE_SUFFIX_FAMILIES:
            suffix = ":".join(parts[1:])
            anonymized_parts = [anonymized_parts[0], _opaque_suffix_label(family, suffix)]
    return ":".join(anonymized_parts)


def anonymize_text(text: str) -> str:
    """Replace all occurrences of known tool names in free-form text."""
    return _TOOL_RE.sub(_replace_match, text)


def anonymize_brief_text(text: str) -> str:
    """Best-effort anonymization for already-rendered agent-facing brief text.

    This is used to refresh historical briefs created before the current
    anonymization rules existed. Structured feedback generation should continue
    to use anonymize_feedback_data() directly.
    """
    lines = []
    for line in text.splitlines():
        if line.startswith("overall: ") and " - " in line:
            prefix, sep, suffix = line.partition(" - ")
            line = f"{prefix}{sep}{sanitize_error(anonymize_text(suffix))}"
        elif " -- " in line and re.match(r"^(?:L\d+|tier\d+|lite|base|medium|large):", line):
            prefix, sep, suffix = line.partition(" -- ")
            line = f"{prefix}{sep}{sanitize_error(anonymize_text(suffix))}"
        else:
            match = _BRIEF_GROUP_RE.match(line)
            if match:
                failed = match.group("failed")
                failed_items = []
                if failed:
                    failed_items = [
                        anonymize_name(item.strip())
                        for item in failed.split(",")
                        if item.strip()
                    ]
                line = (
                    f"{match.group('indent')}{anonymize_name(match.group('bench'))}: "
                    f"{match.group('passed')}/{match.group('total')} passed"
                )
                if failed_items:
                    line += f" [FAIL: {', '.join(failed_items)}]"
            else:
                line = sanitize_error(anonymize_text(line))
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


# ---------------------------------------------------------------------------
# Error message sanitization
# ---------------------------------------------------------------------------

# Benchmark-specific identifiers that leak internal details.
# Each tuple: (pattern, replacement).
_DOMAIN_SCRUB: List[tuple] = [
    # ── Database ──────────────────────────────────────────────────────
    # Sysbench table/database names
    (re.compile(r'\bsbtest\w*', re.IGNORECASE), '<table>'),
    # HammerDB / TPC-C / TPC-H domain tables
    (re.compile(
        r'\b(?:warehouse|district|customer|history|new_?order|orders|order_line'
        r'|stock|item|lineitem|partsupp|supplier|part|nation|region)\b',
        re.IGNORECASE,
    ), '<table>'),
    # SQL statement bodies: strip content after SQL keyword.
    # Keeps the keyword so agents know the *type* of failure.
    (re.compile(
        r"((?:INSERT\s+INTO|UPDATE|DELETE\s+FROM|CREATE\s+(?:TABLE|INDEX|DATABASE)"
        r"|DROP\s+(?:TABLE|INDEX|DATABASE)|ALTER\s+TABLE|SELECT)\s+)\S.*",
        re.IGNORECASE,
    ), r'\1<query>'),

    # ── Message Queue ─────────────────────────────────────────────────
    # Pytest test class/function identifiers (e.g. "TestCreateAndCloseConnection",
    # "test_basic_publish", "FAILED tests/test_foo.py::TestBar::test_baz")
    (re.compile(
        r'\bFAILED\s+\S+::\S+',
    ), 'FAILED <test>'),
    (re.compile(
        r'\bTest[A-Z]\w+',
    ), '<test_case>'),

    # ── HTTP Server ───────────────────────────────────────────────────
    # TFB well-known endpoint paths that fingerprint TechEmpower benchmarks
    (re.compile(
        r'(?:/plaintext|/json|/db|/queries|/fortunes|/updates)'
        r'(?:\?\w+=\w+)?',
    ), '<endpoint>'),
    # TFB expected body value
    (re.compile(
        r'Hello,?\s*World!?',
        re.IGNORECASE,
    ), '<expected>'),
    # h1spec / cispa rule IDs (e.g. "HTTP_Request_Authority", "3.2.1")
    (re.compile(
        r'\bHTTP_(?:Request|Response)_\w+',
    ), '<rule>'),

    # ── Redis KV Store ────────────────────────────────────────────────
    # RESP protocol error details
    (re.compile(r'-ERR\s+.*'), '-ERR <detail>'),
    (re.compile(r'-WRONGTYPE\s+.*'), '-WRONGTYPE <detail>'),
    # Redis key patterns in benchmarks
    (re.compile(r'\bkey:\d+'), 'key:<id>'),
    # YCSB user table keys
    (re.compile(r'\buser\d{10,}'), 'user<id>'),

    # ── Generic (all system types) ────────────────────────────────────
    # Connection strings / URIs
    (re.compile(
        r'(?:mysql|amqp|postgresql|postgres|redis|http|https)://\S+', re.IGNORECASE,
    ), '<uri>'),
    # Absolute file paths (Unix, 3+ segments)
    (re.compile(r'(?:/[\w._-]+){3,}'), '<path>'),
    # Docker image references (org/image:tag)
    (re.compile(r'\b[\w.-]+/[\w.-]+:[\w._-]+\b'), '<image>'),
]


def sanitize_error(text: str) -> str:
    """Remove benchmark-internal content from an error message.

    Applied *after* tool-name anonymization so that tool-name replacements
    happen first, then domain content is scrubbed.
    """
    for pattern, repl in _DOMAIN_SCRUB:
        text = pattern.sub(repl, text)
    return text


def anonymize_suites(suites: Dict[str, str]) -> Dict[str, str]:
    """Anonymize all keys in a suites dict."""
    return {anonymize_name(k): v for k, v in suites.items()}


def anonymize_feedback_data(tiers: List[Dict[str, Any]],
                            error_message: Optional[str] = None,
                            ) -> tuple:
    """Anonymize tier data and error message for agent-facing feedback.

    Returns:
        (anonymized_tiers, anonymized_error_message)
    """
    anon_tiers = []
    for tier in tiers:
        t = dict(tier)
        suites = t.get("suites")
        if isinstance(suites, dict):
            t["suites"] = anonymize_suites(suites)
        for key in ("error", "detail"):
            if t.get(key) and isinstance(t[key], str):
                t[key] = sanitize_error(anonymize_text(t[key]))
        # reason is a short internal tag (e.g. "preflight_failed"), not raw output
        if t.get("reason") and isinstance(t["reason"], str):
            t["reason"] = anonymize_text(t["reason"])
        anon_tiers.append(t)

    anon_error = None
    if error_message:
        anon_error = sanitize_error(anonymize_text(error_message))
    return anon_tiers, anon_error
