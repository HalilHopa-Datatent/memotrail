<div align="center">

# MemoTrail

> 🌐 Toto je automatický překlad. Opravy od komunity jsou vítány! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Váš AI asistent pro kódování zapomíná všechno. MemoTrail to řeší.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Trvalá paměťová vrstva pro AI asistenty kódování.
Každá relace zaznamenána, každé rozhodnutí vyhledatelné, každý kontext zapamatován.

[Rychlý Start](#rychlý-start) · [Jak to Funguje](#jak-to-funguje) · [Dostupné Nástroje](#dostupné-nástroje) · [Roadmap](#roadmap)

</div>

---

## Problém

Každá nová relace Claude Code začíná od nuly. Vaše AI si nepamatuje včerejší 3hodinovou ladící relaci, architektonická rozhodnutí z minulého týdne ani přístupy, které již selhaly.

**Bez MemoTrail:**
```
Vy: "Použijme Redis pro cachování"
AI:  "Jasně, nastavíme Redis"
         ... o 2 týdny později, nová relace ...
Vy: "Proč používáme Redis?"
AI:  "Nemám kontext k tomuto rozhodnutí"
```

**S MemoTrail:**
```
Vy: "Proč používáme Redis?"
AI:  "Na základě relace z 15. ledna — porovnával jste Redis a Memcached.
      Redis byl vybrán pro podporu datových struktur a persistenci.
      Diskuse je v relaci #42."
```

## Rychlý Start

```bash
# 1. Nainstalujte
pip install memotrail

# 2. Připojte ke Claude Code
claude mcp add memotrail -- memotrail serve
```

To je vše. MemoTrail automaticky indexuje vaši historii při prvním spuštění.
Začněte novou relaci a zeptejte se: *"Na čem jsme pracovali minulý týden?"*

## Jak to Funguje

| Krok | Co se děje |
|:----:|:-------------|
| **1. Záznam** | MemoTrail automaticky indexuje nové relace při každém spuštění serveru |
| **2. Rozdělení** | Konverzace jsou rozděleny na smysluplné segmenty |
| **3. Embedding** | Každý fragment je embeddován pomocí `all-MiniLM-L6-v2` (~80MB, běží na CPU) |
| **4. Uložení** | Vektory jdou do ChromaDB, metadata do SQLite — vše v `~/.memotrail/` |
| **5. Hledání** | V další relaci Claude sémanticky prohledá celou vaši historii |
| **6. Zobrazení** | Nejrelevantnější minulý kontext se objeví přesně když ho potřebujete |

> **100% lokální** — žádný cloud, žádné API klíče, žádná data neopouští váš počítač.

## Dostupné Nástroje

Po připojení Claude Code získá tyto MCP nástroje:

| Nástroj | Popis |
|------|-------------|
| `search_chats` | Sémantické vyhledávání ve všech minulých konverzacích |
| `get_decisions` | Získání zaznamenaných architektonických rozhodnutí |
| `get_recent_sessions` | Seznam posledních kódovacích relací se souhrny |
| `get_session_detail` | Detailní pohled na obsah konkrétní relace |
| `save_memory` | Ruční uložení důležitých faktů nebo rozhodnutí |
| `memory_stats` | Zobrazení statistik indexování a využití úložiště |

## CLI Příkazy

```bash
memotrail serve                          # Spustit MCP server (automaticky indexuje nové relace)
memotrail search "redis caching decision"  # Hledat z terminálu
memotrail stats                          # Zobrazit statistiky indexování
memotrail index                          # Ručně přeindexovat (volitelné)
```

## Architektura

```
~/.memotrail/
├── chroma/          # Vektorové embeddingy (ChromaDB)
└── memotrail.db     # Metadata relací (SQLite)
```

| Komponenta | Technologie | Detaily |
|-----------|-----------|---------|
| Embeddingy | `all-MiniLM-L6-v2` | ~80MB, běží na CPU |
| Vektorová DB | ChromaDB | Trvalé lokální úložiště |
| Metadata | SQLite | Jednosouborová databáze |
| Protokol | MCP | Model Context Protocol |

## Proč MemoTrail?

| | MemoTrail | CLAUDE.md / Soubory pravidel | Ruční poznámky |
|---|---|---|---|
| Automatický | Ano — indexuje při každém startu relace | Ne — píšete sami | Ne |
| Vyhledatelný | Sémantické vyhledávání | AI čte, ale jen to co jste napsali | Pouze Ctrl+F |
| Škálovatelný | Tisíce relací | Jediný soubor | Rozptýlené soubory |
| Kontextový | Vrací relevantní kontext | Statická pravidla | Ruční hledání |
| Nastavení | 5 minut | Neustálá údržba | Neustálá údržba |

MemoTrail nenahrazuje `CLAUDE.md` — doplňuje ho. Soubory pravidel jsou pro instrukce. MemoTrail je pro paměť.

## Roadmap

- [x] Indexování relací Claude Code
- [x] Sémantické vyhledávání mezi konverzacemi
- [x] MCP server se 6 nástroji
- [x] CLI pro indexování a vyhledávání
- [x] Auto-indexování při startu serveru
- [ ] Automatická extrakce rozhodnutí
- [ ] Souhrn relací
- [ ] Kolektor Cursor
- [ ] Kolektor Copilot
- [ ] Rozšíření VS Code
- [ ] Cloudová synchronizace (Pro)
- [ ] Týmová paměť (Team)

## Vývoj

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Přispívání

Příspěvky jsou vítány! Viz [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) pro pokyny.

## Licence

MIT — viz [LICENSE](../../LICENSE)

---

<div align="center">

**Vytvořil [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Pokud vám MemoTrail pomáhá, zvažte udělení hvězdičky na GitHub.

</div>
