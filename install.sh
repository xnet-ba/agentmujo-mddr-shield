#!/bin/bash
# install.sh — install mddr-shield on ANY OpenCode agent. Idempotent.
# Usage: ./install.sh [--home DIR] (default $HOME)
# Does: copy skills -> skills dir, server+tools -> data dir, add threat-feed MCP (with backup).
set -u
REPO="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="${1:-$HOME}"
[ "${1:-}" = "--home" ] && HOME_DIR="${2:-$HOME}"
SKILLS_DIR="$HOME_DIR/.config/opencode/skills"
CONFIG="$HOME_DIR/.config/opencode/opencode.json"
DATA="$HOME_DIR/.local/share/mddr-shield"

mkdir -p "$SKILLS_DIR" "$DATA"
for s in mddr-threat-checklist agent-baseline-monitor clickfix-phishing-drill ai-memory-poison-guard attachment-risk-check ir-runbooks-mdrr canary-tripwire; do
  if [ -d "$SKILLS_DIR/$s" ] && diff -q "$REPO/skills/$s/SKILL.md" "$SKILLS_DIR/$s/SKILL.md" >/dev/null; then
    echo "skip skills/$s (isti)"
  else
    mkdir -p "$SKILLS_DIR/$s" && cp "$REPO/skills/$s/SKILL.md" "$SKILLS_DIR/$s/SKILL.md" && echo "skill $s"
  fi
done
cp -r "$REPO/servers/threat-feed-mcp" "$DATA/" 2>/dev/null || { rm -rf "$DATA/threat-feed-mcp"; cp -r "$REPO/servers/threat-feed-mcp" "$DATA/"; }
mkdir -p "$DATA/tools" && cp -r "$REPO/tools/." "$DATA/tools/" && chmod +x "$DATA/tools/agent-audit-log/alog.sh"
echo "data -> $DATA"

[ -f "$CONFIG" ] || { echo "nema $CONFIG — preskacem MCP"; exit 0; }
[ -f "$CONFIG.bak-mddr-shield" ] || cp "$CONFIG" "$CONFIG.bak-mddr-shield"
python3 - "$CONFIG" "$DATA" <<'EOF'
import json, sys
cfg, data = sys.argv[1], sys.argv[2]
d = json.load(open(cfg))
mcp = d.setdefault('mcp', {})
mcp['threat-feed'] = {"type": "local",
    "command": ["python3", f"{data}/threat-feed-mcp/server.py"], "enabled": True}
json.dump(d, open(cfg, 'w'), indent=2)
print('mcp threat-feed upisan')
EOF
echo "gotovo. vazi od sljedece sesije."
