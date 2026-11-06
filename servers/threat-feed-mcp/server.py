#!/usr/bin/env python3
"""threat-feed-mcp — read-only MCP server over a local threat-indicator feed.

Stdio JSON-RPC (MCP-compatible): initialize, tools/list, tools/call, ping.
Tools: threat_lookup (by value substring), threat_list (by type), threat_stats.
Stdlib only. Run: python3 server.py [feed.json]
Bad feed entries (missing type/value) are skipped at load with a stderr note.
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
FEED = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "threat_feed.json")

with open(FEED, encoding="utf-8") as f:
    _raw = json.load(f)
_inds, _skipped = [], 0
for _i in _raw.get("indicators", []) if isinstance(_raw, dict) else []:
    if isinstance(_i, dict) and isinstance(_i.get("type"), str) and isinstance(_i.get("value"), str):
        _inds.append(_i)
    else:
        _skipped += 1
if _skipped:
    sys.stderr.write(f"threat-feed: skipped {_skipped} malformed entries\n")
DATA = {"indicators": _inds,
        "source": _raw.get("source") if isinstance(_raw, dict) else None,
        "sources": _raw.get("sources") if isinstance(_raw, dict) else None}


def tool_defs():
    return [
        {"name": "threat_lookup",
         "description": "Find threat indicators whose value contains QUERY (case-insensitive).",
         "inputSchema": {"type": "object",
                         "properties": {"query": {"type": "string"}},
                         "required": ["query"]}},
        {"name": "threat_list",
         "description": "List indicators of one TYPE: cve, technique, or family.",
         "inputSchema": {"type": "object",
                         "properties": {"type": {"type": "string"}},
                         "required": ["type"]}},
        {"name": "threat_stats",
         "description": "Counts per indicator type plus feed source.",
         "inputSchema": {"type": "object", "properties": {}}},
    ]


def call(name, args):
    if not isinstance(args, dict):
        return {"error": "arguments must be an object", "code": -32602}
    inds = DATA.get("indicators", [])
    if name == "threat_lookup":
        q = args.get("query", "")
        if not isinstance(q, str):
            return {"error": "query must be a string", "code": -32602}
        q = q.lower()
        hits = [i for i in inds if q in i["value"].lower()]
        return {"matches": len(hits), "indicators": hits[:50]}
    if name == "threat_list":
        t = args.get("type", "")
        if not isinstance(t, str):
            return {"error": "type must be a string", "code": -32602}
        hits = [i for i in inds if i["type"] == t]
        return {"matches": len(hits), "indicators": hits}
    if name == "threat_stats":
        by_type = {}
        for i in inds:
            by_type[i["type"]] = by_type.get(i["type"], 0) + 1
        src = DATA.get("source") or DATA.get("sources")
        return {"source": src, "total": len(inds), "by_type": by_type}
    return {"error": f"unknown tool: {name}", "code": -32601}


def respond(mid, result=None, error=None, code=-32602):
    msg = {"jsonrpc": "2.0", "id": mid}
    if error is not None:
        msg["error"] = {"code": code, "message": error}
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def handle(req):
    """Process one parsed request. Returns False for notifications (no reply)."""
    if not isinstance(req, dict):
        return {"error": "request must be an object", "code": -32700}
    mid, method, params = req.get("id"), req.get("method"), req.get("params", {})
    if params is None:
        params = {}
    if not isinstance(params, dict):
        return {"error": "params must be an object", "code": -32602}
    if method == "initialize":
        return {"result": {"protocolVersion": "2024-11-05",
                           "serverInfo": {"name": "threat-feed-mcp", "version": "1.1.0"},
                           "capabilities": {"tools": {}}}}
    if method == "tools/list":
        return {"result": {"tools": tool_defs()}}
    if method == "tools/call":
        name = params.get("name", "")
        out = call(name, params.get("arguments", {}))
        if "error" in out:
            return {"error": out["error"], "code": out.get("code", -32602)}
        return {"result": {"content": [{"type": "text",
                                        "text": json.dumps(out, ensure_ascii=False)}]}}
    if method in ("ping", "notifications/initialized", "notifications/cancelled"):
        if method == "ping":
            return {"result": {}}
        return None  # notification: no reply
    return {"error": f"unknown method: {method}", "code": -32601}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
            sys.stdout.flush()
            continue
        mid = req.get("id") if isinstance(req, dict) else None
        out = handle(req)
        if out is None:
            continue  # notification: never reply
        if mid is None and "error" not in out:
            continue  # result for a notification: never reply
        if "error" in out:
            respond(mid, error=out["error"], code=out.get("code", -32602))
        else:
            respond(mid, result=out["result"])


if __name__ == "__main__":
    main()
