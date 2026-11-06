#!/usr/bin/env python3
"""status.py — one-page health summary from existing tool outputs. Stdlib only.

Usage: status.py --asset snap.json --tls tls.json [--manifest m.json] [--feed f.json]
No collection here — run inventory.py / tls_inventory.py first.
States: ok / error / unknown. Exit 0 = summary rendered; exit 1 = an input
failed to load or a collection clearly failed (empty listeners with no error
is reported as unknown, not clean).
"""
import json
import sys


def load(p):
    try:
        with open(p) as f:
            d = json.load(f)
        return d, None
    except Exception as e:
        return None, f"{p}: {type(e).__name__}"


def main():
    a = sys.argv[1:]
    get = lambda k: a[a.index(k) + 1] if k in a and a.index(k) + 1 < len(a) else None
    asset, tls = get("--asset"), get("--tls")
    if not asset or not tls:
        print(__doc__)
        sys.exit(2)
    bad = False
    A, e1 = load(asset)
    T, e2 = load(tls)
    M, e3 = (load(get("--manifest")) if get("--manifest") else (None, None))
    F, e4 = (load(get("--feed")) if get("--feed") else (None, None))
    for e in (e1, e2):
        if e:
            print(f"ERROR: {e}")
            bad = True
    for name, e in (("manifest", e3), ("feed", e4)):
        if e:
            print(f"WARN: {name}: {e}")

    if isinstance(A, dict) and not A.get("listeners") and not e1:
        print("WARN: asset has no listeners \u2014 failing closed")
        asset_state, bad = "unknown", True
    else:
        asset_state = "unknown" if e1 else "ok"
        bad = bad or bool(e1)
    if isinstance(T, list) and not T and not e2:
        print("WARN: tls list empty \u2014 failing closed")
        tls_state, bad = "unknown", True
    else:
        tls_state = "unknown" if e2 else "ok"
        bad = bad or bool(e2)
    if "--strict" in sys.argv[1:] and ("unknown" in (asset_state, tls_state) or exp_unk or hsts_unk):
        print("STRICT: unknown states present")
        bad = True

    pub = sorted({(x.get("addr"), x.get("port")) for x in (A or {}).get("listeners", [])
                  if x.get("exposure") == "public"})
    exp, exp_unk, nohsts, hsts_unk = [], [], [], []
    if isinstance(T, list):
        for x in T:
            dl = x.get("days_left")
            if dl is None:
                exp_unk.append(x.get("host"))
            elif dl < 30:
                exp.append(x.get("host"))
            h = x.get("hsts")
            if not h or (isinstance(h, str) and h.startswith("error")):
                (hsts_unk if isinstance(h, str) else nohsts).append(x.get("host"))
    else:
        bad = True

    if isinstance(M, dict):
        mok = all(M.get(f) for f in ("agent", "identity")) and isinstance(M.get("tools"), list)
    else:
        mok = None
    if isinstance(F, dict):
        fcount = F.get("count", F.get("total", "n/a"))
    else:
        fcount = "n/a"

    lines = [
        f"asset: {asset_state}, tls: {tls_state}",
        f"public listeners: {len(pub) if asset_state == 'ok' else 'unknown'}",
        f"certs expiring <30d: {len(exp)}" + (f" ({', '.join(map(str, exp))})" if exp else ""),
        f"certs unknown: {len(exp_unk)}" + (f" ({', '.join(map(str, exp_unk))})" if exp_unk else ""),
        f"hosts without HSTS: {len(nohsts)}" + (f" ({', '.join(map(str, nohsts))})" if nohsts else ""),
        f"hosts HSTS unknown: {len(hsts_unk)}",
        f"manifest: {'OK' if mok else ('INVALID' if mok is False else 'skip')}",
        f"feed indicators: {fcount}",
    ]
    print("\n".join(lines))
    print(json.dumps({"asset_state": asset_state, "tls_state": tls_state,
                      "public": pub, "expiring": exp, "expiry_unknown": exp_unk,
                      "no_hsts": nohsts, "hsts_unknown": hsts_unk}))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
