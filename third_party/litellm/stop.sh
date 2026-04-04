#!/usr/bin/env bash
#
# Stop a background LiteLLM proxy (native or Docker).
#

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Stop Docker container if running ───────────────────────────
if docker ps -q --filter name=litellm-proxy 2>/dev/null | grep -q .; then
    echo "Stopping Docker container 'litellm-proxy' ..."
    docker stop litellm-proxy && docker rm litellm-proxy
    echo "Done."
fi

# ── Stop native background process ────────────────────────────
PID_FILE="$SCRIPT_DIR/litellm.pid"
if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping LiteLLM proxy (PID $PID) ..."
        kill "$PID"
        echo "Done."
    else
        echo "PID $PID is not running."
    fi
    rm -f "$PID_FILE"
else
    echo "No litellm.pid found. Nothing to stop."
fi
