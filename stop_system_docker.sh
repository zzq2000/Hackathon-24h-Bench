#!/bin/bash
#
# Docker Mode System Shutdown Script
#
# This script stops running agent controller containers and test runners.
# Supports stopping individual instances by RUN_ID or all instances at once.
#
# Usage:
#   ./stop_system_docker.sh [options]
#
# Options:
#   --run-id <id>     Stop only the instance with the given RUN_ID
#   --list            List all running instances
#   --all             Stop all instances (default)
#   --keep-runner     Don't stop the test runner(s)
#
# Legacy options (kept for backward compatibility):
#   --agent <type>    Stop containers matching agent type pattern
#

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Default values
RUN_ID=""
LIST_MODE=false
STOP_ALL=false
STOP_RUNNER=true
LEGACY_AGENT=""
ACTION_SET=false  # tracks whether user specified an action

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --run-id)
            RUN_ID="$2"
            ACTION_SET=true
            shift 2
            ;;
        --list)
            LIST_MODE=true
            ACTION_SET=true
            shift
            ;;
        --all)
            STOP_ALL=true
            ACTION_SET=true
            shift
            ;;
        --agent)
            LEGACY_AGENT="$2"
            ACTION_SET=true
            shift 2
            ;;
        --keep-runner)
            STOP_RUNNER=false
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --run-id <id>     Stop only the instance with the given RUN_ID"
            echo "  --list            List all running instances"
            echo "  --all             Stop all instances (default)"
            echo "  --keep-runner     Don't stop the test runner(s)"
            echo ""
            echo "Legacy options:"
            echo "  --agent <type>    Stop containers matching agent type pattern"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Default to --all if no action specified
if [ "$ACTION_SET" = false ]; then
    STOP_ALL=true
fi

RUN_STATE_DIR="$SCRIPT_DIR/.run_state"

# ─── List mode ───────────────────────────────────────────────────────────────

if [ "$LIST_MODE" = true ]; then
    echo "========================================"
    echo "Running Instances"
    echo "========================================"

    if [ ! -d "$RUN_STATE_DIR" ] || [ -z "$(ls -A "$RUN_STATE_DIR" 2>/dev/null)" ]; then
        echo "(no tracked instances)"
        # Also show any agent-controller containers that might be running without state files
        RUNNING=$(docker ps --filter "name=agent-controller-" --format "{{.Names}}\t{{.Status}}" 2>/dev/null || true)
        if [ -n "$RUNNING" ]; then
            echo ""
            echo "Untracked containers (no .run_state files):"
            echo "$RUNNING"
        fi
        exit 0
    fi

    printf "%-60s  %-12s  %-12s\n" "RUN_ID" "CONTAINER" "TEST_RUNNER"
    printf "%-60s  %-12s  %-12s\n" "------" "---------" "-----------"

    for pid_file in "$RUN_STATE_DIR"/*.pid "$RUN_STATE_DIR"/*.container; do
        [ -f "$pid_file" ] || continue
        # Extract RUN_ID from filename
        basename_f="$(basename "$pid_file")"
        rid="${basename_f%.*}"
        # Skip if we already printed this RUN_ID
        [[ "$pid_file" == *.container ]] && [ -f "$RUN_STATE_DIR/${rid}.pid" ] && continue

        # Container status
        container_status="n/a"
        if [ -f "$RUN_STATE_DIR/${rid}.container" ]; then
            cname="$(cat "$RUN_STATE_DIR/${rid}.container")"
            if docker ps -q -f "name=^${cname}$" 2>/dev/null | grep -q .; then
                container_status="running"
            else
                container_status="stopped"
            fi
        fi

        # Test runner status
        runner_status="n/a"
        if [ -f "$RUN_STATE_DIR/${rid}.pid" ]; then
            rpid="$(cat "$RUN_STATE_DIR/${rid}.pid")"
            if ps -p "$rpid" > /dev/null 2>&1; then
                runner_status="running"
            else
                runner_status="stopped"
            fi
        fi

        printf "%-60s  %-12s  %-12s\n" "$rid" "$container_status" "$runner_status"
    done

    exit 0
fi

# ─── Stop helper functions ───────────────────────────────────────────────────

stop_instance() {
    local rid="$1"
    echo "Stopping instance: $rid"

    # Stop Docker container
    if [ -f "$RUN_STATE_DIR/${rid}.container" ]; then
        local cname
        cname="$(cat "$RUN_STATE_DIR/${rid}.container")"
        if docker ps -q -f "name=^${cname}$" 2>/dev/null | grep -q .; then
            echo "  Stopping container: $cname"
            docker stop "$cname" 2>/dev/null || true
            docker rm -f "$cname" 2>/dev/null || true
        else
            # Container not running; clean up if it exists as stopped
            docker rm -f "$cname" 2>/dev/null || true
        fi
        rm -f "$RUN_STATE_DIR/${rid}.container"
    fi

    # Stop test runner
    if [ "$STOP_RUNNER" = true ] && [ -f "$RUN_STATE_DIR/${rid}.pid" ]; then
        local rpid
        rpid="$(cat "$RUN_STATE_DIR/${rid}.pid")"
        if ps -p "$rpid" > /dev/null 2>&1; then
            echo "  Killing test runner (PID: $rpid)"
            kill "$rpid" 2>/dev/null || true
            sleep 1
            # Force kill if still running
            if ps -p "$rpid" > /dev/null 2>&1; then
                kill -9 "$rpid" 2>/dev/null || true
            fi
        fi
        rm -f "$RUN_STATE_DIR/${rid}.pid"
    fi

    echo "  Instance stopped: $rid"
}

# ─── Stop by RUN_ID ─────────────────────────────────────────────────────────

if [ -n "$RUN_ID" ]; then
    echo "========================================"
    echo "Stopping Instance: $RUN_ID"
    echo "========================================"

    if [ ! -f "$RUN_STATE_DIR/${RUN_ID}.pid" ] && [ ! -f "$RUN_STATE_DIR/${RUN_ID}.container" ]; then
        echo "Error: No tracked instance found for RUN_ID: $RUN_ID"
        echo "Use --list to see running instances."
        exit 1
    fi

    stop_instance "$RUN_ID"

    echo ""
    echo "========================================"
    echo "Instance stopped"
    echo "========================================"
    exit 0
fi

# ─── Legacy --agent mode ────────────────────────────────────────────────────

if [ -n "$LEGACY_AGENT" ]; then
    echo "========================================"
    echo "Stopping containers for agent: $LEGACY_AGENT"
    echo "========================================"

    # Stop any container whose name matches the agent type pattern
    docker ps -a --filter "name=agent-controller-" --format "{{.Names}}" 2>/dev/null | while read -r name; do
        if [ -n "$name" ] && [[ "$name" == *"${LEGACY_AGENT}"* ]]; then
            echo "Stopping container: $name"
            docker stop "$name" 2>/dev/null || true
            docker rm -f "$name" 2>/dev/null || true
        fi
    done

    # Also stop matching run_state instances
    if [ -d "$RUN_STATE_DIR" ]; then
        for container_file in "$RUN_STATE_DIR"/*.container; do
            [ -f "$container_file" ] || continue
            local_rid="$(basename "${container_file%.container}")"
            if [[ "$local_rid" == *"${LEGACY_AGENT}"* ]]; then
                stop_instance "$local_rid"
            fi
        done
    fi

    # Stop test runner via legacy PID file if present
    if [ "$STOP_RUNNER" = true ] && [ -f "$SCRIPT_DIR/.test_runner.pid" ]; then
        RUNNER_PID=$(cat "$SCRIPT_DIR/.test_runner.pid")
        if ps -p "$RUNNER_PID" > /dev/null 2>&1; then
            echo "Killing legacy test runner (PID: $RUNNER_PID)"
            kill "$RUNNER_PID" 2>/dev/null || true
            sleep 1
            if ps -p "$RUNNER_PID" > /dev/null 2>&1; then
                kill -9 "$RUNNER_PID" 2>/dev/null || true
            fi
        fi
        rm -f "$SCRIPT_DIR/.test_runner.pid"
    fi

    echo ""
    echo "========================================"
    echo "System stopped"
    echo "========================================"
    exit 0
fi

# ─── Stop all (default) ─────────────────────────────────────────────────────

echo "========================================"
echo "Stopping All Instances"
echo "========================================"

# Stop all tracked instances from .run_state/
if [ -d "$RUN_STATE_DIR" ]; then
    FOUND_ANY=false
    for state_file in "$RUN_STATE_DIR"/*.pid "$RUN_STATE_DIR"/*.container; do
        [ -f "$state_file" ] || continue
        basename_f="$(basename "$state_file")"
        rid="${basename_f%.*}"
        # Skip if we already handled this RUN_ID (avoid double processing)
        if [ "${state_file}" != "$RUN_STATE_DIR/${rid}.pid" ] && [ -f "$RUN_STATE_DIR/${rid}.pid" ]; then
            continue
        fi
        FOUND_ANY=true
        stop_instance "$rid"
    done
fi

# Also stop any agent-controller containers not tracked by .run_state
docker ps -a --filter "name=agent-controller-" --format "{{.Names}}" 2>/dev/null | while read -r name; do
    if [ -n "$name" ]; then
        echo "Stopping untracked container: $name"
        docker stop "$name" 2>/dev/null || true
        docker rm -f "$name" 2>/dev/null || true
    fi
done

# Stop test runner via legacy PID file if present (backward compat)
if [ "$STOP_RUNNER" = true ] && [ -f "$SCRIPT_DIR/.test_runner.pid" ]; then
    RUNNER_PID=$(cat "$SCRIPT_DIR/.test_runner.pid")
    if ps -p "$RUNNER_PID" > /dev/null 2>&1; then
        echo "Killing legacy test runner (PID: $RUNNER_PID)"
        kill "$RUNNER_PID" 2>/dev/null || true
        sleep 1
        if ps -p "$RUNNER_PID" > /dev/null 2>&1; then
            kill -9 "$RUNNER_PID" 2>/dev/null || true
        fi
    fi
    rm -f "$SCRIPT_DIR/.test_runner.pid"
fi

# Best-effort: remove leftover mq_bench helper containers (Kafka verifiable consumer).
docker ps -a --filter "name=mqbench_consumer_" --format "{{.Names}}" 2>/dev/null | while read -r name; do
    if [ -n "$name" ]; then
        echo "Removing leftover container: $name"
        docker rm -f "$name" 2>/dev/null || true
    fi
done

# Clean up empty .run_state directory
if [ -d "$RUN_STATE_DIR" ] && [ -z "$(ls -A "$RUN_STATE_DIR" 2>/dev/null)" ]; then
    rmdir "$RUN_STATE_DIR" 2>/dev/null || true
fi

echo ""
echo "========================================"
echo "System stopped"
echo "========================================"

# Show remaining containers
REMAINING=$(docker ps --filter "name=agent-controller-" --format "{{.Names}}" 2>/dev/null)
if [ -n "$REMAINING" ]; then
    echo ""
    echo "Note: Some containers may still be running:"
    echo "$REMAINING"
fi
