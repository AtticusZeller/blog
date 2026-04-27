#!/usr/bin/env bash
# sync.sh — Sync content from main -> page, convert syntax, build Hugo site.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Syncing main -> page ==="

# Extract posts from main branch
rm -rf content/posts/
mkdir -p content/posts
git archive main -- posts/ | tar -x -C content/ --strip-components=0

# Convert Obsidian syntax -> Hugo syntax
converted=0
for f in content/posts/*.md; do
    [ -f "$f" ] || continue
    uv run python3 obs2hugo.py "$f" "$f"
    converted=$((converted + 1))
done

echo "Synced + converted $converted posts"

# Build
echo "=== Building Hugo site ==="
hugo --minify

echo "=== Done. public/ ready for deploy ==="
echo "To deploy: git add -A && git commit -m 'deploy' && git push origin page"
