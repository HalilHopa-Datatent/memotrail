<div align="center">

# MemoTrail

**Your AI coding assistant forgets everything. MemoTrail fixes that.**

[🇨🇳 中文](docs/i18n/README.zh-CN.md) · [🇹🇼 繁體中文](docs/i18n/README.zh-TW.md) · [🇯🇵 日本語](docs/i18n/README.ja.md) · [🇵🇹 Português](docs/i18n/README.pt.md) · [🇰🇷 한국어](docs/i18n/README.ko.md) · [🇪🇸 Español](docs/i18n/README.es.md) · [🇩🇪 Deutsch](docs/i18n/README.de.md) · [🇫🇷 Français](docs/i18n/README.fr.md) · [🇮🇱 עברית](docs/i18n/README.he.md) · [🇸🇦 العربية](docs/i18n/README.ar.md) · [🇷🇺 Русский](docs/i18n/README.ru.md) · [🇵🇱 Polski](docs/i18n/README.pl.md) · [🇨🇿 Čeština](docs/i18n/README.cs.md) · [🇳🇱 Nederlands](docs/i18n/README.nl.md) · [🇹🇷 Türkçe](docs/i18n/README.tr.md) · [🇺🇦 Українська](docs/i18n/README.uk.md) · [🇻🇳 Tiếng Việt](docs/i18n/README.vi.md) · [🇮🇩 Indonesia](docs/i18n/README.id.md) · [🇹🇭 ไทย](docs/i18n/README.th.md) · [🇮🇳 हिन्दी](docs/i18n/README.hi.md) · [🇧🇩 বাংলা](docs/i18n/README.bn.md) · [🇵🇰 اردو](docs/i18n/README.ur.md) · [🇷🇴 Română](docs/i18n/README.ro.md) · [🇸🇪 Svenska](docs/i18n/README.sv.md) · [🇮🇹 Italiano](docs/i18n/README.it.md) · [🇬🇷 Ελληνικά](docs/i18n/README.el.md) · [🇭🇺 Magyar](docs/i18n/README.hu.md) · [🇫🇮 Suomi](docs/i18n/README.fi.md) · [🇩🇰 Dansk](docs/i18n/README.da.md) · [🇳🇴 Norsk](docs/i18n/README.no.md)

[![PyPI version](https://img.shields.io/pypi/v/memotrail?color=blue)](https://pypi.org/project/memotrail/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/HalilHopa-Datatent/memotrail?style=social)](https://github.com/HalilHopa-Datatent/memotrail)

A persistent memory layer for AI coding assistants.
Every session recorded, every decision searchable, every context remembered.

[Quick Start](#quick-start) · [How It Works](#how-it-works) · [Available Tools](#available-tools) · [Roadmap](#roadmap)

</div>

---

## The Problem

Every new Claude Code session starts from zero. Your AI doesn't remember yesterday's 3-hour debugging session, the architectural decisions you made last week, or the approaches that already failed.

**Without MemoTrail:**
```
You: "Let's use Redis for caching"
AI:  "Sure, let's set up Redis"
         ... 2 weeks later, new session ...
You: "Why are we using Redis?"
AI:  "I don't have context on that decision"
```

**With MemoTrail:**
```
You: "Why are we using Redis?"
AI:  "Based on session from Jan 15 — you evaluated Redis vs Memcached.
      Redis was chosen for its data structure support and persistence.
      The discussion is in session #42."
```

## Quick Start

```bash
# 1. Install
pip install memotrail

# 2. Connect to Claude Code
claude mcp add memotrail -- memotrail serve
```

That's it. MemoTrail automatically indexes your history on first launch.
Start a new session and ask: *"What did we work on last week?"*

<div align="center">
<img src="demo.gif" alt="MemoTrail Demo" width="800">
</div>

## How It Works

| Step | What happens |
|:----:|:-------------|
| **1. Record** | MemoTrail auto-indexes new sessions every time the server starts |
| **2. Chunk** | Conversations are split into meaningful segments |
| **3. Embed** | Each chunk is embedded using `all-MiniLM-L6-v2` (~80MB, runs on CPU) |
| **4. Store** | Vectors go to ChromaDB, metadata to SQLite — all under `~/.memotrail/` |
| **5. Search** | Next session, Claude queries your full history semantically |
| **6. Surface** | The most relevant past context appears right when you need it |

> **100% local** — no cloud, no API keys, no data leaves your machine.

## Available Tools

Once connected, Claude Code gets these MCP tools:

| Tool | Description |
|------|-------------|
| `search_chats` | Semantic search across all past conversations |
| `get_decisions` | Retrieve recorded architectural decisions |
| `get_recent_sessions` | List recent coding sessions with summaries |
| `get_session_detail` | Deep dive into a specific session's content |
| `save_memory` | Manually save important facts or decisions |
| `memory_stats` | View indexing statistics and storage usage |

## CLI Commands

```bash
memotrail serve                          # Start MCP server (auto-indexes new sessions)
memotrail search "redis caching decision"  # Search from terminal
memotrail stats                          # View indexing stats
memotrail index                          # Manually re-index (optional)
```

## Architecture

```
~/.memotrail/
├── chroma/          # Vector embeddings (ChromaDB)
└── memotrail.db     # Session metadata (SQLite)
```

| Component | Technology | Details |
|-----------|-----------|---------|
| Embeddings | `all-MiniLM-L6-v2` | ~80MB, runs on CPU |
| Vector DB | ChromaDB | Persistent, local storage |
| Metadata | SQLite | Single-file database |
| Protocol | MCP | Model Context Protocol |

## Why MemoTrail?

| | MemoTrail | CLAUDE.md / Rules files | Manual notes |
|---|---|---|---|
| Automatic | Yes — indexes on every session start | No — you write it | No |
| Searchable | Semantic search | AI reads it, but only what you wrote | Ctrl+F only |
| Scales | Thousands of sessions | Single file | Scattered files |
| Context-aware | Returns relevant context | Static rules | Manual lookup |
| Setup | 5 minutes | Always maintained | Always maintained |

MemoTrail doesn't replace `CLAUDE.md` — it complements it. Rules files are for instructions. MemoTrail is for memory.

## Roadmap

- [x] Claude Code session indexing
- [x] Semantic search across conversations
- [x] MCP server with 6 tools
- [x] CLI for indexing and searching
- [x] Auto-indexing on server startup (no manual `memotrail index` needed)
- [ ] Automatic decision extraction
- [ ] Session summarization
- [ ] Cursor collector
- [ ] Copilot collector
- [ ] VS Code extension
- [ ] Cloud sync (Pro)
- [ ] Team memory (Team)

## Development

```bash
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail
pip install -e ".[dev]"
pytest
ruff check src/
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

**Good first issues:**
- [ ] Add Cursor session collector
- [ ] Add Copilot session collector
- [ ] Improve chunking strategy
- [ ] Add BM25 keyword search alongside semantic search

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**Built by [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

If MemoTrail helps you, consider giving it a star on GitHub.

</div>
