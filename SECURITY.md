# Security Policy

## Podržane verzije

| Verzija | Podrška |
|:--|:--|
| 1.x (aktualna minor) | ✅ |
| starije | ❌ (nadogradi) |

## Prijava ranjivosti

Ne otvaraj javni issue za sigurnosni problem. Javi privatno vlasniku repoa
(`xnet-ba`) — opiši utjecaj, korake reprodukcije i, ako imaš, prijedlog popravke.
Odgovaramo u razumnom roku; objavu koordiniramo prije mergea popravke.

## Garancije i granice alata (pročitati prije upotrebe)

- Izvještaji nikad ne tvrde "čisto" na osnovu neuspjelog prikupljanja:
  `shield-status`/`shield-audit` razlikuju `ok` / `error` / `unknown`
  i izlaze s kodom ≠ 0 kad ulaz ne valja.
- `threat-feed-mcp` je read-only: ne izvršava komande, ne piše po disku
  (osim stderr napomene o lošim zapisima).
- `canary-tripwire` detektira PISANJE/brisanje mamca, ne čitanje.
- `cve-match` šalje javna imena+verzije paketa na OSV.dev (bez ključa);
  pokrivenost ispisuje (`checked X of Y`), Debian revizije mogu prebaciti.
- `alog.sh` escapea JSON, uklanja kontrolne znakove i redigira
  `Bearer`/lozinke/API-ključeve; fajl se kreira s 0600. Ne upisuj tajne u log —
  redakcija je zadnja linija, ne prva.
- Mamci (`canary.py deploy`) su inertni tekst bez pravih kredencijala.
- Izlazni JSON-ovi alata nasljeđuju umask; na višekorisničkim sistemima
  postavi `umask 077` prije snimanja osjetljivih snimaka.
