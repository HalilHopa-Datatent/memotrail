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
| **1. Spela in** | MemoTrail autoindexerar nya sessioner vid varje serverstart |
| **2. Dela upp** | Konversationer delas upp i meningsfulla segment |
| **3. Bädda in** | Varje segment bäddas in med `all-MiniLM-L6-v2` (~80MB, körs på CPU) |
| **4. Lagra** | Vektorer till ChromaDB, metadata till SQLite — allt under `~/.memotrail/` |
| **5. Sök** | Nästa session söker Claude semantiskt igenom hela din historik |
| **6. Visa** | Den mest relevanta historiska kontexten dyker upp precis när du behöver den |

> **100% lokalt** — inget moln, inga API-nycklar, ingen data lämnar din maskin.

## Licens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Byggd av [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Om MemoTrail hjälper dig, överväg att ge en stjärna på GitHub.

</div>
