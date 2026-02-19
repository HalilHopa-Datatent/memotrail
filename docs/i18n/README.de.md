<div align="center">

# MemoTrail

> 🌐 Dies ist eine automatische Übersetzung. Community-Korrekturen sind willkommen! · [English](../../README.md)

[🇨🇳 中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md) · [🇵🇹 Português](README.pt.md) · [🇰🇷 한국어](README.ko.md) · [🇪🇸 Español](README.es.md) · [🇩🇪 Deutsch](README.de.md) · [🇫🇷 Français](README.fr.md) · [🇮🇱 עברית](README.he.md) · [🇸🇦 العربية](README.ar.md) · [🇷🇺 Русский](README.ru.md) · [🇵🇱 Polski](README.pl.md) · [🇨🇿 Čeština](README.cs.md) · [🇳🇱 Nederlands](README.nl.md) · [🇹🇷 Türkçe](README.tr.md) · [🇺🇦 Українська](README.uk.md) · [🇻🇳 Tiếng Việt](README.vi.md) · [🇮🇩 Indonesia](README.id.md) · [🇹🇭 ไทย](README.th.md) · [🇮🇳 हिन्दी](README.hi.md) · [🇧🇩 বাংলা](README.bn.md) · [🇵🇰 اردو](README.ur.md) · [🇷🇴 Română](README.ro.md) · [🇸🇪 Svenska](README.sv.md) · [🇮🇹 Italiano](README.it.md) · [🇬🇷 Ελληνικά](README.el.md) · [🇭🇺 Magyar](README.hu.md) · [🇫🇮 Suomi](README.fi.md) · [🇩🇰 Dansk](README.da.md) · [🇳🇴 Norsk](README.no.md)

**Dein AI-Codierassistent vergisst alles. MemoTrail löst das.**

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

Eine persistente Speicherschicht für AI-Codierassistenten.
Jede Sitzung aufgezeichnet, jede Entscheidung durchsuchbar, jeder Kontext gespeichert.

[Schnellstart](#schnellstart) · [Funktionsweise](#funktionsweise) · [Verfügbare Tools](#verfügbare-tools) · [Roadmap](#roadmap)

</div>

---

## Das Problem

Jede neue Claude Code Sitzung beginnt bei Null. Deine AI erinnert sich nicht an die 3-stündige Debugging-Session von gestern, die Architekturentscheidungen von letzter Woche oder die Ansätze, die bereits gescheitert sind.

**Ohne MemoTrail:**
```
Du: "Lass uns Redis für Caching nutzen"
AI:  "Klar, richten wir Redis ein"
         ... 2 Wochen später, neue Sitzung ...
Du: "Warum nutzen wir Redis?"
AI:  "Ich habe keinen Kontext zu dieser Entscheidung"
```

**Mit MemoTrail:**
```
Du: "Warum nutzen wir Redis?"
AI:  "Basierend auf der Sitzung vom 15. Januar — du hast Redis vs Memcached evaluiert.
      Redis wurde wegen der Datenstruktur-Unterstützung und Persistenz gewählt.
      Die Diskussion ist in Sitzung #42."
```

## Schnellstart

```bash
# 1. Installieren
pip install memotrail

# 2. Mit Claude Code verbinden
claude mcp add memotrail -- memotrail serve
```

Das war's. MemoTrail indexiert automatisch deinen Verlauf beim ersten Start.
Starte eine neue Sitzung und frage: *"Woran haben wir letzte Woche gearbeitet?"*

## Funktionsweise

| Schritt | Was passiert |
|:----:|:-------------|
| **1. Aufzeichnen** | MemoTrail indexiert neue Sitzungen automatisch bei jedem Serverstart |
| **2. Aufteilen** | Gespräche werden in sinnvolle Segmente aufgeteilt |
| **3. Einbetten** | Jeder Abschnitt wird mit `all-MiniLM-L6-v2` eingebettet (~80MB, läuft auf CPU) |
| **4. Speichern** | Vektoren gehen in ChromaDB, Metadaten in SQLite — alles unter `~/.memotrail/` |
| **5. Suchen** | In der nächsten Sitzung durchsucht Claude deinen gesamten Verlauf semantisch |
| **6. Anzeigen** | Der relevanteste vergangene Kontext erscheint genau dann, wenn du ihn brauchst |

> **100% lokal** — keine Cloud, keine API-Schlüssel, keine Daten verlassen deinen Rechner.

## Verfügbare Tools

Nach der Verbindung erhält Claude Code diese MCP-Tools:

| Tool | Beschreibung |
|------|-------------|
| `search_chats` | Semantische Suche über alle vergangenen Gespräche |
| `get_decisions` | Aufgezeichnete Architekturentscheidungen abrufen |
| `get_recent_sessions` | Letzte Coding-Sitzungen mit Zusammenfassungen auflisten |
| `get_session_detail` | Detaillierter Einblick in den Inhalt einer bestimmten Sitzung |
| `save_memory` | Wichtige Fakten oder Entscheidungen manuell speichern |
| `memory_stats` | Indexierungsstatistiken und Speichernutzung anzeigen |

## CLI-Befehle

```bash
memotrail serve                          # MCP-Server starten (indexiert neue Sitzungen automatisch)
memotrail search "redis caching decision"  # Vom Terminal aus suchen
memotrail stats                          # Indexierungsstatistiken anzeigen
memotrail index                          # Manuell neu indexieren (optional)
```

## Architektur

```
~/.memotrail/
├── chroma/          # Vektor-Embeddings (ChromaDB)
└── memotrail.db     # Sitzungs-Metadaten (SQLite)
```

| Komponente | Technologie | Details |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, läuft auf CPU |
| Vektor-DB | ChromaDB | Persistenter lokaler Speicher |
| Metadaten | SQLite | Einzeldatei-Datenbank |
| Protokoll | MCP | Model Context Protocol |

## Warum MemoTrail?

| | MemoTrail | CLAUDE.md / Regeldateien | Manuelle Notizen |
|---|---|---|---|
| Automatisch | Ja — indexiert bei jedem Sitzungsstart | Nein — du schreibst es | Nein |
| Durchsuchbar | Semantische Suche | AI liest es, aber nur was du geschrieben hast | Nur Ctrl+F |
| Skalierbar | Tausende Sitzungen | Einzelne Datei | Verstreute Dateien |
| Kontextbewusst | Gibt relevanten Kontext zurück | Statische Regeln | Manuelle Suche |
| Einrichtung | 5 Minuten | Ständige Pflege | Ständige Pflege |

MemoTrail ersetzt nicht `CLAUDE.md` — es ergänzt es. Regeldateien sind für Anweisungen. MemoTrail ist für Erinnerungen.

## Roadmap

- [x] Claude Code Sitzungsindexierung
- [x] Semantische Suche über Gespräche
- [x] MCP-Server mit 6 Tools
- [x] CLI für Indexierung und Suche
- [x] Auto-Indexierung beim Serverstart
- [ ] Automatische Entscheidungsextraktion
- [ ] Sitzungszusammenfassung
- [ ] Cursor-Kollektor
- [ ] Copilot-Kollektor
- [ ] VS Code Erweiterung
- [ ] Cloud-Synchronisation (Pro)
- [ ] Team-Speicher (Team)

## Entwicklung

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Mitwirken

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) für Richtlinien.

## Lizenz

MIT — siehe [LICENSE](../../LICENSE)

---

<div align="center">

**Erstellt von [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

Wenn MemoTrail dir hilft, erwäge einen Stern auf GitHub zu geben.

</div>
