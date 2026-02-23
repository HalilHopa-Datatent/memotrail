<div align="center">

# MemoTrail

> 🌐 Detta är en automatisk översättning. Rättelser från communityn välkomnas! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Din AI-kodassistent glömmer allt. MemoTrail löser det.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Ett beständigt minneslager för AI-kodassistenter.
Varje session inspelad, varje beslut sökbart, varje kontext ihågkommen.

</div>

---

## Nyheter i v0.3.0

- **Automatisk sessionssammanfattning** — varje session får en AI-genererad sammanfattning (inga API-nycklar behövs)
- **Automatisk beslutsextraktion** — arkitekturbeslut detekteras från konversationer med mönstermatchning
- **BM25-nyckelordssökning** — nytt `search_keyword`-verktyg för exakta termer, felmeddelanden, funktionsnamn
- **Hybridsökning** — kombinerar semantisk + nyckelordsresultat med reciprocal rank fusion
- **Cursor IDE-stöd** — indexerar Cursors chatthistorik från `state.vscdb`-filer
- **Realtidsfilövervakning** — nya sessioner indexeras omedelbart via watchdog (ingen omstart behövs)
- **Uppdelningsstrategier** — välj mellan tokenbaserad, turbaserad eller rekursiv uppdelning
- **VS Code-tillägg** — sök, indexera och visa statistik direkt från VS Code
- **69 tester** — omfattande testtäckning över alla moduler

## Problemet

Varje ny Claude Code-session börjar från noll. Din AI minns inte gårdagens 3 timmars felsökningssession, förra veckans arkitekturbeslut eller tillvägagångssätten som redan misslyckats.

**Utan MemoTrail:**
```
Du: "Låt oss använda Redis för caching"
AI:  "Visst, låt oss konfigurera Redis"
         ... 2 veckor senare, ny session ...
Du: "Varför använder vi Redis?"
AI:  "Jag har ingen kontext om det beslutet"
```

**Med MemoTrail:**
```
Du: "Varför använder vi Redis?"
AI:  "Baserat på sessionen den 15 januari — du utvärderade Redis vs Memcached.
      Redis valdes för dess stöd för datastrukturer och beständighet.
      Diskussionen finns i session #42."
```

## Snabbstart

```bash
# 1. Installera
pip install memotrail

# 2. Anslut till Claude Code
claude mcp add memotrail -- memotrail serve
```

Det är allt. MemoTrail indexerar automatiskt din historik vid första starten.

## Hur Det Fungerar

| Steg | Vad som händer |
|:----:|:-------------|
| **1. Spela in** | MemoTrail autoindexerar nya sessioner vid start + övervakar nya filer i realtid |
| **2. Dela upp** | Konversationer delas upp med token-, turbaserade eller rekursiva strategier |
| **3. Bädda in** | Varje segment bäddas in med `all-MiniLM-L6-v2` (~80MB, körs på CPU) |
| **4. Extrahera** | Sammanfattningar och arkitekturbeslut extraheras automatiskt |
| **5. Lagra** | Vektorer till ChromaDB, metadata till SQLite — allt under `~/.memotrail/` |
| **6. Sök** | Semantisk + BM25-nyckelordssökning genom hela din historik |
| **7. Visa** | Den mest relevanta historiska kontexten dyker upp precis när du behöver den |

> **100% lokalt** — inget moln, inga API-nycklar, ingen data lämnar din maskin.
>
> **Projektmedveten** — varje projekts konversationer lagras separat. Sök inom ett enskilt projekt eller över alla projekt samtidigt.
>
> **Multiplattform** — stöder Claude Code och Cursor IDE, med fler på gång.

## Tillgängliga Verktyg

När MemoTrail är anslutet får Claude Code dessa MCP-verktyg:

| Verktyg | Beskrivning |
|---------|-------------|
| `search_chats` | Semantisk sökning över alla tidigare konversationer |
| `search_keyword` | BM25-nyckelordssökning — utmärkt för exakta termer, funktionsnamn, felmeddelanden |
| `get_decisions` | Hämta registrerade arkitekturbeslut (automatiskt extraherade + manuella) |
| `get_recent_sessions` | Lista senaste kodsessioner med AI-genererade sammanfattningar |
| `get_session_detail` | Fördjupa dig i en specifik sessions innehåll |
| `save_memory` | Spara viktiga fakta eller beslut manuellt |
| `memory_stats` | Visa indexeringsstatistik och lagringsanvändning |

## CLI-kommandon

```bash
memotrail serve                          # Starta MCP-servern (autoindexerar nya sessioner)
memotrail search "redis caching beslut"  # Sök från terminalen
memotrail stats                          # Visa indexeringsstatistik
memotrail index                          # Manuell omindexering (valfritt)
```

## Arkitektur

```
~/.memotrail/
├── chroma/          # Vektorinbäddningar (ChromaDB)
└── memotrail.db     # Sessionsmetadata (SQLite)
```

| Komponent | Teknologi | Detaljer |
|-----------|-----------|---------|
| Inbäddningar | `all-MiniLM-L6-v2` | ~80MB, körs på CPU |
| Vektor-DB | ChromaDB | Beständig, lokal lagring |
| Nyckelordssökning | BM25 | Ren Python, inga extra beroenden |
| Metadata | SQLite | Enfilsdatabas |
| Filövervakning | watchdog | Realtidsdetektering av sessioner |
| Protokoll | MCP | Model Context Protocol |

### Stödda Plattformar

| Plattform | Status | Format |
|-----------|--------|--------|
| Claude Code | Stöds | JSONL-sessionsfiler |
| Cursor IDE | Stöds | state.vscdb (SQLite) |
| GitHub Copilot | Planerad | — |

### Uppdelningsstrategier

| Strategi | Bäst för |
|----------|----------|
| `token` (standard) | Allmänt bruk — grupperar meddelanden upp till tokengräns |
| `turn` | Konversationsfokuserat — grupperar användar+assistent-par |
| `recursive` | Långt innehåll — delar upp på stycken, meningar, ord |

## Varför MemoTrail?

| | MemoTrail | CLAUDE.md / Regelfiler | Manuella anteckningar |
|---|---|---|---|
| Automatiskt | Ja — indexerar vid varje sessionsstart | Nej — du skriver det | Nej |
| Sökbart | Semantisk sökning | AI läser det, men bara det du skrev | Ctrl+F enbart |
| Skalbart | Tusentals sessioner | Enskild fil | Utspridda filer |
| Kontextmedveten | Returnerar relevant kontext | Statiska regler | Manuell uppslagning |
| Installation | 5 minuter | Alltid underhållen | Alltid underhållen |

MemoTrail ersätter inte `CLAUDE.md` — det kompletterar det. Regelfiler är för instruktioner. MemoTrail är för minne.

## Färdplan

- [x] Claude Code-sessionsindexering
- [x] Semantisk sökning över konversationer
- [x] MCP-server med 7 verktyg
- [x] CLI för indexering och sökning
- [x] Autoindexering vid serverstart (inget manuellt `memotrail index` behövs)
- [x] Automatisk beslutsextraktion
- [x] Sessionssammanfattning
- [x] Cursor IDE-samlare
- [x] BM25-nyckelordssökning + hybridsökning
- [x] Realtidsfilövervakning (watchdog)
- [x] Flera uppdelningsstrategier (token, tur, rekursiv)
- [x] VS Code-tillägg
- [ ] Copilot-samlare
- [ ] Molnsynkronisering (Pro)
- [ ] Teamminne (Team)

## VS Code-tillägg

MemoTrail inkluderar ett VS Code-tillägg för direkt IDE-integration.

**Tillgängliga kommandon:**
- `MemoTrail: Search Conversations` — semantisk sökning
- `MemoTrail: Keyword Search` — BM25-nyckelordssökning
- `MemoTrail: Recent Sessions` — visa sessionsstatistik
- `MemoTrail: Index Sessions Now` — utlös manuell indexering
- `MemoTrail: Show Stats` — visa indexeringsstatistik

**Installation:**
```bash
cd vscode-extension
npm install
npm run compile
# Tryck sedan F5 i VS Code för att starta Extension Development Host
```

## Utveckling

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Bidra

Bidrag välkomnas! Se [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) för riktlinjer.

**Bra första problem:**
- [ ] Lägg till GitHub Copilot-sessionssamlare
- [ ] Lägg till Windsurf/Codeium-sessionssamlare
- [ ] Lägg till molnsynkronisering (valfritt)
- [ ] Lägg till delat teamminne

## Licens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Byggd av [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Om MemoTrail hjälper dig, överväg att ge en stjärna på GitHub.

</div>
