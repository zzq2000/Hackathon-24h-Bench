#!/usr/bin/env bash
#
# Start the LiteLLM proxy server.
#
# This translates Azure OpenAI endpoints into standard OpenAI-compatible
# endpoints so that any tool expecting OPENAI_API_BASE / OPENAI_API_KEY
# can work transparently.
#
# Usage:
#   ./run.sh                 # foreground, default port 4000
#   ./run.sh --port 8000     # custom port
#   ./run.sh --background    # run in background (nohup)
#   ./run.sh --docker        # run via Docker instead of pip install
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT=4000
HOST="0.0.0.0"
BACKGROUND=false
USE_DOCKER=false
CONFIG="$SCRIPT_DIR/config.yaml"
LOG_FILE="$SCRIPT_DIR/litellm.log"

show_help() {
    cat <<'EOF'
Usage: ./run.sh [options]

Options:
  --port <port>       Port to listen on (default: 4000)
  --host <host>       Host to bind to (default: 0.0.0.0)
  --background        Run the proxy in the background via nohup
  --docker            Run the proxy inside a Docker container
  --config <path>     Path to LiteLLM config file (default: ./config.yaml)
  --help, -h          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --port)       PORT="$2";       shift 2 ;;
        --host)       HOST="$2";       shift 2 ;;
        --background) BACKGROUND=true; shift   ;;
        --docker)     USE_DOCKER=true; shift   ;;
        --config)     CONFIG="$2";     shift 2 ;;
        -h|--help)    show_help;       exit 0  ;;
        *)            echo "Unknown option: $1"; exit 1 ;;
    esac
done

# ── Load .env if present ───────────────────────────────────────
if [[ -f "$SCRIPT_DIR/.env" ]]; then
    echo "Loading environment from .env ..."
    set -a
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/.env"
    set +a
fi

# ── Validate required env vars ─────────────────────────────────
missing=()
for var in AZURE_API_KEY AZURE_API_BASE AZURE_API_VERSION; do
    if [[ -z "${!var:-}" ]]; then
        missing+=("$var")
    fi
done

if [[ ${#missing[@]} -gt 0 ]]; then
    echo "ERROR: Missing required environment variables:"
    printf '  %s\n' "${missing[@]}"
    echo ""
    echo "Set them in .env or export them before running this script."
    exit 1
fi

# Default master key if not set
export LITELLM_MASTER_KEY="${LITELLM_MASTER_KEY:-sk-litellm-proxy}"

# ── Activate local venv if it exists ───────────────────────────
if [[ -d "$SCRIPT_DIR/.venv" ]]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/.venv/bin/activate"
fi

# ── Docker mode ────────────────────────────────────────────────
if $USE_DOCKER; then
    echo "Starting LiteLLM proxy via Docker on port $PORT ..."
    docker run -d \
        --name litellm-proxy \
        --restart unless-stopped \
        -p "$PORT:4000" \
        -v "$CONFIG:/app/config.yaml" \
        -e AZURE_API_KEY="$AZURE_API_KEY" \
        -e AZURE_API_BASE="$AZURE_API_BASE" \
        -e AZURE_API_VERSION="$AZURE_API_VERSION" \
        -e LITELLM_MASTER_KEY="$LITELLM_MASTER_KEY" \
        ghcr.io/berriai/litellm:main-latest \
        --config /app/config.yaml --host 0.0.0.0 --port 4000
    echo ""
    echo "LiteLLM proxy running in Docker container 'litellm-proxy'."
    echo "  Endpoint:  http://localhost:$PORT"
    echo "  Master key: $LITELLM_MASTER_KEY"
    echo ""
    echo "Stop with:  docker stop litellm-proxy && docker rm litellm-proxy"
    exit 0
fi

# ── Native mode ────────────────────────────────────────────────
if ! command -v litellm &>/dev/null; then
    echo "ERROR: litellm not found. Run ./setup.sh first."
    exit 1
fi

echo "Starting LiteLLM proxy on $HOST:$PORT ..."
echo "  Config:     $CONFIG"
echo "  Master key: $LITELLM_MASTER_KEY"
echo ""

if $BACKGROUND; then
    nohup litellm --config "$CONFIG" --host "$HOST" --port "$PORT" \
        > "$LOG_FILE" 2>&1 &
    PID=$!
    echo "$PID" > "$SCRIPT_DIR/litellm.pid"
    echo "LiteLLM proxy started in background (PID $PID)."
    echo "  Log:  $LOG_FILE"
    echo "  Stop: kill \$(cat litellm.pid)"
else
    exec litellm --config "$CONFIG" --host "$HOST" --port "$PORT"
fi
