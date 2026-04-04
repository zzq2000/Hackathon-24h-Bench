#!/bin/bash
#
# Docker Mode System Startup Script
#
# This script starts the code agent controller in Docker container mode
# with improved security through container isolation.
#
# Usage:
#   ./start_system_docker.sh [options]
#
# Options:
#   --agent <type>           Agent type: codex, claude, gemini, kimi, opencode, qwen, grok, cline (default: codex)
#   --model <name>           Model name to use
#   --system-type <type>     System type: database, message_queue (default: database)
#   --sut-dir <path>         SUT working directory (preferred; e.g., ./workspace/database/database_gpt or ./message_queue_gpt)
#   --run-id <id>            Reuse an existing run_id (resume previous run/logs)
#   --resume-latest          Reuse latest run_id from logs/latest
#   --max-iterations <n>     Max improvement iterations for controller (0 = unlimited)
#   --use-resume <bool>      Use resume in improve iterations: true/false (default: true)
#   --use_spec               Copy root spec/<system-type> into workspace spec folder
#   --controller-only        Only start the agent controller
#   --runner-only            Only start the test runner
#   --network <mode>          Docker network mode (e.g., host, bridge; default: bridge)
#   --build                  Build Docker image before starting
#   --detach                 Run container in detached mode
#
# Environment Variables:
#   CODE_AGENT               Default agent type
#   CODE_AGENT_MODEL         Model name
#   SUT_DIR                  SUT working directory (preferred)
#   DATABASE_DIR             Deprecated alias for SUT_DIR
#   TEST_INTERVAL            Test runner interval in seconds (default: 900)
#   FIRST_TEST_DELAY_SEC     Delay before first test after controller start (default: 3600; 0 in --runner-only mode)
#   BENCHMARK_TIMEOUT        Optional per-benchmark timeout seconds (if unset, use test_runner config default)
#   TIER_MODE                Tier execution/report mode: full or ladder
#   RUN_ALL_TIERS            Continue running later tiers after earlier tier failures (default: true)
#   CODE_AGENT_WAIT_TIME     Controller loop wait seconds override
#   CODE_AGENT_MAX_RETRIES   Agent command retry count override
#   CODE_AGENT_COMMAND_TIMEOUT Agent command timeout seconds override
#   OPENAI_API_KEY           Required for Codex agent
#   ANTHROPIC_API_KEY        Claude key (compatible)
#   ANTHROPIC_AUTH_TOKEN     Claude gateway auth token
#   API_TIMEOUT_MS           Claude gateway timeout in ms (optional)
#   GEMINI_API_KEY           Preferred for Gemini agent
#   KIMI_API_KEY             Preferred for Kimi agent
#   MOONSHOT_API_KEY         Back-compat alias for Kimi
#   OPENCODE_API_KEY         Preferred for OpenCode agent
#   OPENCODE_PERMISSION      OpenCode permission JSON override (default in Docker: all allow)
#   QWEN_API_KEY             Preferred for Qwen agent
#   DASHSCOPE_API_KEY        DashScope key for Qwen
#   GROK_API_KEY             Preferred for Grok agent
#   XAI_API_KEY              X.AI key (Grok/OpenCode compatible)
#   GOOGLE_API_KEY           Google key (OpenCode compatible)
#   OPENROUTER_API_KEY       OpenRouter key (OpenCode compatible)
#

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Auto-activate Python virtual environment if not already in one.
# The test runner runs on the host and needs the installed dependencies.
if [ -z "${VIRTUAL_ENV:-}" ]; then
    if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
        # shellcheck disable=SC1091
        source "$SCRIPT_DIR/.venv/bin/activate"
    elif command -v conda >/dev/null 2>&1 && conda info --envs 2>/dev/null | grep -q hackathon-24h-bench; then
        eval "$(conda shell.bash hook 2>/dev/null)" && conda activate hackathon-24h-bench
    fi
fi

# Load environment variables from .env file if it exists
# Only set variables that are not already present in the environment,
# so that command-line injection (e.g. ANTHROPIC_BASE_URL=... ./start_system_docker.sh)
# takes priority over .env values.
if [ -f "$SCRIPT_DIR/.env" ]; then
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip comments and blank lines
        line="${line## }"
        [[ -z "$line" || "$line" == \#* ]] && continue
        key="${line%%=*}"
        key="${key## }"
        key="${key%% }"
        [[ -z "$key" ]] && continue
        # Only export if not already set
        if [ -z "${!key+x}" ]; then
            eval "export $line"
        fi
    done < "$SCRIPT_DIR/.env"
fi

# Default values
AGENT_TYPE="${CODE_AGENT:-codex}"
MODEL_NAME="${CODE_AGENT_MODEL:-}"
PROVIDER_NAME=""
SYSTEM_TYPE="${SYSTEM_TYPE:-database}"
SUT_DIR="${SUT_DIR:-}"
DATABASE_DIR="${DATABASE_DIR:-}"
LOG_DIR="${LOG_DIR:-./logs}"
SAVE_IO=true
RUN_CONTROLLER=true
RUN_RUNNER=true
TEST_INTERVAL="${TEST_INTERVAL:-1800}"
FIRST_TEST_DELAY_SEC="${FIRST_TEST_DELAY_SEC:-}"
BENCHMARK_TIMEOUT="${BENCHMARK_TIMEOUT:-}"
TIER_MODE="${TIER_MODE:-}"
RUN_ALL_TIERS="${RUN_ALL_TIERS:-}"
TIERS=""
BUILD_IMAGE=false
DETACH=true
DOCKER_IMAGE=""
DOCKER_IMAGE_EXPLICIT=false
SESSION_DIR=".agent_sessions"  # Will be extended with RUN_ID after it's generated
CUSTOM_AGENTS_DIR=""
RUN_ID_OVERRIDE=""
RESUME_LATEST=false
EXPLICIT_SUT_DIR=false
MAX_ITERATIONS=0
USE_RESUME=true
USE_SPEC=true
DOCKER_NETWORK=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --agent)
            AGENT_TYPE="$2"
            shift 2
            ;;
        --model)
            MODEL_NAME="$2"
            shift 2
            ;;
        --provider)
            PROVIDER_NAME="$2"
            shift 2
            ;;
        --system-type)
            SYSTEM_TYPE="$2"
            shift 2
            ;;
        --sut-dir)
            SUT_DIR="$2"
            EXPLICIT_SUT_DIR=true
            shift 2
            ;;
        --run-id)
            RUN_ID_OVERRIDE="$2"
            shift 2
            ;;
        --resume-latest)
            RESUME_LATEST=true
            shift
            ;;
        --max-iterations)
            MAX_ITERATIONS="$2"
            shift 2
            ;;
        --use-resume)
            USE_RESUME="$2"
            shift 2
            ;;
        --use-spec)
            USE_SPEC=true
            shift
            ;;
        --controller-only)
            RUN_CONTROLLER=true
            RUN_RUNNER=false
            shift
            ;;
        --runner-only)
            RUN_CONTROLLER=false
            RUN_RUNNER=true
            shift
            ;;
        --build)
            BUILD_IMAGE=true
            shift
            ;;
        --detach)
            DETACH=true
            shift
            ;;
        --docker-image)
            DOCKER_IMAGE="$2"
            DOCKER_IMAGE_EXPLICIT=true
            shift 2
            ;;
        --custom-agents-dir)
            CUSTOM_AGENTS_DIR="$2"
            shift 2
            ;;
        --log-dir)
            LOG_DIR="$2"
            shift 2
            ;;
        --tiers)
            TIERS="$2"
            shift 2
            ;;
        --tier-mode)
            TIER_MODE="$2"
            shift 2
            ;;
        --run-all-tiers)
            RUN_ALL_TIERS=true
            shift
            ;;
        --stop-on-tier-failure)
            RUN_ALL_TIERS=false
            shift
            ;;
        --save-io)
            SAVE_IO=true
            shift
            ;;
        --network)
            DOCKER_NETWORK="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --agent <type>           Agent type: codex, claude, gemini, kimi, opencode, qwen, grok, cline (default: codex)"
            echo "  --model <name>           Model name to use"
            echo "  --system-type <type>     System type: database, message_queue (default: database)"
            echo "  --sut-dir <path>         SUT working directory (preferred)"
            echo "  --run-id <id>            Reuse an existing run_id (resume previous run/logs)"
            echo "  --resume-latest          Reuse latest run_id from logs/latest"
            echo "  --max-iterations <n>     Max improvement iterations for controller (0 = unlimited)"
            echo "  --use-resume <bool>      Use resume in improve iterations: true/false (default: true)"
            echo "  --use_spec               Copy root spec/<system-type> into workspace spec folder"
            echo "  --log-dir <path>         Log directory (default: ./logs)"
            echo "  --save-io                Save full input/output to JSON files"
            echo "  --controller-only        Only start the agent controller"
            echo "  --runner-only            Only start the test runner"
            echo "  --build                  Build Docker image before starting"
            echo "  --detach                 Run container in detached mode"
            echo "  --docker-image <name>    Docker image name (default: code-agent-controller:<agent>)"
            echo "  --custom-agents-dir      Custom agents directory"
            echo "  --tiers <list>           Comma-separated tiers for test_runner (e.g. L0 or L0,L1)"
            echo "  --tier-mode <mode>       Tier mode for test_runner: full or ladder"
            echo "  --network <mode>         Docker network mode (e.g., host, bridge; default: bridge)"
            echo "  --run-all-tiers          Continue running later tiers after earlier tier failures (default)"
            echo "  --stop-on-tier-failure   Skip remaining tiers after the first failed tier"
            echo ""
            echo "Environment Variables:"
            echo "  CODE_AGENT               Default agent type"
            echo "  CODE_AGENT_MODEL         Model name"
            echo "  SUT_DIR                  SUT working directory (preferred)"
            echo "  DATABASE_DIR             Deprecated alias for SUT_DIR"
            echo "  LOG_DIR                  Log directory"
            echo "  TEST_INTERVAL            Test interval in seconds (default: 900)"
            echo "  FIRST_TEST_DELAY_SEC     Delay before first test (default: 3600; 0 in --runner-only mode)"
            echo "  BENCHMARK_TIMEOUT        Optional per-benchmark timeout seconds"
            echo "  TIER_MODE                Tier mode for test_runner: full or ladder"
            echo "  RUN_ALL_TIERS            Continue running later tiers after earlier tier failures (default: true)"
            echo "  CODE_AGENT_WAIT_TIME     Controller loop wait seconds override"
            echo "  CODE_AGENT_MAX_RETRIES   Agent command retry count override"
            echo "  CODE_AGENT_COMMAND_TIMEOUT Agent command timeout seconds override"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ "$DOCKER_IMAGE_EXPLICIT" = false ]; then
    DOCKER_IMAGE="code-agent-controller:${AGENT_TYPE}"
fi

normalize_opencode_model_name() {
    local model_name="$1"
    local config_path="$SCRIPT_DIR/third_party/bailian/opencode.json"
    local canonical=""
    local raw_model="$model_name"

    if [[ "$model_name" == bailian-coding-plan/* ]]; then
        raw_model="${model_name#bailian-coding-plan/}"
    elif [[ "$model_name" == */* ]]; then
        printf '%s\n' "$model_name"
        return 0
    fi

    if [ -z "$raw_model" ]; then
        printf '%s\n' "$model_name"
        return 0
    fi

    if [ -f "$config_path" ] && command -v jq &>/dev/null; then
        canonical="$(jq -r --arg m "$raw_model" '
            first(
              .provider["bailian-coding-plan"].models
              | to_entries[]
              | select((.key | ascii_downcase) == ($m | ascii_downcase))
              | .key
            ) // empty
        ' "$config_path" 2>/dev/null)"
    elif [ -f "$config_path" ] && grep -qi "\"$raw_model\"" "$config_path"; then
        canonical="$raw_model"
    fi

    if [ -n "$canonical" ]; then
        printf '%s\n' "$canonical"
    else
        printf '%s\n' "$model_name"
    fi
}

# Backward compatibility: DATABASE_DIR is a deprecated alias for SUT_DIR.
if [ -z "$SUT_DIR" ] && [ -n "$DATABASE_DIR" ]; then
    SUT_DIR="$DATABASE_DIR"
fi

if ! [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
    echo "Error: --max-iterations must be a non-negative integer"
    exit 1
fi

if [ "$AGENT_TYPE" = "opencode" ] && [ -n "$MODEL_NAME" ]; then
    NORMALIZED_OPENCODE_MODEL="$(normalize_opencode_model_name "$MODEL_NAME")"
    if [ "$NORMALIZED_OPENCODE_MODEL" != "$MODEL_NAME" ]; then
        echo "Normalized OpenCode model: $MODEL_NAME -> $NORMALIZED_OPENCODE_MODEL"
        MODEL_NAME="$NORMALIZED_OPENCODE_MODEL"
    fi
fi

case "$(echo "$USE_RESUME" | tr '[:upper:]' '[:lower:]')" in
    true|false|1|0|yes|no|on|off) ;;
    *)
        echo "Error: --use-resume must be true/false (also accepts 1/0, yes/no, on/off)"
        exit 1
        ;;
esac

get_agent_cli_bin() {
    case "$1" in
        codex) echo "codex" ;;
        claude) echo "claude" ;;
        gemini) echo "gemini" ;;
        kimi) echo "kimi" ;;
        opencode) echo "opencode" ;;
        qwen) echo "qwen" ;;
        grok) echo "grok" ;;
        cline) echo "cline" ;;
        *) echo "" ;;
    esac
}

build_agent_image() {
    local install_mysql_client="false"
    if [ "$SYSTEM_TYPE" = "database" ]; then
        install_mysql_client="true"
    fi

    docker build -f Dockerfile.agents -t "$DOCKER_IMAGE" \
        --build-arg USER_UID="$(id -u)" \
        --build-arg USER_GID="$(id -g)" \
        --build-arg TARGET_AGENT="$AGENT_TYPE" \
        --build-arg INSTALL_MYSQL_CLIENT="$install_mysql_client" \
        .
}

# In runner-only mode, first test should run immediately unless user explicitly sets FIRST_TEST_DELAY_SEC.
if [ "$RUN_CONTROLLER" = false ] && [ "$RUN_RUNNER" = true ] && [ -z "${FIRST_TEST_DELAY_SEC:-}" ]; then
    FIRST_TEST_DELAY_SEC=0
elif [ -z "${FIRST_TEST_DELAY_SEC:-}" ]; then
    FIRST_TEST_DELAY_SEC=1800
fi

# Get actual model from agent-specific env var or generic env var (never use "default")
AGENT_UPPER=$(echo "$AGENT_TYPE" | tr '[:lower:]' '[:upper:]')
MODEL_VAR="${AGENT_UPPER}_MODEL"
if [ -n "$MODEL_NAME" ]; then
    MODEL_STR="$MODEL_NAME"
elif [ -n "${!MODEL_VAR:-}" ]; then
    MODEL_STR="${!MODEL_VAR}"
elif [ -n "${CODE_AGENT_MODEL:-}" ]; then
    MODEL_STR="$CODE_AGENT_MODEL"
else
    MODEL_STR="unknown"
fi
MODEL_STR="${MODEL_STR//\//-}"  # 替换 / 为 -
MODEL_STR="${MODEL_STR//:/-}"   # 替换 : 为 -
MODEL_STR="${MODEL_STR// /_}"   # 替换空格为 _

# Resolve --resume-latest into --run-id.
if [ "$RESUME_LATEST" = true ] && [ -z "$RUN_ID_OVERRIDE" ]; then
    LATEST_PATH="$LOG_DIR/latest"
    if [[ "$LATEST_PATH" != /* ]]; then
        LATEST_PATH="$SCRIPT_DIR/$LATEST_PATH"
    fi
    if [ -L "$LATEST_PATH" ]; then
        LATEST_TARGET="$(readlink "$LATEST_PATH" 2>/dev/null || true)"
        RUN_ID_OVERRIDE="$(basename "$LATEST_TARGET")"
    elif [ -d "$LATEST_PATH" ]; then
        RUN_ID_OVERRIDE="$(basename "$(readlink -f "$LATEST_PATH")")"
    fi
    if [ -z "$RUN_ID_OVERRIDE" ] || [ "$RUN_ID_OVERRIDE" = "latest" ]; then
        echo "Error: --resume-latest could not resolve run_id from $LATEST_PATH"
        exit 1
    fi
fi

# Generate run_id with system_type (format: {system_type}_{agent}_{model}_{timestamp})
# If --run-id is provided, reuse it to continue previous run context.
if [ -n "$RUN_ID_OVERRIDE" ]; then
    RUN_ID="$RUN_ID_OVERRIDE"
else
    RUN_ID="${SYSTEM_TYPE}_${AGENT_TYPE}_${MODEL_STR}_$(date +%Y%m%d_%H%M%S)"
fi
export AGENT_RUN_ID="$RUN_ID"

# Set default SUT directory based on system type with run_id
if [ -z "$SUT_DIR" ]; then
    SUT_DIR="./workspace/${SYSTEM_TYPE}/${RUN_ID}"
fi
export SYSTEM_TYPE
mkdir -p "$SUT_DIR"
export SUT_DIR

# Isolate session directory per RUN_ID to avoid conflicts between concurrent instances
SESSION_DIR=".agent_sessions/${RUN_ID}"

# Resolve absolute paths
SUT_DIR="$(cd "$SCRIPT_DIR" && mkdir -p "$SUT_DIR" && cd "$SUT_DIR" && pwd)"
SESSION_DIR="$(cd "$SCRIPT_DIR" && mkdir -p "$SESSION_DIR" && cd "$SESSION_DIR" && pwd)"
mkdir -p "$SESSION_DIR/home" "$SESSION_DIR/xdg_config" "$SESSION_DIR/xdg_state"

# For OpenCode, sync host config into both HOME and XDG config locations used in container.
if [ "$AGENT_TYPE" = "opencode" ]; then
    OPENCODE_CONFIG_SRC="$SCRIPT_DIR/third_party/bailian/opencode.json"
    OPENCODE_XDG_TARGET_DIR="$SESSION_DIR/xdg_config/opencode"
    OPENCODE_HOME_TARGET_DIR="$SESSION_DIR/home/.config/opencode"

    if [ -f "$OPENCODE_CONFIG_SRC" ]; then
        mkdir -p "$OPENCODE_XDG_TARGET_DIR" "$OPENCODE_HOME_TARGET_DIR"
        cp "$OPENCODE_CONFIG_SRC" "$OPENCODE_XDG_TARGET_DIR/config.json"
        cp "$OPENCODE_CONFIG_SRC" "$OPENCODE_HOME_TARGET_DIR/config.json"
        echo "Synced OpenCode config: $OPENCODE_CONFIG_SRC"
    else
        echo "Warning: OpenCode config not found: $OPENCODE_CONFIG_SRC"
    fi
fi

# For Claude agent, skip onboarding wizard.
# Provider registry + _build_env() handle all API keys, base URLs, and model
# settings via container environment variables — no settings.json env overrides needed.
if [ "$AGENT_TYPE" = "claude" ]; then
    echo '{"hasCompletedOnboarding": true}' > "$SESSION_DIR/home/.claude.json"
fi

if [ "$USE_SPEC" = true ]; then
    SPEC_SOURCE_DIR="$SCRIPT_DIR/spec/$SYSTEM_TYPE"
    SPEC_TARGET_DIR="$SUT_DIR/spec"
    mkdir -p "$SPEC_TARGET_DIR"
    if [ -d "$SPEC_SOURCE_DIR" ]; then
        cp -a "$SPEC_SOURCE_DIR/." "$SPEC_TARGET_DIR/"
        echo "Spec copied: $SPEC_SOURCE_DIR -> $SPEC_TARGET_DIR"
    else
        echo "Warning: spec source directory not found: $SPEC_SOURCE_DIR"
    fi
fi

# Log directory (LogManager will create runs/ subdirectory)
LOG_DIR="${LOG_DIR:-./logs}"
LOG_DIR="$(cd "$SCRIPT_DIR" && mkdir -p "$LOG_DIR" && cd "$LOG_DIR" && pwd)"
AGENT_SESSION_SCOPE="${SYSTEM_TYPE}|${AGENT_TYPE}|${MODEL_STR}|/workspace/${SYSTEM_TYPE}"
export AGENT_SESSION_SCOPE

# Default tiers per system type (unless provided)
if [ -z "$TIERS" ] && [ "$SYSTEM_TYPE" = "message_queue" ]; then
    TIERS="L0,L1,L2"
fi

echo "========================================"
echo "Code Agent Controller (Docker Mode)"
echo "========================================"
echo "Agent Type:    $AGENT_TYPE"
echo "Model:         ${MODEL_NAME:-default}"
echo "System Type:   $SYSTEM_TYPE"
echo "SUT Dir:       $SUT_DIR"
echo "Session Dir:   $SESSION_DIR"
echo "Session Scope: $AGENT_SESSION_SCOPE"
echo "Log Dir:       $LOG_DIR"
echo "Save IO:       $SAVE_IO"
echo "Test Interval: $TEST_INTERVAL seconds"
echo "First Test Delay: $FIRST_TEST_DELAY_SEC seconds"
echo "Max Iterations: $MAX_ITERATIONS"
echo "Use Resume:    $USE_RESUME"
echo "Use Spec:      $USE_SPEC"
if [ -n "$BENCHMARK_TIMEOUT" ]; then
    echo "Benchmark Timeout: $BENCHMARK_TIMEOUT seconds"
else
    echo "Benchmark Timeout: default (from config/global.yaml or test_runner default)"
fi
echo "Tiers:         ${TIERS:-default}"
echo "Network:       ${DOCKER_NETWORK:-default}"
echo "Docker Image:  $DOCKER_IMAGE"
echo "========================================"

# Check Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    exit 1
fi

# Build Docker image if requested or not exists
if [ "$BUILD_IMAGE" = true ] || ! docker image inspect "$DOCKER_IMAGE" &> /dev/null; then
    echo "Building Docker image for agent '$AGENT_TYPE': $DOCKER_IMAGE"
    build_agent_image
fi

# Ensure target agent CLI exists in image (protect against wrong/reused image tag)
AGENT_CLI_BIN="$(get_agent_cli_bin "$AGENT_TYPE")"
if [ -n "$AGENT_CLI_BIN" ]; then
    if ! docker run --rm --entrypoint sh "$DOCKER_IMAGE" -lc "command -v $AGENT_CLI_BIN >/dev/null 2>&1"; then
        echo "Agent CLI '$AGENT_CLI_BIN' is missing in $DOCKER_IMAGE, rebuilding..."
        build_agent_image
    fi
fi

# For database system type, ensure mysql client exists in container image.
if [ "$SYSTEM_TYPE" = "database" ]; then
    if ! docker run --rm --entrypoint sh "$DOCKER_IMAGE" -lc "command -v mysql >/dev/null 2>&1"; then
        echo "MySQL client is missing in $DOCKER_IMAGE for database mode, rebuilding..."
        build_agent_image
    fi
fi

# Use arrays to properly handle special characters in values
DOCKER_ARGS=()

# Timezone: sync host timezone into container so log timestamps match
if [ -f /etc/localtime ]; then
    DOCKER_ARGS+=("-v" "/etc/localtime:/etc/localtime:ro")
fi
HOST_TZ="${TZ:-$(cat /etc/timezone 2>/dev/null || readlink -f /etc/localtime 2>/dev/null | sed 's|.*/zoneinfo/||' || echo '')}"
if [ -n "$HOST_TZ" ]; then
    DOCKER_ARGS+=("-e" "TZ=$HOST_TZ")
fi

# User mapping
DOCKER_ARGS+=("--user" "$(id -u):$(id -g)")

# Volume mounts - use system type for container path
DOCKER_ARGS+=("-v" "$SUT_DIR:/workspace/${SYSTEM_TYPE}:rw")
DOCKER_ARGS+=("-v" "$SESSION_DIR:/workspace/sessions:rw")
DOCKER_ARGS+=("-v" "$LOG_DIR:/workspace/logs:rw")
# Keep runtime code and config in sync with host files without rebuilding image.
DOCKER_ARGS+=("-v" "$SCRIPT_DIR/code_agent_controller:/workspace/controller/code_agent_controller:ro")
DOCKER_ARGS+=("-v" "$SCRIPT_DIR/config:/workspace/controller/config:ro")

# Custom agents directory mount
if [ -n "$CUSTOM_AGENTS_DIR" ] && [ -d "$CUSTOM_AGENTS_DIR" ]; then
    CUSTOM_AGENTS_DIR="$(cd "$CUSTOM_AGENTS_DIR" && pwd)"
    DOCKER_ARGS+=("-v" "$CUSTOM_AGENTS_DIR:/workspace/custom_agents:ro")
    DOCKER_ARGS+=("-e" "CUSTOM_AGENTS_DIR=/workspace/custom_agents")
fi

# Mount Codex CLI config into container (copy to temp dir so source is not modified)
if [ "$AGENT_TYPE" = "codex" ]; then
    CODEX_CONFIG_SRC=""
    if [ -d "$SCRIPT_DIR/third_party/codex" ]; then
        CODEX_CONFIG_SRC="$SCRIPT_DIR/third_party/codex"
    elif [ -d "$HOME/.codex" ]; then
        CODEX_CONFIG_SRC="$HOME/.codex"
    fi
    if [ -n "$CODEX_CONFIG_SRC" ]; then
        CODEX_CONFIG_TMP="$(mktemp -d)"
        cp -a "$CODEX_CONFIG_SRC/." "$CODEX_CONFIG_TMP/"
        echo "Copied Codex CLI config from $CODEX_CONFIG_SRC to $CODEX_CONFIG_TMP"
        DOCKER_ARGS+=("-v" "$CODEX_CONFIG_TMP:/workspace/sessions/home/.codex:rw")
        # FAKE_KEY fallback for legacy config.toml that uses env_key = "FAKE_KEY".
        # ProviderRegistry will patch env_key to the actual key var at runtime.
        [ -z "${FAKE_KEY:-}" ] && DOCKER_ARGS+=("-e" "FAKE_KEY=${OPENAI_API_KEY:-sk-placeholder}")
    fi
fi

# Run ID was generated earlier with system_type
echo "Run ID: $RUN_ID"
if [ -n "${AGENT_START_EPOCH:-}" ]; then
    export AGENT_START_EPOCH
else
    export AGENT_START_EPOCH="$(date +%s)"
fi
export FIRST_TEST_DELAY_SEC

# Environment variables (using arrays to handle special characters in API keys)
# For OpenCode in Docker, default to non-interactive full permissions unless user overrides.
if [ "$AGENT_TYPE" = "opencode" ] && [ -z "${OPENCODE_PERMISSION:-}" ]; then
    OPENCODE_PERMISSION='{"external_directory":"allow","read":"allow","edit":"allow","glob":"allow","grep":"allow","list":"allow","bash":"allow","task":"allow","todowrite":"allow","todoread":"allow","question":"allow","webfetch":"allow","websearch":"allow","codesearch":"allow","lsp":"allow","doom_loop":"allow","skill":"allow"}'
    echo "OpenCode permission: using default all-allow policy in Docker mode"
fi

DOCKER_ARGS+=("-e" "CONTAINER_MODE=true")
DOCKER_ARGS+=("-e" "SESSION_DIR=/workspace/sessions")
DOCKER_ARGS+=("-e" "HOME=/workspace/sessions/home")
DOCKER_ARGS+=("-e" "XDG_CONFIG_HOME=/workspace/sessions/xdg_config")
DOCKER_ARGS+=("-e" "XDG_STATE_HOME=/workspace/sessions/xdg_state")
DOCKER_ARGS+=("-e" "LOG_DIR=/workspace/logs")
DOCKER_ARGS+=("-e" "AGENT_RUN_ID=$RUN_ID")
DOCKER_ARGS+=("-e" "AGENT_SESSION_SCOPE=$AGENT_SESSION_SCOPE")
DOCKER_ARGS+=("-e" "SYSTEM_TYPE=$SYSTEM_TYPE")
DOCKER_ARGS+=("-e" "SUT_DIR=/workspace/${SYSTEM_TYPE}")

# Pass API keys (explicitly include values, properly quoted via array)
[ -n "$OPENAI_API_KEY" ] && DOCKER_ARGS+=("-e" "OPENAI_API_KEY=$OPENAI_API_KEY")
[ -n "$ANTHROPIC_API_KEY" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY")
[ -n "$ANTHROPIC_AUTH_TOKEN" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_AUTH_TOKEN=$ANTHROPIC_AUTH_TOKEN")
[ -n "$ANTHROPIC_BASE_URL" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_BASE_URL=$ANTHROPIC_BASE_URL")
[ -n "$ANTHROPIC_MODEL" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_MODEL=$ANTHROPIC_MODEL")
[ -n "$ANTHROPIC_DEFAULT_OPUS_MODEL" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_DEFAULT_OPUS_MODEL=$ANTHROPIC_DEFAULT_OPUS_MODEL")
[ -n "$ANTHROPIC_DEFAULT_SONNET_MODEL" ] && DOCKER_ARGS+=("-e" "ANTHROPIC_DEFAULT_SONNET_MODEL=$ANTHROPIC_DEFAULT_SONNET_MODEL")
[ -n "$API_TIMEOUT_MS" ] && DOCKER_ARGS+=("-e" "API_TIMEOUT_MS=$API_TIMEOUT_MS")
[ -n "$GEMINI_API_KEY" ] && DOCKER_ARGS+=("-e" "GEMINI_API_KEY=$GEMINI_API_KEY")
[ -n "$KIMI_API_KEY" ] && DOCKER_ARGS+=("-e" "KIMI_API_KEY=$KIMI_API_KEY")
[ -n "$MOONSHOT_API_KEY" ] && DOCKER_ARGS+=("-e" "MOONSHOT_API_KEY=$MOONSHOT_API_KEY")
[ -n "$OPENCODE_API_KEY" ] && DOCKER_ARGS+=("-e" "OPENCODE_API_KEY=$OPENCODE_API_KEY")
[ -n "$OPENCODE_PERMISSION" ] && DOCKER_ARGS+=("-e" "OPENCODE_PERMISSION=$OPENCODE_PERMISSION")
[ -n "$QWEN_API_KEY" ] && DOCKER_ARGS+=("-e" "QWEN_API_KEY=$QWEN_API_KEY")
[ -n "$DASHSCOPE_API_KEY" ] && DOCKER_ARGS+=("-e" "DASHSCOPE_API_KEY=$DASHSCOPE_API_KEY")
[ -n "$GROK_API_KEY" ] && DOCKER_ARGS+=("-e" "GROK_API_KEY=$GROK_API_KEY")
[ -n "$XAI_API_KEY" ] && DOCKER_ARGS+=("-e" "XAI_API_KEY=$XAI_API_KEY")
[ -n "$GOOGLE_API_KEY" ] && DOCKER_ARGS+=("-e" "GOOGLE_API_KEY=$GOOGLE_API_KEY")
[ -n "$OPENROUTER_API_KEY" ] && DOCKER_ARGS+=("-e" "OPENROUTER_API_KEY=$OPENROUTER_API_KEY")
[ -n "$LITELLM_API_KEY" ] && DOCKER_ARGS+=("-e" "LITELLM_API_KEY=$LITELLM_API_KEY")
[ -n "$LITELLM_BASE_URL" ] && DOCKER_ARGS+=("-e" "LITELLM_BASE_URL=$LITELLM_BASE_URL")
[ -n "$VLLM_API_KEY" ] && DOCKER_ARGS+=("-e" "VLLM_API_KEY=$VLLM_API_KEY")
[ -n "$VLLM_BASE_URL" ] && DOCKER_ARGS+=("-e" "VLLM_BASE_URL=$VLLM_BASE_URL")
[ -n "$SGLANG_API_KEY" ] && DOCKER_ARGS+=("-e" "SGLANG_API_KEY=$SGLANG_API_KEY")
[ -n "$SGLANG_BASE_URL" ] && DOCKER_ARGS+=("-e" "SGLANG_BASE_URL=$SGLANG_BASE_URL")
[ -n "$MINIMAX_API_KEY" ] && DOCKER_ARGS+=("-e" "MINIMAX_API_KEY=$MINIMAX_API_KEY")
[ -n "$MINIMAX_BASE_URL" ] && DOCKER_ARGS+=("-e" "MINIMAX_BASE_URL=$MINIMAX_BASE_URL")
[ -n "$OPENAI_BASE_URL" ] && DOCKER_ARGS+=("-e" "OPENAI_BASE_URL=$OPENAI_BASE_URL")
[ -n "$KIMI_BASE_URL" ] && DOCKER_ARGS+=("-e" "KIMI_BASE_URL=$KIMI_BASE_URL")
[ -n "$GROK_BASE_URL" ] && DOCKER_ARGS+=("-e" "GROK_BASE_URL=$GROK_BASE_URL")
[ -n "$KIMI_THINKING" ] && DOCKER_ARGS+=("-e" "KIMI_THINKING=$KIMI_THINKING")
[ -n "$KIMI_MODEL_NAME" ] && DOCKER_ARGS+=("-e" "KIMI_MODEL_NAME=$KIMI_MODEL_NAME")
[ -n "$KIMI_MODEL_MAX_CONTEXT_SIZE" ] && DOCKER_ARGS+=("-e" "KIMI_MODEL_MAX_CONTEXT_SIZE=$KIMI_MODEL_MAX_CONTEXT_SIZE")
[ -n "$KIMI_MODEL_CAPABILITIES" ] && DOCKER_ARGS+=("-e" "KIMI_MODEL_CAPABILITIES=$KIMI_MODEL_CAPABILITIES")
[ -n "$OPENCODE_APPROVAL_MODE" ] && DOCKER_ARGS+=("-e" "OPENCODE_APPROVAL_MODE=$OPENCODE_APPROVAL_MODE")
# Map GEMINI_API_KEY to GOOGLE_GENERATIVE_AI_API_KEY for OpenCode's @ai-sdk/google
if [ "$AGENT_TYPE" = "opencode" ]; then
    GOOGLE_GENERATIVE_AI_API_KEY="${GOOGLE_GENERATIVE_AI_API_KEY:-${GEMINI_API_KEY:-${GOOGLE_API_KEY:-}}}"
    [ -n "$GOOGLE_GENERATIVE_AI_API_KEY" ] && DOCKER_ARGS+=("-e" "GOOGLE_GENERATIVE_AI_API_KEY=$GOOGLE_GENERATIVE_AI_API_KEY")
fi
[ -n "$QWEN_APPROVAL_MODE" ] && DOCKER_ARGS+=("-e" "QWEN_APPROVAL_MODE=$QWEN_APPROVAL_MODE")
[ -n "$CLINE_API_KEY" ] && DOCKER_ARGS+=("-e" "CLINE_API_KEY=$CLINE_API_KEY")
[ -n "$CLINE_BASE_URL" ] && DOCKER_ARGS+=("-e" "CLINE_BASE_URL=$CLINE_BASE_URL")
[ -n "$CLINE_MODEL" ] && DOCKER_ARGS+=("-e" "CLINE_MODEL=$CLINE_MODEL")
[ -n "$CLINE_PROVIDER" ] && DOCKER_ARGS+=("-e" "CLINE_PROVIDER=$CLINE_PROVIDER")

# Pass model environment variables (explicitly include values)
[ -n "$CODE_AGENT_MODEL" ] && DOCKER_ARGS+=("-e" "CODE_AGENT_MODEL=$CODE_AGENT_MODEL")
[ -n "$CODE_AGENT_WAIT_TIME" ] && DOCKER_ARGS+=("-e" "CODE_AGENT_WAIT_TIME=$CODE_AGENT_WAIT_TIME")
[ -n "$CODE_AGENT_MAX_RETRIES" ] && DOCKER_ARGS+=("-e" "CODE_AGENT_MAX_RETRIES=$CODE_AGENT_MAX_RETRIES")
[ -n "$CODE_AGENT_COMMAND_TIMEOUT" ] && DOCKER_ARGS+=("-e" "CODE_AGENT_COMMAND_TIMEOUT=$CODE_AGENT_COMMAND_TIMEOUT")
[ -n "$AGENT_WAIT_TIME" ] && DOCKER_ARGS+=("-e" "AGENT_WAIT_TIME=$AGENT_WAIT_TIME")
[ -n "$AGENT_MAX_RETRIES" ] && DOCKER_ARGS+=("-e" "AGENT_MAX_RETRIES=$AGENT_MAX_RETRIES")
[ -n "$AGENT_COMMAND_TIMEOUT" ] && DOCKER_ARGS+=("-e" "AGENT_COMMAND_TIMEOUT=$AGENT_COMMAND_TIMEOUT")
[ -n "$CODEX_MODEL" ] && DOCKER_ARGS+=("-e" "CODEX_MODEL=$CODEX_MODEL")
[ -n "$CODEX_PROVIDER" ] && DOCKER_ARGS+=("-e" "CODEX_PROVIDER=$CODEX_PROVIDER")
[ -n "$CODEX_WIRE_API" ] && DOCKER_ARGS+=("-e" "CODEX_WIRE_API=$CODEX_WIRE_API")
[ -n "$CLAUDE_MODEL" ] && DOCKER_ARGS+=("-e" "CLAUDE_MODEL=$CLAUDE_MODEL")
[ -n "$GEMINI_MODEL" ] && DOCKER_ARGS+=("-e" "GEMINI_MODEL=$GEMINI_MODEL")
[ -n "$KIMI_MODEL" ] && DOCKER_ARGS+=("-e" "KIMI_MODEL=$KIMI_MODEL")
[ -n "$OPENCODE_MODEL" ] && DOCKER_ARGS+=("-e" "OPENCODE_MODEL=$OPENCODE_MODEL")
[ -n "$QWEN_MODEL" ] && DOCKER_ARGS+=("-e" "QWEN_MODEL=$QWEN_MODEL")
[ -n "$GROK_MODEL" ] && DOCKER_ARGS+=("-e" "GROK_MODEL=$GROK_MODEL")

# Security options
# Codex CLI's bwrap sandbox is bypassed in container mode (the container
# itself provides isolation), so no extra capabilities are needed.
DOCKER_ARGS+=("--security-opt" "no-new-privileges:true")
DOCKER_ARGS+=("--cap-drop" "ALL")
DOCKER_ARGS+=("--cap-add" "NET_BIND_SERVICE")

# Network mode: explicit --network flag > codex default (host) > bridge (Docker default)
if [ -n "$DOCKER_NETWORK" ]; then
    DOCKER_ARGS+=("--network" "$DOCKER_NETWORK")
elif [ "$AGENT_TYPE" = "codex" ]; then
    DOCKER_ARGS+=("--network" "host")
fi

# Container name (use RUN_ID for uniqueness so multiple instances can coexist)
CONTAINER_NAME="agent-controller-${RUN_ID}"

# Build controller command arguments (also use array)
CONTROLLER_ARGS=("--agent" "$AGENT_TYPE" "--system-type" "$SYSTEM_TYPE" "--sut-dir" "/workspace/${SYSTEM_TYPE}")
[ -n "$MODEL_NAME" ] && CONTROLLER_ARGS+=("--model" "$MODEL_NAME")
[ -n "$PROVIDER_NAME" ] && CONTROLLER_ARGS+=("--provider" "$PROVIDER_NAME")
CONTROLLER_ARGS+=("--log-dir" "/workspace/logs")
CONTROLLER_ARGS+=("--use-resume" "$USE_RESUME")
[ "$MAX_ITERATIONS" -gt 0 ] && CONTROLLER_ARGS+=("--max-iterations" "$MAX_ITERATIONS")
[ "$SAVE_IO" = true ] && CONTROLLER_ARGS+=("--save-io")

# Start controller in Docker
if [ "$RUN_CONTROLLER" = true ]; then
    echo "Starting agent controller in Docker..."

    # Stop existing container if running
    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

    if [ "$DETACH" = true ]; then
        docker run -d \
            --name "$CONTAINER_NAME" \
            "${DOCKER_ARGS[@]}" \
            "$DOCKER_IMAGE" \
            "${CONTROLLER_ARGS[@]}"

        echo "Container started: $CONTAINER_NAME"
        echo "View logs: docker logs -f $CONTAINER_NAME"
    else
        # Run in foreground (will block)
        if [ "$RUN_RUNNER" = true ]; then
            # Run controller in background if we also need runner
            docker run -d \
                --name "$CONTAINER_NAME" \
                "${DOCKER_ARGS[@]}" \
                "$DOCKER_IMAGE" \
                "${CONTROLLER_ARGS[@]}"

            echo "Container started in background: $CONTAINER_NAME"
        else
            # Run interactively
            docker run --rm \
                "${DOCKER_ARGS[@]}" \
                "$DOCKER_IMAGE" \
                "${CONTROLLER_ARGS[@]}"
        fi
    fi
fi

# Start test runner on host
if [ "$RUN_RUNNER" = true ]; then
    echo "Starting test runner on host..."
    echo "Test interval: $TEST_INTERVAL seconds"
    echo "First test delay: $FIRST_TEST_DELAY_SEC seconds"
    if [ -n "$BENCHMARK_TIMEOUT" ]; then
        echo "Benchmark timeout: $BENCHMARK_TIMEOUT seconds"
    else
        echo "Benchmark timeout: default (from config/global.yaml or test_runner default)"
    fi
    if [ -n "$TIER_MODE" ]; then
        echo "Tier mode: $TIER_MODE"
    elif [ -n "$RUN_ALL_TIERS" ]; then
        echo "Run all tiers: $RUN_ALL_TIERS"
    else
        echo "Tier mode: default (full unless config/env overrides it)"
    fi

    # Run test_runner.py on host (it needs access to Docker for benchmarks)
    RUNNER_ARGS=(
        --sut-dir "$SUT_DIR"
        --system-type "$SYSTEM_TYPE"
        --interval "$TEST_INTERVAL"
        --log-dir "$LOG_DIR"
        --no-console-log
    )
    if [ -n "$TIERS" ]; then
        RUNNER_ARGS+=(--tiers "$TIERS")
    fi
    if [ -n "$BENCHMARK_TIMEOUT" ]; then
        RUNNER_ARGS+=(--benchmark-timeout "$BENCHMARK_TIMEOUT")
    fi
    if [ -n "$TIER_MODE" ]; then
        RUNNER_ARGS+=(--tier-mode "$TIER_MODE")
    elif [[ "${RUN_ALL_TIERS,,}" =~ ^(1|true|yes|on)$ ]]; then
        RUNNER_ARGS+=(--run-all-tiers)
    elif [[ "${RUN_ALL_TIERS,,}" =~ ^(0|false|no|off)$ ]]; then
        RUNNER_ARGS+=(--stop-on-tier-failure)
    fi

    WAIT_SNAPSHOT_SEC="${WAIT_SNAPSHOT_SEC:-1800}" LOG_DIR="$LOG_DIR" AGENT_START_EPOCH="$AGENT_START_EPOCH" FIRST_TEST_DELAY_SEC="$FIRST_TEST_DELAY_SEC" \
        python3 -m test_runner "${RUNNER_ARGS[@]}" &

    RUNNER_PID=$!
    echo "Test runner PID: $RUNNER_PID"

    # Store PID and container name in per-RUN_ID state files for precise stop
    mkdir -p .run_state
    echo "$RUNNER_PID" > ".run_state/${RUN_ID}.pid"

    echo "Test runner started"
fi

# Record container name in run state (outside the runner block so it's always saved)
if [ "$RUN_CONTROLLER" = true ]; then
    mkdir -p .run_state
    echo "$CONTAINER_NAME" > ".run_state/${RUN_ID}.container"
fi

echo ""
echo "System started successfully!"
echo "Run ID: $RUN_ID"
echo ""
echo "To stop this instance:"
echo "  ./stop_system_docker.sh --run-id $RUN_ID"
echo ""
echo "To stop all instances:"
echo "  ./stop_system_docker.sh --all"
echo ""
echo "To list running instances:"
echo "  ./stop_system_docker.sh --list"
echo ""
echo "To view controller logs:"
echo "  docker logs -f $CONTAINER_NAME"
echo "  tail -f $LOG_DIR/runs/$RUN_ID/controller.log"
echo "  (or: tail -f $LOG_DIR/latest/controller.log  -- points to last started instance)"
echo ""
echo "To view test runner logs:"
echo "  tail -f $LOG_DIR/runs/$RUN_ID/test_runner.log"
if [ "$SAVE_IO" = true ]; then
    echo ""
    echo "Iteration details:"
    echo "  ls $LOG_DIR/latest/iterations/"
fi
