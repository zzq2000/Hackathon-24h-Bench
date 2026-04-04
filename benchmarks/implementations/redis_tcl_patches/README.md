# Redis TCL Test Patches

This directory contains patches for the frozen Redis TCL test suite (tag: 7.2.4).

## Purpose

The official Redis TCL test suite (`tests/unit/`) is tightly coupled with
`redis-server`: it auto-starts/stops instances, uses `redis-cli`, and depends
on internal commands (`CONFIG SET`, `DEBUG OBJECT`, etc.).

These patches modify the test infrastructure to connect to an **external** server
(via `REDIS_HOST`/`REDIS_PORT` environment variables) instead of launching its own.

## Patch scope

| File (relative to Redis `tests/`) | Patch description |
|---|---|
| `support/server.tcl` | Skip redis-server startup/stop; connect to `$env(REDIS_HOST):$env(REDIS_PORT)` |
| `support/util.tcl` | Adjust `wait_for_condition` for external server |
| `support/tmpfile.tcl` | Write temp files to benchmark `output_dir` |

## Version binding

These patches are pinned to Redis tag `7.2.4`. They must be updated if the
frozen TCL version changes in `config/system.redis_kvstore.yaml`.
