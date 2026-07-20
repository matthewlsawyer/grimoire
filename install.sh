#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $(basename "$0")"
    echo ""
    echo "  Install grimoire skills into the invoking directory's .agents/skills/"
    echo "  Run from the project that should receive the spells."
    exit 1
}

if [[ $# -ne 0 ]]; then
    usage
fi

GRIMOIRE_ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST_ROOT="$(pwd)/.agents/skills"

mkdir -p "$DEST_ROOT"

shopt -s nullglob
skill_dirs=()
for dir in "$GRIMOIRE_ROOT"/*/; do
    if [[ -f "${dir}SKILL.md" ]]; then
        skill_dirs+=("$dir")
    fi
done
shopt -u nullglob

if ((${#skill_dirs[@]} == 0)); then
    echo "Error: no skills with SKILL.md under $GRIMOIRE_ROOT"
    exit 1
fi

echo "▶ Installing grimoire → $DEST_ROOT"
echo ""

installed=0
for skill_dir in "${skill_dirs[@]}"; do
    skill_name="$(basename "$skill_dir")"
    target="$DEST_ROOT/$skill_name"
    rm -rf "$target"
    cp -R "$skill_dir" "$target"
    echo "  ✓ $skill_name/"
    installed=$((installed + 1))
done

echo ""
echo "✓ Installation complete"
echo ""
echo "  Source: $GRIMOIRE_ROOT"
echo "  Dest:   $DEST_ROOT"
echo "  Skills: $installed installed"
