<div align="center">

# 🛡️ AgentMujo MDDR Shield

### Operativni security-pack izveden iz Microsoft Digital Defense Report 2026

**7 skills · 10 alata · 1 MCP server — sve testirano, stdlib only**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-OpenCode-blue.svg)](https://opencode.ai)
[![MCP](https://img.shields.io/badge/MCP-stdio-red.svg)](#-mcp-server)
[![Source](https://img.shields.io/badge/Source-MDDR_2026-grey.svg)](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Microsoft-Digital-Defense-Report-2026-v1.1.pdf)
[![Status](https://img.shields.io/badge/Status-v1.12_stable-success.svg)](#)
[![Skills](https://img.shields.io/badge/Skills-7-orange.svg)](#-skills)
[![Tools](https://img.shields.io/badge/Tools-10-purple.svg)](#-tools)

| 🧠 Skills (znanje) | 🔧 Tools (izvršno) | 🌐 MCP |
|:--|:--|:--|
| Checkliste, monitoring, drillovi, memory-guard | IoC ekstrakcija, audit-log | Read-only threat-feed |

</div>

---

<div align="center">

## 🎯 Zašto ovaj repo postoji

</div>

> Cyber rizik je postao **kontinuirano stanje poslovanja**, a ne incident koji se čeka.
> Identitet je primarna kontrolna ravan. Ljudi su i dalje glavni ulaz.
> Agenti napadnuti preko validnih kredencijala izgledaju legitimno —
> vidi se samo devijacija od normale.
> — *sinteza nalaza MDDR 2026, primijenjena na malu infrastrukturu*

Microsoftov izvještaj (103 strane, period jul 2025 – jun 2026) pisan je za enterprise.
Ovaj repo ga **prevodi u operativne procedure za mali tim**: 2 servera, cloud, AI agenti.
Svaka preporuka ovdje ima: konkretnu provjeru, očekivani dokaz i ocjenu — ništa deklarativno.

<div align="center">

## 🗺️ Mapa repoa

</div>

```text
agentmujo-mddr-shield/
├── skills/
│   ├── mddr-threat-checklist/   S1  10 prioriteta → provjerljiva checklista
│   ├── agent-baseline-monitor/  S2  behavior-baseline i anomalije agenata
│   ├── clickfix-phishing-drill/ S3  simulacije socijalnog inženjeringa
│   └── ai-memory-poison-guard/  S4  zaštita perzistentne memorije / RAG-a
├── tools/
│   ├── ioc-extract/             T1  PDF/TXT → strukturisani JSON indikatori
│   └── agent-audit-log/         T2  JSONL format + alog.sh + pragovi
├── servers/
│   └── threat-feed-mcp/         T3  read-only MCP server (stdio, bez dependencija)
├── manifest.json                mašinski opis paketa
└── LICENSE                      MIT
```

<div align="center">

## 🧠 Skills

</div>

### S1 · ✅ `mddr-threat-checklist` — od strategije do provjere

| Stavka | Sadržaj |
|:--|:--|
| 🎯 Namjena | 10 MDDR prioriteta (str. 7) pretvoriti u checklistu za konkretno okruženje |
| ❌ Problem koji rješava | Generičke preporuke se nikad ne primijene jer niko ne zna prvi korak |
| ⚙️ Funkcionalnosti | Prioritet → konkretna provjera → dokaz (komanda + izlaz) → ocjena 🟢🟡🔴 |
| 📥 Ulaz | Popis sistema (npr. `web1, laptop`) |
| 📤 Izlaz | Status-tabela + lista stavki za potvrdu + trigger sljedeće provjere |
| 📦 Zavisnosti | Nema |
| 💡 Primjer | `Prioritet 2 → panel 2FA: isključen 🔴 (provjereno panel-CLI-jem)` |
| 🔁 Reuse | Svaki budući audit, svaki novi servis |

### S2 · ✅ `agent-baseline-monitor` — vidi anomaliju koja liči na normalu

| Stavka | Sadržaj |
|:--|:--|
| 🎯 Namjena | Behavior-baseline po agentu: identitet + alati + frekvencija (MDDR str. 17) |
| ❌ Problem koji rješava | Zloupotreba preko validnih kredencijala izgleda legitimno |
| ⚙️ Funkcionalnosti | Profil iz `audit.jsonl` + 5 pravila (burst, novi alat, noćni rad, deny-spike, trošak) |
| 📥 Ulaz | Putanja loga + vremenski prozor (default 7 dana) |
| 📤 Izlaz | Profili, rangirane devijacije s dokazima, prijedlog kalibracije pragova |
| 📦 Zavisnosti | T2 audit-log (u ovom repou) |
| 💡 Primjer | `agent deploy prvi put zvao shell u 03:12 → alert` |

### S3 · ✅ `clickfix-phishing-drill` — vježbaj ulaz koji se najviše eksploatiše

| Stavka | Sadržaj |
|:--|:--|
| 🎯 Namjena | Sigurne, mjerljive simulacije socijalnog inženjeringa |
| ❌ Problem koji rješava | Ljudi su glavni initial-access put (MDDR takeaway 3), a odbrana se ne vježba |
| ⚙️ Funkcionalnosti | Scenarij (ClickFix dijalog, QR-phishing) + crvene zastavice + bodovna lista + debrief |
| 📥 Ulaz | Ciljna grupa + težina (basic/intermediate/advanced) |
| 📤 Izlaz | Scenario-paket + scoring sheet + debrief agenda |
| 🛡️ Ograda | Bez stvarnog slanja bez pisane potvrde; bez lažnih login-formi; mjeri se prijava, ne samo klik |

### S4 · ✅ `ai-memory-poison-guard` — memorija je napadna površina

| Stavka | Sadržaj |
|:--|:--|
| 🎯 Namjena | Validacija upisa u dugoročnu memoriju/RAG protiv poisoninga i XPIA (MDDR str. 25) |
| ❌ Problem koji rješava | Otrovani sadržaj se vraća kao "pouzdani kontekst" kroz sesije |
| ⚙️ Funkcionalnosti | Provenance-provjera, karantin (ne brisanje), re-verifikacija, pravila za vault |
| 📥 Ulaz | Memorijski zapis + porijeklo (izvor, putanja, sesija) |
| 📤 Izlaz | Verdict: prihvati / karantin / odbij + razlog |
| 🔗 Odnos | `prompt-injection-defense` pokriva prompt-nivo; ovaj pokriva **perzistentni** sloj — nadogradnja, ne duplikat |

<div align="center">

## 🔧 Tools

</div>

### T1 · ✅ `ioc-extract` — od izvještaja do feeda za 2 sekunde

```bash
python3 tools/ioc-extract/ioc_extract.py MDDR2026.txt -o iocs.json
# → 118 indikatora: 9 CVE + 21 tehnika + 9 familija + 79 skala-figura
python3 tools/ioc-extract/build_feed.py r1.iocs.json r2.iocs.json -o servers/threat-feed-mcp/threat_feed.json
# → spojen, dedupliciran feed iz više izvora (prvi viđeni zapis pobjeđuje)
```

- Bez zavisnosti (stdlib). Testirano na punom MDDR tekstu: tačno pronalazi
  `CVE-2020-1472`, `Qilin`, `Tycoon2FA`, `Pesky Pika` — svaki s brojem stranice.
- Ponovno upotrebljivo za svaki budući izvještaj **uz dopunu TECH/FAMILY lista** (liste su iz MDDR 2026).

### T4 · ✅ `asset-inventory` — sljedeći `:8000` se ne čeka, nego se lovi
```bash
python3 tools/asset-inventory/inventory.py --snap snap.json
python3 tools/asset-inventory/inventory.py --diff snap.json
# → {"added": [...], "removed": [...]}
```

Read-only, stdlib, Linux: `ss` + `docker` → klasifikacija `localhost/private/public` + diff protiv prošlog stanja. Testirano (7 asserta) i verificirano uživo — `:8000` potvrđeno zatvoren.

### T5 · ✅ `tls-inventory` — certovi i TLS na svim domenama

```bash
python3 tools/tls-inventory/tls_inventory.py portal.example api.example
# → TLS verzija, subject/issuer, dani do isteka, tip ključa, HSTS
```

Read-only (openssl + stdlib). Uživo na test-labu: LE certovi uredni, ali API domena **nema HSTS** — zabilježeno kao nalaz.

### T6 · ✅ `agent-manifest` — red za svakog agenta

```bash
python3 tools/agent-manifest/manifest_lint.py tools/agent-manifest/example.json
# → OK: deploy (identity=svc-deploy, tools=3)
```

JSON manifest (nula zavisnosti — zato JSON, ne YAML) kompatibilan sa S2 baselineom.

### T7 · ✅ `canary-tripwire` — mamac koji otkriva uljeza

```bash
python3 tools/canary-tripwire/canary.py deploy /srv/backup --state ~/.local/share/mddr-shield/canary-state.json
python3 tools/canary-tripwire/canary.py check   # OK ili TRIP + lista
```

Inertni mamci (bez pravih kredencijala), dnevna provjera, na TRIP se ide po B6 runbooku.

### T11 · ✅ `cve-match` — inventar protiv ranjivosti (zatvara TVM petlju)

```bash
python3 tools/sbom-inventory/sbom.py --snap sbom.json
python3 tools/cve-match/match.py sbom.json -o vulns.json
# → queried N packages, M vuln hits (OSV.dev, bez ključa; offline → jasan exit 2)
```

pip→PyPI, dpkg→Debian ekosistemi. Debian revizije mogu prebaciti; severity/summary su u batch-odgovoru često prazni (prikaz n/a).

### T10 · ✅ `shield-audit` — jedna komanda, cijela provjera (B-ocjena: runner postoji)

```bash
python3 tools/shield-audit/audit.py --hosts $(cat domains.txt) --out-dir ./audit
# → asset.json + tls.json + sbom.json + report.json + sažetak na ekranu
# + napomena: identity-provjere ostaju skill-vođene (S1), jer su platform-specifične
```

Read-only, spaja T4+T5+T9+T8. Testiran end-to-end na test-labu.

### T9 · ✅ `sbom-inventory` — šta je instalirano (prioritet 8)

```bash
python3 tools/sbom-inventory/sbom.py --snap sbom.json
# → pip:93 npm:10 dpkg:1541 docker:19 (primjer s test-laba)
```

Read-only: `pip freeze` + `npm ls -g` + `dpkg -l` + `docker images` u jedan JSON. Nedostaje alat → preskače se.

### T8 · ✅ `shield-status` — jedan pogled na sistem

```bash
python3 tools/asset-inventory/inventory.py --snap snap.json
python3 tools/tls-inventory/tls_inventory.py $(cat domains.txt) --json-out tls.json
python3 tools/shield-status/status.py --asset snap.json --tls tls.json
# → public listeners: 12 / certs expiring <30d: 0 / hosts without HSTS: 16 ...
```

Ne prikuplja ništa novo — samo sažima postojeće izlaze (T4+T5, opcionalno manifest i feed).

### T2 · ✅ `agent-audit-log` — jedan red po pozivu alata
```bash
tools/agent-audit-log/alog.sh deploy shell "systemctl status app" ok
# → {"ts":"...","agent":"deploy","tool":"shell","action":"...","result":"ok"}
```

JSONL format (nikad tajne u logu) + ručna rotacija + 5 baseline pragova u `SPEC.md`.

<div align="center">

## 🌐 MCP server

</div>

### T3 · ✅ `threat-feed-mcp` — threat-indikatori za agente, read-only

Stdio JSON-RPC server, **nula zavisnosti**, 39 seed-indikatora iz MDDR-a:

| Alat | Opis |
|:--|:--|
| `threat_lookup` | Pretraga po substringu (`{"query":"qilin"}` → familija + stranica) |
| `threat_list` | Lista po tipu: `cve`, `technique`, `family` |
| `threat_stats` | Brojevi po tipu + izvor feeda |

Priključak na OpenCode (`opencode.json → mcp`):

```json
"threat-feed": {
  "type": "local",
  "command": ["python3", "/putanja/do/servers/threat-feed-mcp/server.py"],
  "enabled": true
}
```

<div align="center">

## 🚀 Quickstart

</div>

```bash
git clone https://github.com/xnet-ba/agentmujo-mddr-shield.git
cd agentmujo-mddr-shield
./install.sh            # skills + MCP + data dir, idempotentno, uz backup
./install.sh --check    # preflight: python3/git obavezni, openssl/ss/docker opcioni
# ./uninstall.sh        # potpuno uklanjanje, cuva rucne izmjene skillova
```
Radi na **bilo kojem OpenCode agentu**: staze se izvode iz `$HOME`, jedina zavisnost je `python3` (stdlib) i `openssl` za B2. Verificiran na Linux test-labu — installer pokriven testovima u tests/.
```bash
# 1. Pokreni checklistu (S1) nad svojom infrastrukturom
# 2. Uključi audit-log (T2): export AGENT_AUDIT_LOG=./audit.jsonl
# 3. Ekstrahuj indikatore iz bilo kojeg izvještaja (T1)
python3 tools/ioc-extract/ioc_extract.py izvestaj.txt -o iocs.json
# 4. Jednom komandom provjeri sistem (T10)
python3 tools/shield-audit/audit.py --hosts $(cat domains.txt) --out-dir ./audit
```

### S5 · ✅ `attachment-risk-check` · S6 · ✅ `ir-runbooks-mdrr` · S7 · ✅ `canary-tripwire`

| Skill | Ukratko |
|:--|:--|
| `attachment-risk-check` | Rizik po tipu fajla iz MDDR statistike (SVG 47%, DOC 17%) + procedura prije otvaranja |
| `ir-runbooks-mdrr` | 3 runbooka prvog sata: token-abuse, ClickFix trag, ransomware sumnja |
| `canary-tripwire` | Strategija mamaca + cadence provjere + trip-procedura (uz T7 alat) |

<div align="center">

## ✔️ Verifikacija (v1.12 — 60 asserta, svi zeleni)

</div>

| Komponenta | Test | Rezultat |
|:--|:--|:--|
| T1 `ioc_extract.py` | Pun MDDR tekst (351.773 znaka) | ✅ 118 indikatora, tačni CVE/familije + stranice |
| T2 `alog.sh` | Self-test upis + čitanje | ✅ validan JSONL red |
| T3 `server.py` | initialize → tools/list → stats → lookup | ✅ sva 4 odgovora ispravna |
| S1–S4 | Format SKILL.md (Purpose/Guidance/Expected Output) | ✅ kompatibilno s OpenCode + skills-packs |
| Svi alati | Offline fixture-testovi + live smoke na test-labu | ✅ vidi tests/ |
| T4–T9 | Fixture + live testovi + install round-trip | ✅ vidi tests/ |
| T10 `audit.py` | E2E runner na test-labu | ✅ report.json + 4 artefakta |
| T3 `server.py` | 8 slucajeva (bad input, notifikacije, malformed feed) | ✅ bez pada |
| T11 `match.py` | Offline parsing + live OSV | ✅ + upozorenje o pokrivenosti |

<div align="center">

## ⚠️ Napomene i ograničenja

</div>

- Brojke iz MDDR-a su **Microsoftova vendor-telemetrija** — citirati uz izvor, ne kao globalne.
- Projekcije (npr. "milijarda agenata do 2028") su nedokazane i tako su označene.
- Drill-skill (S3) nikad ne šalje stvarni phishing bez pisane potvrde.
- Mreža: samo T11 kontaktira vanjski servis (OSV.dev, javna imena+verzije paketa, bez ključa); sve ostalo radi offline.
- T8/T10 sažimaju postojeće izlaze; prazan ulaz = status `unknown`, ne `0`.
- Preporuke skalirane na malu infrastrukturu; enterprise okruženja prilagođavaju pragove.

<div align="center">

## 📄 Licenca

**MIT** — slobodno korištenje, izmjene i distribucija uz zadržavanje obavijesti o autorskim pravima.

Izvorni izvještaj: [Microsoft Digital Defense Report 2026 (PDF)](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Microsoft-Digital-Defense-Report-2026-v1.1.pdf) — besplatan javni dokument, vlasništvo Microsofta.

</div>
