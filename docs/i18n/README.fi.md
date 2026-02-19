<div align="center">

# MemoTrail

> 🌐 Tämä on automaattinen käännös. Yhteisön korjaukset ovat tervetulleita! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**AI-koodausapurisi unohtaa kaiken. MemoTrail korjaa sen.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Pysyvä muistikerros AI-koodausapureille.
Jokainen istunto tallennettu, jokainen päätös haettavissa, jokainen konteksti muistettu.

</div>

---

## Ongelma

Jokainen uusi Claude Code -istunto alkaa nollasta. AI:si ei muista eilistä 3 tunnin virheenkorjausistuntoa, viime viikon arkkitehtuuripäätöksiä tai lähestymistapoja jotka jo epäonnistuivat.

**Ilman MemoTrailia:**
```
Sinä: "Käytetään Redistä välimuistiin"
AI:    "Tietysti, otetaan Redis käyttöön"
         ... 2 viikkoa myöhemmin, uusi istunto ...
Sinä: "Miksi käytämme Redistä?"
AI:    "Minulla ei ole kontekstia tuosta päätöksestä"
```

**MemoTrailin kanssa:**
```
Sinä: "Miksi käytämme Redistä?"
AI:    "Tammikuun 15. istunnon perusteella — arvioit Redis vs Memcached.
        Redis valittiin sen tietorakenteiden tuen ja pysyvyyden vuoksi.
        Keskustelu on istunnossa #42."
```

## Pikaopas

```bash
# 1. Asenna
pip install memotrail

# 2. Yhdistä Claude Codeen
claude mcp add memotrail -- memotrail serve
```

Siinä se. MemoTrail indeksoi automaattisesti historiasi ensimmäisellä käynnistyksellä.

## Miten Se Toimii

| Vaihe | Mitä tapahtuu |
|:----:|:-------------|
| **1. Tallenna** | MemoTrail indeksoi automaattisesti uudet istunnot jokaisella palvelinkäynnistyksellä |
| **2. Jaa** | Keskustelut jaetaan merkityksellisiin segmentteihin |
| **3. Upota** | Jokainen segmentti upotetaan `all-MiniLM-L6-v2`:lla (~80MB, toimii CPU:lla) |
| **4. Talleta** | Vektorit ChromaDB:hen, metatiedot SQLiteen — kaikki `~/.memotrail/` alla |
| **5. Hae** | Seuraavassa istunnossa Claude hakee semanttisesti koko historiastasi |
| **6. Näytä** | Olennaisin aiempi konteksti ilmestyy juuri kun tarvitset sitä |

> **100% paikallinen** — ei pilveä, ei API-avaimia, mikään data ei poistu koneeltasi.

## Lisenssi

MIT — katso [LICENSE](../../LICENSE)

---

<div align="center">

**Rakentanut [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Jos MemoTrail auttaa sinua, harkitse tähden antamista GitHubissa.

</div>
