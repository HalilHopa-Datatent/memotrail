# 🔍 MemoTrail

**Every AI coding conversation you've ever had — searchable and remembered.**

MemoTrail is a persistent memory layer for AI coding assistants. It automatically records your sessions, indexes them semantically, and surfaces the most relevant past context in every new session.

> *"Why did we switch from Postgres to Redis 3 months ago?"*
> → MemoTrail finds the exact conversation where you decided that.

## The Problem

Every time you start a new Claude Code session, it's a blank slate. Your AI doesn't remember that you spent 3 hours yesterday debugging that auth flow, or that you decided to use Redis instead of Memcached, or that you tried approach X and it failed.

**You repeat yourself. Every. Single. Day.**

## The Solution

MemoTrail runs as an MCP server that gives your AI coding assistant a real memory:

- 🔍 **Search past conversations** — "What did we discuss about authentication?"
- 🧠 **Automatic indexing** — Every session is recorded and searchable
- 📝 **Decision tracking** — Important choices are preserved
- 🔒 **100% local** — Your data never leaves your machine
- ⚡ **5 min setup** — One install, one command

## Quick Start

```bash
# Install
pip install memotrail

# Index your existing Claude Code history
memotrail index

# Add to Claude Code
claude mcp add memotrail -- memotrail serve
```

That's it. Start a new Claude Code session and ask:
> "What did we work on last week?"

## How It Works

```
You code with Claude Code
        ↓
MemoTrail records the conversation
        ↓
Messages are chunked and embedded
        ↓
Stored locally (ChromaDB + SQLite)
        ↓
    Next session...
        ↓
Claude Code calls MemoTrail tools
        ↓
Relevant past context surfaces automatically
```

## Available Tools

Once connected, Claude Code can use these tools:

| Tool | What it does |
|------|-------------|
| `search_chats` | Search past conversations semantically |
| `get_decisions` | List recorded architectural decisions |
| `get_recent_sessions` | See what you worked on recently |
| `get_session_detail` | Deep dive into a specific session |
| `save_memory` | Manually save important facts |
| `memory_stats` | See how much is indexed |

## CLI Commands

```bash
# Index existing Claude Code history
memotrail index

# Search from terminal
memotrail search "redis caching decision"

# View stats
memotrail stats

# Run MCP server (usually called by Claude Code)
memotrail serve
```

## Architecture

```
~/.memotrail/
├── chroma/          # Vector embeddings (semantic search)
└── memotrail.db     # Session metadata (SQLite)
```

Everything runs locally. No cloud, no accounts, no API keys needed.

- **Embedding model**: `all-MiniLM-L6-v2` (~80MB, runs on CPU)
- **Vector DB**: ChromaDB (persistent, local)
- **Metadata**: SQLite (single file)

## Roadmap

- [x] Claude Code session indexing
- [x] Semantic search across conversations
- [x] MCP server with 6 tools
- [x] CLI for indexing and searching
- [ ] Automatic decision extraction
- [ ] Session summarization
- [ ] Cursor collector
- [ ] Copilot collector
- [ ] VS Code extension
- [ ] Cloud sync (Pro)
- [ ] Team memory (Team)

## Development

```bash
# Clone
git clone https://github.com/melihhopa/memotrail.git
cd memotrail

# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check src/
```

## Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

Good first issues:
- [ ] Add Cursor session collector
- [ ] Add Copilot session collector
- [ ] Improve chunking strategy
- [ ] Add BM25 keyword search alongside semantic search

## License

MIT — see [LICENSE](LICENSE)

---

**Built by [Melih Hopa](https://melihhopa.com)** | [memotrail.ai](https://memotrail.ai)
