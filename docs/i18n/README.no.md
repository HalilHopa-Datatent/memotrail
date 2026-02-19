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

## Hvordan Det Fungerer

| Trinn | Hva som skjer |
|:----:|:-------------|
| **1. Registrer** | MemoTrail autoindekserer nye økter ved hver serverstart |
| **2. Del opp** | Samtaler deles opp i meningsfulle segmenter |
| **3. Bygg inn** | Hvert segment bygges inn med `all-MiniLM-L6-v2` (~80MB, kjører på CPU) |
| **4. Lagre** | Vektorer til ChromaDB, metadata til SQLite — alt under `~/.memotrail/` |
| **5. Søk** | Neste økt søker Claude semantisk gjennom hele historikken din |
| **6. Vis** | Den mest relevante historiske konteksten dukker opp akkurat når du trenger den |

> **100% lokalt** — ingen sky, ingen API-nøkler, ingen data forlater maskinen din.

## Lisens

MIT — se [LICENSE](../../LICENSE)

---

<div align="center">

**Bygget av [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Hvis MemoTrail hjelper deg, vurder å gi en stjerne på GitHub.

</div>
