<div align="center">

# MemoTrail

> 🌐 Dette er en automatisk oversettelse. Rettelser fra fellesskapet er velkomne! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**AI-kodingsassistenten din glemmer alt. MemoTrail fikser det.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Et vedvarende minnelag for AI-kodingsassistenter.
Hver økt registrert, hver beslutning søkbar, hver kontekst husket.

</div>

---

## Nytt i v0.3.0

- **Automatisk øktsammendrag** — hver økt får et AI-generert sammendrag (ingen API-nøkler nødvendig)
- **Automatisk beslutningsutvinning** — arkitekturbeslutninger oppdages fra samtaler ved hjelp av mønstermatchning
- **BM25-nøkkelordsøk** — nytt `search_keyword`-verktøy for eksakte termer, feilmeldinger, funksjonsnavn
- **Hybridsøk** — kombinerer semantiske + nøkkelordsresultater med reciprocal rank fusion
- **Cursor IDE-støtte** — indekserer Cursors chattehistorikk fra `state.vscdb`-filer
- **Filovervåking i sanntid** — nye økter indekseres umiddelbart via watchdog (ingen omstart nødvendig)
- **Oppdelsingsstrategier** — velg mellom tokenbasert, turbasert eller rekursiv oppdeling
- **VS Code-utvidelse** — søk, indekser og vis statistikk direkte fra VS Code
- **69 tester** — omfattende testdekning på tvers av alle moduler

## Problemet

Hver ny Claude Code-økt starter fra null. AI-en din husker ikke gårsdagens 3-timers feilsøkingsøkt, forrige ukes arkitekturbeslutninger eller tilnærmingene som allerede feilet.

**Uten MemoTrail:**
```
Du: "La oss bruke Redis for caching"
AI:  "Selvfølgelig, la oss konfigurere Redis"
         ... 2 uker senere, ny økt ...
Du: "Hvorfor bruker vi Redis?"
AI:  "Jeg har ingen kontekst om den beslutningen"
```

**Med MemoTrail:**
```
Du: "Hvorfor bruker vi Redis?"
AI:  "Basert på økten den 15. januar — du evaluerte Redis vs Memcached.
      Redis ble valgt for sin datastrukturstøtte og persistens.
      Diskusjonen er i økt #42."
```

## Hurtigstart

```bash
# 1. Installer
pip install memotrail

# 2. Koble til Claude Code
claude mcp add memotrail -- memotrail serve
```

Det er det. MemoTrail indekserer automatisk historikken din ved første oppstart.


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## Hvordan Det Fungerer

| Trinn | Hva som skjer |
|:----:|:-------------|
| **1. Registrer** | MemoTrail autoindekserer nye økter ved oppstart + overvåker nye filer i sanntid |
| **2. Del opp** | Samtaler deles opp med token-, turbaserte eller rekursive strategier |
| **3. Bygg inn** | Hvert segment bygges inn med `all-MiniLM-L6-v2` (~80MB, kjører på CPU) |
| **4. Utvinne** | Sammendrag og arkitekturbeslutninger utvinnes automatisk |
| **5. Lagre** | Vektorer til ChromaDB, metadata til SQLite — alt under `~/.memotrail/` |
| **6. Søk** | Semantisk + BM25-nøkkelordsøk på tvers av hele historikken din |
| **7. Vis** | Den mest relevante historiske konteksten dukker opp akkurat når du trenger den |

> **100% lokalt** — ingen sky, ingen API-nøkler, ingen data forlater maskinen din.
>
> **Prosjektbevisst** — hvert prosjekts samtaler lagres separat. Søk innenfor et enkelt prosjekt eller på tvers av alle prosjekter samtidig.
>
> **Multiplattform** — støtter Claude Code og Cursor IDE, med flere på vei.

## Tilgjengelige Verktøy

Når MemoTrail er tilkoblet, får Claude Code disse MCP-verktøyene:

| Verktøy | Beskrivelse |
|---------|-------------|
| `search_chats` | Semantisk søk på tvers av alle tidligere samtaler |
| `search_keyword` | BM25-nøkkelordsøk — utmerket for eksakte termer, funksjonsnavn, feilmeldinger |
| `get_decisions` | Hent registrerte arkitekturbeslutninger (automatisk utvunnet + manuelle) |
| `get_recent_sessions` | List nylige kodingsøkter med AI-genererte sammendrag |
| `get_session_detail` | Dykk dypt inn i en spesifikk økts innhold |
| `save_memory` | Lagre viktige fakta eller beslutninger manuelt |
| `memory_stats` | Se indekseringsstatistikk og lagringsbruk |

## CLI-kommandoer

```bash
memotrail serve                          # Start MCP-serveren (autoindekserer nye økter)
memotrail search "redis caching beslut"  # Søk fra terminalen
memotrail stats                          # Se indekseringsstatistikk
memotrail index                          # Manuell reindeksering (valgfritt)
```

## Arkitektur

```
~/.memotrail/
├── chroma/          # Vektorinnbygginger (ChromaDB)
└── memotrail.db     # Øktmetadata (SQLite)
```

| Komponent | Teknologi | Detaljer |
|-----------|-----------|---------|
| Innbygginger | `all-MiniLM-L6-v2` | ~80MB, kjører på CPU |
| Vektor-DB | ChromaDB | Vedvarende, lokal lagring |
| Nøkkelordsøk | BM25 | Ren Python, ingen ekstra avhengigheter |
| Metadata | SQLite | Enkeltfil-database |
| Filovervåking | watchdog | Sanntids øktdetektering |
| Protokoll | MCP | Model Context Protocol |

### Støttede Plattformer

| Plattform | Status | Format |
|-----------|--------|--------|
| Claude Code | Støttet | JSONL-øktfiler |
| Cursor IDE | Støttet | state.vscdb (SQLite) |
| GitHub Copilot | Planlagt | — |

### Oppdelsingsstrategier

| Strategi | Best for |
|----------|----------|
| `token` (standard) | Generell bruk — grupperer meldinger opp til tokengrense |
| `turn` | Samtalefokusert — grupperer bruker+assistent-par |
| `recursive` | Langt innhold — deler opp i avsnitt, setninger, ord |

## Hvorfor MemoTrail?

| | MemoTrail | CLAUDE.md / Regelfiler | Manuelle notater |
|---|---|---|---|
| Automatisk | Ja — indekserer ved hver øktstart | Nei — du skriver det | Nei |
| Søkbart | Semantisk søk | AI leser det, men bare det du skrev | Kun Ctrl+F |
| Skalerbart | Tusenvis av økter | Enkelt fil | Spredte filer |
| Kontekstbevisst | Returnerer relevant kontekst | Statiske regler | Manuelt oppslag |
| Oppsett | 5 minutter | Alltid vedlikeholdt | Alltid vedlikeholdt |

MemoTrail erstatter ikke `CLAUDE.md` — det komplementerer det. Regelfiler er for instruksjoner. MemoTrail er for minne.

## Veikart

- [x] Claude Code-øktindeksering
- [x] Semantisk søk på tvers av samtaler
- [x] MCP-server med 7 verktøy
- [x] CLI for indeksering og søk
- [x] Autoindeksering ved serverstart (ingen manuell `memotrail index` nødvendig)
- [x] Automatisk beslutningsutvinning
- [x] Øktsammendrag
- [x] Cursor IDE-samler
- [x] BM25-nøkkelordsøk + hybridsøk
- [x] Filovervåking i sanntid (watchdog)
- [x] Flere oppdelsingsstrategier (token, tur, rekursiv)
- [x] VS Code-utvidelse
- [ ] Copilot-samler
- [ ] Skysynkronisering (Pro)
- [ ] Teamminne (Team)

## VS Code-utvidelse

MemoTrail inkluderer en VS Code-utvidelse for direkte IDE-integrasjon.

**Tilgjengelige kommandoer:**
- `MemoTrail: Search Conversations` — semantisk søk
- `MemoTrail: Keyword Search` — BM25-nøkkelordsøk
- `MemoTrail: Recent Sessions` — vis øktstatistikk
- `MemoTrail: Index Sessions Now` — utløs manuell indeksering
- `MemoTrail: Show Stats` — vis indekseringsstatistikk

**Oppsett:**
```bash
cd vscode-extension
npm install
npm run compile
# Trykk deretter F5 i VS Code for å starte Extension Development Host
```

## Utvikling

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Bidra

Bidrag er velkomne! Se [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) for retningslinjer.

**Gode første oppgaver:**
- [ ] Legg til GitHub Copilot-øktsamler
- [ ] Legg til Windsurf/Codeium-øktsamler
- [ ] Legg til skysynkronisering (opt-in)
- [ ] Legg til teamminne-deling

## Lisens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Bygget av [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Hvis MemoTrail hjelper deg, vurder å gi en stjerne på GitHub.

</div>
