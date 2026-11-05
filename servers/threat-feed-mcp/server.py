#!/usr/bin/env python3
"""threat-feed-mcp — read-only MCP server over a local threat-indicator feed.

Stdio JSON-RPC (MCP-compatible): initialize, tools/list, tools/call.
Tools: threat_lookup (by value substring), threat_list (by type), threat_stats.
Stdlib only. Run: python3 server.py [feed.json]
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
FEED = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "threat_feed.json")

with open(FEED, encoding="utf-8") as f:
    DATA = json.load(f)


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
    inds = DATA.get("indicators", [])
    if name == "threat_lookup":
        q = args.get("query", "").lower()
        hits = [i for i in inds if q in i["value"].lower()]
        return {"matches": len(hits), "indicators": hits[:50]}
    if name == "threat_list":
        t = args.get("type", "")
        hits = [i for i in inds if i["type"] == t]
        return {"matches": len(hits), "indicators": hits}
    if name == "threat_stats":
        by_type = {}
        for i in inds:
            by_type[i["type"]] = by_type.get(i["type"], 0) + 1
        src = DATA.get("source") or DATA.get("sources")
        return {"source": src, "total": len(inds), "by_type": by_type}
    return {"error": f"unknown tool: {name}"}


def respond(mid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": mid}
    if error is not None:
        msg["error"] = {"code": -32602, "message": error}
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        mid, method, params = req.get("id"), req.get("method"), req.get("params", {})
        if method == "initialize":
            respond(mid, {"protocolVersion": "2024-11-05",
                          "serverInfo": {"name": "threat-feed-mcp", "version": "1.0.0"},
                          "capabilities": {"tools": {}}})
        elif method == "tools/list":
            respond(mid, {"tools": tool_defs()})
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments", {})
            out = call(name, args)
            if "error" in out:
                respond(mid, error=out["error"])
            else:
                respond(mid, {"content": [{"type": "text",
                                           "text": json.dumps(out, ensure_ascii=False)}]})
        else:
            respond(mid, error=f"unknown method: {method}")


if __name__ == "__main__":
    main()
