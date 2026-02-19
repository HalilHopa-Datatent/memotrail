<div align="center">

# MemoTrail

> 🌐 Dit is een automatische vertaling. Correcties van de community zijn welkom! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Je AI-codeerassistent vergeet alles. MemoTrail lost dat op.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Een persistente geheugenlaag voor AI-codeerassistenten.
Elke sessie vastgelegd, elke beslissing doorzoekbaar, elke context onthouden.

[Snelstart](#snelstart) · [Hoe Het Werkt](#hoe-het-werkt) · [Beschikbare Tools](#beschikbare-tools) · [Roadmap](#roadmap)

</div>

---

## Het Probleem

Elke nieuwe Claude Code sessie begint vanaf nul. Je AI herinnert zich niet de 3 uur durende debugsessie van gisteren, de architectuurbeslissingen van vorige week, of de aanpakken die al gefaald hebben.

**Zonder MemoTrail:**
```
Jij: "Laten we Redis gebruiken voor caching"
AI:   "Natuurlijk, laten we Redis instellen"
         ... 2 weken later, nieuwe sessie ...
Jij: "Waarom gebruiken we Redis?"
AI:   "Ik heb geen context over die beslissing"
```

**Met MemoTrail:**
```
Jij: "Waarom gebruiken we Redis?"
AI:   "Op basis van de sessie van 15 januari — je hebt Redis vs Memcached geëvalueerd.
       Redis werd gekozen vanwege de datastructuurondersteuning en persistentie.
       De discussie staat in sessie #42."
```

## Snelstart

```bash
# 1. Installeren
pip install memotrail

# 2. Verbinden met Claude Code
claude mcp add memotrail -- memotrail serve
```

Dat is alles. MemoTrail indexeert automatisch je geschiedenis bij de eerste start.
Begin een nieuwe sessie en vraag: *"Waar hebben we vorige week aan gewerkt?"*

## Hoe Het Werkt

| Stap | Wat er gebeurt |
|:----:|:-------------|
| **1. Opnemen** | MemoTrail indexeert automatisch nieuwe sessies bij elke serverstart |
| **2. Opdelen** | Gesprekken worden opgedeeld in betekenisvolle segmenten |
| **3. Embedden** | Elk fragment wordt geëmbed met `all-MiniLM-L6-v2` (~80MB, draait op CPU) |
| **4. Opslaan** | Vectoren gaan naar ChromaDB, metadata naar SQLite — alles onder `~/.memotrail/` |
| **5. Zoeken** | In de volgende sessie doorzoekt Claude je volledige geschiedenis semantisch |
| **6. Tonen** | De meest relevante context uit het verleden verschijnt precies wanneer je het nodig hebt |

> **100% lokaal** — geen cloud, geen API-sleutels, geen data verlaat je machine.

## Beschikbare Tools

Na verbinding krijgt Claude Code deze MCP-tools:

| Tool | Beschrijving |
|------|-------------|
| `search_chats` | Semantisch zoeken in alle eerdere gesprekken |
| `get_decisions` | Vastgelegde architectuurbeslissingen ophalen |
| `get_recent_sessions` | Recente codeersessies met samenvattingen weergeven |
| `get_session_detail` | Diep inzoomen op de inhoud van een specifieke sessie |
| `save_memory` | Handmatig belangrijke feiten of beslissingen opslaan |
| `memory_stats` | Indexeringsstatistieken en opslaggebruik bekijken |

## CLI-Commando's

```bash
memotrail serve                          # MCP-server starten (indexeert automatisch nieuwe sessies)
memotrail search "redis caching decision"  # Zoeken vanuit de terminal
memotrail stats                          # Indexeringsstatistieken bekijken
memotrail index                          # Handmatig opnieuw indexeren (optioneel)
```

## Architectuur

```
~/.memotrail/
├── chroma/          # Vector-embeddings (ChromaDB)
└── memotrail.db     # Sessie-metadata (SQLite)
```

| Component | Technologie | Details |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, draait op CPU |
| Vector DB | ChromaDB | Persistente lokale opslag |
| Metadata | SQLite | Enkelvoudige bestandsdatabase |
| Protocol | MCP | Model Context Protocol |

## Waarom MemoTrail?

| | MemoTrail | CLAUDE.md / Regelbestanden | Handmatige notities |
|---|---|---|---|
| Automatisch | Ja — indexeert bij elke sessiestart | Nee — je schrijft het zelf | Nee |
| Doorzoekbaar | Semantisch zoeken | AI leest het, maar alleen wat je hebt geschreven | Alleen Ctrl+F |
| Schaalbaar | Duizenden sessies | Enkel bestand | Verspreide bestanden |
| Contextbewust | Geeft relevante context terug | Statische regels | Handmatig zoeken |
| Instelling | 5 minuten | Constant onderhoud | Constant onderhoud |

MemoTrail vervangt `CLAUDE.md` niet — het vult het aan. Regelbestanden zijn voor instructies. MemoTrail is voor geheugen.

## Roadmap

- [x] Claude Code sessie-indexering
- [x] Semantisch zoeken over gesprekken
- [x] MCP-server met 6 tools
- [x] CLI voor indexering en zoeken
- [x] Auto-indexering bij serverstart
- [ ] Automatische beslissingsextractie
- [ ] Sessiesamenvatting
- [ ] Cursor-collector
- [ ] Copilot-collector
- [ ] VS Code-extensie
- [ ] Cloudsynchronisatie (Pro)
- [ ] Teamgeheugen (Team)

## Ontwikkeling

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Bijdragen

Bijdragen zijn welkom! Zie [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) voor richtlijnen.

## Licentie

MIT — zie [LICENSE](../../LICENSE)

---

<div align="center">

**Gemaakt door [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Als MemoTrail je helpt, overweeg dan een ster te geven op GitHub.

</div>
