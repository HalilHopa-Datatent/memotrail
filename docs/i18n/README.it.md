<div align="center">

# MemoTrail

> 🌐 Questa è una traduzione automatica. Le correzioni della comunità sono benvenute! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Il tuo assistente di codice AI dimentica tutto. MemoTrail risolve questo problema.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Un livello di memoria persistente per assistenti di codice AI.
Ogni sessione registrata, ogni decisione ricercabile, ogni contesto ricordato.

[Avvio Rapido](#avvio-rapido) · [Come Funziona](#come-funziona) · [Strumenti Disponibili](#strumenti-disponibili) · [Roadmap](#roadmap)

</div>

---

## Novita nella v0.3.0

- **Riassunti automatici delle sessioni** — ogni sessione riceve un riassunto generato dall'AI (nessuna chiave API necessaria)
- **Estrazione automatica delle decisioni** — decisioni architetturali rilevate dalle conversazioni tramite pattern matching
- **Ricerca per parole chiave BM25** — nuovo strumento `search_keyword` per termini esatti, messaggi di errore, nomi di funzioni
- **Ricerca ibrida** — combina risultati semantici + per parole chiave usando reciprocal rank fusion
- **Supporto Cursor IDE** — indicizza la cronologia chat di Cursor dai file `state.vscdb`
- **Monitoraggio file in tempo reale** — nuove sessioni indicizzate istantaneamente tramite watchdog (nessun riavvio necessario)
- **Strategie di suddivisione** — scelta tra suddivisione per token, per turno o ricorsiva
- **Estensione VS Code** — cerca, indicizza e visualizza statistiche direttamente da VS Code
- **69 test** — copertura completa dei test su tutti i moduli

---

## Il Problema

Ogni nuova sessione di Claude Code parte da zero. La tua AI non ricorda la sessione di debug di 3 ore di ieri, le decisioni architetturali della settimana scorsa, o gli approcci che hanno già fallito.

**Senza MemoTrail:**
```
Tu: "Usiamo Redis per il caching"
AI:  "Certo, configuriamo Redis"
         ... 2 settimane dopo, nuova sessione ...
Tu: "Perché stiamo usando Redis?"
AI:  "Non ho contesto su quella decisione"
```

**Con MemoTrail:**
```
Tu: "Perché stiamo usando Redis?"
AI:  "In base alla sessione del 15 gennaio — hai valutato Redis vs Memcached.
      Redis è stato scelto per il supporto alle strutture dati e la persistenza.
      La discussione è nella sessione #42."
```

## Avvio Rapido

```bash
# 1. Installare
pip install memotrail

# 2. Connettere a Claude Code
claude mcp add memotrail -- memotrail serve
```

Tutto qui. MemoTrail indicizza automaticamente la tua cronologia al primo avvio.
Inizia una nuova sessione e chiedi: *"Su cosa abbiamo lavorato la settimana scorsa?"*

## Come Funziona

| Passo | Cosa succede |
|:----:|:-------------|
| **1. Registrare** | MemoTrail indicizza automaticamente le nuove sessioni all'avvio + monitora nuovi file in tempo reale |
| **2. Suddividere** | Le conversazioni vengono suddivise con strategie per token, per turno o ricorsive |
| **3. Incorporare** | Ogni frammento viene incorporato con `all-MiniLM-L6-v2` (~80MB, gira su CPU) |
| **4. Estrarre** | Riassunti e decisioni architetturali vengono estratti automaticamente |
| **5. Archiviare** | I vettori vanno in ChromaDB, i metadati in SQLite — tutto sotto `~/.memotrail/` |
| **6. Cercare** | Ricerca semantica + BM25 per parole chiave nell'intera cronologia |
| **7. Mostrare** | Il contesto passato più rilevante appare proprio quando ne hai bisogno |

> **100% locale** — nessun cloud, nessuna chiave API, nessun dato lascia la tua macchina.

> **Multipiattaforma** — supporta Claude Code e Cursor IDE, con altri in arrivo.

## Strumenti Disponibili

Una volta connesso, Claude Code ottiene questi strumenti MCP:

| Strumento | Descrizione |
|------|-------------|
| `search_chats` | Ricerca semantica in tutte le conversazioni passate |
| `search_keyword` | Ricerca BM25 per parole chiave — ideale per termini esatti, nomi di funzioni, messaggi di errore |
| `get_decisions` | Recuperare le decisioni architetturali registrate (auto-estratte + manuali) |
| `get_recent_sessions` | Elencare le sessioni recenti con riassunti generati dall'AI |
| `get_session_detail` | Esplorare in dettaglio il contenuto di una sessione specifica |
| `save_memory` | Salvare manualmente fatti o decisioni importanti |
| `memory_stats` | Visualizzare statistiche di indicizzazione e utilizzo dello storage |

## Comandi CLI

```bash
memotrail serve                          # Avviare il server MCP (indicizza automaticamente le nuove sessioni)
memotrail search "redis caching decision"  # Cercare dal terminale
memotrail stats                          # Visualizzare statistiche di indicizzazione
memotrail index                          # Re-indicizzare manualmente (opzionale)
```

## Architettura

```
~/.memotrail/
├── chroma/          # Embedding vettoriali (ChromaDB)
└── memotrail.db     # Metadati di sessione (SQLite)
```

| Componente | Tecnologia | Dettagli |
|-----------|-----------|---------|
| Embedding | `all-MiniLM-L6-v2` | ~80MB, gira su CPU |
| DB Vettoriale | ChromaDB | Storage locale persistente |
| Ricerca per Parole Chiave | BM25 | Python puro, nessuna dipendenza aggiuntiva |
| Metadati | SQLite | Database a file singolo |
| Monitoraggio File | watchdog | Rilevamento sessioni in tempo reale |
| Protocollo | MCP | Model Context Protocol |

#### Piattaforme Supportate

| Piattaforma | Stato | Formato |
|-------------|-------|---------|
| Claude Code | Supportato | File sessione JSONL |
| Cursor IDE | Supportato | state.vscdb (SQLite) |
| GitHub Copilot | Pianificato | — |

#### Strategie di Suddivisione

| Strategia | Utilizzo |
|-----------|----------|
| `token` (predefinita) | Uso generale — raggruppa messaggi fino al limite di token |
| `turn` | Focalizzata sulla conversazione — raggruppa coppie utente+assistente |
| `recursive` | Contenuto lungo — suddivide per paragrafi, frasi, parole |

## Perché MemoTrail?

| | MemoTrail | CLAUDE.md / File di regole | Note manuali |
|---|---|---|---|
| Automatico | Sì — indicizza ad ogni avvio di sessione | No — lo scrivi tu | No |
| Ricercabile | Ricerca semantica | L'AI lo legge, ma solo ciò che hai scritto | Solo Ctrl+F |
| Scalabile | Migliaia di sessioni | File singolo | File sparsi |
| Contestuale | Restituisce contesto rilevante | Regole statiche | Ricerca manuale |
| Configurazione | 5 minuti | Manutenzione costante | Manutenzione costante |

MemoTrail non sostituisce `CLAUDE.md` — lo completa. I file di regole sono per le istruzioni. MemoTrail è per la memoria.

## Roadmap

- [x] Indicizzazione sessioni Claude Code
- [x] Ricerca semantica tra le conversazioni
- [x] Server MCP con 7 strumenti
- [x] CLI per indicizzazione e ricerca
- [x] Auto-indicizzazione all'avvio del server
- [x] Estrazione automatica delle decisioni
- [x] Riassunto delle sessioni
- [x] Collettore Cursor IDE
- [x] Ricerca BM25 per parole chiave + ricerca ibrida
- [x] Monitoraggio file in tempo reale (watchdog)
- [x] Strategie multiple di suddivisione (token, turno, ricorsiva)
- [x] Estensione VS Code
- [ ] Collettore Copilot
- [ ] Sincronizzazione cloud (Pro)
- [ ] Memoria di team (Team)

## Estensione VS Code

Cerca, indicizza e visualizza statistiche direttamente da VS Code.

**Comandi:**
- **Search Conversations** — ricerca semantica da VS Code
- **Keyword Search** — ricerca BM25 per termini esatti
- **Recent Sessions** — visualizzazione sessioni recenti con riassunti
- **Index Sessions Now** — avvio indicizzazione su richiesta
- **Show Stats** — visualizzazione statistiche della memoria

## Sviluppo

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contribuire

I contributi sono benvenuti! Vedi [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) per le linee guida.

## Licenza

MIT — vedi [LICENSE](../../LICENSE)

---

<div align="center">

**Creato da [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Se MemoTrail ti aiuta, considera di dargli una stella su GitHub.

</div>
