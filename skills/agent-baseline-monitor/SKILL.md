---
name: agent-baseline-monitor
description: Per-agent behavior baseline and anomaly detection
---
# agent-baseline-monitor


## Purpose
Detect anomalous AI-agent behavior by comparing live tool-use against a per-agent baseline (MDDR 2026, p. 17: normal = which identity, which tools, at what frequency — deviation becomes visible).

## Guidance
- Work only within the authorized scope. Read the audit log (`audit.jsonl` from `agent-audit-log`); never modify agent permissions as a side effect.
- Input: path to JSONL log (`ts, agent, tool, action, cost_ms?, result`) + time window (default 7 days).
- Build a baseline profile per agent: tool set, calls/min distribution, active hours, deny/error rate.
- Apply rules (defaults, calibrate after 2 weeks of logs): shell-burst (>30 shell calls/min) → alert + review; first use of a tool outside the agent's list → alert; activity 01–05h without announced work → alert; >10 deny/error in 5 min → alert + temporary stop proposal; cost 10x above average → review.
- Threat actors operate through valid credentials and sanctioned workflows, so the finding must show *why* the deviation matters, not just that a threshold fired.
- Minimize exposure of secrets: truncate action strings, never log tokens or keys.
- Use AgentMujo Core Skills for planning, research, debugging, verification, and reporting.

## Expected Output
Per-agent baseline profiles, ranked deviations with evidence (log excerpts), threshold-calibration suggestions, and remaining uncertainties.
