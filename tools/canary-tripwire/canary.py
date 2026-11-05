#!/usr/bin/env python3
"""canary.py — deploy and check tripwire canaries. Stdlib only.

Usage: canary.py deploy DIR [--state FILE]   # drop canary files, record hashes
       canary.py check [--state FILE]         # exit 0 = OK, 1 = TRIP (lists touched)
Canaries are inert text files; any read won't trip them, any WRITE will.
"""
import hashlib
import json
import os
import sys
import time

CANARY_NAMES = (".backup-keys.txt", ".old-credentials.bak", "passwords-old.csv")
CANARY_TEXT = ("DO NOT USE — decommissioned credential store.\n"
               "If you are reading this on a server, report it: this file is a tripwire.\n")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def deploy(d, state):
    os.makedirs(d, exist_ok=True)
    st = {"deployed_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "canaries": []}
    if os.path.exists(state):
        try:
            st = json.load(open(state))
        except Exception:
            pass
    for n in CANARY_NAMES:
        p = os.path.join(d, n)
        if not os.path.exists(p):
            open(p, "w").write(CANARY_TEXT)
        st["canaries"] = [c for c in st["canaries"] if c["path"] != p]
        st["canaries"].append({"path": p, "sha256": sha(p)})
    json.dump(st, open(state, "w"), indent=2)
    print(f"deployed {len(CANARY_NAMES)} canaries in {d}")


def check(state):
    if not os.path.exists(state):
        print("no state — deploy first")
        sys.exit(2)
    st = json.load(open(state))
    tripped = [c["path"] for c in st["canaries"]
               if not os.path.exists(c["path"]) or sha(c["path"]) != c["sha256"]]
    if tripped:
        print("TRIP:")
        for p in tripped:
            print(f" - {p}")
        sys.exit(1)
    print(f"OK: {len(st['canaries'])} canaries untouched")


def main():
    a = sys.argv[1:]
    state = os.path.expanduser("~/.local/share/mddr-shield/canary-state.json")
    if "--state" in a:
        state = a[a.index("--state") + 1]
    if not a or a[0] not in ("deploy", "check"):
        print(__doc__)
        sys.exit(2)
    if a[0] == "deploy":
        if len(a) < 2 or a[1].startswith("--"):
            print("deploy needs DIR")
            sys.exit(2)
        deploy(a[1], state)
    else:
        check(state)


if __name__ == "__main__":
    main()
