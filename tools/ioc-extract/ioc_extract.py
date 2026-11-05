#!/usr/bin/env python3
"""ioc_extract.py — extract threat indicators from a report text file to JSON.

Usage: ioc_extract.py INPUT.txt [-o iocs.json]
Extracts: CVE IDs, MITRE-like technique names, known threat/malware family
mentions, and money/scale figures with page context. Stdlib only.
"""
import json
import re
import sys

CVE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b")
TECH = re.compile(
    r"\b(ClickFix|QR[- ]?phishing|password spray|token abuse|credential theft|"
    r"prompt injection|cross-prompt injection|XPIA|memory poisoning|"
    r"spear phishing|ransomware|supply[- ]chain compromise|DDoS|"
    r"drive-by compromise|trusted relationship|valid accounts|"
    r"external remote services|malicious link injection|jailbreak|"
    r"goal hijacking|data exfiltration|reconnaissance)\b",
    re.IGNORECASE,
)
FAMILY = re.compile(
    r"\b(Qilin|Akira|PlayCrypt|Gentlemen|INC Ransom|Sinobi|Tycoon2FA|"
    r"Pesky Pika|TikTok ClickFix)\b"
)
SCALE = re.compile(
    r"(\d[\d.,]*\s*(?:trillion|billion|million)|\d+\s*%|\d+\s*attacks)"
)

PAGE = re.compile(r"===== PAGE (\d+) =====")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "-o" else None
    if len(sys.argv) > 2 and not out and sys.argv[2] != "-o":
        print(__doc__)
        sys.exit(1)
    if out is None and len(sys.argv) > 3:
        out = sys.argv[3]

    text = open(src, encoding="utf-8", errors="replace").read()
    # split into page chunks for context
    parts = PAGE.split(text)
    chunks = []
    if parts[0].strip():
        chunks.append(("0", parts[0]))
    for i in range(1, len(parts), 2):
        chunks.append((parts[i], parts[i + 1] if i + 1 < len(parts) else ""))

    seen = set()
    iocs = []
    for page, chunk in chunks:
        for kind, rx in (("cve", CVE), ("technique", TECH),
                         ("family", FAMILY), ("scale", SCALE)):
            for m in rx.finditer(chunk):
                val = re.sub(r"\s+", " ", m.group(0)).strip()
                key = (kind, val.lower())
                if key in seen:
                    continue
                seen.add(key)
                iocs.append({"type": kind, "value": val, "page": int(page)})

    result = {"source": src, "count": len(iocs), "indicators": iocs}
    js = json.dumps(result, indent=2, ensure_ascii=False)
    if out or "-o" in sys.argv:
        out = out or "iocs.json"
        open(out, "w", encoding="utf-8").write(js)
        print(f"wrote {out} ({len(iocs)} indicators)")
    else:
        print(js)


if __name__ == "__main__":
    main()
