"""MemoTrail MCP Server — persistent memory for AI coding assistants."""

import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from memotrail.core import Indexer, Searcher
from memotrail.storage import SQLiteStore, ChromaStore
from memotrail.core.embedder import Embedder
from memotrail.utils import get_logger

logger = get_logger("memotrail.server")

# ── Initialize components ─────────────────────────────────────

sqlite_store = SQLiteStore()
chroma_store = ChromaStore()
embedder = Embedder()
indexer = Indexer(sqlite_store, chroma_store, embedder=embedder)
searcher = Searcher(sqlite_store, chroma_store, embedder=embedder)

# ── MCP Server ─────────────────────────────────────────────────

app = Server("memotrail")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MemoTrail tools."""
    return [
        Tool(
            name="search_chats",
            description=(
                "Search past AI coding conversations semantically. "
                "Use this to find previous discussions, decisions, and solutions. "
                "Example: search_chats('Why did we switch to Redis?')"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default: 5)",
                        "default": 5,
                    },
                    "project": {
                        "type": "string",
                        "description": "Filter by project name (optional)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_decisions",
            description=(
                "Get a list of recorded decisions from past sessions. "
                "Useful for understanding why certain choices were made."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "Filter by project (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default: 10)",
                        "default": 10,
                    },
                },
            },
        ),
        Tool(
            name="get_recent_sessions",
            description=(
                "Get summaries of recent coding sessions. "
                "Useful for context on what was worked on recently."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of sessions (default: 5)",
                        "default": 5,
                    },
                },
            },
        ),
        Tool(
            name="get_session_detail",
            description="Get full details of a specific session by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID to retrieve",
                    },
                },
                "required": ["session_id"],
            },
        ),
        Tool(
            name="save_memory",
            description=(
                "Save an important fact, decision, or note to long-term memory. "
                "Example: save_memory('We use PostgreSQL 16 with pgvector', ['database', 'stack'])"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The information to remember",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional tags for categorization",
                    },
                },
                "required": ["content"],
            },
        ),
        Tool(
            name="memory_stats",
            description="Get statistics about indexed sessions, messages, and memories.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "search_chats":
            return await _search_chats(arguments)
        elif name == "get_decisions":
            return await _get_decisions(arguments)
        elif name == "get_recent_sessions":
            return await _get_recent_sessions(arguments)
        elif name == "get_session_detail":
            return await _get_session_detail(arguments)
        elif name == "save_memory":
            return await _save_memory(arguments)
        elif name == "memory_stats":
            return await _memory_stats(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.error(f"Tool error ({name}): {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# ── Tool implementations ───────────────────────────────────────

async def _search_chats(args: dict) -> list[TextContent]:
    query = args["query"]
    limit = args.get("limit", 5)
    project = args.get("project")

    results = searcher.search_chats(query, limit=limit, project=project)

    if not results:
        return [TextContent(type="text", text="No matching conversations found.")]

    output_parts = [f"Found {len(results)} relevant conversation(s):\n"]
    for i, r in enumerate(results, 1):
        output_parts.append(
            f"--- Result {i} (score: {r.score:.2f}) ---\n"
            f"Session: {r.session_id}\n"
            f"Project: {r.project or 'unknown'}\n"
            f"Time: {r.timestamp or 'unknown'}\n"
            f"Content:\n{r.chunk_text}\n"
        )

    return [TextContent(type="text", text="\n".join(output_parts))]


async def _get_decisions(args: dict) -> list[TextContent]:
    project = args.get("project")
    limit = args.get("limit", 10)

    decisions = sqlite_store.get_decisions(project=project, limit=limit)

    if not decisions:
        return [TextContent(type="text", text="No decisions recorded yet.")]

    output_parts = [f"Found {len(decisions)} decision(s):\n"]
    for d in decisions:
        output_parts.append(
            f"• [{d.category}] {d.decision_text}\n"
            f"  Context: {d.context or 'N/A'}\n"
            f"  Session: {d.session_id} | Date: {d.created_at}\n"
        )

    return [TextContent(type="text", text="\n".join(output_parts))]


async def _get_recent_sessions(args: dict) -> list[TextContent]:
    limit = args.get("limit", 5)

    sessions = sqlite_store.get_recent_sessions(limit=limit)

    if not sessions:
        return [TextContent(type="text", text="No sessions indexed yet. Run 'memotrail index' first.")]

    output_parts = [f"Last {len(sessions)} session(s):\n"]
    for s in sessions:
        output_parts.append(
            f"• {s.id}\n"
            f"  Project: {s.project or 'unknown'}\n"
            f"  Started: {s.started_at}\n"
            f"  Messages: {s.message_count}\n"
            f"  Summary: {s.summary or 'No summary yet'}\n"
        )

    return [TextContent(type="text", text="\n".join(output_parts))]


async def _get_session_detail(args: dict) -> list[TextContent]:
    session_id = args["session_id"]
    session = sqlite_store.get_session(session_id)

    if not session:
        return [TextContent(type="text", text=f"Session not found: {session_id}")]

    messages = sqlite_store.get_session_messages(session_id)

    output_parts = [
        f"Session: {session.id}\n"
        f"Project: {session.project or 'unknown'}\n"
        f"Started: {session.started_at}\n"
        f"Ended: {session.ended_at or 'ongoing'}\n"
        f"Messages: {session.message_count}\n"
        f"Summary: {session.summary or 'No summary'}\n"
        f"Tags: {', '.join(session.tags) if session.tags else 'none'}\n"
        f"\n--- Messages ---\n"
    ]

    for msg in messages[:50]:  # Limit to 50 messages
        output_parts.append(f"[{msg.role}]: {msg.content[:500]}\n")

    if len(messages) > 50:
        output_parts.append(f"\n... and {len(messages) - 50} more messages")

    return [TextContent(type="text", text="\n".join(output_parts))]


async def _save_memory(args: dict) -> list[TextContent]:
    content = args["content"]
    tags = args.get("tags", [])

    memory_id = indexer.index_memory(content, tags)

    return [TextContent(
        type="text",
        text=f"Memory saved: {memory_id}\nContent: {content}\nTags: {', '.join(tags) if tags else 'none'}",
    )]


async def _memory_stats(args: dict) -> list[TextContent]:
    db_stats = sqlite_store.get_stats()
    chat_chunks = chroma_store.get_collection_count(ChromaStore.CHAT_COLLECTION)
    memory_chunks = chroma_store.get_collection_count(ChromaStore.MEMORY_COLLECTION)

    text = (
        f"MemoTrail Stats:\n"
        f"  Sessions indexed: {db_stats['total_sessions']}\n"
        f"  Messages stored: {db_stats['total_messages']}\n"
        f"  Decisions recorded: {db_stats['total_decisions']}\n"
        f"  Chat chunks (searchable): {chat_chunks}\n"
        f"  Memory notes: {memory_chunks}\n"
    )

    return [TextContent(type="text", text=text)]


# ── Entry point ────────────────────────────────────────────────

async def run_server():
    """Run the MCP server via stdio."""
    logger.info("Starting MemoTrail MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """CLI entry point for MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
