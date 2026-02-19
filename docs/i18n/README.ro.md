<div align="center">

# MemoTrail

> 🌐 Aceasta este o traducere automată. Corecțiile comunității sunt binevenite! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Asistentul tău AI de cod uită totul. MemoTrail rezolvă asta.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Un strat de memorie persistentă pentru asistenți AI de cod.
Fiecare sesiune înregistrată, fiecare decizie căutabilă, fiecare context amintit.

[Start Rapid](#start-rapid) · [Cum Funcționează](#cum-funcționează) · [Instrumente Disponibile](#instrumente-disponibile) · [Roadmap](#roadmap)

</div>

---

## Problema

Fiecare sesiune nouă Claude Code începe de la zero. AI-ul tău nu își amintește sesiunea de depanare de 3 ore de ieri, deciziile de arhitectură de săptămâna trecută sau abordările care au eșuat deja.

**Fără MemoTrail:**
```
Tu: "Să folosim Redis pentru caching"
AI:  "Sigur, să configurăm Redis"
         ... 2 săptămâni mai târziu, sesiune nouă ...
Tu: "De ce folosim Redis?"
AI:  "Nu am context despre această decizie"
```

**Cu MemoTrail:**
```
Tu: "De ce folosim Redis?"
AI:  "Pe baza sesiunii din 15 ianuarie — ai evaluat Redis vs Memcached.
      Redis a fost ales pentru suportul structurilor de date și persistență.
      Discuția este în sesiunea #42."
```

## Start Rapid

```bash
# 1. Instalează
pip install memotrail

# 2. Conectează la Claude Code
claude mcp add memotrail -- memotrail serve
```

Asta e tot. MemoTrail indexează automat istoricul tău la prima pornire.
Începe o sesiune nouă și întreabă: *"La ce am lucrat săptămâna trecută?"*

## Cum Funcționează

| Pas | Ce se întâmplă |
|:----:|:-------------|
| **1. Înregistrare** | MemoTrail indexează automat sesiunile noi la fiecare pornire a serverului |
| **2. Segmentare** | Conversațiile sunt împărțite în segmente semnificative |
| **3. Embedding** | Fiecare fragment este embedded folosind `all-MiniLM-L6-v2` (~80MB, rulează pe CPU) |
| **4. Stocare** | Vectorii merg în ChromaDB, metadatele în SQLite — totul în `~/.memotrail/` |
| **5. Căutare** | În sesiunea următoare, Claude caută semantic în tot istoricul tău |
| **6. Afișare** | Contextul trecut cel mai relevant apare exact când ai nevoie |

> **100% local** — fără cloud, fără chei API, nicio dată nu părăsește mașina ta.

## Instrumente Disponibile

Odată conectat, Claude Code primește aceste instrumente MCP:

| Instrument | Descriere |
|------|-------------|
| `search_chats` | Căutare semantică în toate conversațiile trecute |
| `get_decisions` | Obținerea deciziilor de arhitectură înregistrate |
| `get_recent_sessions` | Listarea sesiunilor recente cu rezumate |
| `get_session_detail` | Examinare detaliată a conținutului unei sesiuni specifice |
| `save_memory` | Salvarea manuală a faptelor sau deciziilor importante |
| `memory_stats` | Vizualizarea statisticilor de indexare și utilizare a stocării |

## Comenzi CLI

```bash
memotrail serve                          # Pornește serverul MCP (indexează automat sesiunile noi)
memotrail search "redis caching decision"  # Caută din terminal
memotrail stats                          # Vizualizează statisticile de indexare
memotrail index                          # Re-indexează manual (opțional)
```

## Arhitectură

```
~/.memotrail/
├── chroma/          # Embedding-uri vectoriale (ChromaDB)
└── memotrail.db     # Metadate de sesiune (SQLite)
```

| Componentă | Tehnologie | Detalii |
|-----------|-----------|---------|
| Embedding-uri | `all-MiniLM-L6-v2` | ~80MB, rulează pe CPU |
| BD Vectorială | ChromaDB | Stocare locală persistentă |
| Metadate | SQLite | Bază de date într-un singur fișier |
| Protocol | MCP | Model Context Protocol |

## De ce MemoTrail?

| | MemoTrail | CLAUDE.md / Fișiere de reguli | Note manuale |
|---|---|---|---|
| Automat | Da — indexează la fiecare pornire de sesiune | Nu — le scrii tu | Nu |
| Căutabil | Căutare semantică | AI-ul citește, dar doar ce ai scris | Doar Ctrl+F |
| Scalabil | Mii de sesiuni | Fișier unic | Fișiere împrăștiate |
| Contextual | Returnează context relevant | Reguli statice | Căutare manuală |
| Configurare | 5 minute | Întreținere constantă | Întreținere constantă |

MemoTrail nu înlocuiește `CLAUDE.md` — îl completează. Fișierele de reguli sunt pentru instrucțiuni. MemoTrail este pentru memorie.

## Roadmap

- [x] Indexarea sesiunilor Claude Code
- [x] Căutare semantică între conversații
- [x] Server MCP cu 6 instrumente
- [x] CLI pentru indexare și căutare
- [x] Auto-indexare la pornirea serverului
- [ ] Extracție automată a deciziilor
- [ ] Rezumat de sesiuni
- [ ] Colector Cursor
- [ ] Colector Copilot
- [ ] Extensie VS Code
- [ ] Sincronizare cloud (Pro)
- [ ] Memorie de echipă (Team)

## Dezvoltare

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contribuții

Contribuțiile sunt binevenite! Vezi [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) pentru ghid.

## Licență

MIT — vezi [LICENSE](../../LICENSE)

---

<div align="center">

**Creat de [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Dacă MemoTrail te ajută, ia în considerare să dai o stea pe GitHub.

</div>
