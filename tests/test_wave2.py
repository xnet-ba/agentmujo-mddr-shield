"""Tests for tls-inventory parsing (offline) + manifest linter + canary. No network."""
import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
failures = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


# --- B2: parsing helpers tested via canned openssl-style output ---
sys.path.insert(0, os.path.join(REPO, "tools", "tls-inventory"))
import re
import importlib.util
spec = importlib.util.spec_from_file_location(
    "tls_inventory", os.path.join(REPO, "tools", "tls-inventory", "tls_inventory.py"))
tls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tls)

fake_verbose = "  Protocol  : TLSv1.3\n-----BEGIN CERTIFICATE-----\nMIIB\n-----END CERTIFICATE-----\n"
m = re.search(r"^\s*Protocol\s*:\s*(\S+)", fake_verbose, re.M)
check("b2 tls regex", m and m.group(1) == "TLSv1.3")
check("b2 pem slice", "BEGIN CERTIFICATE" in fake_verbose)

# --- B4: manifest linter on fixtures ---
LINT = os.path.join(REPO, "tools", "agent-manifest", "manifest_lint.py")
good = {"agent": "deploy", "identity": "svc-deploy",
        "tools": ["shell", "read"],
        "limits": {"max_shell_per_min": 30, "allowed_hours": "06-22"}}
bad = {"agent": "x"}
with tempfile.TemporaryDirectory() as t:
    g, b = os.path.join(t, "g.json"), os.path.join(t, "b.json")
    json.dump(good, open(g, "w"))
    json.dump(bad, open(b, "w"))
    r1 = subprocess.run([sys.executable, LINT, g], capture_output=True, text=True)
    r2 = subprocess.run([sys.executable, LINT, b], capture_output=True, text=True)
    check("b4 good passes", r1.returncode == 0 and "OK" in r1.stdout)
    check("b4 bad fails", r2.returncode != 0 and "identity" in r2.stdout + r2.stderr)

# --- C1: canary deploy + check + trip ---
CAN = os.path.join(REPO, "tools", "canary-tripwire", "canary.py")
with tempfile.TemporaryDirectory() as t:
    state = os.path.join(t, "state.json")
    r = subprocess.run([sys.executable, CAN, "deploy", t, "--state", state],
                       capture_output=True, text=True)
    check("c1 deploy", r.returncode == 0)
    r = subprocess.run([sys.executable, CAN, "check", "--state", state],
                       capture_output=True, text=True)
    check("c1 check clean", r.returncode == 0 and "OK" in r.stdout)
    # trip it: modify a canary
    cfiles = json.load(open(state))["canaries"]
    open(cfiles[0]["path"], "a").write("intruder was here")
    r = subprocess.run([sys.executable, CAN, "check", "--state", state],
                       capture_output=True, text=True)
    check("c1 trip detected", r.returncode != 0 and "TRIP" in r.stdout)

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
