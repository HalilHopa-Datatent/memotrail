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

## Hogyan Működik

| Lépés | Mi történik |
|:----:|:-------------|
| **1. Rögzítés** | A MemoTrail automatikusan indexeli az új munkameneteket minden szerver indításkor |
| **2. Felosztás** | A beszélgetések értelmes szegmensekre oszlanak |
| **3. Beágyazás** | Minden szegmens `all-MiniLM-L6-v2`-vel beágyazódik (~80MB, CPU-n fut) |
| **4. Tárolás** | Vektorok a ChromaDB-be, metaadatok az SQLite-ba — mind a `~/.memotrail/` alatt |
| **5. Keresés** | A következő munkamenetben Claude szemantikusan keres az egész előzményeidben |
| **6. Megjelenítés** | A legrelevánsabb korábbi kontextus pontosan akkor jelenik meg, amikor szükséged van rá |

> **100% helyi** — nincs felhő, nincsenek API-kulcsok, semmilyen adat nem hagyja el a gépedet.

## Licenc

MIT — lásd [LICENSE](../../LICENSE)

---

<div align="center">

**Készítette: [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Ha a MemoTrail segít, fontold meg egy csillag adását a GitHub-on.

</div>
