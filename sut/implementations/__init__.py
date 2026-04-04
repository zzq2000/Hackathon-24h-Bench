"""
SUT Implementations Package

Contains concrete implementations of System Under Test types.
"""

# Import implementations to register them
try:
    from .database import DatabaseSUT
except ImportError:
    DatabaseSUT = None

try:
    from .message_queue import MessageQueueSUT
except ImportError:
    MessageQueueSUT = None

try:
    from .http_server import HttpServerSUT
except ImportError:
    HttpServerSUT = None

try:
    from .redis_kvstore import RedisKVStoreSUT
except ImportError:
    RedisKVStoreSUT = None

__all__ = []
if DatabaseSUT:
    __all__.append("DatabaseSUT")
if MessageQueueSUT:
    __all__.append("MessageQueueSUT")
if HttpServerSUT:
    __all__.append("HttpServerSUT")
if RedisKVStoreSUT:
    __all__.append("RedisKVStoreSUT")
