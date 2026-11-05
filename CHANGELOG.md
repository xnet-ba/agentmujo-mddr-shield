# Changelog

## 1.10.0 — 2026-11-05
- Audit-fixes (vanjski nalaz): fail-open -> ok/error/unknown + exit!=0 (COR-001); alog.sh JSON escape+redakcija+0600 (SEC-001); anonimizacija tragova infrastrukture (SEC-004); installer JSONC/atomski upis/cuvanje korisnickih podataka (SEC-003); cve-match pokrivenost+multiarch+arg-parsiranje (COR-002); frontmatter na skillovima (DOC-001); canary read-scope+refuse-overwrite (SEC-002); ipaddress klasifikacija+docker opsezi (COR-003); MCP validacija+ping+feed-skip (COR-004); README popravke (DOC-002); strozi manifest lint (COR-006); SECURITY.md + CI (ARH-001).

## 1.9.0 — 2026-11-05
- Novo: T11 `cve-match` — sbom.json protiv OSV.dev (PyPI/Debian, bez ključa, offline exit 2).
- TVM petlja zatvorena: inventar → ranjivosti.

## 1.8.0 — 2026-11-05
- Novo: T10 `shield-audit` — jedna komanda pokreće T4+T5+T9+T8 i izdaje report.json.
- Fix: `%zone` sufiks više ne jede port (T4).
- E2E test runnera na test-labu.

## 1.7.1 — 2026-11-05
- `install.sh --check`: preflight preduvjeta (obavezni python3>=3.8, git; opcioni openssl/ss/docker); install odbija bez obaveznih.
- Testovi za oba slucaja (ima/nema dependencija).

## 1.7.0 — 2026-11-05
- Novo: T9 `sbom-inventory` (pip/npm/dpkg/docker → JSON, read-only).
- Uživo na test-labu: 93/10/1541/19.

## 1.6.0 — 2026-11-05
- Novo: T8 `shield-status` — kompozitor postojećih izlaza u jednu stranicu (bez nove logike prikupljanja).

## 1.5.1 — 2026-11-05
- Fix: server podrzava i `sources` (novi feed-format) i `source` (stari seed).
- C1 dogfood na TestLab test-diru: deploy → OK → TRIP → ciscenje.

## 1.5.0 — 2026-11-05
- Novo: `build_feed.py` — spajanje više iocs.json u jedan feed (dedup, više izvora).
- T1→T3 pipeline zatvoren: extract → build_feed → MCP server.

## 1.4.1 — 2026-11-05
- Fix: `--json-out` vrijednost se više ne skenira kao host; HSTS `error:...` vs `None` ostaju razdvojeni.
- Puni krug na TestLab (više domena): 21× TLSv1.3/RSA/LE, 0 isteklih <30d; dio domena bez HSTS (sistemski nalaz);
  `panel-host:443` odbijen (samo admin-port, očekivano).

## 1.4.0 — 2026-11-05
- Novo: B2 `tls-inventory`, B4 `agent-manifest` (linter + primjer), B5 `attachment-risk-check`, B6 `ir-runbooks-mdrr`, C1 `canary-tripwire` (alat + skill).
- `tests/test_wave2.py` (7 asserta: tls-regex, lint OK/bad, canary deploy/check/trip).
- Uživo: LE certovi uredni, TLSv1.3; API domena bez HSTS (nalaz).
- installer pokriva svih 7 skillova; dogfood na TestLab.

## 1.3.0 — 2026-11-05
- Novo: T4 `asset-inventory` (ss+docker snapshot, exposure-klasifikacija, diff) + `tests/test_asset.py` (7 asserta).
- Uživo verificirano: `:8000` zatvoren, javni listeneri popisani.

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
