#!/usr/bin/env python3
"""audit.py — one-command MDDR system check. Read-only, stdlib only.

Usage: audit.py --hosts h1 h2 [...] --out-dir DIR
Runs: asset-inventory (T4) -> tls-inventory (T5) -> sbom-inventory (T9)
      -> shield-status (T8) -> report.json + console summary.
Identity checks (MFA/2FA/SSH) stay skill-guided (S1): platform-specific.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(ROOT, "tools")


def run(mod, *args):
    r = subprocess.run([sys.executable, mod, *args], capture_output=True, text=True)
    return r


def main():
    a = sys.argv[1:]
    hosts, out = [], None
    i = 0
    while i < len(a):
        if a[i] == "--hosts":
            i += 1
            while i < len(a) and not a[i].startswith("--"):
                hosts.append(a[i]); i += 1
        elif a[i] == "--out-dir" and i + 1 < len(a):
            out = a[i + 1]; i += 2
        else:
            i += 1
    if not hosts or not out:
        print(__doc__)
        sys.exit(2)
    os.makedirs(out, exist_ok=True)
    snap = os.path.join(out, "asset.json")
    tlsf = os.path.join(out, "tls.json")
    sbomf = os.path.join(out, "sbom.json")

    r = run(os.path.join(TOOLS, "asset-inventory", "inventory.py"), "--snap", snap)
    if r.returncode != 0:
        print("asset-inventory FAILED:\n" + r.stderr[:500]); sys.exit(1)
    r = run(os.path.join(TOOLS, "tls-inventory", "tls_inventory.py"), *hosts, "--json-out", tlsf)
    if r.returncode != 0:
        print("tls-inventory FAILED:\n" + r.stderr[:500]); sys.exit(1)
    r = run(os.path.join(TOOLS, "sbom-inventory", "sbom.py"), "--snap", sbomf)
    if r.returncode != 0:
        print("sbom-inventory FAILED:\n" + r.stderr[:500]); sys.exit(1)

    r = run(os.path.join(TOOLS, "shield-status", "status.py"),
            "--asset", snap, "--tls", tlsf)
    print(r.stdout)
    if r.returncode != 0:
        print("shield-status reported input problems (see above)")
    try:
        for f in (snap, tlsf, sbomf):
            json.load(open(f))
    except Exception as e:
        print(f"collection output invalid: {e}")
        sys.exit(1)
    report = {"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "hosts": hosts,
              "files": {"asset": snap, "tls": tlsf, "sbom": sbomf},
              "summary": [ln for ln in r.stdout.splitlines() if ln and not ln.startswith("{")]}
    rep = os.path.join(out, "report.json")
    json.dump(report, open(rep, "w"), indent=2)
    print(f"report -> {rep}")
    print("NOTE: identity checks (MFA/2FA/SSH) are skill-guided: see S1 mddr-threat-checklist.")


if __name__ == "__main__":
    main()
