"""MemoTrail CLI — index history and run MCP server."""

import argparse
import sys

from memotrail.utils import get_logger

logger = get_logger("memotrail.cli")


def cmd_serve(args):
    """Run the MCP server."""
    from memotrail.server import main as server_main
    server_main()


def cmd_index(args):
    """Index Claude Code conversation history."""
    from memotrail.collectors.claude_code import find_session_files, parse_session_file
    from memotrail.core.indexer import Indexer

    logger.info("Indexing Claude Code conversation history...")

    files = find_session_files()
    if not files:
        print("No Claude Code sessions found.")
        print("Make sure you have used Claude Code and sessions exist in ~/.claude/projects/")
        return

    indexer = Indexer()
    sqlite = indexer.sqlite
    indexed = 0
    skipped = 0
    total_messages = 0

    for f in files:
        file_path = str(f)
        if sqlite.is_file_indexed(file_path):
            skipped += 1
            continue

        parsed = parse_session_file(f)
        if not parsed["messages"]:
            continue

        try:
            session_id = indexer.index_session(
                messages=parsed["messages"],
                project=parsed["project"],
                source="claude_code",
            )
            sqlite.mark_file_indexed(file_path, session_id)
            indexed += 1
            total_messages += len(parsed["messages"])
            print(f"  ✓ Indexed: {parsed['project'] or 'unknown'} "
                  f"({len(parsed['messages'])} messages)")
        except Exception as e:
            logger.error(f"Failed to index session: {e}")
            print(f"  ✗ Failed: {parsed.get('source_file', 'unknown')} — {e}")

    print(f"\nDone! Indexed {indexed} new sessions ({total_messages} messages)")
    if skipped:
        print(f"  Skipped {skipped} already-indexed sessions")
    print(f"You can now use MemoTrail in Claude Code:")
    print(f"  claude mcp add memotrail -- memotrail serve")


def cmd_search(args):
    """Quick search from CLI."""
    from memotrail.core.searcher import Searcher

    searcher = Searcher()
    results = searcher.search_chats(args.query, limit=args.limit)

    if not results:
        print("No results found.")
        return

    for i, r in enumerate(results, 1):
        print(f"\n--- Result {i} (score: {r.score:.2f}) ---")
        print(f"Session: {r.session_id} | Project: {r.project or 'unknown'}")
        print(f"Time: {r.timestamp or 'unknown'}")
        print(r.chunk_text[:500])


def cmd_stats(args):
    """Show MemoTrail statistics."""
    from memotrail.storage import SQLiteStore, ChromaStore

    sqlite = SQLiteStore()
    chroma = ChromaStore()

    db_stats = sqlite.get_stats()
    chat_chunks = chroma.get_collection_count(ChromaStore.CHAT_COLLECTION)
    memory_chunks = chroma.get_collection_count(ChromaStore.MEMORY_COLLECTION)

    print("MemoTrail Stats")
    print("=" * 30)
    print(f"Sessions indexed:     {db_stats['total_sessions']}")
    print(f"Messages stored:      {db_stats['total_messages']}")
    print(f"Decisions recorded:   {db_stats['total_decisions']}")
    print(f"Chat chunks:          {chat_chunks}")
    print(f"Memory notes:         {memory_chunks}")


def main():
    parser = argparse.ArgumentParser(
        prog="memotrail",
        description="MemoTrail — Persistent memory for AI coding assistants",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Run MCP server")

    # index
    index_parser = subparsers.add_parser("index", help="Index Claude Code history")

    # search
    search_parser = subparsers.add_parser("search", help="Search conversations")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-n", "--limit", type=int, default=5, help="Max results")

    # stats
    stats_parser = subparsers.add_parser("stats", help="Show statistics")

    args = parser.parse_args()

    if args.command == "serve":
        cmd_serve(args)
    elif args.command == "index":
        cmd_index(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "stats":
        cmd_stats(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
