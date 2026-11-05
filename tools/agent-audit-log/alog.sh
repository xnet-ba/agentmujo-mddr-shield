#!/bin/bash
# alog.sh AGENT TOOL "ACTION" [RESULT] — append-only JSONL red u audit log.
# shortcut: rotacija je ručna (mjesečni fajl); upgrade na cron kad log naraste.
LOG="${AGENT_AUDIT_LOG:-$HOME/.local/share/mddr-shield/audit.jsonl}"
TS="$(date -Iseconds)"
AGENT="${1:?agent}"; TOOL="${2:?tool}"; ACTION="${3:?action}"; RESULT="${4:-ok}"
printf '{"ts":"%s","agent":"%s","tool":"%s","action":"%s","result":"%s"}\n' \
  "$TS" "$AGENT" "$TOOL" "${ACTION//\"/}" "$RESULT" >> "$LOG"
