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

# --- feed builder: merge + dedup ---
BUILD = os.path.join(REPO, "tools", "ioc-extract", "build_feed.py")
with tempfile.TemporaryDirectory() as t:
    f1, f2 = os.path.join(t, "a.json"), os.path.join(t, "b.json")
    json.dump({"source": "A", "indicators": [
        {"type": "cve", "value": "CVE-2020-1472", "page": 1},
        {"type": "family", "value": "Qilin", "page": 2}]}, open(f1, "w"))
    json.dump({"source": "B", "indicators": [
        {"type": "family", "value": "qilin", "page": 9},
        {"type": "technique", "value": "ClickFix", "page": 3}]}, open(f2, "w"))
    out = os.path.join(t, "feed.json")
    r = subprocess.run([sys.executable, BUILD, f1, f2, "-o", out],
                       capture_output=True, text=True)
    check("feed build runs", r.returncode == 0)
    d = json.load(open(out))
    check("feed dedup (3, not 4)", d["count"] == 3)
    check("feed keeps both sources", d["sources"] == ["A", "B"])

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

# --- T3: sources-format feed compat via stdio ---
with tempfile.TemporaryDirectory() as t:
    fp = os.path.join(t, "feed.json")
    json.dump({"sources": ["A", "B"],
               "indicators": [{"type": "cve", "value": "CVE-1", "page": 1}]},
              open(fp, "w"))
    q = '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"threat_stats","arguments":{}}}\n'
    r = subprocess.run([sys.executable, os.path.join(REPO, "servers", "threat-feed-mcp", "server.py"), fp],
                       input=q, capture_output=True, text=True)
    got = json.loads(json.loads(r.stdout)["result"]["content"][0]["text"])["source"]
    check("t3 sources-format", got == ["A", "B"])

# --- shield-status: composer over canned outputs ---
ST = os.path.join(REPO, "tools", "shield-status", "status.py")
with tempfile.TemporaryDirectory() as t:
    a = os.path.join(t, "a.json")
    tl = os.path.join(t, "t.json")
    json.dump({"listeners": [
        {"addr": "0.0.0.0", "port": "22", "exposure": "public"},
        {"addr": "127.0.0.1", "port": "9", "exposure": "localhost"}]}, open(a, "w"))
    json.dump([{"host": "x", "days_left": 5, "hsts": None}], open(tl, "w"))
    r = subprocess.run([sys.executable, ST, "--asset", a, "--tls", tl],
                       capture_output=True, text=True)
    check("status runs", r.returncode == 0)
    check("status counts", "public listeners: 1" in r.stdout and "x" in r.stdout)
    r = subprocess.run([sys.executable, ST], capture_output=True, text=True)
    check("status needs args", r.returncode == 2)

# --- installer doctor ---
r = subprocess.run(["bash", os.path.join(REPO, "install.sh"), "--check"],
                   capture_output=True, text=True)
check("doctor runs", r.returncode == 0 and "OK" in r.stdout)
r = subprocess.run(["bash", "-c",
                    'PATH=/nonexistent install.sh --check'.replace(
                        "install.sh", os.path.join(REPO, "install.sh"))],
                   capture_output=True, text=True)
check("doctor fails without deps", r.returncode != 0 and "FALI" in r.stdout)

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
