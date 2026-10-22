#!/usr/bin/env bash
set -euo pipefail

current=$(git branch --show-current)
target="${1:-}"

if [[ -z "$target" ]]; then
  echo "Usage: bash switch.sh <main|page>"
  echo "Current branch: $current"
  exit 1
fi

if [[ "$target" == "$current" ]]; then
  echo "Already on $target"
  exit 0
fi

rm -f .hugo_build.lock
git checkout "$target"
echo "Switched to $target"
