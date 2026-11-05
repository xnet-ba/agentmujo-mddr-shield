"""Tests for cve-match (offline: query building + response parsing)."""
import importlib.util
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
failures = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


spec = importlib.util.spec_from_file_location(
    "match", os.path.join(REPO, "tools", "cve-match", "match.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

sbom = {"pip": ["django==3.2.0", "requests==2.31.0", "nover"],
        "dpkg": ["bash 5.2-1", "xx 1"]}
qs = m.build_queries(sbom)
check("queries built", len(qs) == 4)
check("pypi ecosystem", qs[0] == {"package": {"name": "django", "ecosystem": "PyPI"}, "version": "3.2.0"})
check("debian ecosystem", qs[2]["package"] == {"name": "bash", "ecosystem": "Debian"})

canned = [{"vulns": [{"id": "CVE-2021-1", "summary": "x" * 200,
                      "severity": [{"type": "CVSS_V3", "score": "7.5"}]}]},
          {}, {}, {}]
hits = m.parse_results(qs, canned)
check("hits parsed", len(hits) == 1 and hits[0]["id"] == "CVE-2021-1")
check("severity+trim", hits[0]["severity"] == "7.5" and len(hits[0]["summary"]) == 160)

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
