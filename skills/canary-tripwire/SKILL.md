---
name: canary-tripwire
description: Tripwire canary strategy and check cadence
---
# canary-tripwire


## Purpose
Catch intruders early with tripwire canaries (MDDR assume-breach mindset): inert decoy files whose only reader is an attacker or a mistake.

## Guidance
- Work only within the authorized scope. Deploy only on systems you administer.
- DETECTION SCOPE (honest): hash comparison catches WRITE, delete, and replace —
  it does NOT catch read-only access (`cat`). A canary proves someone wrote where
  they shouldn't, not who looked. For read detection you need kernel auditing
  (auditd/inotify), which is outside this tool.
- Placement: directories attackers enumerate first — home roots, web roots, backup dirs, `/tmp`-adjacent shares. Names must look valuable but never collide with real files (`.backup-keys.txt`, `.old-credentials.bak`, `passwords-old.csv`).
- The tool REFUSES to overwrite an existing non-canary file (checks tripwire marker).
- The `canary.py` tool handles deploy (`canary.py deploy DIR`) and verification (`canary.py check`); schedule `check` at least daily (existing cron or manual).
- On TRIP: treat as Runbook 1/3 (ir-runbooks-mdrr) — preserve the canary, snapshot logs, do not tip off by deleting immediately; investigate first, then rotate and redeploy.
- Never place a canary where legitimate automation writes (backups, log rotation) — false trips erode trust.
- Minimize exposure of secrets: canaries contain NO real credentials, only tripwire text.
- Use your core planning/research skills for planning, research, debugging, verification, and reporting.

## Expected Output
Deployment map (dir → canaries), check cadence, trip procedure reference, and remaining uncertainties.
