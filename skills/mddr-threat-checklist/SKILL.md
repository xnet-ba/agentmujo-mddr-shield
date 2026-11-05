---
name: mddr-threat-checklist
description: Turn the 10 MDDR 2026 priorities into a verifiable checklist
---
# mddr-threat-checklist


## Purpose
Turn the 10 Microsoft Digital Defense Report 2026 priorities (p. 7) into a verifiable checklist for a concrete environment (Test Lab, Test Lab, or any small infra).

## Guidance
- Work only within the authorized scope. Read-only checks first (`read-only CLI listing`, `ls`, `stat`, log reads); never change production config without explicit approval.
- Map each priority to: concrete check → evidence (command + output) → rating (🟢 ok / 🟡 recommendation / 🔴 critical).
- The 10 priorities: 1) govern cyber risk at leadership level; 2) defend identity as primary control plane (passkeys, phishing-resistant MFA, privilege reduction, JIT/rotation); 3) AI governance and data controls; 4) reduce exposure and edge risk (asset inventory, patch edge fast); 5) cross-signal correlation; 6) continuous threat-vulnerability management; 7) validate exposure via proactive (assume-breach) testing; 8) secure software dependencies (inventory, provenance, containment); 9) collective defense (share indicators); 10) long-horizon transitions (cryptographic inventory, post-quantum planning).
- Scale enterprise recommendations down: 2 machines + cloud means the same controls, lighter tooling.
- Distinguish confirmed findings from hypotheses. Never invent 2FA/MFA status — read it from the system.
- Minimize exposure of secrets: checklist reports statuses, never keys, tokens, or reset codes.
- Use AgentMujo Core Skills for planning, research, debugging, verification, and reporting.

## Expected Output
Status table (check → evidence → 🟢/🟡/🔴), list of items needing approval (with exact commands to fix), recommended re-check trigger, and remaining uncertainties.
