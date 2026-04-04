"""
Curated Redis protocol and command conformance probes used by redis_bench.
"""

from __future__ import annotations

import socket
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple


class RedisCaseFailure(RuntimeError):
    """Raised when a conformance probe observes incorrect behavior."""


class RedisCommandError(RuntimeError):
    """Raised when the server returns a RESP error reply."""


@dataclass(frozen=True)
class RespErrorReply:
    message: str


def _fail(message: str) -> None:
    raise RedisCaseFailure(message)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        _fail(message)


def _assert_equal(actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        _fail(f"{message}: expected {expected!r}, got {actual!r}")


def _assert_in(actual: Any, expected: Iterable[Any], message: str) -> None:
    values = tuple(expected)
    if actual not in values:
        _fail(f"{message}: expected one of {values!r}, got {actual!r}")


def _to_float(value: Any, field: str) -> float:
    try:
        return float(str(value))
    except Exception as exc:
        raise RedisCaseFailure(f"{field}: expected float-compatible reply, got {value!r}") from exc


def _to_int(value: Any, field: str) -> int:
    try:
        return int(str(value))
    except Exception as exc:
        raise RedisCaseFailure(f"{field}: expected int-compatible reply, got {value!r}") from exc


def _pairs_to_dict(items: Sequence[Any], field: str) -> Dict[str, str]:
    if len(items) % 2 != 0:
        _fail(f"{field}: expected flat key/value array, got odd-length payload {items!r}")
    result: Dict[str, str] = {}
    for idx in range(0, len(items), 2):
        result[str(items[idx])] = str(items[idx + 1])
    return result


def _as_str_list(items: Sequence[Any]) -> List[str]:
    return [str(item) for item in items]


def _build_resp_command(*args: Any) -> bytes:
    parts = [f"*{len(args)}\r\n".encode("utf-8")]
    for arg in args:
        if isinstance(arg, bytes):
            data = arg
        else:
            data = str(arg).encode("utf-8")
        parts.append(f"${len(data)}\r\n".encode("utf-8"))
        parts.append(data)
        parts.append(b"\r\n")
    return b"".join(parts)


class RedisRespClient:
    def __init__(self, host: str, port: int, timeout_sec: float):
        self._sock = socket.create_connection((host, port), timeout=timeout_sec)
        self._sock.settimeout(timeout_sec)
        self._buffer = bytearray()

    def __enter__(self) -> "RedisRespClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._sock.close()
        except Exception:
            pass

    def send_command(
        self,
        *args: Any,
        inline: bool = False,
        raw: Optional[bytes] = None,
        expect_error: bool = False,
    ) -> Any:
        if raw is not None:
            payload = raw
        elif inline:
            line = " ".join(str(arg) for arg in args).encode("utf-8")
            payload = line + b"\r\n"
        else:
            payload = _build_resp_command(*args)
        self._sock.sendall(payload)
        return self.read_reply(expect_error=expect_error)

    def pipeline(self, commands: Sequence[Sequence[Any]]) -> List[Any]:
        payload = b"".join(_build_resp_command(*cmd) for cmd in commands)
        self._sock.sendall(payload)
        return [self.read_reply() for _ in commands]

    def read_reply(self, expect_error: bool = False) -> Any:
        prefix = self._read_exact(1)
        if prefix == b"+":
            return self._read_line().decode("utf-8", errors="replace")
        if prefix == b"-":
            message = self._read_line().decode("utf-8", errors="replace")
            if expect_error:
                return RespErrorReply(message=message)
            raise RedisCommandError(message)
        if prefix == b":":
            return int(self._read_line())
        if prefix == b"$":
            length = int(self._read_line())
            if length == -1:
                return None
            data = self._read_exact(length)
            self._read_exact(2)
            return data.decode("utf-8", errors="replace")
        if prefix == b"*":
            length = int(self._read_line())
            if length == -1:
                return None
            return [self.read_reply() for _ in range(length)]
        raise RedisCaseFailure(f"Unsupported RESP prefix: {prefix!r}")

    def _read_line(self) -> bytes:
        while True:
            idx = self._buffer.find(b"\r\n")
            if idx >= 0:
                data = bytes(self._buffer[:idx])
                del self._buffer[:idx + 2]
                return data
            chunk = self._sock.recv(4096)
            if not chunk:
                raise RedisCaseFailure("Unexpected EOF while reading RESP line")
            self._buffer.extend(chunk)

    def _read_exact(self, length: int) -> bytes:
        while len(self._buffer) < length:
            chunk = self._sock.recv(max(4096, length - len(self._buffer)))
            if not chunk:
                raise RedisCaseFailure(f"Unexpected EOF while reading {length} bytes")
            self._buffer.extend(chunk)
        data = bytes(self._buffer[:length])
        del self._buffer[:length]
        return data


@dataclass
class RedisCaseContext:
    host: str
    port: int
    deadline: float
    case_id: str
    output_dir: Path
    token: str

    def client(self) -> RedisRespClient:
        return RedisRespClient(self.host, self.port, self.remaining_timeout())

    def key(self, suffix: str) -> str:
        return f"lab:{self.case_id}:{self.token}:{suffix}"

    def remaining_timeout(self) -> float:
        remaining = self.deadline - time.time()
        if remaining <= 0:
            raise TimeoutError(f"Case {self.case_id} exhausted its timeout budget")
        return max(0.1, remaining)

    def sleep(self, seconds: float) -> None:
        if time.time() + seconds > self.deadline:
            raise TimeoutError(f"Case {self.case_id} cannot sleep {seconds}s within timeout budget")
        time.sleep(seconds)


def _scan_collect(
    client: RedisRespClient,
    command: str,
    key: Optional[str] = None,
    *,
    match: Optional[str] = None,
    count: Optional[int] = None,
) -> List[Any]:
    cursor = "0"
    collected: List[Any] = []
    while True:
        args: List[Any] = [command]
        if key is not None:
            args.append(key)
        args.append(cursor)
        if match is not None:
            args.extend(["MATCH", match])
        if count is not None:
            args.extend(["COUNT", count])
        reply = client.send_command(*args)
        _assert(isinstance(reply, list) and len(reply) == 2, f"{command}: expected two-element reply, got {reply!r}")
        cursor = str(reply[0])
        batch = reply[1] or []
        _assert(isinstance(batch, list), f"{command}: expected array payload, got {reply!r}")
        collected.extend(batch)
        if cursor == "0":
            break
    return collected


def _wait_for_bgsave_idle(ctx: RedisCaseContext, client: RedisRespClient) -> None:
    while True:
        info = client.send_command("INFO", "persistence")
        if not isinstance(info, str):
            return
        in_progress = None
        for line in info.splitlines():
            if line.startswith("rdb_bgsave_in_progress:"):
                in_progress = line.split(":", 1)[1].strip()
                break
        if in_progress in {None, "0"}:
            return
        ctx.sleep(0.1)


def _expect_ok(reply: Any, command: str) -> None:
    _assert_equal(reply, "OK", f"{command}: expected OK")


def _case_protocol_inline_ping(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("PING", inline=True)
        _assert_equal(reply, "PONG", "PING inline")


def _case_protocol_bulk_ping(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("PING")
        _assert_equal(reply, "PONG", "PING bulk")


def _case_set_get_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("setget")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("GET", key), "v1", "GET after SET")


def _case_del_single(ctx: RedisCaseContext) -> None:
    key = ctx.key("del1")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("DEL", key), 1, "DEL single")
        _assert_equal(client.send_command("GET", key), None, "GET after DEL")


def _case_del_multi(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("delm1")
    key2 = ctx.key("delm2")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", key1, "a", key2, "b"), "MSET")
        _assert_equal(client.send_command("DEL", key1, key2), 2, "DEL multi")


def _case_exists_single(ctx: RedisCaseContext) -> None:
    key = ctx.key("exists1")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v"), "SET")
        _assert_equal(client.send_command("EXISTS", key), 1, "EXISTS existing key")
        _assert_equal(client.send_command("EXISTS", ctx.key("missing")), 0, "EXISTS missing key")


def _case_exists_multi(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("existsm1")
    key2 = ctx.key("existsm2")
    missing = ctx.key("existsm3")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", key1, "a", key2, "b"), "MSET")
        _assert_equal(client.send_command("EXISTS", key1, key2, missing), 2, "EXISTS multi")


def _case_echo_basic(ctx: RedisCaseContext) -> None:
    message = f"hello:{ctx.token}"
    with ctx.client() as client:
        _assert_equal(client.send_command("ECHO", message), message, "ECHO")


def _case_command_response(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("COMMAND")
        _assert(isinstance(reply, list), f"COMMAND: expected array reply, got {reply!r}")


def _case_error_unknown_command(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("NOTACMD", expect_error=True)
        _assert(isinstance(reply, RespErrorReply), f"unknown command: expected error, got {reply!r}")
        _assert(reply.message, "unknown command: expected non-empty error message")


def _case_set_ex(ctx: RedisCaseContext) -> None:
    key = ctx.key("setex")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1", "EX", 1), "SET EX")
        _assert_equal(client.send_command("GET", key), "v1", "GET before EX expiry")
        ctx.sleep(1.2)
        _assert_equal(client.send_command("GET", key), None, "GET after EX expiry")


def _case_set_px(ctx: RedisCaseContext) -> None:
    key = ctx.key("setpx")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1", "PX", 150), "SET PX")
        _assert_equal(client.send_command("GET", key), "v1", "GET before PX expiry")
        ctx.sleep(0.3)
        _assert_equal(client.send_command("GET", key), None, "GET after PX expiry")


def _case_set_nx(ctx: RedisCaseContext) -> None:
    key = ctx.key("setnxopt")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1", "NX"), "SET NX first")
        _assert_equal(client.send_command("SET", key, "v2", "NX"), None, "SET NX existing key")
        _assert_equal(client.send_command("GET", key), "v1", "SET NX preserves old value")


def _case_set_xx(ctx: RedisCaseContext) -> None:
    key = ctx.key("setxxopt")
    with ctx.client() as client:
        _assert_equal(client.send_command("SET", key, "v1", "XX"), None, "SET XX missing key")
        _expect_ok(client.send_command("SET", key, "v1"), "SET baseline")
        _expect_ok(client.send_command("SET", key, "v2", "XX"), "SET XX existing key")
        _assert_equal(client.send_command("GET", key), "v2", "SET XX updated value")


def _case_setnx_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("setnx")
    with ctx.client() as client:
        _assert_equal(client.send_command("SETNX", key, "v1"), 1, "SETNX first write")
        _assert_equal(client.send_command("SETNX", key, "v2"), 0, "SETNX existing key")


def _case_setex_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("setex-basic")
    with ctx.client() as client:
        _expect_ok(client.send_command("SETEX", key, 1, "v1"), "SETEX")
        _assert_equal(client.send_command("GET", key), "v1", "GET after SETEX")
        ctx.sleep(1.2)
        _assert_equal(client.send_command("GET", key), None, "SETEX expiry")


def _case_getset_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("getset")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET baseline")
        _assert_equal(client.send_command("GETSET", key, "v2"), "v1", "GETSET old value")
        _assert_equal(client.send_command("GET", key), "v2", "GETSET new value")


def _case_incr_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("incr")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, 1), "SET numeric")
        _assert_equal(client.send_command("INCR", key), 2, "INCR")


def _case_decr_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("decr")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, 3), "SET numeric")
        _assert_equal(client.send_command("DECR", key), 2, "DECR")


def _case_incrby_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("incrby")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, 2), "SET numeric")
        _assert_equal(client.send_command("INCRBY", key, 5), 7, "INCRBY")


def _case_decrby_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("decrby")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, 10), "SET numeric")
        _assert_equal(client.send_command("DECRBY", key, 4), 6, "DECRBY")


def _case_incrbyfloat_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("incrbyfloat")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "1.5"), "SET float")
        reply = client.send_command("INCRBYFLOAT", key, "0.5")
        _assert(abs(_to_float(reply, "INCRBYFLOAT") - 2.0) < 1e-6, f"INCRBYFLOAT: expected 2.0, got {reply!r}")


def _case_append_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("append")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "hello"), "SET")
        _assert_equal(client.send_command("APPEND", key, "world"), 10, "APPEND length")
        _assert_equal(client.send_command("GET", key), "helloworld", "APPEND result")


def _case_strlen_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("strlen")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "hello"), "SET")
        _assert_equal(client.send_command("STRLEN", key), 5, "STRLEN")


def _case_mget_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("mget1")
    key2 = ctx.key("mget2")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", key1, "a", key2, "b"), "MSET")
        reply = client.send_command("MGET", key1, key2, ctx.key("missing"))
        _assert_equal(reply, ["a", "b", None], "MGET")


def _case_mset_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("mset1")
    key2 = ctx.key("mset2")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", key1, "a", key2, "b"), "MSET")
        _assert_equal(client.send_command("GET", key1), "a", "MSET key1")
        _assert_equal(client.send_command("GET", key2), "b", "MSET key2")


def _case_expire_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("expire")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("EXPIRE", key, 1), 1, "EXPIRE")
        ctx.sleep(1.2)
        _assert_equal(client.send_command("GET", key), None, "GET after EXPIRE")


def _case_ttl_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("ttl")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("EXPIRE", key, 5), 1, "EXPIRE")
        ttl = _to_int(client.send_command("TTL", key), "TTL")
        _assert(0 < ttl <= 5, f"TTL: expected positive value <= 5, got {ttl}")


def _case_pttl_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("pttl")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("PEXPIRE", key, 500), 1, "PEXPIRE")
        ttl = _to_int(client.send_command("PTTL", key), "PTTL")
        _assert(0 < ttl <= 500, f"PTTL: expected positive value <= 500, got {ttl}")


def _case_persist_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("persist")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("EXPIRE", key, 5), 1, "EXPIRE")
        _assert_equal(client.send_command("PERSIST", key), 1, "PERSIST")
        _assert_equal(client.send_command("TTL", key), -1, "TTL after PERSIST")


def _case_keys_pattern(ctx: RedisCaseContext) -> None:
    prefix = ctx.key("keys")
    key1 = f"{prefix}:a"
    key2 = f"{prefix}:b"
    other = ctx.key("other")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", key1, "1", key2, "2", other, "3"), "MSET")
        reply = client.send_command("KEYS", f"{prefix}:*")
        _assert(set(_as_str_list(reply)) == {key1, key2}, f"KEYS pattern: expected only prefixed keys, got {reply!r}")


def _case_type_string(ctx: RedisCaseContext) -> None:
    key = ctx.key("type")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("TYPE", key), "string", "TYPE string")


def _case_rename_basic(ctx: RedisCaseContext) -> None:
    old = ctx.key("rename-old")
    new = ctx.key("rename-new")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", old, "v1"), "SET")
        _expect_ok(client.send_command("RENAME", old, new), "RENAME")
        _assert_equal(client.send_command("GET", old), None, "RENAME removed old key")
        _assert_equal(client.send_command("GET", new), "v1", "RENAME new key")


def _case_dbsize_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("dbsize1")
    key2 = ctx.key("dbsize2")
    with ctx.client() as client:
        before = _to_int(client.send_command("DBSIZE"), "DBSIZE before")
        _expect_ok(client.send_command("MSET", key1, "1", key2, "2"), "MSET")
        after = _to_int(client.send_command("DBSIZE"), "DBSIZE after")
        _assert(after >= before + 2, f"DBSIZE: expected delta >= 2, got before={before}, after={after}")


def _case_lpush_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lpush")
    with ctx.client() as client:
        _assert_equal(client.send_command("LPUSH", key, "a", "b"), 2, "LPUSH")
        _assert_equal(client.send_command("LRANGE", key, 0, -1), ["b", "a"], "LPUSH order")


def _case_rpush_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-rpush")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b"), 2, "RPUSH")
        _assert_equal(client.send_command("LRANGE", key, 0, -1), ["a", "b"], "RPUSH order")


def _case_lpop_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lpop")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b"), 2, "RPUSH")
        _assert_equal(client.send_command("LPOP", key), "a", "LPOP")


def _case_rpop_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-rpop")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b"), 2, "RPUSH")
        _assert_equal(client.send_command("RPOP", key), "b", "RPOP")


def _case_llen_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-llen")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b", "c"), 3, "RPUSH")
        _assert_equal(client.send_command("LLEN", key), 3, "LLEN")


def _case_lrange_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lrange")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b", "c"), 3, "RPUSH")
        _assert_equal(client.send_command("LRANGE", key, 0, 1), ["a", "b"], "LRANGE")


def _case_lindex_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lindex")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b"), 2, "RPUSH")
        _assert_equal(client.send_command("LINDEX", key, 1), "b", "LINDEX")


def _case_lset_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lset")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b"), 2, "RPUSH")
        _expect_ok(client.send_command("LSET", key, 1, "z"), "LSET")
        _assert_equal(client.send_command("LINDEX", key, 1), "z", "LSET result")


def _case_linsert_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-linsert")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "c"), 2, "RPUSH")
        _assert_equal(client.send_command("LINSERT", key, "BEFORE", "c", "b"), 3, "LINSERT")
        _assert_equal(client.send_command("LRANGE", key, 0, -1), ["a", "b", "c"], "LINSERT order")


def _case_lrem_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("list-lrem")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", key, "a", "b", "a", "c"), 4, "RPUSH")
        _assert_equal(client.send_command("LREM", key, 0, "a"), 2, "LREM removed count")
        _assert_equal(client.send_command("LRANGE", key, 0, -1), ["b", "c"], "LREM result")


def _case_rpoplpush_basic(ctx: RedisCaseContext) -> None:
    src = ctx.key("list-src")
    dst = ctx.key("list-dst")
    with ctx.client() as client:
        _assert_equal(client.send_command("RPUSH", src, "a", "b"), 2, "RPUSH src")
        _assert_equal(client.send_command("RPOPLPUSH", src, dst), "b", "RPOPLPUSH")
        _assert_equal(client.send_command("LRANGE", src, 0, -1), ["a"], "RPOPLPUSH src state")
        _assert_equal(client.send_command("LRANGE", dst, 0, -1), ["b"], "RPOPLPUSH dst state")


def _case_hset_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hset")
    with ctx.client() as client:
        _assert_equal(client.send_command("HSET", key, "field", "value"), 1, "HSET")
        _assert_equal(client.send_command("HGET", key, "field"), "value", "HSET value")


def _case_hget_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hget")
    with ctx.client() as client:
        _assert_equal(client.send_command("HSET", key, "field", "value"), 1, "HSET")
        _assert_equal(client.send_command("HGET", key, "field"), "value", "HGET")


def _case_hdel_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hdel")
    with ctx.client() as client:
        _assert_equal(client.send_command("HSET", key, "field", "value"), 1, "HSET")
        _assert_equal(client.send_command("HDEL", key, "field"), 1, "HDEL")
        _assert_equal(client.send_command("HGET", key, "field"), None, "HDEL removed field")


def _case_hexists_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hexists")
    with ctx.client() as client:
        _assert_equal(client.send_command("HSET", key, "field", "value"), 1, "HSET")
        _assert_equal(client.send_command("HEXISTS", key, "field"), 1, "HEXISTS existing")
        _assert_equal(client.send_command("HEXISTS", key, "missing"), 0, "HEXISTS missing")


def _case_hgetall_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hgetall")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        reply = client.send_command("HGETALL", key)
        _assert_equal(_pairs_to_dict(reply, "HGETALL"), {"a": "1", "b": "2"}, "HGETALL")


def _case_hmset_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hmset")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        _assert_equal(client.send_command("HMGET", key, "a", "b"), ["1", "2"], "HMSET values")


def _case_hmget_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hmget")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        _assert_equal(client.send_command("HMGET", key, "a", "b", "c"), ["1", "2", None], "HMGET")


def _case_hincrby_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hincr")
    with ctx.client() as client:
        _assert_equal(client.send_command("HSET", key, "field", 1), 1, "HSET")
        _assert_equal(client.send_command("HINCRBY", key, "field", 4), 5, "HINCRBY")


def _case_hkeys_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hkeys")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        _assert(set(_as_str_list(client.send_command("HKEYS", key))) == {"a", "b"}, "HKEYS")


def _case_hvals_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hvals")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        _assert(set(_as_str_list(client.send_command("HVALS", key))) == {"1", "2"}, "HVALS")


def _case_hlen_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hash-hlen")
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2"), "HMSET")
        _assert_equal(client.send_command("HLEN", key), 2, "HLEN")


def _case_sadd_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-sadd")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        _assert_equal(client.send_command("SISMEMBER", key, "a"), 1, "SADD membership")


def _case_srem_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-srem")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        _assert_equal(client.send_command("SREM", key, "a"), 1, "SREM")
        _assert_equal(client.send_command("SISMEMBER", key, "a"), 0, "SREM removed member")


def _case_smembers_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-smembers")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        _assert(set(_as_str_list(client.send_command("SMEMBERS", key))) == {"a", "b"}, "SMEMBERS")


def _case_sismember_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-sismember")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a"), 1, "SADD")
        _assert_equal(client.send_command("SISMEMBER", key, "a"), 1, "SISMEMBER existing")
        _assert_equal(client.send_command("SISMEMBER", key, "b"), 0, "SISMEMBER missing")


def _case_scard_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-scard")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        _assert_equal(client.send_command("SCARD", key), 2, "SCARD")


def _case_sunion_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("set-sunion1")
    key2 = ctx.key("set-sunion2")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key1, "a", "b"), 2, "SADD key1")
        _assert_equal(client.send_command("SADD", key2, "b", "c"), 2, "SADD key2")
        _assert(set(_as_str_list(client.send_command("SUNION", key1, key2))) == {"a", "b", "c"}, "SUNION")


def _case_sinter_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("set-sinter1")
    key2 = ctx.key("set-sinter2")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key1, "a", "b"), 2, "SADD key1")
        _assert_equal(client.send_command("SADD", key2, "b", "c"), 2, "SADD key2")
        _assert(set(_as_str_list(client.send_command("SINTER", key1, key2))) == {"b"}, "SINTER")


def _case_sdiff_basic(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("set-sdiff1")
    key2 = ctx.key("set-sdiff2")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key1, "a", "b"), 2, "SADD key1")
        _assert_equal(client.send_command("SADD", key2, "b", "c"), 2, "SADD key2")
        _assert(set(_as_str_list(client.send_command("SDIFF", key1, key2))) == {"a"}, "SDIFF")


def _case_spop_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-spop")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        popped = client.send_command("SPOP", key)
        _assert_in(popped, {"a", "b"}, "SPOP member")
        _assert_equal(client.send_command("SCARD", key), 1, "SPOP cardinality")


def _case_srandmember_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("set-srand")
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, "a", "b"), 2, "SADD")
        member = client.send_command("SRANDMEMBER", key)
        _assert_in(member, {"a", "b"}, "SRANDMEMBER")


def _case_zadd_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zadd")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZRANGE", key, 0, -1), ["one", "two"], "ZADD ordering")


def _case_zrem_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zrem")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZREM", key, "one"), 1, "ZREM")
        _assert_equal(client.send_command("ZRANGE", key, 0, -1), ["two"], "ZREM result")


def _case_zscore_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zscore")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one"), 1, "ZADD")
        _assert(abs(_to_float(client.send_command("ZSCORE", key, "one"), "ZSCORE") - 1.0) < 1e-6, "ZSCORE value")


def _case_zrank_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zrank")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZRANK", key, "two"), 1, "ZRANK")


def _case_zrange_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zrange")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZRANGE", key, 0, -1), ["one", "two"], "ZRANGE")


def _case_zrevrange_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zrevrange")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZREVRANGE", key, 0, -1), ["two", "one"], "ZREVRANGE")


def _case_zrangebyscore_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zrangebyscore")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two", 3, "three"), 3, "ZADD")
        _assert_equal(client.send_command("ZRANGEBYSCORE", key, 1, 2), ["one", "two"], "ZRANGEBYSCORE")


def _case_zcard_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zcard")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        _assert_equal(client.send_command("ZCARD", key), 2, "ZCARD")


def _case_zcount_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zcount")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two", 3, "three"), 3, "ZADD")
        _assert_equal(client.send_command("ZCOUNT", key, 1, 2), 2, "ZCOUNT")


def _case_zincrby_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zincrby")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one"), 1, "ZADD")
        reply = client.send_command("ZINCRBY", key, 1.5, "one")
        _assert(abs(_to_float(reply, "ZINCRBY") - 2.5) < 1e-6, "ZINCRBY result")


def _case_zpopmin_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zpopmin")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        reply = client.send_command("ZPOPMIN", key)
        _assert_equal(reply[:2], ["one", "1"], "ZPOPMIN result")


def _case_zpopmax_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zset-zpopmax")
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "one", 2, "two"), 2, "ZADD")
        reply = client.send_command("ZPOPMAX", key)
        _assert_equal(reply[:2], ["two", "2"], "ZPOPMAX result")


def _case_bgsave_basic(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("BGSAVE")
        _assert(isinstance(reply, str) and reply, f"BGSAVE: expected simple string reply, got {reply!r}")
        _assert(any(token in reply.lower() for token in ("background", "scheduled", "ok")), f"BGSAVE: unexpected reply {reply!r}")
        _wait_for_bgsave_idle(ctx, client)
        _assert_equal(client.send_command("PING"), "PONG", "PING after BGSAVE")


def _case_save_basic(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        try:
            _expect_ok(client.send_command("SAVE"), "SAVE")
        except RedisCommandError as exc:
            if "background save already in progress" not in str(exc).lower():
                raise
            _wait_for_bgsave_idle(ctx, client)
            _expect_ok(client.send_command("SAVE"), "SAVE retry")
        _assert_equal(client.send_command("PING"), "PONG", "PING after SAVE")


def _case_subscribe_publish_basic(ctx: RedisCaseContext) -> None:
    channel = ctx.key("pubsub")
    payload = f"msg:{ctx.token}"
    with ctx.client() as sub_client, ctx.client() as pub_client:
        ack = sub_client.send_command("SUBSCRIBE", channel)
        _assert_equal(ack, ["subscribe", channel, 1], "SUBSCRIBE ack")
        _assert_equal(pub_client.send_command("PUBLISH", channel, payload), 1, "PUBLISH subscriber count")
        message = sub_client.read_reply()
        _assert_equal(message, ["message", channel, payload], "SUBSCRIBE message")
        _assert_equal(sub_client.send_command("UNSUBSCRIBE", channel), ["unsubscribe", channel, 0], "UNSUBSCRIBE cleanup")


def _case_psubscribe_basic(ctx: RedisCaseContext) -> None:
    channel = ctx.key("pchan")
    pattern = f"{ctx.key('pchan')}:*"
    target = f"{channel}:1"
    payload = f"msg:{ctx.token}"
    with ctx.client() as sub_client, ctx.client() as pub_client:
        ack = sub_client.send_command("PSUBSCRIBE", pattern)
        _assert_equal(ack, ["psubscribe", pattern, 1], "PSUBSCRIBE ack")
        _assert_equal(pub_client.send_command("PUBLISH", target, payload), 1, "PUBLISH psubscriber count")
        message = sub_client.read_reply()
        _assert_equal(message, ["pmessage", pattern, target, payload], "PSUBSCRIBE message")
        _assert_equal(sub_client.send_command("PUNSUBSCRIBE", pattern), ["punsubscribe", pattern, 0], "PUNSUBSCRIBE cleanup")


def _case_unsubscribe_basic(ctx: RedisCaseContext) -> None:
    channel = ctx.key("unsubscribe")
    with ctx.client() as client:
        _assert_equal(client.send_command("SUBSCRIBE", channel), ["subscribe", channel, 1], "SUBSCRIBE ack")
        _assert_equal(client.send_command("UNSUBSCRIBE", channel), ["unsubscribe", channel, 0], "UNSUBSCRIBE ack")


def _case_pubsub_channels(ctx: RedisCaseContext) -> None:
    channel = ctx.key("channels")
    with ctx.client() as sub_client, ctx.client() as client:
        _assert_equal(sub_client.send_command("SUBSCRIBE", channel), ["subscribe", channel, 1], "SUBSCRIBE ack")
        channels = client.send_command("PUBSUB", "CHANNELS", f"{channel}*")
        _assert(channel in _as_str_list(channels), f"PUBSUB CHANNELS: expected {channel!r}, got {channels!r}")
        _assert_equal(sub_client.send_command("UNSUBSCRIBE", channel), ["unsubscribe", channel, 0], "UNSUBSCRIBE cleanup")


def _case_multi_exec_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("multi-exec")
    with ctx.client() as client:
        _expect_ok(client.send_command("MULTI"), "MULTI")
        _assert_equal(client.send_command("SET", key, "v1"), "QUEUED", "SET queued")
        _assert_equal(client.send_command("GET", key), "QUEUED", "GET queued")
        _assert_equal(client.send_command("EXEC"), ["OK", "v1"], "EXEC replies")


def _case_multi_discard_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("multi-discard")
    with ctx.client() as client:
        _expect_ok(client.send_command("MULTI"), "MULTI")
        _assert_equal(client.send_command("SET", key, "v1"), "QUEUED", "SET queued")
        _expect_ok(client.send_command("DISCARD"), "DISCARD")
        _assert_equal(client.send_command("GET", key), None, "DISCARD rolled back transaction")


def _case_watch_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("watch")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET baseline")
        _expect_ok(client.send_command("WATCH", key), "WATCH")
        _expect_ok(client.send_command("MULTI"), "MULTI")
        _assert_equal(client.send_command("SET", key, "v2"), "QUEUED", "SET queued")
        _assert_equal(client.send_command("EXEC"), ["OK"], "EXEC after WATCH")
        _assert_equal(client.send_command("GET", key), "v2", "WATCH preserved update")


def _case_watch_modified(ctx: RedisCaseContext) -> None:
    key = ctx.key("watch-mod")
    with ctx.client() as client1, ctx.client() as client2:
        _expect_ok(client1.send_command("SET", key, "v1"), "SET baseline")
        _expect_ok(client1.send_command("WATCH", key), "WATCH")
        _expect_ok(client2.send_command("SET", key, "v2"), "SET external modification")
        _expect_ok(client1.send_command("MULTI"), "MULTI")
        _assert_equal(client1.send_command("SET", key, "v3"), "QUEUED", "SET queued")
        _assert_equal(client1.send_command("EXEC"), None, "EXEC should abort after WATCH violation")


def _case_select_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("select")
    with ctx.client() as client:
        _expect_ok(client.send_command("SELECT", 0), "SELECT 0")
        _expect_ok(client.send_command("SET", key, "db0"), "SET db0")
        _expect_ok(client.send_command("SELECT", 1), "SELECT 1")
        _assert_equal(client.send_command("GET", key), None, "GET in db1 before SET")
        _expect_ok(client.send_command("SET", key, "db1"), "SET db1")
        _expect_ok(client.send_command("SELECT", 0), "SELECT back db0")
        _assert_equal(client.send_command("GET", key), "db0", "DB0 value")
        _expect_ok(client.send_command("SELECT", 1), "SELECT db1 again")
        _assert_equal(client.send_command("GET", key), "db1", "DB1 value")


def _case_flushdb_basic(ctx: RedisCaseContext) -> None:
    key0 = ctx.key("flushdb0")
    key1 = ctx.key("flushdb1")
    with ctx.client() as client:
        _expect_ok(client.send_command("SELECT", 0), "SELECT 0")
        _expect_ok(client.send_command("SET", key0, "db0"), "SET db0")
        _expect_ok(client.send_command("SELECT", 1), "SELECT 1")
        _expect_ok(client.send_command("SET", key1, "db1"), "SET db1")
        _expect_ok(client.send_command("FLUSHDB"), "FLUSHDB")
        _assert_equal(client.send_command("DBSIZE"), 0, "DBSIZE after FLUSHDB")
        _expect_ok(client.send_command("SELECT", 0), "SELECT 0 again")
        _assert_equal(client.send_command("GET", key0), "db0", "FLUSHDB isolation")


def _case_flushall_basic(ctx: RedisCaseContext) -> None:
    key0 = ctx.key("flushall0")
    key1 = ctx.key("flushall1")
    with ctx.client() as client:
        _expect_ok(client.send_command("SELECT", 0), "SELECT 0")
        _expect_ok(client.send_command("SET", key0, "db0"), "SET db0")
        _expect_ok(client.send_command("SELECT", 1), "SELECT 1")
        _expect_ok(client.send_command("SET", key1, "db1"), "SET db1")
        _expect_ok(client.send_command("FLUSHALL"), "FLUSHALL")
        _assert_equal(client.send_command("DBSIZE"), 0, "DBSIZE db1 after FLUSHALL")
        _expect_ok(client.send_command("SELECT", 0), "SELECT 0 again")
        _assert_equal(client.send_command("DBSIZE"), 0, "DBSIZE db0 after FLUSHALL")


def _case_pipeline_multi_commands(ctx: RedisCaseContext) -> None:
    key1 = ctx.key("pipe1")
    key2 = ctx.key("pipe2")
    with ctx.client() as client:
        replies = client.pipeline([
            ("SET", key1, "1"),
            ("SET", key2, "2"),
            ("MGET", key1, key2),
        ])
        _assert_equal(replies, ["OK", "OK", ["1", "2"]], "pipeline replies")


def _case_scan_basic(ctx: RedisCaseContext) -> None:
    prefix = ctx.key("scan")
    keys = [f"{prefix}:{idx}" for idx in range(3)]
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", *(item for key in keys for item in (key, "1"))), "MSET")
        found = _scan_collect(client, "SCAN", match=f"{prefix}:*", count=10)
        _assert(set(_as_str_list(found)) == set(keys), f"SCAN: expected {keys!r}, got {found!r}")


def _case_scan_match(ctx: RedisCaseContext) -> None:
    prefix = ctx.key("scan-match")
    keys = [f"{prefix}:{idx}" for idx in range(3)]
    other = ctx.key("scan-other")
    with ctx.client() as client:
        _expect_ok(client.send_command("MSET", *(item for key in keys for item in (key, "1")), other, "1"), "MSET")
        found = _scan_collect(client, "SCAN", match=f"{prefix}:*", count=10)
        _assert(set(_as_str_list(found)) == set(keys), f"SCAN MATCH: expected {keys!r}, got {found!r}")


def _case_scan_count(ctx: RedisCaseContext) -> None:
    prefix = ctx.key("scan-count")
    keys = [f"{prefix}:{idx}" for idx in range(20)]
    with ctx.client() as client:
        flat_args: List[Any] = []
        for key in keys:
            flat_args.extend([key, "1"])
        _expect_ok(client.send_command("MSET", *flat_args), "MSET")
        found = _scan_collect(client, "SCAN", match=f"{prefix}:*", count=5)
        _assert(set(_as_str_list(found)) == set(keys), f"SCAN COUNT: expected {len(keys)} keys, got {found!r}")


def _case_sscan_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("sscan")
    members = {"a", "b", "c"}
    with ctx.client() as client:
        _assert_equal(client.send_command("SADD", key, *sorted(members)), 3, "SADD")
        found = _scan_collect(client, "SSCAN", key, count=5)
        _assert(set(_as_str_list(found)) == members, f"SSCAN: expected {members!r}, got {found!r}")


def _case_hscan_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("hscan")
    expected = {"a": "1", "b": "2", "c": "3"}
    with ctx.client() as client:
        _expect_ok(client.send_command("HMSET", key, "a", "1", "b", "2", "c", "3"), "HMSET")
        found = _scan_collect(client, "HSCAN", key, count=5)
        _assert_equal(_pairs_to_dict(found, "HSCAN"), expected, "HSCAN")


def _case_zscan_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("zscan")
    expected = {"a": "1", "b": "2", "c": "3"}
    with ctx.client() as client:
        _assert_equal(client.send_command("ZADD", key, 1, "a", 2, "b", 3, "c"), 3, "ZADD")
        found = _scan_collect(client, "ZSCAN", key, count=5)
        _assert_equal(_pairs_to_dict(found, "ZSCAN"), expected, "ZSCAN")


def _case_info_basic(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("INFO")
        _assert(isinstance(reply, str) and reply.strip(), f"INFO: expected non-empty bulk string, got {reply!r}")
        _assert(":" in reply, f"INFO: expected key:value payload, got {reply!r}")


def _case_config_get_basic(ctx: RedisCaseContext) -> None:
    with ctx.client() as client:
        reply = client.send_command("CONFIG", "GET", "databases")
        _assert(isinstance(reply, list) and len(reply) == 2, f"CONFIG GET: expected 2-element array, got {reply!r}")
        _assert_equal(str(reply[0]).lower(), "databases", "CONFIG GET key")
        _assert(_to_int(reply[1], "CONFIG GET value") >= 16, f"CONFIG GET databases: expected >= 16, got {reply[1]!r}")


def _case_client_list_basic(ctx: RedisCaseContext) -> None:
    with ctx.client() as client1, ctx.client() as client2:
        reply = client1.send_command("CLIENT", "LIST")
        _assert(isinstance(reply, str) and reply.strip(), f"CLIENT LIST: expected non-empty bulk string, got {reply!r}")
        _assert(("addr=" in reply) or ("id=" in reply), f"CLIENT LIST: expected addr=/id= fields, got {reply!r}")


def _case_randomkey_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("randomkey")
    with ctx.client() as client:
        _expect_ok(client.send_command("FLUSHDB"), "FLUSHDB")
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        _assert_equal(client.send_command("RANDOMKEY"), key, "RANDOMKEY")


def _case_object_encoding_basic(ctx: RedisCaseContext) -> None:
    key = ctx.key("encoding")
    with ctx.client() as client:
        _expect_ok(client.send_command("SET", key, "v1"), "SET")
        reply = client.send_command("OBJECT", "ENCODING", key)
        _assert(isinstance(reply, str) and reply.strip(), f"OBJECT ENCODING: expected non-empty bulk string, got {reply!r}")


CASE_HANDLERS: Dict[str, Callable[[RedisCaseContext], None]] = {
    "protocol_inline_ping": _case_protocol_inline_ping,
    "protocol_bulk_ping": _case_protocol_bulk_ping,
    "set_get_basic": _case_set_get_basic,
    "del_single": _case_del_single,
    "del_multi": _case_del_multi,
    "exists_single": _case_exists_single,
    "exists_multi": _case_exists_multi,
    "echo_basic": _case_echo_basic,
    "command_response": _case_command_response,
    "error_unknown_command": _case_error_unknown_command,
    "set_ex": _case_set_ex,
    "set_px": _case_set_px,
    "set_nx": _case_set_nx,
    "set_xx": _case_set_xx,
    "setnx_basic": _case_setnx_basic,
    "setex_basic": _case_setex_basic,
    "getset_basic": _case_getset_basic,
    "incr_basic": _case_incr_basic,
    "decr_basic": _case_decr_basic,
    "incrby_basic": _case_incrby_basic,
    "decrby_basic": _case_decrby_basic,
    "incrbyfloat_basic": _case_incrbyfloat_basic,
    "append_basic": _case_append_basic,
    "strlen_basic": _case_strlen_basic,
    "mget_basic": _case_mget_basic,
    "mset_basic": _case_mset_basic,
    "expire_basic": _case_expire_basic,
    "ttl_basic": _case_ttl_basic,
    "pttl_basic": _case_pttl_basic,
    "persist_basic": _case_persist_basic,
    "keys_pattern": _case_keys_pattern,
    "type_string": _case_type_string,
    "rename_basic": _case_rename_basic,
    "dbsize_basic": _case_dbsize_basic,
    "lpush_basic": _case_lpush_basic,
    "rpush_basic": _case_rpush_basic,
    "lpop_basic": _case_lpop_basic,
    "rpop_basic": _case_rpop_basic,
    "llen_basic": _case_llen_basic,
    "lrange_basic": _case_lrange_basic,
    "lindex_basic": _case_lindex_basic,
    "lset_basic": _case_lset_basic,
    "linsert_basic": _case_linsert_basic,
    "lrem_basic": _case_lrem_basic,
    "rpoplpush_basic": _case_rpoplpush_basic,
    "hset_basic": _case_hset_basic,
    "hget_basic": _case_hget_basic,
    "hdel_basic": _case_hdel_basic,
    "hexists_basic": _case_hexists_basic,
    "hgetall_basic": _case_hgetall_basic,
    "hmset_basic": _case_hmset_basic,
    "hmget_basic": _case_hmget_basic,
    "hincrby_basic": _case_hincrby_basic,
    "hkeys_basic": _case_hkeys_basic,
    "hvals_basic": _case_hvals_basic,
    "hlen_basic": _case_hlen_basic,
    "sadd_basic": _case_sadd_basic,
    "srem_basic": _case_srem_basic,
    "smembers_basic": _case_smembers_basic,
    "sismember_basic": _case_sismember_basic,
    "scard_basic": _case_scard_basic,
    "sunion_basic": _case_sunion_basic,
    "sinter_basic": _case_sinter_basic,
    "sdiff_basic": _case_sdiff_basic,
    "spop_basic": _case_spop_basic,
    "srandmember_basic": _case_srandmember_basic,
    "zadd_basic": _case_zadd_basic,
    "zrem_basic": _case_zrem_basic,
    "zscore_basic": _case_zscore_basic,
    "zrank_basic": _case_zrank_basic,
    "zrange_basic": _case_zrange_basic,
    "zrevrange_basic": _case_zrevrange_basic,
    "zrangebyscore_basic": _case_zrangebyscore_basic,
    "zcard_basic": _case_zcard_basic,
    "zcount_basic": _case_zcount_basic,
    "zincrby_basic": _case_zincrby_basic,
    "zpopmin_basic": _case_zpopmin_basic,
    "zpopmax_basic": _case_zpopmax_basic,
    "bgsave_basic": _case_bgsave_basic,
    "save_basic": _case_save_basic,
    "subscribe_publish_basic": _case_subscribe_publish_basic,
    "psubscribe_basic": _case_psubscribe_basic,
    "unsubscribe_basic": _case_unsubscribe_basic,
    "pubsub_channels": _case_pubsub_channels,
    "multi_exec_basic": _case_multi_exec_basic,
    "multi_discard_basic": _case_multi_discard_basic,
    "watch_basic": _case_watch_basic,
    "watch_modified": _case_watch_modified,
    "select_basic": _case_select_basic,
    "flushdb_basic": _case_flushdb_basic,
    "flushall_basic": _case_flushall_basic,
    "pipeline_multi_commands": _case_pipeline_multi_commands,
    "scan_basic": _case_scan_basic,
    "scan_match": _case_scan_match,
    "scan_count": _case_scan_count,
    "sscan_basic": _case_sscan_basic,
    "hscan_basic": _case_hscan_basic,
    "zscan_basic": _case_zscan_basic,
    "info_basic": _case_info_basic,
    "config_get_basic": _case_config_get_basic,
    "client_list_basic": _case_client_list_basic,
    "randomkey_basic": _case_randomkey_basic,
    "object_encoding_basic": _case_object_encoding_basic,
}


def run_redis_case(
    case_id: str,
    host: str,
    port: int,
    timeout_sec: int,
    output_dir: Path,
) -> Dict[str, Any]:
    handler = CASE_HANDLERS.get(case_id)
    if handler is None:
        raise RedisCaseFailure(f"Unsupported redis conformance case: {case_id}")

    started = time.time()
    ctx = RedisCaseContext(
        host=host,
        port=port,
        deadline=started + max(1, timeout_sec),
        case_id=case_id,
        output_dir=output_dir,
        token=uuid.uuid4().hex[:8],
    )
    handler(ctx)
    return {"elapsed_sec": round(time.time() - started, 6)}
