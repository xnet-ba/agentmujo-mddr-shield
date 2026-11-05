"""Smoke tests: T1 extractor + T3 feed logic. Run: python3 tests/test_tools.py"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
sys.path.insert(0, os.path.join(REPO, "servers", "threat-feed-mcp"))

failures = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


# T1: run extractor on fixture
out = os.path.join(BASE, "fixture-out.json")
r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "ioc-extract", "ioc_extract.py"),
                    os.path.join(BASE, "fixture.txt"), "-o", out],
                   capture_output=True, text=True)
check("t1 runs", r.returncode == 0)
d = json.load(open(out))
vals = {(x["type"], x["value"].lower()) for x in d["indicators"]}
check("t1 finds CVE-2020-1472", ("cve", "cve-2020-1472") in vals)
check("t1 finds Qilin family", ("family", "qilin") in vals)
check("t1 finds ClickFix technique", ("technique", "clickfix") in vals)
os.remove(out)

# T3: import server logic, test call() directly
import server
stats = server.call("threat_stats", {})
check("t3 stats total>0", stats.get("total", 0) > 0)
hits = server.call("threat_lookup", {"query": "qilin"})
check("t3 lookup qilin", hits.get("matches", 0) >= 1)
check("t3 unknown tool errors", "error" in server.call("nope", {}))

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
