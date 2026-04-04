#!/usr/bin/env bash
set -euo pipefail

target_dir="${1:?target dir required}"
primary_url="${2:-}"
fallback_url="${3:-}"

tmp_dir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_dir"
}
trap cleanup EXIT

install_from_url() {
  local url="$1"
  local archive_path="$tmp_dir/ycsb.tar.gz"
  local extract_dir="$tmp_dir/extract"
  local entrypoint
  local root_dir

  [[ -n "$url" ]] || return 1

  rm -rf "$archive_path" "$extract_dir" "$target_dir"
  mkdir -p "$extract_dir"

  curl -fL --retry 3 --retry-delay 1 -o "$archive_path" "$url"
  tar -xzf "$archive_path" -C "$extract_dir"

  entrypoint="$(
    find "$extract_dir" -type f \( -path '*/bin/ycsb.sh' -o -path '*/bin/ycsb' \) | head -n 1
  )"
  [[ -n "$entrypoint" ]] || return 1

  root_dir="${entrypoint%/bin/ycsb.sh}"
  root_dir="${root_dir%/bin/ycsb}"
  mv "$root_dir" "$target_dir"
  chmod +x "$target_dir"/bin/ycsb*
}

install_from_url "$primary_url" || install_from_url "$fallback_url"

test -x "$target_dir/bin/ycsb.sh" -o -x "$target_dir/bin/ycsb"
