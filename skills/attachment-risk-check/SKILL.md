---
name: attachment-risk-check
description: Attachment risk rating from MDDR delivery statistics
---
# attachment-risk-check


## Purpose
Assess attachment risk before opening, using MDDR 2026 cybercrime delivery statistics.

## Guidance
- Work only within the authorized scope. Never open the attachment to "check" — assess by type, source, and context first.
- Risk table (MDDR 2026 observed shares, cite with source):
  - SVG in mail body / as attachment — was the leading delivery mechanism (47% by November); QR-code payloads 145M+ wave.
  - DOC/DOCX — peaked at 17% (December); macro / template-injection risk.
  - HTML attachments with login forms — credential-harvesting pattern; open only in isolated browser, never enter credentials.
  - Archives (zip/iso/img) from unknown senders — treat as hostile until scanned.
- Procedure: 1) verify sender via separate channel if unexpected; 2) check extension vs. claimed content (double extensions, mismatch); 3) scan with local AV / VirusTotal only if approved; 4) open Office docs with macros disabled; 5) report suspected phish per drill scoring (S3).
- Minimize exposure of secrets: verdicts reference file names/hashes, never file contents.
- Use AgentMujo Core Skills for planning, research, debugging, verification, and reporting.

## Expected Output
Risk rating (low/elevated/high) with reasons, safe-handling steps taken, and remaining uncertainties.
