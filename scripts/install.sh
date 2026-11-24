#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEMINI_CFG_DIR="$HOME/.gemini/config"
AGENTS_SKILLS_DIR="$HOME/.agents/skills"

mkdir -p "$GEMINI_CFG_DIR" "$AGENTS_SKILLS_DIR"

chmod +x "$REPO_ROOT/skills/lit-search-verify/scripts/search_papers.py"
chmod +x "$REPO_ROOT/skills/lit-search-verify/scripts/verify_bibtex.py"

ln -sfn "$REPO_ROOT/GEMINI.md" "$GEMINI_CFG_DIR/GEMINI.md"

cat > "$GEMINI_CFG_DIR/skills.json" <<EOF
{
  "entries": [
    { "path": "$REPO_ROOT/skills" }
  ]
}
EOF

for skill_dir in "$REPO_ROOT/skills"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  ln -sfn "$skill_dir" "$AGENTS_SKILLS_DIR/$skill_name"
done

echo "Linked GEMINI.md -> $GEMINI_CFG_DIR/GEMINI.md"
echo "Wrote skills.json -> $GEMINI_CFG_DIR/skills.json (path: $REPO_ROOT/skills)"
echo "Linked skills -> $AGENTS_SKILLS_DIR"
