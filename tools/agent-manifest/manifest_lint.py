#!/usr/bin/env python3
"""manifest_lint.py — validate an agent manifest (JSON). Stdlib only.

Manifest (JSON): {"agent": str, "identity": str, "tools": [str...],
  "limits": {"max_shell_per_min": int, "allowed_hours": "HH-HH"}}
Usage: manifest_lint.py manifest.json  (exit 0 = OK, 1 = errors listed)
Why JSON not YAML: zero dependencies on any agent.
"""
import json
import re
import sys

REQUIRED = ("agent", "identity", "tools")


def lint(m):
    errs = []
    for f in REQUIRED:
        if f not in m:
            errs.append(f"missing: {f}")
    if "tools" in m and (not isinstance(m["tools"], list) or not m["tools"]):
        errs.append("tools must be a non-empty list")
    lim = m.get("limits", {})
    if "max_shell_per_min" in lim and not isinstance(lim["max_shell_per_min"], int):
        errs.append("limits.max_shell_per_min must be int")
    if "allowed_hours" in lim and not re.match(r"^\d{2}-\d{2}$", lim["allowed_hours"]):
        errs.append("limits.allowed_hours must be HH-HH")
    # S2 compatibility: baseline needs identity + tool list
    return errs


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    m = json.load(open(sys.argv[1]))
    errs = lint(m)
    if errs:
        print("INVALID:")
        for e in errs:
            print(f" - {e}")
        sys.exit(1)
    print(f"OK: {m.get('agent')} (identity={m.get('identity')}, "
          f"tools={len(m.get('tools', []))})")


if __name__ == "__main__":
    main()
