#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

entrypoints=(
  "scripts/install-skill.sh"
  "scripts/check-environment.sh"
  "scripts/process-reference-video-phase1.sh"
  "scripts/process-reference-videos-mix.sh"
  "scripts/check-creative-material.sh"
  "scripts/test-install.sh"
)

for file in "${entrypoints[@]}"; do
  test -f "$file" || { echo "missing $file"; exit 1; }
  test -x "$file" || { echo "not executable $file"; exit 1; }
  if rg -n 'pwsh|powershell|\.ps1' "$file"; then
    echo "$file must be a native macOS/Linux entrypoint, not a PowerShell wrapper"
    exit 1
  fi
done

if rg -n 'pwsh|PowerShell 7|brew install --cask powershell' README.md skills/zk-creative-process/SKILL.md examples docs; then
  echo "Mac-facing docs should use native .sh entrypoints, not pwsh."
  exit 1
fi

bash -n "${entrypoints[@]}"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

scripts/check-environment.sh --test-dir "$tmp_dir/env-check"

scripts/install-skill.sh --codex-skills-dir "$tmp_dir/skills"
test -f "$tmp_dir/skills/zk-creative-process/SKILL.md"
test -x "$tmp_dir/skills/zk-creative-process/scripts/check-environment.sh"
