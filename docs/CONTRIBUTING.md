# Contributing to MemoTrail

Thank you for your interest in contributing to MemoTrail! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.11+
- Git

### Getting Started

```bash
# Clone the repository
git clone https://github.com/HalilHopa-Datatent/memotrail.git
cd memotrail

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check src/ tests/
ruff format src/ tests/
```

## Project Structure

```
src/memotrail/
├── server.py          # MCP server (main entry point)
├── cli.py             # CLI commands (index, search, serve, stats)
├── core/              # Chunker, Embedder, Indexer, Searcher
├── collectors/        # Platform-specific log parsers
├── extractors/        # Decision & summary extraction
├── storage/           # ChromaDB and SQLite wrappers
└── utils/             # Config, token counting, logging
```

## How to Contribute

### Reporting Bugs

- Open an issue at [GitHub Issues](https://github.com/HalilHopa-Datatent/memotrail/issues)
- Include steps to reproduce, expected behavior, and actual behavior
- Include your Python version and OS

### Adding a New Collector

MemoTrail uses a collector pattern for platform support. To add a new collector:

1. Create a new file in `src/memotrail/collectors/` (e.g., `cursor.py`)
2. Implement the session discovery and parsing logic
3. Follow the pattern established in `claude_code.py`
4. Add tests in `tests/`

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Run tests: `pytest`
5. Run linter: `ruff check src/ tests/`
6. Commit with a clear message
7. Push and open a Pull Request

## Conventions

- **Type hints** everywhere
- **Dataclasses** for data models
- **Lazy-load** heavy dependencies (sentence-transformers, tiktoken)
- Line length: **100 characters**
- Linter: **ruff**
- Test framework: **pytest**

## Code Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting. Configuration is in `pyproject.toml`.

Key rules:
- `E` — pycodestyle errors
- `F` — PyFlakes
- `I` — isort (import ordering)
- `N` — pep8-naming
- `W` — pycodestyle warnings

## Data Storage

All user data is stored locally in `~/.memotrail/`:
- `chroma/` — Vector embeddings (ChromaDB)
- `memotrail.db` — Metadata (SQLite)

Never add cloud storage or external API calls without explicit opt-in.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
