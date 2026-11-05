"""Tests for sbom-inventory parsers (offline) + live smoke (counts only)."""
import importlib.util
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


spec = importlib.util.spec_from_file_location(
    "sbom", os.path.join(REPO, "tools", "sbom-inventory", "sbom.py"))
sbom = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbom)

check("pip parse", sbom.parse_pip("a==1.0\n# c\nb==2.0\n") == ["a==1.0", "b==2.0"])
npm = "/usr/lib\n`-- pm2@5.3.0\n`-- nodemon@3.1.0\n"
check("npm parse", sorted(sbom.parse_npm(npm)) == ["nodemon@3.1.0", "pm2@5.3.0"])
dpkg = "ii  bash  5.2-1  amd64  shell\nii  coreutils 9.1 x all\nrc  old 1 x x\n"
check("dpkg parse", sbom.parse_dpkg(dpkg) == ["bash 5.2-1", "coreutils 9.1"])
check("docker parse", sbom.parse_docker("a:1\nb:2\n") == ["a:1", "b:2"])

r = subprocess.run([sys.executable, os.path.join(REPO, "tools", "sbom-inventory", "sbom.py")],
                   capture_output=True, text=True)
check("live smoke", r.returncode == 0 and "dpkg:" in r.stdout)
print("LIVE:", r.stdout.strip())

print("FAILURES:", failures if failures else "none")
sys.exit(1 if failures else 0)
