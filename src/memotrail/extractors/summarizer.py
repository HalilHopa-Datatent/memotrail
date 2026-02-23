"""Session summarizer: generates summaries from conversation messages."""

import re
from memotrail.utils import get_logger

logger = get_logger("memotrail.extractors.summarizer")

# Action verbs that indicate what was accomplished
_ACTION_PATTERNS = [
    r"(?:created?|wrote|added|implemented?|built)\s+(.{10,80})",
    r"(?:fixed|resolved|debugged|patched)\s+(.{10,80})",
    r"(?:refactored|restructured|reorganized|moved)\s+(.{10,80})",
    r"(?:updated|changed|modified|edited)\s+(.{10,80})",
    r"(?:deleted|removed|cleaned up)\s+(.{10,80})",
    r"(?:configured|set up|installed|deployed)\s+(.{10,80})",
    r"(?:tested|reviewed|analyzed|investigated)\s+(.{10,80})",
]

# Patterns for file operations
_FILE_PATTERN = re.compile(r"[`'\"]?(\S+\.(?:py|js|ts|tsx|jsx|go|rs|java|rb|md|yaml|yml|json|toml))[`'\"]?")


def summarize_session(messages: list[dict]) -> str | None:
    """Generate a summary for a session from its messages.

    Uses heuristic extraction — no LLM API calls needed.

    Args:
        messages: List of {"role": str, "content": str}

    Returns:
        Summary string or None if not enough content
    """
    if not messages or len(messages) < 2:
        return None

    user_messages = [m for m in messages if m.get("role") in ("user", "human")]
    assistant_messages = [m for m in messages if m.get("role") == "assistant"]

    if not user_messages:
        return None

    # 1. Extract the initial intent from first user message
    intent = _extract_intent(user_messages[0].get("content", ""))

    # 2. Collect key actions from assistant messages
    actions = _extract_actions(assistant_messages)

    # 3. Collect files mentioned
    files = _extract_files(messages)

    # 4. Build summary
    parts = []

    if intent:
        parts.append(intent)

    if actions:
        action_str = "; ".join(actions[:3])
        parts.append(f"Actions: {action_str}")

    if files:
        file_str = ", ".join(sorted(files)[:5])
        parts.append(f"Files: {file_str}")

    if not parts:
        # Fallback: use truncated first user message
        first_content = user_messages[0].get("content", "").strip()
        if first_content:
            summary = first_content[:150]
            if len(first_content) > 150:
                summary += "..."
            return summary
        return None

    summary = ". ".join(parts)
    if len(summary) > 300:
        summary = summary[:297] + "..."

    return summary


def _extract_intent(first_message: str) -> str | None:
    """Extract the user's intent from their first message."""
    content = first_message.strip()
    if not content:
        return None

    # Take first line or first sentence
    first_line = content.split("\n")[0].strip()

    # If it's short enough, use as-is
    if len(first_line) <= 120:
        return first_line

    # Try to extract first sentence
    sentence_end = re.search(r"[.!?]\s", first_line)
    if sentence_end:
        return first_line[: sentence_end.start() + 1]

    # Truncate
    return first_line[:120] + "..."


def _extract_actions(assistant_messages: list[dict]) -> list[str]:
    """Extract key actions from assistant responses."""
    actions = []
    seen = set()

    for msg in assistant_messages:
        content = msg.get("content", "")
        for pattern in _ACTION_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the match
                action = match.strip().rstrip(".,;:")
                action_lower = action.lower()
                if action_lower not in seen and len(action) > 5:
                    seen.add(action_lower)
                    actions.append(action)

    return actions[:5]


def _extract_files(messages: list[dict]) -> set[str]:
    """Extract file paths mentioned in messages."""
    files = set()
    for msg in messages:
        content = msg.get("content", "")
        matches = _FILE_PATTERN.findall(content)
        for m in matches:
            # Filter out common false positives
            if not m.startswith("http") and "/" not in m[:2]:
                basename = m.split("/")[-1]
                files.add(basename)
    return files
