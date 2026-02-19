"""Claude Code collector: parses Claude Code session logs."""

import json
from pathlib import Path
from datetime import datetime, timezone

from memotrail.utils import config, get_logger

logger = get_logger("memotrail.collectors.claude_code")


def find_session_files(log_dir: Path | None = None) -> list[Path]:
    """Find all Claude Code JSONL session files.

    Claude Code stores sessions in:
    ~/.claude/projects/<project-hash>/sessions/<session-id>/

    Each session directory may contain JSONL files with conversation data.
    """
    base_dir = log_dir or config.claude_code_log_dir
    if not base_dir.exists():
        logger.warning(f"Claude Code log directory not found: {base_dir}")
        return []

    session_files = []

    # Walk through project directories
    for project_dir in base_dir.iterdir():
        if not project_dir.is_dir():
            continue

        # Look for session directories
        sessions_dir = project_dir / "sessions"
        if sessions_dir.exists():
            for session_dir in sessions_dir.iterdir():
                if not session_dir.is_dir():
                    continue
                # Look for JSONL files in session directory
                for f in session_dir.glob("*.jsonl"):
                    session_files.append(f)

        # Also check for direct JSONL files in project dir
        for f in project_dir.glob("*.jsonl"):
            session_files.append(f)

    logger.info(f"Found {len(session_files)} session files in {base_dir}")
    return sorted(session_files)


def parse_session_file(filepath: Path) -> dict:
    """Parse a Claude Code JSONL session file.

    Returns:
        dict with keys: project, messages, source_file
    """
    messages = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract message based on Claude Code log format
                msg = _extract_message(entry)
                if msg:
                    messages.append(msg)
    except Exception as e:
        logger.error(f"Error parsing {filepath}: {e}")
        return {"project": None, "messages": [], "source_file": str(filepath)}

    # Infer project name from path
    project = _infer_project(filepath)

    return {
        "project": project,
        "messages": messages,
        "source_file": str(filepath),
    }


def _extract_message(entry: dict) -> dict | None:
    """Extract a message from a Claude Code log entry.

    Claude Code log format varies, but typically has:
    - type: "human" or "assistant"
    - message: {role: str, content: str/list}
    - timestamp or ts
    """
    # Format 1: Direct role/content
    if "role" in entry and "content" in entry:
        content = entry["content"]
        if isinstance(content, list):
            # Content blocks - extract text parts
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
            content = "\n".join(text_parts)

        if not content or not content.strip():
            return None

        return {
            "role": entry["role"],
            "content": content.strip(),
            "timestamp": entry.get("timestamp", entry.get("ts", "")),
        }

    # Format 2: Nested message
    if "message" in entry:
        msg = entry["message"]
        if isinstance(msg, dict):
            return _extract_message(msg)

    # Format 3: type + content
    if "type" in entry:
        role_map = {"human": "user", "user": "user", "assistant": "assistant"}
        role = role_map.get(entry["type"])
        if role and "content" in entry:
            content = entry["content"]
            if isinstance(content, str) and content.strip():
                return {
                    "role": role,
                    "content": content.strip(),
                    "timestamp": entry.get("timestamp", entry.get("ts", "")),
                }

    return None


def _infer_project(filepath: Path) -> str | None:
    """Infer project name from file path.

    Path pattern: ~/.claude/projects/<project-hash>/sessions/<session-id>/file.jsonl
    """
    parts = filepath.parts

    # Try to find "projects" in path
    for i, part in enumerate(parts):
        if part == "projects" and i + 1 < len(parts):
            project_hash = parts[i + 1]
            # The project hash might be a readable name or a hash
            # Return it as-is for now
            return project_hash

    return None


def collect_all_sessions(log_dir: Path | None = None) -> list[dict]:
    """Collect and parse all Claude Code sessions.

    Returns:
        List of parsed sessions, each with: project, messages, source_file
    """
    files = find_session_files(log_dir)
    sessions = []

    for f in files:
        parsed = parse_session_file(f)
        if parsed["messages"]:  # Only include non-empty sessions
            sessions.append(parsed)
            logger.info(
                f"Collected session: {parsed['project'] or 'unknown'} "
                f"({len(parsed['messages'])} messages)"
            )

    logger.info(f"Collected {len(sessions)} sessions total")
    return sessions
