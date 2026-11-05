"""Tests for asset-inventory. Run: python3 tests/test_asset.py"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
failures = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


INV = os.path.join(REPO, "tools", "asset-inventory", "inventory.py")
FIX = os.path.join(BASE, "ss-fixture.txt")

r = subprocess.run([sys.executable, INV, "--ss-file", FIX],
                   capture_output=True, text=True)
check("runs", r.returncode == 0)
d = json.loads(r.stdout)
by_port = {x["port"]: x for x in d["listeners"]}
check("8000 public", by_port.get("8000", {}).get("exposure") == "public")
check("9100 localhost", by_port.get("9100", {}).get("exposure") == "localhost")
check("53 private(tailscale)", by_port.get("53", {}).get("exposure") == "private")
check("8083 ipv6 public", by_port.get("8083", {}).get("exposure") == "public")
priv53 = [x for x in d["listeners"] if x["port"] == "53"]
check("53 sve private", len(priv53) == 3 and all(x["exposure"] == "private" for x in priv53))

snap = os.path.join(BASE, "snap-test.json")
subprocess.run([sys.executable, INV, "--ss-file", FIX, "--snap", snap],
               check=True, capture_output=True)
r2 = subprocess.run([sys.executable, INV, "--ss-file", FIX, "--diff", snap],
                    capture_output=True, text=True)
d2 = json.loads(r2.stdout)
check("diff nema promjena", d2.get("added") == [] and d2.get("removed") == [])
os.remove(snap)

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
