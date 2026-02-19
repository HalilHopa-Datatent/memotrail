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
| **1. Optag** | MemoTrail autoindekserer nye sessioner ved hver serverstart |
| **2. Opdel** | Samtaler opdeles i meningsfulde segmenter |
| **3. Indlejr** | Hvert segment indlejres med `all-MiniLM-L6-v2` (~80MB, kører på CPU) |
| **4. Gem** | Vektorer til ChromaDB, metadata til SQLite — alt under `~/.memotrail/` |
| **5. Søg** | Næste session søger Claude semantisk i hele din historik |
| **6. Vis** | Den mest relevante historiske kontekst dukker op præcis når du har brug for den |

> **100% lokalt** — ingen sky, ingen API-nøgler, ingen data forlader din maskine.

## Licens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Bygget af [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Hvis MemoTrail hjælper dig, overvej at give en stjerne på GitHub.

</div>
