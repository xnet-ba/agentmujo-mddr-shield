#!/bin/bash
# alog.sh AGENT TOOL "ACTION" [RESULT] — append-only JSONL red u audit log.
# Escape/redakcija preko python3 (obavezan po install.sh --check).
# shortcut: rotacija je rucna (mjesecni fajl); upgrade na cron kad log naraste.
set -u
AGENT="${1:?agent}"; TOOL="${2:?tool}"; ACTION="${3:?action}"; RESULT="${4:-ok}"
LOG="${AGENT_AUDIT_LOG:-$HOME/.local/share/mddr-shield/audit.jsonl}"
mkdir -p "$(dirname "$LOG")"
[ -f "$LOG" ] || { touch "$LOG" && chmod 600 "$LOG"; }
export ALOG_AGENT="$AGENT" ALOG_TOOL="$TOOL" ALOG_ACTION="$ACTION" ALOG_RESULT="$RESULT" ALOG_LOG="$LOG"
python3 - <<'EOF'
import json, os, re
def clean(s):
    s = re.sub(r'[\x00-\x1f\x7f]', ' ', s)  # kontrolni znakovi van
    s = re.sub(r'(?i)(bearer\s+)\S+', r'\1REDACTED', s)
    s = re.sub(r'(?i)(password\s*[:=]\s*)\S+', r'\1REDACTED', s)
    s = re.sub(r'(?i)(api[_-]?key\s*[:=]\s*)\S+', r'\1REDACTED', s)
    return s[:2000]
rec = {"ts": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
       "agent": clean(os.environ["ALOG_AGENT"]), "tool": clean(os.environ["ALOG_TOOL"]),
       "action": clean(os.environ["ALOG_ACTION"]), "result": clean(os.environ["ALOG_RESULT"])}
with open(os.environ["ALOG_LOG"], "a") as f:
    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
EOF
