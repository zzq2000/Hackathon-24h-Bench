#!/usr/bin/env bash
#
# Setup script for the LiteLLM proxy.
# Installs LiteLLM into the active Python environment and copies
# the .env template if one doesn't already exist.
#
# Usage:
#   ./setup.sh            # install litellm[proxy]
#   ./setup.sh --venv     # create a dedicated venv first
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

USE_VENV=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --venv)
            USE_VENV=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./setup.sh [--venv]"
            echo "  --venv   Create a dedicated .venv in this directory"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# ── Optionally create a dedicated venv ──────────────────────────
if $USE_VENV; then
    if [[ ! -d "$SCRIPT_DIR/.venv" ]]; then
        echo "Creating virtual environment in $SCRIPT_DIR/.venv ..."
        python3 -m venv "$SCRIPT_DIR/.venv"
    fi
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/.venv/bin/activate"
    echo "Activated venv: $SCRIPT_DIR/.venv"
fi

# ── Install LiteLLM with proxy extras ──────────────────────────
echo "Installing litellm[proxy] ..."
pip install --quiet --upgrade 'litellm[proxy]'

# ── Verify installation ────────────────────────────────────────
if command -v litellm &>/dev/null; then
    echo "litellm installed: $(litellm --version 2>/dev/null || echo 'ok')"
else
    echo "Warning: litellm binary not found on PATH."
    echo "You may need to activate your venv or add pip's bin dir to PATH."
fi

# ── Seed .env from template if missing ─────────────────────────
if [[ ! -f "$SCRIPT_DIR/.env" ]]; then
    if [[ -f "$SCRIPT_DIR/.env.example" ]]; then
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        echo "Created .env from .env.example — edit it with your Azure credentials."
    else
        echo "No .env.example found; skipping .env creation."
    fi
else
    echo ".env already exists — skipping."
fi

echo ""
echo "Setup complete.  Next steps:"
echo "  1. Edit .env with your Azure OpenAI credentials"
echo "  2. Run:  ./run.sh"
