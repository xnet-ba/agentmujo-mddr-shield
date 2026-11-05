<div align="center">

# 🛡️ AgentMujo MDDR Shield

### Operativni security-pack izveden iz Microsoft Digital Defense Report 2026

**4 skills · 2 CLI alata · 1 MCP server — sve testirano, bez vanjskih zavisnosti**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-OpenCode-blue.svg)](https://opencode.ai)
[![Skills](https://img.shields.io/badge/Skills-4-orange.svg)](#-skills)
[![Tools](https://img.shields.io/badge/Tools-2-purple.svg)](#-tools)
[![MCP](https://img.shields.io/badge/MCP-stdio-red.svg)](#-mcp-server)
[![Source](https://img.shields.io/badge/Source-MDDR_2026-grey.svg)](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Microsoft-Digital-Defense-Report-2026-v1.1.pdf)
[![Status](https://img.shields.io/badge/Status-v1.0.0_stable-success.svg)](#)

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
| 📥 Ulaz | Popis sistema (npr. `test-node, test-laptop`) |
| 📤 Izlaz | Status-tabela + lista stavki za potvrdu + trigger sljedeće provjere |
| 📦 Zavisnosti | Nema |
| 💡 Primjer | `Prioritet 2 → panel MFA: prazno 🔴 (panel user-show command)` |
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
```

- Bez zavisnosti (stdlib). Testirano na punom MDDR tekstu: tačno pronalazi
  `CVE-2020-1472`, `Qilin`, `Tycoon2FA`, `Pesky Pika` — svaki s brojem stranice.
- Ponovno upotrebljivo za **svaki budući izvještaj**.

### T2 · ✅ `agent-audit-log` — jedan red po pozivu alata

```bash
tools/agent-audit-log/alog.sh deploy shell "systemctl status app" ok
# → {"ts":"...","agent":"deploy","tool":"shell","action":"...","result":"ok"}
```

JSONL format (nikad tajne u logu) + mjesečna rotacija + 5 baseline pragova u `SPEC.md`.

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
# 1. Pokreni checklistu (S1) nad svojom infrastrukturom
# 2. Uključi audit-log (T2): export AGENT_AUDIT_LOG=./audit.jsonl
# 3. Ekstrahuj indikatore iz bilo kojeg izvještaja (T1)
python3 tools/ioc-extract/ioc_extract.py izvestaj.txt -o iocs.json
# 4. Testiraj MCP server
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' \
  | python3 servers/threat-feed-mcp/server.py
```

<div align="center">

## ✔️ Verifikacija (v1.0.0)

</div>

| Komponenta | Test | Rezultat |
|:--|:--|:--|
| T1 `ioc_extract.py` | Pun MDDR tekst (351.773 znaka) | ✅ 118 indikatora, tačni CVE/familije + stranice |
| T2 `alog.sh` | Self-test upis + čitanje | ✅ validan JSONL red |
| T3 `server.py` | initialize → tools/list → stats → lookup | ✅ sva 4 odgovora ispravna |
| S1–S4 | Format SKILL.md (Purpose/Guidance/Expected Output) | ✅ kompatibilno s OpenCode + skills-packs |

<div align="center">

## ⚠️ Napomene i ograničenja

</div>

- Brojke iz MDDR-a su **Microsoftova vendor-telemetrija** — citirati uz izvor, ne kao globalne.
- Projekcije (npr. "milijarda agenata do 2028") su nedokazane i tako su označene.
- Drill-skill (S3) nikad ne šalje stvarni phishing bez pisane potvrde.
- Preporuke skalirane na malu infrastrukturu; enterprise okruženja prilagođavaju pragove.

<div align="center">

## 📄 Licenca

**MIT** — slobodno korištenje, izmjene i distribucija uz zadržavanje obavijesti o autorskim pravima.

Izvorni izvještaj: [Microsoft Digital Defense Report 2026 (PDF)](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/msc/documents/presentations/CSR/Microsoft-Digital-Defense-Report-2026-v1.1.pdf) — besplatan javni dokument, vlasništvo Microsofta.

</div>
