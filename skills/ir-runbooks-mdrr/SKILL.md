---
name: ir-runbooks-mdrr
description: First-hour runbooks: token abuse, ClickFix trace, ransomware
---
# ir-runbooks-mdrr


## Purpose
Three MDDR-grounded incident runbooks for a small infra (few hosts + cloud). Complements the general `incident-response` skill with concrete first-hour steps.

## Guidance
- Work only within the authorized scope. Preserve evidence before containing: snapshot logs, list sessions, freeze the state you found.
- Runbook 1 — suspected token/session abuse: snapshot what you can in parallel (active sessions, last log lines), then revoke and rotate IMMEDIATELY — do not wait for full forensics. Hunt after containment (audit log, auth log). Identity-first (MDDR priority 2).
- Runbook 2 — ClickFix trace on a machine: assume user executed the lure; isolate host from network, capture browser history/downloads, check scheduled tasks and startup entries, reimage-or-rebuild rather than "clean".
- Runbook 3 — suspected ransomware: disconnect affected host immediately (do not shut down before memory capture if feasible), verify backups are intact and OFFLINE before any restore, restore to isolation and validate, then reintroduce. Never pay before exhausting restore options.
- After each: write a one-page postmortem (timeline, root cause, gap closed) and feed indicator changes back into the threat feed.
- Minimize exposure of secrets: runbooks handle credentials by reference (IDs), rotate — never log values.
- Use your core planning/research skills for planning, research, debugging, verification, and reporting.

## Expected Output
Executed runbook with timestamped steps, evidence inventory, containment and recovery status, postmortem, and remaining uncertainties.
