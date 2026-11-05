# Changelog

## 1.2.0 — 2026-11-05
- Prenosivost: `install.sh` / `uninstall.sh` (idempotentno, backup `opencode.json.bak-mddr-shield`, rucne izmjene skillova se cuvaju); sve staze iz `$HOME`, jedina zavisnost `python3`.
- `tests/test_install.sh`: round-trip instalacije u temp HOME (5 asserta).
- TestLab je test-poligon: installer verificiran uživo.
- Bez izmjena skills/tools/servera.

## 1.1.0 — 2026-11-05
- Dodano: `tests/` — smoke testovi za T1 (ekstrakcija na fixtureu) i T3 (feed logika), 7 asserta, stdlib only.
- Bez izmjena skills/tools/servera; manifest bump na 1.1.0.

## 1.0.0 — 2026-11-05
- Inicijalno izdanje: 4 skills (S1–S4), T1 `ioc-extract`, T2 `agent-audit-log`, T3 `threat-feed-mcp` (39 seed-indikatora), HTML README, MIT licenca.
- Verifikovano: T1 118 indikatora na MDDR tekstu, T2 JSONL self-test, T3 4/4 MCP poziva, MCP uživo nakon restarta.
