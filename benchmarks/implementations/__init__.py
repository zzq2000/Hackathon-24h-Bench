"""
Benchmark Implementations Package

Contains concrete implementations of benchmark runners.
"""

# Import implementations to register them
try:
    from .sysbench import SysbenchRunner
except ImportError:
    SysbenchRunner = None

try:
    from .tpcc import TPCCRunner
except ImportError:
    TPCCRunner = None

try:
    from .tpch import TPCHRunner
except ImportError:
    TPCHRunner = None

try:
    from .mq_bench import MessageQueueBenchRunner
except ImportError:
    MessageQueueBenchRunner = None

try:
    from .http_bench import HttpBenchRunner
except ImportError:
    HttpBenchRunner = None

try:
    from .redis_bench import RedisBenchRunner
except ImportError:
    RedisBenchRunner = None

__all__ = []
if SysbenchRunner:
    __all__.append("SysbenchRunner")
if TPCCRunner:
    __all__.append("TPCCRunner")
if TPCHRunner:
    __all__.append("TPCHRunner")
if MessageQueueBenchRunner:
    __all__.append("MessageQueueBenchRunner")
if HttpBenchRunner:
    __all__.append("HttpBenchRunner")
if RedisBenchRunner:
    __all__.append("RedisBenchRunner")
