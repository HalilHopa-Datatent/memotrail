# MemoTrail — Project Context for Claude Code

## What is this?
MemoTrail is a persistent memory layer for AI coding assistants (MCP server).
It records all AI coding sessions, indexes them with embeddings, and provides
semantic search so the AI can "remember" past conversations.

## Tech Stack
- Python 3.11+
- MCP SDK (Model Context Protocol)
- ChromaDB (vector storage)
- SQLite (metadata)
- sentence-transformers (embeddings: all-MiniLM-L6-v2)
- watchdog (file watching)
- tiktoken (token counting)

## Project Structure
- `src/memotrail/server.py` — MCP server (main entry point)
- `src/memotrail/cli.py` — CLI commands (index, search, serve, stats)
- `src/memotrail/core/` — Chunker, Embedder, Indexer, Searcher
- `src/memotrail/collectors/` — Platform-specific log parsers (Claude Code first)
- `src/memotrail/storage/` — ChromaDB and SQLite wrappers
- `src/memotrail/utils/` — Config, token counting, logging

## Conventions
- Use type hints everywhere
- Dataclasses for data models
- Lazy-load heavy dependencies (sentence-transformers)
- All data stored in ~/.memotrail/
- Tests in tests/ directory, run with pytest

## Key Decisions
- MIT licensed, open source
- Local-first: no cloud, no API keys needed
- Claude Code is the first supported platform
- Architecture is platform-agnostic (collectors pattern)
- ChromaDB for vector search, SQLite for metadata
