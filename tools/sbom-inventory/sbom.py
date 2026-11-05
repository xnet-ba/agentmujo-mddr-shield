#!/usr/bin/env python3
"""sbom.py — software inventory snapshot. Read-only, stdlib only (Linux).

Usage: sbom.py [--snap FILE]
Collects: pip freeze, npm global list, dpkg list, docker images.
Missing tools are skipped. Prints summary; --snap writes full JSON.
"""
import json
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return ""


def parse_pip(text):
    return sorted({ln.strip() for ln in text.splitlines()
                   if ln.strip() and not ln.startswith("#")})


def parse_npm(text):
    return sorted(set(re.findall(r"^\S*\s(\S+@\S+)", text, re.M)))


def parse_dpkg(text):
    return sorted({f"{p[1]} {p[2]}" for p in
                   (ln.split() for ln in text.splitlines())
                   if len(p) > 2 and p[0] == "ii"})


def parse_docker(text):
    return sorted({ln.strip() for ln in text.splitlines() if ln.strip()})


def snapshot():
    return {"host": socket.gethostname(),
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pip": parse_pip(run(["pip", "freeze"])),
            "npm": parse_npm(run(["npm", "ls", "-g", "--depth=0"])),
            "dpkg": parse_dpkg(run(["dpkg", "-l"])),
            "docker": parse_docker(run(["docker", "images",
                                        "--format", "{{.Repository}}:{{.Tag}}"]))}


def main():
    snap = None
    if "--snap" in sys.argv:
        snap = sys.argv[sys.argv.index("--snap") + 1]
    d = snapshot()
    print(f"pip:{len(d['pip'])} npm:{len(d['npm'])} "
          f"dpkg:{len(d['dpkg'])} docker:{len(d['docker'])}")
    if snap:
        json.dump(d, open(snap, "w"), indent=2)
        print(f"wrote {snap}")


if __name__ == "__main__":
    main()
