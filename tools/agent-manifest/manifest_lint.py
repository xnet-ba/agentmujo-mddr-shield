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
    if not isinstance(m, dict):
        return ["manifest must be an object"]
    for f in REQUIRED:
        if f not in m:
            errs.append(f"missing: {f}")
    for f in ("agent", "identity"):
        if f in m and (not isinstance(m[f], str) or not m[f].strip()):
            errs.append(f"{f} must be a non-empty string")
    if "tools" in m and (not isinstance(m["tools"], list) or not m["tools"]
                         or not all(isinstance(t, str) and t.strip() for t in m["tools"])):
        errs.append("tools must be a non-empty list of strings")
    lim = m.get("limits", {})
    if "limits" in m and not isinstance(lim, dict):
        errs.append("limits must be an object")
    elif isinstance(lim, dict):
        mx = lim.get("max_shell_per_min")
        if "max_shell_per_min" in lim and (isinstance(mx, bool) or not isinstance(mx, int) or mx <= 0):
            errs.append("limits.max_shell_per_min must be a positive int")
        ah = lim.get("allowed_hours")
        if "allowed_hours" in lim:
            import re as _re
            mm = _re.match(r"^(\d{2})-(\d{2})$", ah) if isinstance(ah, str) else None
            bad = not mm or not (0 <= int(mm.group(1)) <= 23 and 0 <= int(mm.group(2)) <= 23)
            if bad:
                errs.append("limits.allowed_hours must be HH-HH with 00-23")
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
