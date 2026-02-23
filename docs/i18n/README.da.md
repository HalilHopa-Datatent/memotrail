<div align="center">

# MemoTrail

> 🌐 Dette er en automatisk oversættelse. Rettelser fra fællesskabet er velkomne! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Din AI-kodningsassistent glemmer alt. MemoTrail løser det.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Et vedvarende hukommelseslag for AI-kodningsassistenter.
Hver session optaget, hver beslutning søgbar, hver kontekst husket.

</div>

---

## Nyheder i v0.3.0

- **Automatisk sessionsopsummering** — hver session får et AI-genereret resumé (ingen API-nøgler nødvendige)
- **Automatisk beslutningsudtrækning** — arkitekturbeslutninger detekteres fra samtaler ved hjælp af mønstergenkendelse
- **BM25-nøgleordssøgning** — nyt `search_keyword`-værktøj til præcise termer, fejlmeddelelser, funktionsnavne
- **Hybridsøgning** — kombinerer semantiske + nøgleordsresultater med reciprocal rank fusion
- **Cursor IDE-understøttelse** — indekserer Cursors chathistorik fra `state.vscdb`-filer
- **Filovervågning i realtid** — nye sessioner indekseres øjeblikkeligt via watchdog (ingen genstart nødvendig)
- **Opdelingsstrategier** — vælg mellem token-baseret, turbaseret eller rekursiv opdeling
- **VS Code-udvidelse** — søg, indekser og se statistik direkte fra VS Code
- **69 tests** — omfattende testdækning på tværs af alle moduler

## Problemet

Hver ny Claude Code-session starter fra nul. Din AI husker ikke gårsdagens 3-timers fejlsøgningssession, sidste uges arkitekturbeslutninger eller tilgange der allerede fejlede.

**Uden MemoTrail:**
```
Dig: "Lad os bruge Redis til caching"
AI:   "Selvfølgelig, lad os konfigurere Redis"
         ... 2 uger senere, ny session ...
Dig: "Hvorfor bruger vi Redis?"
AI:   "Jeg har ingen kontekst om den beslutning"
```

**Med MemoTrail:**
```
Dig: "Hvorfor bruger vi Redis?"
AI:   "Baseret på sessionen den 15. januar — du evaluerede Redis vs Memcached.
       Redis blev valgt for dets datastrukturunderstøttelse og vedholdenhed.
       Diskussionen er i session #42."
```

## Hurtig Start

```bash
# 1. Installer
pip install memotrail

# 2. Forbind til Claude Code
claude mcp add memotrail -- memotrail serve
```

Det er det. MemoTrail indekserer automatisk din historik ved første start.

## Hvordan Det Virker

| Trin | Hvad der sker |
|:----:|:-------------|
| **1. Optag** | MemoTrail autoindekserer nye sessioner ved start + overvåger nye filer i realtid |
| **2. Opdel** | Samtaler opdeles med token-, turbaserede eller rekursive strategier |
| **3. Indlejr** | Hvert segment indlejres med `all-MiniLM-L6-v2` (~80MB, kører på CPU) |
| **4. Udtræk** | Resuméer og arkitekturbeslutninger udtrækkes automatisk |
| **5. Gem** | Vektorer til ChromaDB, metadata til SQLite — alt under `~/.memotrail/` |
| **6. Søg** | Semantisk + BM25-nøgleordssøgning på tværs af hele din historik |
| **7. Vis** | Den mest relevante historiske kontekst dukker op præcis når du har brug for den |

> **100% lokalt** — ingen sky, ingen API-nøgler, ingen data forlader din maskine.
>
> **Projektbevidst** — hvert projekts samtaler gemmes separat. Søg inden for et enkelt projekt eller på tværs af alle projekter på én gang.
>
> **Multiplatform** — understøtter Claude Code og Cursor IDE, med flere på vej.

## Tilgængelige Værktøjer

Når MemoTrail er forbundet, får Claude Code disse MCP-værktøjer:

| Værktøj | Beskrivelse |
|---------|-------------|
| `search_chats` | Semantisk søgning på tværs af alle tidligere samtaler |
| `search_keyword` | BM25-nøgleordssøgning — fantastisk til præcise termer, funktionsnavne, fejlmeddelelser |
| `get_decisions` | Hent registrerede arkitekturbeslutninger (automatisk udtrukne + manuelle) |
| `get_recent_sessions` | List seneste kodesessioner med AI-genererede resuméer |
| `get_session_detail` | Dyk dybt ned i en specifik sessions indhold |
| `save_memory` | Gem vigtige fakta eller beslutninger manuelt |
| `memory_stats` | Se indekseringsstatistik og lagringsforbrug |

## CLI-kommandoer

```bash
memotrail serve                          # Start MCP-serveren (autoindekserer nye sessioner)
memotrail search "redis caching beslut"  # Søg fra terminalen
memotrail stats                          # Se indekseringsstatistik
memotrail index                          # Manuel genindeksering (valgfrit)
```

## Arkitektur

```
~/.memotrail/
├── chroma/          # Vektorindlejringer (ChromaDB)
└── memotrail.db     # Sessionsmetadata (SQLite)
```

| Komponent | Teknologi | Detaljer |
|-----------|-----------|---------|
| Indlejringer | `all-MiniLM-L6-v2` | ~80MB, kører på CPU |
| Vektor-DB | ChromaDB | Vedvarende, lokal lagring |
| Nøgleordssøgning | BM25 | Ren Python, ingen ekstra afhængigheder |
| Metadata | SQLite | Enkeltfils-database |
| Filovervågning | watchdog | Realtids-sessionsdetektering |
| Protokol | MCP | Model Context Protocol |

### Understøttede Platforme

| Platform | Status | Format |
|----------|--------|--------|
| Claude Code | Understøttet | JSONL-sessionsfiler |
| Cursor IDE | Understøttet | state.vscdb (SQLite) |
| GitHub Copilot | Planlagt | — |

### Opdelingsstrategier

| Strategi | Bedst til |
|----------|-----------|
| `token` (standard) | Generel brug — grupperer beskeder op til tokengrænse |
| `turn` | Samtalefokuseret — grupperer bruger+assistent-par |
| `recursive` | Langt indhold — opdeler i afsnit, sætninger, ord |

## Hvorfor MemoTrail?

| | MemoTrail | CLAUDE.md / Regelfiler | Manuelle noter |
|---|---|---|---|
| Automatisk | Ja — indekserer ved hver sessionsstart | Nej — du skriver det | Nej |
| Søgbart | Semantisk søgning | AI læser det, men kun hvad du skrev | Kun Ctrl+F |
| Skalerbart | Tusindvis af sessioner | Enkelt fil | Spredte filer |
| Kontekstbevidst | Returnerer relevant kontekst | Statiske regler | Manuel opslag |
| Opsætning | 5 minutter | Altid vedligeholdt | Altid vedligeholdt |

MemoTrail erstatter ikke `CLAUDE.md` — det supplerer det. Regelfiler er til instruktioner. MemoTrail er til hukommelse.

## Køreplan

- [x] Claude Code-sessionsindeksering
- [x] Semantisk søgning på tværs af samtaler
- [x] MCP-server med 7 værktøjer
- [x] CLI til indeksering og søgning
- [x] Autoindeksering ved serverstart (ingen manuel `memotrail index` nødvendig)
- [x] Automatisk beslutningsudtrækning
- [x] Sessionsopsummering
- [x] Cursor IDE-indsamler
- [x] BM25-nøgleordssøgning + hybridsøgning
- [x] Filovervågning i realtid (watchdog)
- [x] Flere opdelingsstrategier (token, tur, rekursiv)
- [x] VS Code-udvidelse
- [ ] Copilot-indsamler
- [ ] Skysynkronisering (Pro)
- [ ] Teamhukommelse (Team)

## VS Code-udvidelse

MemoTrail inkluderer en VS Code-udvidelse til direkte IDE-integration.

**Tilgængelige kommandoer:**
- `MemoTrail: Search Conversations` — semantisk søgning
- `MemoTrail: Keyword Search` — BM25-nøgleordssøgning
- `MemoTrail: Recent Sessions` — se sessionsstatistik
- `MemoTrail: Index Sessions Now` — udløs manuel indeksering
- `MemoTrail: Show Stats` — vis indekseringsstatistik

**Opsætning:**
```bash
cd vscode-extension
npm install
npm run compile
# Tryk derefter F5 i VS Code for at starte Extension Development Host
```

## Udvikling

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Bidrag

Bidrag er velkomne! Se [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) for retningslinjer.

**Gode første opgaver:**
- [ ] Tilføj GitHub Copilot-sessionsindsamler
- [ ] Tilføj Windsurf/Codeium-sessionsindsamler
- [ ] Tilføj skysynkronisering (opt-in)
- [ ] Tilføj teamhukommelsesdeling

## Licens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Bygget af [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Hvis MemoTrail hjælper dig, overvej at give en stjerne på GitHub.

</div>
