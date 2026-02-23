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

## What's New in v0.3.0

- **Automatic session summarization** — every session gets an AI-generated summary (no API keys needed)
- **Automatic decision extraction** — architectural decisions detected from conversations using pattern matching
- **BM25 keyword search** — new `search_keyword` tool for exact terms, error messages, function names
- **Hybrid search** — combines semantic + keyword results using reciprocal rank fusion
- **Cursor IDE support** — indexes Cursor chat history from `state.vscdb` files
- **Real-time file watching** — new sessions indexed instantly via watchdog (no restart needed)
- **Chunking strategies** — choose between token-based, turn-based, or recursive splitting
- **VS Code extension** — search, index, and view stats directly from VS Code
- **69 tests** — comprehensive test coverage across all modules

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

# 2. Connect to Claude Code (current project)
claude mcp add memotrail -- memotrail serve

# Or connect globally (all projects)
claude mcp add -s user memotrail -- memotrail serve
```

That's it. MemoTrail automatically indexes your history on first launch.
Start a new session and ask: *"What did we work on last week?"*

<div align="center">
<img src="demo.gif" alt="MemoTrail Demo" width="800">
</div>

## How It Works

| Step | What happens |
|:----:|:-------------|
| **1. Record** | MemoTrail auto-indexes new sessions on startup + watches for new files in real-time |
| **2. Chunk** | Conversations are split using token, turn-based, or recursive strategies |
| **3. Embed** | Each chunk is embedded using `all-MiniLM-L6-v2` (~80MB, runs on CPU) |
| **4. Extract** | Summaries and architectural decisions are automatically extracted |
| **5. Store** | Vectors go to ChromaDB, metadata to SQLite — all under `~/.memotrail/` |
| **6. Search** | Semantic + BM25 keyword search across your full history |
| **7. Surface** | The most relevant past context appears right when you need it |

> **100% local** — no cloud, no API keys, no data leaves your machine.
>
> **Project-aware** — each project's conversations are stored separately. Search within a single project or across all projects at once.
>
> **Multi-platform** — supports Claude Code and Cursor IDE, with more coming soon.

## Available Tools

Once connected, Claude Code gets these MCP tools:

| Tool | Description |
|------|-------------|
| `search_chats` | Semantic search across all past conversations |
| `search_keyword` | BM25 keyword search — great for exact terms, function names, error messages |
| `get_decisions` | Retrieve recorded architectural decisions (auto-extracted + manual) |
| `get_recent_sessions` | List recent coding sessions with AI-generated summaries |
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
| Keyword Search | BM25 | Pure Python, no extra dependencies |
| Metadata | SQLite | Single-file database |
| File Watching | watchdog | Real-time session detection |
| Protocol | MCP | Model Context Protocol |

### Supported Platforms

| Platform | Status | Format |
|----------|--------|--------|
| Claude Code | Supported | JSONL session files |
| Cursor IDE | Supported | state.vscdb (SQLite) |
| GitHub Copilot | Planned | — |

### Chunking Strategies

| Strategy | Best for |
|----------|----------|
| `token` (default) | General use — groups messages up to token limit |
| `turn` | Conversation-focused — groups user+assistant pairs |
| `recursive` | Long content — splits on paragraphs, sentences, words |

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
- [x] MCP server with 7 tools
- [x] CLI for indexing and searching
- [x] Auto-indexing on server startup (no manual `memotrail index` needed)
- [x] Automatic decision extraction
- [x] Session summarization
- [x] Cursor IDE collector
- [x] BM25 keyword search + hybrid search
- [x] Real-time file watching (watchdog)
- [x] Multiple chunking strategies (token, turn, recursive)
- [x] VS Code extension
- [ ] Copilot collector
- [ ] Cloud sync (Pro)
- [ ] Team memory (Team)

## VS Code Extension

MemoTrail includes a VS Code extension for direct IDE integration.

**Commands available:**
- `MemoTrail: Search Conversations` — semantic search
- `MemoTrail: Keyword Search` — BM25 keyword search
- `MemoTrail: Recent Sessions` — view session stats
- `MemoTrail: Index Sessions Now` — trigger manual indexing
- `MemoTrail: Show Stats` — display indexing statistics

**Setup:**
```bash
cd vscode-extension
npm install
npm run compile
# Then press F5 in VS Code to launch Extension Development Host
```

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
- [ ] Add GitHub Copilot session collector
- [ ] Add Windsurf/Codeium session collector
- [ ] Add cloud sync option (opt-in)
- [ ] Add team memory sharing

## License

MIT — see [LICENSE](LICENSE)

---

<div align="center">

**Built by [Halil Hopa](https://halilhopa.com)** · [memotrail.ai](https://memotrail.ai)

If MemoTrail helps you, consider giving it a star on GitHub.

</div>
