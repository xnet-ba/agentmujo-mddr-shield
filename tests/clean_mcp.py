#!/usr/bin/env python3
"""clean_mcp.py — remove threat-feed entry from opencode.json. Atomic, loud errors."""
import json
import os
import sys
import tempfile

cfg = sys.argv[1]
try:
    with open(cfg) as f:
        d = json.load(f)
except Exception as e:
    print(f"NE MOGU procitati {cfg}: {e} — server se NE brise, nista nije dirano")
    sys.exit(3)
if "threat-feed" in d.get("mcp", {}):
    del d["mcp"]["threat-feed"]
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(cfg) or ".")
    with os.fdopen(fd, "w") as f:
        json.dump(d, f, indent=2)
    os.replace(tmp, cfg)
    print("mcp threat-feed uklonjen")
else:
    print("mcp vec cist")
