#!/usr/bin/env python3
"""inventory.py — snapshot TCP listen stanja + diff. Read-only, stdlib only (Linux).

Usage: inventory.py [--snap FILE] [--diff OLD.json] [--ss-file FIXTURE]
Izlaz: JSON {host, ts, listeners: [{addr, port, exposure}], docker: [...]}.
Exposure: localhost | private | public.
"""
import json
import ipaddress
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout
    except Exception:
        return ""


def classify(addr):
    """localhost / private / public via ipaddress; unknown on garbage.
    Wildcards (0.0.0.0, ::, *) count as public: they accept the world."""
    if addr in ("*", "0.0.0.0", "::"):
        return "public"
    try:
        ip = ipaddress.ip_address(addr)
    except ValueError:
        return "unknown"
    if ip.is_loopback:
        return "localhost"
    if not ip.is_global:
        # RFC1918, ULA fc00::/7, CGNAT 100.64/10, link-local, reserved
        return "private"
    return "public"


def parse_ss(text):
    out = []
    for ln in text.splitlines()[1:]:
        parts = ln.split()
        if len(parts) < 5:
            continue
        local = parts[3]
        addr, _, port = local.rpartition(":")
        addr = addr.strip("[]").split("%")[0]  # strip [ ] + %iface zone
        out.append({"addr": addr, "port": port, "exposure": classify(addr)})
    return out


def parse_docker(text):
    out = []
    for ln in text.splitlines():
        # 0.0.0.0:8000->80, [::]:8080->80, 0.0.0.0:8000-8010->8000-8010
        for m in re.finditer(r"(\[?[0-9a-fA-F:.]+\]?):(\d+(?:-\d+)?)->", ln):
            addr = m.group(1).strip("[]")
            for port in expand_range(m.group(2)):
                out.append({"addr": addr, "port": port, "exposure": classify(addr)})
    return out


def expand_range(pr):
    if "-" in pr:
        a, b = pr.split("-", 1)
        try:
            lo, hi = int(a), int(b)
            if 0 < lo <= hi <= 65535 and hi - lo <= 1000:
                return [str(p) for p in range(lo, hi + 1)]
        except ValueError:
            pass
    return [pr]


def snapshot(ss_text=None, docker_text=None):
    if ss_text is None:
        ss_text = run(["ss", "-tln"])
    if docker_text is None:
        docker_text = run(["docker", "ps", "--format", "{{.Names}} {{.Ports}}"])
    return {"host": socket.gethostname(),
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "listeners": parse_ss(ss_text), "docker": parse_docker(docker_text)}


def main():
    a = sys.argv[1:]
    snap = diff = ss_file = None
    i = 0
    while i < len(a):
        if a[i] == "--snap" and i + 1 < len(a):
            snap = a[i + 1]; i += 2
        elif a[i] == "--diff" and i + 1 < len(a):
            diff = a[i + 1]; i += 2
        elif a[i] == "--ss-file" and i + 1 < len(a):
            ss_file = a[i + 1]; i += 2
        else:
            i += 1
    ss_text = open(ss_file).read() if ss_file else None
    cur = snapshot(ss_text)
    if diff:
        old = json.load(open(diff))
        key = lambda x: (x["addr"], x["port"])
        oldk = {key(x) for x in old.get("listeners", []) + old.get("docker", [])}
        curk = {key(x) for x in cur["listeners"] + cur["docker"]}
        cur["added"] = sorted(curk - oldk)
        cur["removed"] = sorted(oldk - curk)
    js = json.dumps(cur, indent=2)
    if snap:
        open(snap, "w").write(js)
        print(f"wrote {snap} ({len(cur['listeners'])} listeners)")
    else:
        print(js)


if __name__ == "__main__":
    main()
