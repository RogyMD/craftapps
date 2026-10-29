#!/bin/sh
# Structural checks for every skill in skills/.
# Usage (from the repository root): sh scripts/validate-skills.sh
# Dependencies: POSIX sh, awk, grep, sed, git (optional, for the ignore check).

status=0
fail() { echo "  FAIL: $*"; status=1; skill_ok=0; }

# Print the value of a single-line frontmatter field from a Markdown file.
field() {
  awk -v key="$2" '
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---" { exit }
    NR > 1 && index($0, key ":") == 1 { sub("^" key ":[ ]*", ""); print; exit }
  ' "$1"
}

# Check that relative Markdown links in a file point to existing files.
check_links() {
  dir=$(dirname "$1")
  grep -o '\]([^)#]*)' "$1" | sed 's/^](//; s/)$//' | while read -r target; do
    case "$target" in
      http://*|https://*|mailto:*|"") continue ;;
    esac
    [ -e "$dir/$target" ] || echo "  FAIL: $1 links to missing $target"
  done
}

[ -d skills ] || { echo "Run from the repository root."; exit 1; }

for skill_dir in skills/*/; do
  skill_dir=${skill_dir%/}
  dir_name=$(basename "$skill_dir")
  skill_md="$skill_dir/SKILL.md"
  skill_ok=1
  echo "$dir_name"

  [ -f "$skill_md" ] || { fail "missing SKILL.md"; continue; }
  [ "$(head -n 1 "$skill_md")" = "---" ] || fail "SKILL.md must start with YAML frontmatter (---)"

  name=$(field "$skill_md" name)
  description=$(field "$skill_md" description)

  [ "$name" = "$dir_name" ] || fail "name '$name' must match directory '$dir_name'"
  echo "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' || fail "name must be lowercase letters, digits, hyphens"
  [ ${#name} -le 64 ] || fail "name longer than 64 characters"
  case "$name" in *-app) ;; *) fail "name must end with '-app'" ;; esac

  [ -n "$description" ] || fail "missing description"
  [ ${#description} -le 1024 ] || fail "description longer than 1024 characters (${#description})"
  case "$description" in "Use when"*) ;; *) fail "description should start with 'Use when'" ;; esac

  lines=$(wc -l < "$skill_md" | tr -d ' ')
  [ "$lines" -le 500 ] || fail "SKILL.md has $lines lines (limit 500)"

  for md in "$skill_md" "$skill_dir"/references/*.md "$skill_dir"/examples/*.md; do
    [ -f "$md" ] || continue
    out=$(check_links "$md")
    [ -z "$out" ] || { echo "$out"; status=1; skill_ok=0; }
  done

  # Example artifacts must carry the handoff frontmatter.
  for md in "$skill_dir"/examples/*.md; do
    [ -f "$md" ] || continue
    [ -n "$(field "$md" craftapps_artifact)" ] || fail "$md missing craftapps_artifact frontmatter"
    [ -n "$(field "$md" schema_version)" ] || fail "$md missing schema_version frontmatter"
  done

  [ "$skill_ok" -eq 1 ] && echo "  ok: name=$name, description=${#description} chars, SKILL.md=$lines lines"
done

# Fixtures and skill files must not be hidden by .gitignore.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "gitignore"
  ignored=$(find skills examples -type f ! -path '*/__pycache__/*' | git check-ignore --stdin)
  if [ -n "$ignored" ]; then
    fail "files ignored by .gitignore (rename them or adjust patterns):"
    echo "$ignored" | sed 's/^/    /'
  else
    echo "  ok: no skill or example files are ignored"
  fi
fi

[ "$status" -eq 0 ] && echo "All checks passed." || echo "Validation failed."
exit "$status"
