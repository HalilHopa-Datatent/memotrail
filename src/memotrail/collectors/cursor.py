"""Cursor IDE collector: parses Cursor chat history from state.vscdb files."""

import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional

from memotrail.utils import get_logger

logger = get_logger("memotrail.collectors.cursor")


def _get_cursor_storage_dir() -> Path:
    """Get Cursor's workspace storage directory based on platform."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage"
    elif sys.platform == "win32":
        appdata = Path.home() / "AppData" / "Roaming"
        return appdata / "Cursor" / "User" / "workspaceStorage"
    else:
        # Linux
        return Path.home() / ".config" / "Cursor" / "User" / "workspaceStorage"


def find_session_files(storage_dir: Path | None = None) -> list[Path]:
    """Find all Cursor state.vscdb files containing chat history.

    Cursor stores sessions in:
    <storage_dir>/<workspace-hash>/state.vscdb

    Each state.vscdb is a SQLite database with chat data in the ItemTable.
    """
    base_dir = storage_dir or _get_cursor_storage_dir()
    if not base_dir.exists():
        logger.warning(f"Cursor storage directory not found: {base_dir}")
        return []

    vscdb_files = []
    for workspace_dir in base_dir.iterdir():
        if not workspace_dir.is_dir():
            continue
        state_file = workspace_dir / "state.vscdb"
        if state_file.exists():
            vscdb_files.append(state_file)

    logger.info(f"Found {len(vscdb_files)} Cursor workspace(s) in {base_dir}")
    return sorted(vscdb_files)


def parse_session_file(filepath: Path) -> list[dict]:
    """Parse a Cursor state.vscdb file and extract chat sessions.

    Returns:
        List of session dicts, each with: project, messages, source_file
    """
    sessions = []

    try:
        conn = sqlite3.connect(f"file:{filepath}?mode=ro", uri=True)
        conn.row_factory = sqlite3.Row

        # Cursor stores chat data under these keys
        chat_keys = [
            "workbench.panel.aichat.view.aichat.chatdata",
            "aiService.prompts",
        ]

        for key in chat_keys:
            try:
                row = conn.execute(
                    "SELECT value FROM ItemTable WHERE [key] = ?", (key,)
                ).fetchone()
                if row and row["value"]:
                    parsed = _parse_chat_data(row["value"], key, filepath)
                    sessions.extend(parsed)
            except sqlite3.OperationalError:
                continue

        conn.close()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")

    return sessions


def _parse_chat_data(raw_value: str, key: str, filepath: Path) -> list[dict]:
    """Parse JSON chat data from a Cursor database value."""
    sessions = []

    try:
        data = json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        return []

    project = _infer_project(filepath)

    if key == "workbench.panel.aichat.view.aichat.chatdata":
        sessions.extend(_parse_chatdata_format(data, project, filepath))
    elif key == "aiService.prompts":
        sessions.extend(_parse_prompts_format(data, project, filepath))

    return sessions


def _parse_chatdata_format(data: dict | list, project: Optional[str], filepath: Path) -> list[dict]:
    """Parse the chatdata format (list of conversations)."""
    sessions = []

    # Data can be a list of conversations or a dict with tabs/conversations
    conversations = []
    if isinstance(data, list):
        conversations = data
    elif isinstance(data, dict):
        # May have a tabs or conversations key
        for key in ("tabs", "conversations", "chats"):
            if key in data and isinstance(data[key], list):
                conversations = data[key]
                break
        if not conversations and "messages" in data:
            conversations = [data]

    for conv in conversations:
        if not isinstance(conv, dict):
            continue

        messages = _extract_messages_from_conversation(conv)
        if messages:
            sessions.append({
                "project": project,
                "messages": messages,
                "source_file": str(filepath),
            })

    return sessions


def _parse_prompts_format(data: dict | list, project: Optional[str], filepath: Path) -> list[dict]:
    """Parse the aiService.prompts format."""
    sessions = []

    prompts = data if isinstance(data, list) else data.get("prompts", []) if isinstance(data, dict) else []

    for prompt in prompts:
        if not isinstance(prompt, dict):
            continue

        messages = []
        # User prompt
        user_text = prompt.get("prompt", prompt.get("text", prompt.get("query", "")))
        if user_text and isinstance(user_text, str):
            messages.append({
                "role": "user",
                "content": user_text.strip(),
                "timestamp": prompt.get("timestamp", prompt.get("createdAt", "")),
            })

        # Assistant response
        response = prompt.get("response", prompt.get("answer", prompt.get("result", "")))
        if response and isinstance(response, str):
            messages.append({
                "role": "assistant",
                "content": response.strip(),
                "timestamp": prompt.get("timestamp", prompt.get("createdAt", "")),
            })

        if messages:
            sessions.append({
                "project": project,
                "messages": messages,
                "source_file": str(filepath),
            })

    return sessions


def _extract_messages_from_conversation(conv: dict) -> list[dict]:
    """Extract messages from a single conversation object."""
    messages = []

    raw_messages = conv.get("messages", conv.get("bubbles", []))
    if not isinstance(raw_messages, list):
        return []

    for msg in raw_messages:
        if not isinstance(msg, dict):
            continue

        role = msg.get("role", msg.get("type", ""))
        if role in ("human", "user"):
            role = "user"
        elif role in ("assistant", "ai", "bot"):
            role = "assistant"
        else:
            continue

        content = msg.get("content", msg.get("text", msg.get("message", "")))
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    text_parts.append(part.get("text", ""))
                elif isinstance(part, str):
                    text_parts.append(part)
            content = "\n".join(text_parts)

        if content and isinstance(content, str) and content.strip():
            messages.append({
                "role": role,
                "content": content.strip(),
                "timestamp": msg.get("timestamp", msg.get("createdAt", "")),
            })

    return messages


def _infer_project(filepath: Path) -> Optional[str]:
    """Infer project name from workspace metadata."""
    workspace_dir = filepath.parent

    # Try to read workspace.json for the actual folder name
    workspace_json = workspace_dir / "workspace.json"
    if workspace_json.exists():
        try:
            with open(workspace_json, "r") as f:
                data = json.loads(f.read())
                folder = data.get("folder", "")
                if folder:
                    # folder is typically a file:// URI
                    folder = folder.replace("file://", "")
                    return Path(folder).name
        except Exception:
            pass

    # Fallback: use the hash directory name
    return workspace_dir.name


def collect_all_sessions(storage_dir: Path | None = None) -> list[dict]:
    """Collect and parse all Cursor sessions.

    Returns:
        List of parsed sessions, each with: project, messages, source_file
    """
    files = find_session_files(storage_dir)
    all_sessions = []

    for f in files:
        sessions = parse_session_file(f)
        for s in sessions:
            if s["messages"]:
                all_sessions.append(s)
                logger.info(
                    f"Collected Cursor session: {s['project'] or 'unknown'} "
                    f"({len(s['messages'])} messages)"
                )

    logger.info(f"Collected {len(all_sessions)} Cursor sessions total")
    return all_sessions
