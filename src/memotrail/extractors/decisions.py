"""Decision extractor: detects architectural/technical decisions from conversations."""

import re
from dataclasses import dataclass
from memotrail.utils import get_logger

logger = get_logger("memotrail.extractors.decisions")

# Patterns that indicate a decision was made
_DECISION_PATTERNS = [
    # Explicit decisions
    (r"(?:decided|choosing|chose) to\s+(.{15,150})", "general"),
    (r"(?:went|going) with\s+(.{10,120})", "general"),
    (r"(?:let'?s|we(?:'ll)?) use\s+(.{10,120})", "technology"),
    (r"(?:switched?|moving?|migrat\w+) (?:to|from)\s+(.{10,120})", "technology"),
    (r"(?:will|should) use\s+(.{10,120})", "technology"),
    # Architecture patterns
    (r"(?:the|our) architecture (?:is|will be|should be)\s+(.{15,150})", "architecture"),
    (r"(?:using|adopted?|implementing?) (?:a |the )?(\w+ pattern\b.{5,100})", "architecture"),
    # Technology choices
    (r"(?:installed?|added?|import(?:ed|ing)?)\s+([\w-]+)\s+(?:for|as|to)\s+(.{10,100})", "dependency"),
    (r"(?:replaced?|swapped?)\s+(\S+)\s+with\s+(\S+)", "technology"),
    # Approach decisions
    (r"(?:better|best) (?:approach|way|option|solution) (?:is|would be)\s+(.{15,150})", "approach"),
    (r"(?:instead of|rather than)\s+(.{10,100}),?\s+(?:we(?:'ll)?|let'?s|I(?:'ll)?)\s+(.{10,100})", "approach"),
]

# Category keywords for additional classification
_CATEGORY_KEYWORDS = {
    "architecture": ["pattern", "architecture", "design", "structure", "layer", "module", "component"],
    "technology": ["library", "framework", "tool", "database", "api", "sdk", "package"],
    "dependency": ["install", "import", "require", "dependency", "package"],
    "approach": ["approach", "strategy", "method", "technique", "implementation"],
    "convention": ["convention", "naming", "style", "format", "standard", "rule"],
    "security": ["auth", "security", "encrypt", "permission", "token", "credential"],
    "performance": ["performance", "cache", "optimize", "speed", "memory", "latency"],
}


@dataclass
class ExtractedDecision:
    """A decision extracted from conversation."""
    decision_text: str
    context: str
    category: str


def extract_decisions(messages: list[dict]) -> list[ExtractedDecision]:
    """Extract technical/architectural decisions from conversation messages.

    Uses pattern matching — no LLM API calls needed.

    Args:
        messages: List of {"role": str, "content": str}

    Returns:
        List of extracted decisions
    """
    decisions = []
    seen_texts = set()

    for i, msg in enumerate(messages):
        content = msg.get("content", "")
        role = msg.get("role", "unknown")

        for pattern, default_category in _DECISION_PATTERNS:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                # Get the full match text
                decision_text = match.group(0).strip()

                # Clean up
                decision_text = _clean_decision(decision_text)
                if not decision_text or len(decision_text) < 15:
                    continue

                # Deduplicate
                text_lower = decision_text.lower()
                if text_lower in seen_texts:
                    continue
                seen_texts.add(text_lower)

                # Get context (surrounding messages)
                context = _get_context(messages, i)

                # Refine category
                category = _classify_category(decision_text, default_category)

                decisions.append(ExtractedDecision(
                    decision_text=decision_text,
                    context=context,
                    category=category,
                ))

    logger.info(f"Extracted {len(decisions)} decision(s)")
    return decisions[:10]  # Cap at 10 per session


def _clean_decision(text: str) -> str:
    """Clean up extracted decision text."""
    # Remove trailing punctuation and whitespace
    text = text.strip().rstrip(".,;:")
    # Remove markdown artifacts
    text = re.sub(r"[`*_]", "", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text)
    # Truncate if too long
    if len(text) > 200:
        text = text[:197] + "..."
    return text


def _get_context(messages: list[dict], index: int) -> str:
    """Get surrounding context for a decision."""
    context_parts = []

    # Include previous message (the question/prompt)
    if index > 0:
        prev = messages[index - 1]
        prev_content = prev.get("content", "").strip()
        if prev_content:
            role = prev.get("role", "unknown")
            truncated = prev_content[:200]
            if len(prev_content) > 200:
                truncated += "..."
            context_parts.append(f"[{role}]: {truncated}")

    # Include current message snippet
    current = messages[index]
    curr_content = current.get("content", "").strip()
    if curr_content:
        role = current.get("role", "unknown")
        truncated = curr_content[:200]
        if len(curr_content) > 200:
            truncated += "..."
        context_parts.append(f"[{role}]: {truncated}")

    return "\n".join(context_parts)


def _classify_category(text: str, default: str) -> str:
    """Refine the category of a decision based on its content."""
    text_lower = text.lower()

    # Check each category's keywords
    scores: dict[str, int] = {}
    for category, keywords in _CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score

    if scores:
        return max(scores, key=scores.get)

    return default
