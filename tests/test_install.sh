#!/bin/bash
# test_install.sh — installer/uninstaller round-trip in a temp HOME. No touch of real config.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
T="$(mktemp -d)"
mkdir -p "$T/.config/opencode"
echo '{"mcp":{}}' > "$T/.config/opencode/opencode.json"
"$REPO/install.sh" --home "$T" >/dev/null || { echo "FAIL install"; exit 1; }
[ -f "$T/.config/opencode/skills/mddr-threat-checklist/SKILL.md" ] && echo "PASS skills" || { echo "FAIL skills"; exit 1; }
python3 -c "import json;d=json.load(open('$T/.config/opencode/opencode.json'));assert d['mcp']['threat-feed']['command'][1]=='$T/.local/share/mddr-shield/threat-feed-mcp/server.py';print('PASS mcp entry')" || exit 1
"$REPO/install.sh" --home "$T" >/dev/null && echo "PASS idempotent" || { echo "FAIL idempotent"; exit 1; }
"$REPO/uninstall.sh" --home "$T" >/dev/null || { echo "FAIL uninstall"; exit 1; }
python3 -c "import json;d=json.load(open('$T/.config/opencode/opencode.json'));assert 'threat-feed' not in d.get('mcp',{});print('PASS clean')" || exit 1
[ ! -d "$T/.local/share/mddr-shield/threat-feed-mcp" ] && echo "PASS server removed" || { echo "FAIL server"; exit 1; }
mkdir -p "$T/.local/share/mddr-shield" && echo '{"x":1}' > "$T/.local/share/mddr-shield/audit.jsonl"
"$REPO/uninstall.sh" --home "$T" >/dev/null
[ -f "$T/.local/share/mddr-shield/audit.jsonl" ] && echo "PASS user data kept" || { echo "FAIL userdata"; exit 1; }
rm -rf "$T"
echo "SVE PASS"
