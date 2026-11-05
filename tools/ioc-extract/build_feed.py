#!/usr/bin/env python3
"""build_feed.py — merge one or more iocs.json files into a threat_feed.json.

Usage: build_feed.py a.iocs.json [b.iocs.json ...] -o threat_feed.json
Dedupes by (type, value-lower); keeps first page seen, merges source names.
Stdlib only.
"""
import json
import sys


def main():
    if "-o" not in sys.argv or len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    o = sys.argv.index("-o")
    inputs, out = sys.argv[1:o], sys.argv[o + 1]
    seen, inds, sources = set(), [], []
    for f in inputs:
        d = json.load(open(f))
        src = d.get("source", f)
        if src not in sources:
            sources.append(src)
        for i in d.get("indicators", []):
            key = (i.get("type"), str(i.get("value", "")).lower())
            if key in seen:
                continue
            seen.add(key)
            inds.append(i)
    feed = {"sources": sources, "count": len(inds), "indicators": inds}
    json.dump(feed, open(out, "w"), indent=2, ensure_ascii=False)
    print(f"wrote {out} ({len(inds)} indicators from {len(inputs)} files)")


if __name__ == "__main__":
    main()
