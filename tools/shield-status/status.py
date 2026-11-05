#!/usr/bin/env python3
"""status.py — one-page health summary from existing tool outputs. Stdlib only.

Usage: status.py --asset snap.json --tls tls.json [--manifest m.json] [--feed f.json]
No collection here — run inventory.py / tls_inventory.py first. Exit 0 always
(verdicts are data, not errors); prints human summary + JSON.
"""
import json
import sys


def load(p):
    try:
        return json.load(open(p))
    except Exception as e:
        return {"_error": str(e)}


def main():
    a = sys.argv[1:]
    get = lambda k: a[a.index(k) + 1] if k in a else None
    asset, tls = get("--asset"), get("--tls")
    if not asset or not tls:
        print(__doc__)
        sys.exit(2)
    A, T = load(asset), load(tls)
    M = load(get("--manifest")) if get("--manifest") else None
    F = load(get("--feed")) if get("--feed") else None

    pub = sorted({(x["addr"], x["port"]) for x in A.get("listeners", [])
                  if x.get("exposure") == "public"})
    exp = [x["host"] for x in T if isinstance(T, list) and (x.get("days_left") or 999) < 30]
    nohsts = [x["host"] for x in T if isinstance(T, list) and not x.get("hsts")]
    lines = [
        f"public listeners: {len(pub)}",
        f"certs expiring <30d: {len(exp)}" + (f" ({', '.join(exp)})" if exp else ""),
        f"hosts without HSTS: {len(nohsts)}",
        f"manifest: {'OK' if M and not M.get('_error') else 'skip'}",
        f"feed indicators: {F.get('count', F.get('total', 'n/a')) if F else 'n/a'}",
    ]
    print("\n".join(lines))
    print(json.dumps({"public": pub, "expiring": exp, "no_hsts": nohsts}))


if __name__ == "__main__":
    main()
