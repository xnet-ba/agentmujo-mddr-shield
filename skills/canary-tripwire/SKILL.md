# canary-tripwire

## Purpose
Catch intruders early with tripwire canaries (MDDR assume-breach mindset): inert decoy files whose only reader is an attacker or a mistake.

## Guidance
- Work only within the authorized scope. Deploy only on systems you administer.
- Placement: directories attackers enumerate first — home roots, web roots, backup dirs, `/tmp`-adjacent shares. Names must look valuable but never collide with real files (`.backup-keys.txt`, `.old-credentials.bak`, `passwords-old.csv`).
- The `canary.py` tool handles deploy (`canary.py deploy DIR`) and verification (`canary.py check`); schedule `check` at least daily (existing cron or manual).
- On TRIP: treat as Runbook 1/3 (ir-runbooks-mdrr) — preserve the canary, snapshot logs, do not tip off by deleting immediately; investigate first, then rotate and redeploy.
- Never place a canary where legitimate automation writes (backups, log rotation) — false trips erode trust.
- Minimize exposure of secrets: canaries contain NO real credentials, only tripwire text.
- Use AgentMujo Core Skills for planning, research, debugging, verification, and reporting.

## Expected Output
Deployment map (dir → canaries), check cadence, trip procedure reference, and remaining uncertainties.
