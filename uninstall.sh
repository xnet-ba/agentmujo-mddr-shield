#!/bin/bash
# uninstall.sh — remove mddr-shield. Usage: ./uninstall.sh [--home DIR]
set -u
REPO="$(cd "$(dirname "$0")" && pwd)"
HOME_DIR="${1:-$HOME}"
[ "${1:-}" = "--home" ] && HOME_DIR="${2:-$HOME}"
SKILLS_DIR="$HOME_DIR/.config/opencode/skills"
CONFIG="$HOME_DIR/.config/opencode/opencode.json"
DATA="$HOME_DIR/.local/share/mddr-shield"

for s in mddr-threat-checklist agent-baseline-monitor clickfix-phishing-drill ai-memory-poison-guard attachment-risk-check ir-runbooks-mdrr canary-tripwire; do
  if [ -d "$SKILLS_DIR/$s" ]; then
    if diff -q "$REPO/skills/$s/SKILL.md" "$SKILLS_DIR/$s/SKILL.md" >/dev/null 2>&1; then
      rm -rf "$SKILLS_DIR/$s" && echo "uklonjen skill $s"
    else
      echo "preskacem $s (izmijenjen rucno)"
    fi
  fi
done
if [ -f "$CONFIG" ]; then
  python3 - "$CONFIG" <<'EOF'
import json, os, sys, tempfile
cfg = sys.argv[1]
try:
    d = json.load(open(cfg))
except Exception as e:
    print(f"NE MOGU procitati {cfg}: {e}")
    sys.exit(3)
if 'threat-feed' in d.get('mcp', {}):
    del d['mcp']['threat-feed']
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(cfg) or ".")
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, cfg)
    print('mcp threat-feed uklonjen')
else:
    print('mcp vec cist')
EOF
fi
[ -d "$DATA" ] && rm -rf "$DATA/threat-feed-mcp" "$DATA/tools" && rmdir "$DATA" 2>/dev/null && echo "uklonjen $DATA" || echo "$DATA sacuvan (korisnicki podaci: audit.jsonl, *-state.json, snimci)"
echo "gotovo. backup: $CONFIG.bak-mddr-shield"
