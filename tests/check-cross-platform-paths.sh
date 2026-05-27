#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

fail=0

check_no_pattern() {
  local pattern="$1"
  local description="$2"
  shift 2

  if rg -n "$pattern" "$@" >/tmp/zk-cross-platform-paths.$$; then
    echo "FAIL: $description"
    cat /tmp/zk-cross-platform-paths.$$
    fail=1
  else
    echo "OK: $description"
  fi
  rm -f /tmp/zk-cross-platform-paths.$$
}

cd "$repo_root"

check_no_pattern "'([^']*skills\\\\zk-creative-process|[^']*\\.codex\\\\skills|[^']*\\.tmp\\\\[^']*)'" \
  "native macOS/Linux scripts should not hard-code Windows-only path fragments" \
  scripts/*.sh scripts/*.py skills/zk-creative-process/scripts/*.sh skills/zk-creative-process/scripts/*.py

check_no_pattern '"([^"]*skills\\\\zk-creative-process|[^"]*\\.codex\\\\skills|[^"]*\\.tmp\\\\[^"]*)"' \
  "native macOS/Linux scripts should not hard-code Windows-only path fragments in double-quoted strings" \
  scripts/*.sh scripts/*.py skills/zk-creative-process/scripts/*.sh skills/zk-creative-process/scripts/*.py

check_no_pattern '\\.\\scripts\\|C:\\path|USERPROFILE.*quick_validate|Validate skill metadata on Windows' \
  "user docs should include cross-platform commands instead of Windows-only examples" \
  README.md skills/zk-creative-process/SKILL.md docs examples

exit "$fail"
