#!/usr/bin/env bash
set -euo pipefail

cd /opt/ycsb

if [[ -x "./bin/ycsb.sh" ]]; then
  exec ./bin/ycsb.sh "$@"
fi

if [[ -x "./bin/ycsb" ]]; then
  exec ./bin/ycsb "$@"
fi

echo "YCSB entrypoint not found under /opt/ycsb/bin" >&2
exit 1
