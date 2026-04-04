#!/usr/bin/env bash
#
# Hackathon-24h-Bench one-click setup for environments with Python and Docker.
#
# What this script does:
# 1. Creates/reuses a Python environment (conda preferred, venv as fallback)
# 2. Installs Python dependencies
# 3. Verifies Docker CLI + daemon access
# 4. Pulls required benchmark images (optional)
# 5. Initializes required project directories and .env template
#
# Usage:
#   ./setup.sh
#   ./setup.sh --venv                  # Force venv even if conda is available
#   ./setup.sh --env-name dbbench --python-version 3.10
#   ./setup.sh --skip-docker-pull
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ENV_NAME="hackathon-24h-bench"
PYTHON_VERSION="3.10"
SKIP_DOCKER_PULL=false
INSTALL_AGENT_CLI=false
FORCE_VENV=false
VENV_DIR=".venv"
NPM_USER_PREFIX="${NPM_USER_PREFIX:-$HOME/.local/hackathon-24h-bench/npm}"
NPM_USER_BIN="$NPM_USER_PREFIX/bin"

show_help() {
    cat <<'EOF'
Usage: ./setup.sh [options]

Options:
  --env-name <name>         Conda env name (default: hackathon-24h-bench)
  --python-version <ver>    Python version for conda env (default: 3.10)
  --venv                    Force using Python venv instead of conda
  --venv-dir <path>         venv directory (default: .venv)
  --skip-docker-pull        Skip docker pull for benchmark images
  --install-agent-cli       Install agent CLIs (codex/claude/gemini/kimi) on host
                            (not needed when running agents in Docker, which is the default)
  --help, -h                Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --env-name)
            ENV_NAME="$2"
            shift 2
            ;;
        --python-version)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        --venv)
            FORCE_VENV=true
            shift
            ;;
        --venv-dir)
            FORCE_VENV=true
            VENV_DIR="$2"
            shift 2
            ;;
        --skip-docker-pull)
            SKIP_DOCKER_PULL=true
            shift
            ;;
        --install-agent-cli)
            INSTALL_AGENT_CLI=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Error: unknown option $1"
            show_help
            exit 1
            ;;
    esac
done

# Decide whether to use conda or venv
USE_CONDA=false
if [ "$FORCE_VENV" = false ] && command -v conda >/dev/null 2>&1; then
    USE_CONDA=true
fi

echo "=========================================="
echo "Hackathon-24h-Bench environment setup"
echo "=========================================="
if [ "$USE_CONDA" = true ]; then
    echo "Python env:       conda ($ENV_NAME)"
else
    echo "Python env:       venv ($VENV_DIR)"
fi
echo "Python version:   $PYTHON_VERSION"
echo "Skip docker pull: $SKIP_DOCKER_PULL"
echo "Install agent CLI: $INSTALL_AGENT_CLI"
echo "NPM user prefix:  $NPM_USER_PREFIX"
echo "=========================================="

if [ "$USE_CONDA" = true ]; then
    # --- Conda path ---
    CONDA_BASE="$(conda info --base)"
    # shellcheck disable=SC1091
    source "$CONDA_BASE/etc/profile.d/conda.sh"

    if conda env list | awk '{print $1}' | grep -Fxq "$ENV_NAME"; then
        echo "Conda env '$ENV_NAME' already exists, reusing it."
    else
        echo "Creating conda env '$ENV_NAME' with python=$PYTHON_VERSION ..."
        conda create -y -n "$ENV_NAME" "python=$PYTHON_VERSION"
    fi

    echo "Activating conda env '$ENV_NAME' ..."
    conda activate "$ENV_NAME"
else
    # --- venv path ---
    PYTHON_BIN=""
    for candidate in "python${PYTHON_VERSION}" "python3" "python"; do
        if command -v "$candidate" >/dev/null 2>&1; then
            PYTHON_BIN="$candidate"
            break
        fi
    done

    if [ -z "$PYTHON_BIN" ]; then
        echo "Error: no python interpreter found."
        echo "Please install Python >= $PYTHON_VERSION, or install conda."
        exit 1
    fi

    echo "Using Python: $($PYTHON_BIN --version 2>&1)"

    if [ -d "$VENV_DIR" ]; then
        echo "venv '$VENV_DIR' already exists, reusing it."
    else
        echo "Creating venv at '$VENV_DIR' ..."
        "$PYTHON_BIN" -m venv "$VENV_DIR"
    fi

    echo "Activating venv '$VENV_DIR' ..."
    # shellcheck disable=SC1091
    source "$VENV_DIR/bin/activate"
fi

echo "Installing Python dependencies ..."
python -m pip install --upgrade pip
pip install -r requirements.txt

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: docker command not found."
    echo "Please install Docker Engine/Desktop and retry."
    exit 1
fi

echo "Checking Docker daemon ..."
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker daemon is not accessible."
    echo "Please start Docker and ensure your user has permission."
    exit 1
fi

if [ "$SKIP_DOCKER_PULL" = false ]; then
    echo "Pulling benchmark images ..."
    docker pull severalnines/sysbench:latest
    docker pull tpcorg/hammerdb:v4.9
fi

install_agent_cli_if_missing() {
    local binary_name="$1"
    local npm_package="$2"

    if [ -x "$NPM_USER_BIN/$binary_name" ]; then
        echo "Agent CLI '$binary_name' already installed in user prefix."
        return 0
    fi

    if command -v "$binary_name" >/dev/null 2>&1; then
        echo "Agent CLI '$binary_name' already installed."
        return 0
    fi

    echo "Installing '$binary_name' for current user via npm package '$npm_package' ..."
    npm install --global --prefix "$NPM_USER_PREFIX" "$npm_package"
}

install_kimi_cli_if_missing() {
    if command -v kimi >/dev/null 2>&1; then
        echo "Agent CLI 'kimi' already installed."
        return 0
    fi

    echo "Installing 'kimi' via official installer ..."
    curl -fsSL https://code.kimi.com/install.sh | bash

    if [ -x "$HOME/.local/bin/kimi" ]; then
        export PATH="$HOME/.local/bin:$PATH"
        return 0
    fi

    if command -v kimi >/dev/null 2>&1; then
        return 0
    fi

    echo "Error: kimi install finished but 'kimi' command was not found."
    echo "Please check installer output and ensure ~/.local/bin is in PATH."
    exit 1
}

persist_user_bin_path() {
    local shell_name
    local rc_file
    local export_line

    shell_name="$(basename "${SHELL:-bash}")"
    case "$shell_name" in
        zsh)
            rc_file="$HOME/.zshrc"
            ;;
        *)
            rc_file="$HOME/.bashrc"
            ;;
    esac

    export_line="export PATH=\"$NPM_USER_BIN:\$PATH\""
    if [ ! -f "$rc_file" ]; then
        touch "$rc_file"
    fi

    if grep -Fqx "$export_line" "$rc_file"; then
        echo "PATH entry already exists in $rc_file"
    else
        {
            echo ""
            echo "# Added by Hackathon-24h-Bench setup.sh"
            echo "$export_line"
        } >> "$rc_file"
        echo "Added PATH entry to $rc_file"
    fi

    export_line="export PATH=\"$HOME/.local/bin:\$PATH\""
    if grep -Fqx "$export_line" "$rc_file"; then
        echo "PATH entry already exists in $rc_file"
    else
        {
            echo ""
            echo "# Added by Hackathon-24h-Bench setup.sh"
            echo "$export_line"
        } >> "$rc_file"
        echo "Added PATH entry to $rc_file"
    fi
}

ensure_node_runtime() {
    local node_version
    local node_major

    if command -v node >/dev/null 2>&1; then
        node_version="$(node -v)"
        node_major="${node_version#v}"
        node_major="${node_major%%.*}"
        if [ "$node_major" -ge 22 ]; then
            echo "Node.js version $node_version detected (>= 22)."
            return 0
        fi
        echo "Node.js version $node_version detected (< 22), upgrading via nvm."
    else
        echo "Node.js not found, installing via nvm."
    fi

    if ! command -v curl >/dev/null 2>&1; then
        echo "Error: curl command not found."
        echo "Please install curl first, then rerun setup."
        exit 1
    fi

    export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
    if [ ! -s "$NVM_DIR/nvm.sh" ]; then
        echo "Installing nvm ..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
    fi

    # shellcheck disable=SC1090
    source "$NVM_DIR/nvm.sh"
    nvm install 22
    nvm use 22
    nvm alias default 22
}

if [ "$INSTALL_AGENT_CLI" = true ]; then
    ensure_node_runtime
    if ! command -v npm >/dev/null 2>&1; then
        echo "Error: npm command not found after Node.js setup."
        exit 1
    fi

    mkdir -p "$NPM_USER_BIN"
    export PATH="$NPM_USER_BIN:$PATH"

    install_agent_cli_if_missing "codex" "@openai/codex"
    install_agent_cli_if_missing "claude" "@anthropic-ai/claude-code"
    install_agent_cli_if_missing "gemini" "@google/gemini-cli"
    install_kimi_cli_if_missing
    persist_user_bin_path
fi

echo "Initializing directories ..."
mkdir -p logs output test_instances .agent_sessions \
    workspace/database workspace/message_queue workspace/http_server workspace/redis_kvstore

if [ ! -f ".env.template" ]; then
    cat > .env.template <<'EOF'
# OpenAI (Codex)

# Native OpenAI API key
# OPENAI_API_KEY=

# OpenRouter
# OPENROUTER_API_KEY=
# OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/



# Anthropic (Claude Code Agent)

# Native Anthropic API key
# ANTHROPIC_API_KEY=

# Bailian coding plan via Anthropic
# ANTHROPIC_AUTH_TOKEN=
# ANTHROPIC_BASE_URL=https://coding-intl.dashscope.aliyuncs.com/apps/anthropic

# Zai Coding plan via Anthropic
# ANTHROPIC_AUTH_TOKEN=
# ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic

# Moonshot via Anthropic
# ANTHROPIC_BASE_URL=https://api.moonshot.ai/anthropic
# ANTHROPIC_AUTH_TOKEN=

# MiniMax via Anthropic
# ANTHROPIC_AUTH_TOKEN=
# ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic

# OpenRouter via Anthropic
# ANTHROPIC_AUTH_TOKEN=
# ANTHROPIC_BASE_URL=https://openrouter.ai/api



# Google (Gemini CLI Agent)
# GEMINI_API_KEY=
# GOOGLE_API_KEY="$GEMINI_API_KEY"



# OpenCode

# Native OpenAI
# OPENAI_API_KEY=

# Native Anthropic
# ANTHROPIC_API_KEY=

# Bailian via DashScope
# OPENCODE_API_KEY=

# OpenRouter
# OPENCODE_API_KEY=

# Moonshot/Kimi
# OPENCODE_API_KEY=

# MiniMax
# OPENCODE_API_KEY=



# Cline

# Native OpenAI
# CLINE_API_KEY=
# CLINE_PROVIDER=openai

# Native Anthropic
# CLINE_API_KEY=
# CLINE_PROVIDER=anthropic
# CLINE_BASE_URL=https://api.anthropic.com

# Bailian OpenAI Gateway
# CLINE_PROVIDER=bailian
# CLINE_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
# DASHSCOPE_API_KEY=
# CLINE_MODEL=qwen3.5-plus

# OpenRouter
# CLINE_API_KEY=
# OPENROUTER_API_KEY=
# CLINE_PROVIDER=openai

# Moonshot/Kimi
# CLINE_API_KEY=
# KIMI_API_KEY=

# MiniMax
# CLINE_API_KEY=
# MINIMAX_API_KEY=

# CLINE_MODEL=
# CLINE_PROVIDER=

# Kimi (K2.5)
# KIMI_API_KEY=


# litellm
# LITELLM_API_KEY=
# LITELLM_BASE_URL=http://localhost:4000

# vLLM
# VLLM_API_KEY=
# VLLM_BASE_URL=http://localhost:8000/v1

# SGLang
# SGLANG_API_KEY=
# SGLANG_BASE_URL=
EOF
    echo "Created .env template at ./.env"
else
    echo ".env already exists, keeping current values."
fi

echo ""
echo "Setup completed successfully."
echo "To use this environment in a new shell:"
if [ "$USE_CONDA" = true ]; then
    echo "  source \"$(conda info --base)/etc/profile.d/conda.sh\""
    echo "  conda activate $ENV_NAME"
else
    echo "  source $VENV_DIR/bin/activate"
fi
if [ "$INSTALL_AGENT_CLI" = true ]; then
    echo "  source ~/.bashrc  # or source ~/.zshrc"
fi
echo ""
echo "Then start system:"
echo "  ./start_system_docker.sh --agent codex --system-type database"
