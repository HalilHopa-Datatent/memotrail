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

## Uutta versiossa v0.3.0

- **Automaattinen istuntoyhteenveto** — jokainen istunto saa AI:n luoman yhteenvedon (ei API-avaimia tarvita)
- **Automaattinen päätösten poiminta** — arkkitehtuuripäätökset tunnistetaan keskusteluista mallinhaun avulla
- **BM25-avainsanahaku** — uusi `search_keyword`-työkalu tarkoille termeille, virheilmoituksille, funktionimille
- **Hybridihaku** — yhdistää semanttisia + avainsanatuloksia reciprocal rank fusionilla
- **Cursor IDE -tuki** — indeksoi Cursorin keskusteluhistorian `state.vscdb`-tiedostoista
- **Reaaliaikainen tiedostoseuranta** — uudet istunnot indeksoidaan välittömästi watchdogin kautta (uudelleenkäynnistystä ei tarvita)
- **Pilkkomisstrategiat** — valitse token-pohjainen, vuoropohjainen tai rekursiivinen jakaminen
- **VS Code -laajennus** — hae, indeksoi ja näytä tilastoja suoraan VS Codesta
- **69 testiä** — kattava testikattavuus kaikissa moduuleissa

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
| **1. Tallenna** | MemoTrail indeksoi automaattisesti uudet istunnot käynnistyksessä + seuraa uusia tiedostoja reaaliajassa |
| **2. Pilko** | Keskustelut pilkotaan token-, vuoropohjaisilla tai rekursiivisilla strategioilla |
| **3. Upota** | Jokainen segmentti upotetaan `all-MiniLM-L6-v2`:lla (~80MB, toimii CPU:lla) |
| **4. Poimi** | Yhteenvedot ja arkkitehtuuripäätökset poimitaan automaattisesti |
| **5. Talleta** | Vektorit ChromaDB:hen, metatiedot SQLiteen — kaikki `~/.memotrail/` alla |
| **6. Hae** | Semanttinen + BM25-avainsanahaku koko historiastasi |
| **7. Näytä** | Olennaisin aiempi konteksti ilmestyy juuri kun tarvitset sitä |

> **100% paikallinen** — ei pilveä, ei API-avaimia, mikään data ei poistu koneeltasi.
>
> **Projektitietoinen** — jokaisen projektin keskustelut tallennetaan erikseen. Hae yhdestä projektista tai kaikista kerralla.
>
> **Monialustainen** — tukee Claude Codea ja Cursor IDE:tä, lisää tulossa pian.

## Käytettävissä Olevat Työkalut

Yhdistämisen jälkeen Claude Code saa nämä MCP-työkalut:

| Työkalu | Kuvaus |
|---------|--------|
| `search_chats` | Semanttinen haku kaikista aiemmista keskusteluista |
| `search_keyword` | BM25-avainsanahaku — loistava tarkoille termeille, funktionimille, virheilmoituksille |
| `get_decisions` | Hae tallennetut arkkitehtuuripäätökset (automaattisesti poimitut + manuaaliset) |
| `get_recent_sessions` | Listaa viimeisimmät koodausistunnot AI:n luomilla yhteenvedoilla |
| `get_session_detail` | Syvenny tietyn istunnon sisältöön |
| `save_memory` | Tallenna tärkeitä faktoja tai päätöksiä manuaalisesti |
| `memory_stats` | Näytä indeksointitilastot ja tallennustilan käyttö |

## CLI-komennot

```bash
memotrail serve                          # Käynnistä MCP-palvelin (indeksoi automaattisesti uudet istunnot)
memotrail search "redis caching päätös"  # Hae terminaalista
memotrail stats                          # Näytä indeksointitilastot
memotrail index                          # Manuaalinen uudelleenindeksointi (valinnainen)
```

## Arkkitehtuuri

```
~/.memotrail/
├── chroma/          # Vektoriupotukset (ChromaDB)
└── memotrail.db     # Istuntometatiedot (SQLite)
```

| Komponentti | Teknologia | Tiedot |
|-------------|-----------|--------|
| Upotukset | `all-MiniLM-L6-v2` | ~80MB, toimii CPU:lla |
| Vektori-DB | ChromaDB | Pysyvä, paikallinen tallennus |
| Avainsanahaku | BM25 | Puhdas Python, ei ylimääräisiä riippuvuuksia |
| Metatiedot | SQLite | Yhden tiedoston tietokanta |
| Tiedostoseuranta | watchdog | Reaaliaikainen istuntojen tunnistus |
| Protokolla | MCP | Model Context Protocol |

### Tuetut Alustat

| Alusta | Tila | Muoto |
|--------|------|-------|
| Claude Code | Tuettu | JSONL-istuntotiedostot |
| Cursor IDE | Tuettu | state.vscdb (SQLite) |
| GitHub Copilot | Suunniteltu | — |

### Pilkkomisstrategiat

| Strategia | Parhaiten sopii |
|-----------|-----------------|
| `token` (oletus) | Yleiskäyttö — ryhmittää viestejä token-rajaan asti |
| `turn` | Keskustelupainotteinen — ryhmittää käyttäjä+avustaja-pareja |
| `recursive` | Pitkä sisältö — jakaa kappaleisiin, lauseisiin, sanoihin |

## Miksi MemoTrail?

| | MemoTrail | CLAUDE.md / Sääntötiedostot | Manuaaliset muistiinpanot |
|---|---|---|---|
| Automaattinen | Kyllä — indeksoi jokaisella istunnon käynnistyksellä | Ei — sinä kirjoitat sen | Ei |
| Haettavissa | Semanttinen haku | AI lukee sen, mutta vain mitä kirjoitit | Vain Ctrl+F |
| Skaalautuu | Tuhansia istuntoja | Yksittäinen tiedosto | Hajanaisia tiedostoja |
| Kontekstitietoinen | Palauttaa relevantin kontekstin | Staattiset säännöt | Manuaalinen haku |
| Asennus | 5 minuuttia | Aina ylläpidettävä | Aina ylläpidettävä |

MemoTrail ei korvaa `CLAUDE.md`:tä — se täydentää sitä. Sääntötiedostot ovat ohjeita varten. MemoTrail on muistia varten.

## Tiekartta

- [x] Claude Code -istuntojen indeksointi
- [x] Semanttinen haku keskusteluista
- [x] MCP-palvelin 7 työkalulla
- [x] CLI indeksointiin ja hakuun
- [x] Automaattinen indeksointi palvelimen käynnistyksessä (manuaalista `memotrail index`-komentoa ei tarvita)
- [x] Automaattinen päätösten poiminta
- [x] Istuntoyhteenveto
- [x] Cursor IDE -keräin
- [x] BM25-avainsanahaku + hybridihaku
- [x] Reaaliaikainen tiedostoseuranta (watchdog)
- [x] Useita pilkkomisstrategioita (token, vuoro, rekursiivinen)
- [x] VS Code -laajennus
- [ ] Copilot-keräin
- [ ] Pilvisynkronointi (Pro)
- [ ] Tiimimuisti (Team)

## VS Code -laajennus

MemoTrail sisältää VS Code -laajennuksen suoraa IDE-integraatiota varten.

**Käytettävissä olevat komennot:**
- `MemoTrail: Search Conversations` — semanttinen haku
- `MemoTrail: Keyword Search` — BM25-avainsanahaku
- `MemoTrail: Recent Sessions` — näytä istuntotilastot
- `MemoTrail: Index Sessions Now` — käynnistä manuaalinen indeksointi
- `MemoTrail: Show Stats` — näytä indeksointitilastot

**Asennus:**
```bash
cd vscode-extension
npm install
npm run compile
# Paina sitten F5 VS Codessa käynnistääksesi Extension Development Host
```

## Kehitys

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Osallistuminen

Osallistuminen on tervetullutta! Katso [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) ohjeet.

**Hyviä ensimmäisiä tehtäviä:**
- [ ] Lisää GitHub Copilot -istuntokeräin
- [ ] Lisää Windsurf/Codeium -istuntokeräin
- [ ] Lisää pilvisynkronointivaihtoehto (opt-in)
- [ ] Lisää tiimimuistin jakaminen

## Lisenssi

MIT — katso [LICENSE](../../LICENSE)

---

<div align="center">

**Rakentanut [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Jos MemoTrail auttaa sinua, harkitse tähden antamista GitHubissa.

</div>
