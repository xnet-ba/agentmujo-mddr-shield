#!/usr/bin/env python3
"""tls_inventory.py — TLS/cert inventory for our domains. Read-only, stdlib + openssl.

Usage: tls_inventory.py host1 [host2 ...] [--json-out FILE]
For each host: negotiated TLS, cert subject/issuer/expiry/key-type, HSTS header.
"""
import json
import re
import ssl
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone


def run(cmd, inp=""):
    try:
        p = subprocess.run(cmd, input=inp, capture_output=True,
                           text=True, timeout=20)
        return (p.stdout or "") + (p.stderr or "")
    except Exception:
        return ""


def check_host(host):
    out = {"host": host}
    verbose = run(["openssl", "s_client", "-connect", f"{host}:443",
                   "-servername", host], inp="")
    m = re.search(r"^\s*Protocol\s*:\s*(\S+)", verbose, re.M)
    if not m:
        m = re.search(r"New,\s*(\S+),", verbose)  # OpenSSL <3.1 format
    out["tls"] = m.group(1) if m else "unknown"
    cert_pem = verbose[verbose.find("-----BEGIN CERTIFICATE-----"):
                       verbose.find("-----END CERTIFICATE-----") + 25]
    if "BEGIN CERTIFICATE" in verbose:
        base = ["openssl", "x509", "-noout"]
        out["subject"] = run(base + ["-subject"], cert_pem).replace("subject=", "").strip()
        out["issuer"] = run(base + ["-issuer"], cert_pem).replace("issuer=", "").strip()
        out["not_after"] = run(base + ["-enddate"], cert_pem).replace("notAfter=", "").strip()
        try:
            exp = datetime.strptime(out["not_after"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            out["days_left"] = (exp - datetime.now(timezone.utc)).days
        except Exception:
            out["days_left"] = None
        txt = run(["openssl", "x509", "-noout", "-text"], cert_pem)
        ka = re.search(r"Public Key Algorithm:\s*(\S+)", txt)
        out["key_type"] = ka.group(1) if ka else "unknown"
    else:
        out.update({"subject": None, "issuer": None, "not_after": None,
                    "days_left": None, "key_type": None})
    try:
        req = urllib.request.Request(f"https://{host}", method="HEAD")
        with urllib.request.urlopen(req, timeout=15,
                                    context=ssl.create_default_context()) as r:
            out["hsts"] = r.headers.get("Strict-Transport-Security")
    except Exception as e:
        out["hsts"] = f"error: {type(e).__name__}"
    return out


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    out_file = None
    if "--json-out" in sys.argv:
        out_file = sys.argv[sys.argv.index("--json-out") + 1]
    if not a:
        print(__doc__)
        sys.exit(1)
    res = [check_host(h) for h in a]
    js = json.dumps(res, indent=2, ensure_ascii=False)
    if out_file:
        open(out_file, "w").write(js)
        print(f"wrote {out_file} ({len(res)} hosts)")
    else:
        print(js)


if __name__ == "__main__":
    main()
