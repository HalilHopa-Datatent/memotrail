<div align="center">

# MemoTrail

> 🌐 Ez egy automatikus fordítás. A közösségi javítások szívesen fogadottak! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Az AI kódolási asszisztensed mindent elfelejt. A MemoTrail megoldja ezt.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Állandó memóriaréteg AI kódolási asszisztensekhez.
Minden munkamenet rögzítve, minden döntés kereshető, minden kontextus megjegyezve.

</div>

---

## Újdonságok a v0.3.0-ban

- **Automatikus munkamenet-összefoglalás** — minden munkamenet AI-generált összefoglalót kap (nincs szükség API-kulcsokra)
- **Automatikus döntéskinyerés** — az architektúrális döntések mintaillesztéssel detektálódnak a beszélgetésekből
- **BM25 kulcsszavas keresés** — új `search_keyword` eszköz pontos kifejezésekhez, hibaüzenetekhez, függvénynevekhez
- **Hibrid keresés** — szemantikus + kulcsszavas eredményeket kombinál reciprocal rank fusion segítségével
- **Cursor IDE támogatás** — indexeli a Cursor csevegéstörténetét a `state.vscdb` fájlokból
- **Valós idejű fájlfigyelés** — az új munkamenetek azonnal indexelődnek watchdog-gal (nincs szükség újraindításra)
- **Darabolási stratégiák** — válassz token-alapú, tura-alapú vagy rekurzív felosztás között
- **VS Code bővítmény** — keresés, indexelés és statisztikák megtekintése közvetlenül VS Code-ból
- **69 teszt** — átfogó tesztlefedettség minden modulon

## A Probléma

Minden új Claude Code munkamenet nulláról indul. Az AI-d nem emlékszik a tegnapi 3 órás hibakeresési munkamenetre, a múlt heti architektúrális döntésekre, vagy a már kudarcot vallott megközelítésekre.

**MemoTrail nélkül:**
```
Te: "Használjunk Redis-t cachelésre"
AI:  "Rendben, állítsuk be a Redis-t"
         ... 2 héttel később, új munkamenet ...
Te: "Miért használjuk a Redis-t?"
AI:  "Nincs kontextusom erről a döntésről"
```

**MemoTrail-lel:**
```
Te: "Miért használjuk a Redis-t?"
AI:  "A január 15-i munkamenet alapján — összehasonlítottad a Redis-t és a Memcached-et.
      A Redis-t az adatstruktúra támogatás és a perzisztencia miatt választottad.
      A beszélgetés a #42 munkamenetben van."
```

## Gyorsindítás

```bash
# 1. Telepítés
pip install memotrail

# 2. Csatlakozás a Claude Code-hoz
claude mcp add memotrail -- memotrail serve
```

Ennyi. A MemoTrail automatikusan indexeli az előzményeidet az első indításkor.


<div align="center">
<img src="../../demo.gif" alt="MemoTrail Demo" width="800">
<br>
<sub>Install → Connect → See stats → Search past sessions → Save memory → Duplicate &amp; contradiction detection</sub>
</div>

## Hogyan Működik

| Lépés | Mi történik |
|:----:|:-------------|
| **1. Rögzítés** | A MemoTrail automatikusan indexeli az új munkameneteket indításkor + valós időben figyeli az új fájlokat |
| **2. Darabolás** | A beszélgetések token-, tura-alapú vagy rekurzív stratégiákkal oszlanak szegmensekre |
| **3. Beágyazás** | Minden szegmens `all-MiniLM-L6-v2`-vel beágyazódik (~80MB, CPU-n fut) |
| **4. Kinyerés** | Az összefoglalók és architektúrális döntések automatikusan kinyerődnek |
| **5. Tárolás** | Vektorok a ChromaDB-be, metaadatok az SQLite-ba — mind a `~/.memotrail/` alatt |
| **6. Keresés** | Szemantikus + BM25 kulcsszavas keresés a teljes előzményeidben |
| **7. Megjelenítés** | A legrelevánsabb korábbi kontextus pontosan akkor jelenik meg, amikor szükséged van rá |

> **100% helyi** — nincs felhő, nincsenek API-kulcsok, semmilyen adat nem hagyja el a gépedet.
>
> **Projektérzékeny** — minden projekt beszélgetései külön tárolódnak. Kereshetsz egy projekten belül vagy az összes projektben egyszerre.
>
> **Többplatformos** — támogatja a Claude Code-ot és a Cursor IDE-t, további platformok hamarosan.

## Elérhető Eszközök

A csatlakozás után a Claude Code ezeket az MCP-eszközöket kapja:

| Eszköz | Leírás |
|--------|--------|
| `search_chats` | Szemantikus keresés az összes korábbi beszélgetésben |
| `search_keyword` | BM25 kulcsszavas keresés — kiváló pontos kifejezésekhez, függvénynevekhez, hibaüzenetekhez |
| `get_decisions` | Rögzített architektúrális döntések lekérdezése (automatikusan kinyert + manuális) |
| `get_recent_sessions` | Legutóbbi kódolási munkamenetek listája AI-generált összefoglalókkal |
| `get_session_detail` | Részletes betekintés egy adott munkamenet tartalmába |
| `save_memory` | Fontos tények vagy döntések manuális mentése |
| `memory_stats` | Indexelési statisztikák és tárhelyhasználat megtekintése |

## CLI Parancsok

```bash
memotrail serve                          # MCP szerver indítása (automatikusan indexeli az új munkameneteket)
memotrail search "redis caching döntés"  # Keresés terminálból
memotrail stats                          # Indexelési statisztikák megtekintése
memotrail index                          # Manuális újraindexelés (opcionális)
```

## Architektúra

```
~/.memotrail/
├── chroma/          # Vektor beágyazások (ChromaDB)
└── memotrail.db     # Munkamenet metaadatok (SQLite)
```

| Komponens | Technológia | Részletek |
|-----------|-------------|-----------|
| Beágyazások | `all-MiniLM-L6-v2` | ~80MB, CPU-n fut |
| Vektor DB | ChromaDB | Állandó, helyi tárolás |
| Kulcsszavas keresés | BM25 | Tiszta Python, nincs extra függőség |
| Metaadatok | SQLite | Egyfájlos adatbázis |
| Fájlfigyelés | watchdog | Valós idejű munkamenet-érzékelés |
| Protokoll | MCP | Model Context Protocol |

### Támogatott Platformok

| Platform | Állapot | Formátum |
|----------|---------|----------|
| Claude Code | Támogatott | JSONL munkamenet-fájlok |
| Cursor IDE | Támogatott | state.vscdb (SQLite) |
| GitHub Copilot | Tervezett | — |

### Darabolási Stratégiák

| Stratégia | Legjobb ehhez |
|-----------|---------------|
| `token` (alapértelmezett) | Általános használat — üzeneteket csoportosít token-korlát eléréséig |
| `turn` | Beszélgetés-fókuszú — felhasználó+asszisztens párokat csoportosít |
| `recursive` | Hosszú tartalom — bekezdésekre, mondatokra, szavakra bontja |

## Miért MemoTrail?

| | MemoTrail | CLAUDE.md / Szabályfájlok | Manuális jegyzetek |
|---|---|---|---|
| Automatikus | Igen — minden munkamenet-indításkor indexel | Nem — te írod | Nem |
| Kereshető | Szemantikus keresés | AI olvassa, de csak amit írtál | Csak Ctrl+F |
| Skálázható | Ezernyi munkamenet | Egyetlen fájl | Szétszórt fájlok |
| Kontextusérzékeny | Releváns kontextust ad vissza | Statikus szabályok | Manuális keresés |
| Beállítás | 5 perc | Mindig karbantartandó | Mindig karbantartandó |

A MemoTrail nem helyettesíti a `CLAUDE.md`-t — kiegészíti azt. A szabályfájlok utasításokra valók. A MemoTrail a memóriáért felel.

## Ütemterv

- [x] Claude Code munkamenet-indexelés
- [x] Szemantikus keresés beszélgetéseken keresztül
- [x] MCP szerver 7 eszközzel
- [x] CLI indexeléshez és kereséshez
- [x] Automatikus indexelés szerver indításkor (nincs szükség manuális `memotrail index`-re)
- [x] Automatikus döntéskinyerés
- [x] Munkamenet-összefoglalás
- [x] Cursor IDE gyűjtő
- [x] BM25 kulcsszavas keresés + hibrid keresés
- [x] Valós idejű fájlfigyelés (watchdog)
- [x] Többféle darabolási stratégia (token, tura, rekurzív)
- [x] VS Code bővítmény
- [ ] Copilot gyűjtő
- [ ] Felhőszinkronizálás (Pro)
- [ ] Csapatmemória (Team)

## VS Code Bővítmény

A MemoTrail tartalmaz egy VS Code bővítményt a közvetlen IDE-integrációhoz.

**Elérhető parancsok:**
- `MemoTrail: Search Conversations` — szemantikus keresés
- `MemoTrail: Keyword Search` — BM25 kulcsszavas keresés
- `MemoTrail: Recent Sessions` — munkamenet-statisztikák megtekintése
- `MemoTrail: Index Sessions Now` — manuális indexelés indítása
- `MemoTrail: Show Stats` — indexelési statisztikák megjelenítése

**Beállítás:**
```bash
cd vscode-extension
npm install
npm run compile
# Majd nyomd meg az F5-öt VS Code-ban az Extension Development Host indításához
```

## Fejlesztés

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Hozzájárulás

Hozzájárulások szívesen fogadottak! Lásd a [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) fájlt az irányelvekért.

**Jó első problémák:**
- [ ] GitHub Copilot munkamenet-gyűjtő hozzáadása
- [ ] Windsurf/Codeium munkamenet-gyűjtő hozzáadása
- [ ] Felhőszinkronizálás opció hozzáadása (opt-in)
- [ ] Csapatmemória-megosztás hozzáadása

## Licenc

MIT — lásd [LICENSE](../../LICENSE)

---

<div align="center">

**Készítette: [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Ha a MemoTrail segít, fontold meg egy csillag adását a GitHub-on.

</div>
