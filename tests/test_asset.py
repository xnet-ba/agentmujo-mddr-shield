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
check("53 private(vpn)", by_port.get("53", {}).get("exposure") == "private")
check("8083 ipv6 public", by_port.get("8083", {}).get("exposure") == "public")
priv53 = [x for x in d["listeners"] if x["port"] == "53"]
check("53 sve private", len(priv53) == 3 and all(x["exposure"] == "private" for x in priv53))

# --- COR-003: edge klasifikacija ---
import sys as _s
_s.path.insert(0, os.path.join(REPO, "tools", "asset-inventory"))
from inventory import classify
_edge = {"127.0.0.53": "localhost", "::ffff:127.0.0.1": "private",
         "100.64.5.5": "private", "100.10.0.1": "public",
         "fc00::1": "private", "junk": "unknown"}
check("edge klasifikacija", all(classify(k) == v for k, v in _edge.items()))

snap = os.path.join(BASE, "snap-test.json")
subprocess.run([sys.executable, INV, "--ss-file", FIX, "--snap", snap],
               check=True, capture_output=True)
r2 = subprocess.run([sys.executable, INV, "--ss-file", FIX, "--diff", snap],
                    capture_output=True, text=True)
d2 = json.loads(r2.stdout)
check("diff nema promjena", d2.get("added") == [] and d2.get("removed") == [])
os.remove(snap)

# --- status fail-closed: prazan ulaz -> exit 1, strict flag ---
import subprocess as _sp2, tempfile as _tf2, json as _js2
with _tf2.TemporaryDirectory() as t:
    e = os.path.join(t, "e.json"); open(e, "w").write("[]")
    l = os.path.join(t, "l.json"); open(l, "w").write('{"listeners":[]}')
    ST = os.path.join(REPO, "tools", "shield-status", "status.py")
    r = _sp2.run([sys.executable, ST, "--asset", l, "--tls", e], capture_output=True, text=True)
    check("status empty exits 1", r.returncode == 1 and "unknown" in r.stdout)
    ok = os.path.join(t, "ok.json")
    _js2.dump({"listeners": [{"addr": "0.0.0.0", "port": "22", "exposure": "public"}]}, open(ok, "w"))
    r = _sp2.run([sys.executable, ST, "--asset", ok, "--tls", e], capture_output=True, text=True)
    check("status partial exits 1", r.returncode == 1)
    r = _sp2.run([sys.executable, ST, "--asset", ok, "--tls", e, "--strict"],
                 capture_output=True, text=True)
    check("status strict exits 1 on unknown", r.returncode == 1 and "STRICT" in r.stdout)

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
