<div align="center">

# MemoTrail

> 🌐 To jest tłumaczenie automatyczne. Poprawki społeczności są mile widziane! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Twój asystent kodowania AI zapomina wszystko. MemoTrail to rozwiązuje.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Trwała warstwa pamięci dla asystentów kodowania AI.
Każda sesja zapisana, każda decyzja przeszukiwalna, każdy kontekst zapamiętany.

[Szybki Start](#szybki-start) · [Jak to Działa](#jak-to-działa) · [Dostępne Narzędzia](#dostępne-narzędzia) · [Roadmap](#roadmap)

</div>

---

## Problem

Każda nowa sesja Claude Code zaczyna się od zera. Twoje AI nie pamięta wczorajszej 3-godzinnej sesji debugowania, decyzji architektonicznych z zeszłego tygodnia ani podejść, które już zawiodły.

**Bez MemoTrail:**
```
Ty: "Użyjmy Redis do cachowania"
AI:  "Jasne, skonfigurujmy Redis"
         ... 2 tygodnie później, nowa sesja ...
Ty: "Dlaczego używamy Redis?"
AI:  "Nie mam kontekstu tej decyzji"
```

**Z MemoTrail:**
```
Ty: "Dlaczego używamy Redis?"
AI:  "Na podstawie sesji z 15 stycznia — porównywałeś Redis z Memcached.
      Redis został wybrany ze względu na obsługę struktur danych i trwałość.
      Dyskusja jest w sesji #42."
```

## Szybki Start

```bash
# 1. Zainstaluj
pip install memotrail

# 2. Połącz z Claude Code
claude mcp add memotrail -- memotrail serve
```

To wszystko. MemoTrail automatycznie indeksuje Twoją historię przy pierwszym uruchomieniu.
Rozpocznij nową sesję i zapytaj: *"Nad czym pracowaliśmy w zeszłym tygodniu?"*

## Jak to Działa

| Krok | Co się dzieje |
|:----:|:-------------|
| **1. Nagrywanie** | MemoTrail automatycznie indeksuje nowe sesje przy każdym uruchomieniu serwera |
| **2. Podział** | Rozmowy są dzielone na znaczące segmenty |
| **3. Embedding** | Każdy fragment jest embeddowany za pomocą `all-MiniLM-L6-v2` (~80MB, działa na CPU) |
| **4. Przechowywanie** | Wektory trafiają do ChromaDB, metadane do SQLite — wszystko w `~/.memotrail/` |
| **5. Wyszukiwanie** | W następnej sesji Claude przeszukuje semantycznie całą Twoją historię |
| **6. Wyświetlanie** | Najbardziej odpowiedni kontekst z przeszłości pojawia się dokładnie wtedy, gdy go potrzebujesz |

> **100% lokalnie** — bez chmury, bez kluczy API, żadne dane nie opuszczają Twojej maszyny.

## Dostępne Narzędzia

Po połączeniu Claude Code otrzymuje te narzędzia MCP:

| Narzędzie | Opis |
|------|-------------|
| `search_chats` | Wyszukiwanie semantyczne we wszystkich przeszłych rozmowach |
| `get_decisions` | Pobieranie zapisanych decyzji architektonicznych |
| `get_recent_sessions` | Lista ostatnich sesji kodowania z podsumowaniami |
| `get_session_detail` | Szczegółowy wgląd w zawartość konkretnej sesji |
| `save_memory` | Ręczne zapisywanie ważnych faktów lub decyzji |
| `memory_stats` | Podgląd statystyk indeksowania i użycia pamięci |

## Komendy CLI

```bash
memotrail serve                          # Uruchom serwer MCP (automatycznie indeksuje nowe sesje)
memotrail search "redis caching decision"  # Szukaj z terminala
memotrail stats                          # Pokaż statystyki indeksowania
memotrail index                          # Ręcznie przeindeksuj (opcjonalnie)
```

## Architektura

```
~/.memotrail/
├── chroma/          # Embeddingi wektorowe (ChromaDB)
└── memotrail.db     # Metadane sesji (SQLite)
```

| Komponent | Technologia | Szczegóły |
|-----------|-----------|---------|
| Embeddingi | `all-MiniLM-L6-v2` | ~80MB, działa na CPU |
| Wektorowa BD | ChromaDB | Trwałe lokalne przechowywanie |
| Metadane | SQLite | Jednoplikowa baza danych |
| Protokół | MCP | Model Context Protocol |

## Dlaczego MemoTrail?

| | MemoTrail | CLAUDE.md / Pliki reguł | Ręczne notatki |
|---|---|---|---|
| Automatyczny | Tak — indeksuje przy każdym starcie sesji | Nie — sam piszesz | Nie |
| Przeszukiwalny | Wyszukiwanie semantyczne | AI czyta, ale tylko to co napisałeś | Tylko Ctrl+F |
| Skalowalny | Tysiące sesji | Pojedynczy plik | Rozproszone pliki |
| Kontekstowy | Zwraca odpowiedni kontekst | Statyczne reguły | Ręczne szukanie |
| Konfiguracja | 5 minut | Ciągła konserwacja | Ciągła konserwacja |

MemoTrail nie zastępuje `CLAUDE.md` — uzupełnia go. Pliki reguł są do instrukcji. MemoTrail jest do pamięci.

## Roadmap

- [x] Indeksowanie sesji Claude Code
- [x] Wyszukiwanie semantyczne między rozmowami
- [x] Serwer MCP z 6 narzędziami
- [x] CLI do indeksowania i wyszukiwania
- [x] Auto-indeksowanie przy starcie serwera
- [ ] Automatyczna ekstrakcja decyzji
- [ ] Podsumowanie sesji
- [ ] Kolektor Cursor
- [ ] Kolektor Copilot
- [ ] Rozszerzenie VS Code
- [ ] Synchronizacja w chmurze (Pro)
- [ ] Pamięć zespołowa (Team)

## Rozwój

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Współpraca

Współpraca jest mile widziana! Zobacz [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) po wytyczne.

## Licencja

MIT — zobacz [LICENSE](../../LICENSE)

---

<div align="center">

**Stworzone przez [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Jeśli MemoTrail Ci pomaga, rozważ danie gwiazdki na GitHub.

</div>
