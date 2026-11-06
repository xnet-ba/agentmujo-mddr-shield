# agent-audit-log — format i baseline pravila (P0-2)

Cilj: svaki agentov poziv alata ostavlja jedan JSONL red — podloga za behavior-baseline
(MDDR 2026, str. 17: normalno = identitet + alati + frekvencija; devijacija = vidljiva).

## Format (jedan red = jedan događaj)

```json
{"ts":"2026-11-05T08:00:00+01:00","agent":"naziv-agenta","tool":"shell","action":"ls /home/user","cost_ms":120,"result":"ok"}
```

Polja: `ts` (ISO-8601), `agent` (ko), `tool` (koji alat), `action` (skraćeno, bez tajni),
`cost_ms` (opciono), `result` (`ok`/`deny`/`error`). **Nikad tajne, tokeni ni ključevi u log.**

## Logger

`alog.sh` — append-only upis: `alog.sh AGENT TOOL "ACTION" [RESULT]` (detalj u fajlu).
Log: `~/.local/share/mddr-shield/audit.jsonl` (default, može preko `AGENT_AUDIT_LOG`).
Escape/redakcija: JSON escape preko python3 (obavezan po install --check),
uklanja kontrolne znakove/newline, redigira `Bearer`/lozinke/API-ključeve,
krati na 2000 znakova; fajl se kreira s 0600. Redakcija je zadnja linija —
tajne se ne upisuju namjerno.
Rotacija: nema automatske rotacije — ručno preimenuj u `audit-YYYY-MM.jsonl` ili koristi postojeći cron.

## Baseline pravila (v1, pragovi se kalibriraju nakon 2 sedmice logova)

| Pravilo | Prag | Akcija |
|---|---|---|
| shell-burst | >30 shell poziva/min po agentu | alert + pregled |
| novi alat | agent prvi put zove alat izvan svoje liste | alert |
| noćni rad | aktivnost 01–05h bez najavljenog posla | alert |
| deny/error-spike | >10 deny/error u 5 min | alert + privremeni stop |
| trošak | cost_ms red veličine iznad prosjeka ×10 | pregled |

## Status

- [x] 2026-11-05 — format + pravila definisani; `alog.sh` gotov; log prazan (počinje od prve upotrebe)
