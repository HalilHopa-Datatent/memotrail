"""Tests for collector modules — Claude Code and Cursor parsers."""

import json
import tempfile
from pathlib import Path

from memotrail.collectors.claude_code import (
    parse_session_file,
    _extract_message,
    _infer_project,
)
from memotrail.collectors.cursor import (
    _extract_messages_from_conversation,
    _parse_chatdata_format,
    _infer_project as cursor_infer_project,
)


class TestClaudeCodeExtractMessage:
    def test_direct_role_content(self):
        entry = {"role": "user", "content": "Hello world"}
        msg = _extract_message(entry)
        assert msg is not None
        assert msg["role"] == "user"
        assert msg["content"] == "Hello world"

    def test_content_blocks(self):
        entry = {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "First part"},
                {"type": "text", "text": "Second part"},
            ],
        }
        msg = _extract_message(entry)
        assert msg is not None
        assert "First part" in msg["content"]
        assert "Second part" in msg["content"]

    def test_nested_message(self):
        entry = {"message": {"role": "user", "content": "Nested hello"}}
        msg = _extract_message(entry)
        assert msg is not None
        assert msg["content"] == "Nested hello"

    def test_type_content_format(self):
        entry = {"type": "human", "content": "Type format message"}
        msg = _extract_message(entry)
        assert msg is not None
        assert msg["role"] == "user"

    def test_empty_content_returns_none(self):
        entry = {"role": "user", "content": ""}
        msg = _extract_message(entry)
        assert msg is None

    def test_unknown_format_returns_none(self):
        entry = {"foo": "bar"}
        msg = _extract_message(entry)
        assert msg is None

    def test_timestamp_extraction(self):
        entry = {"role": "user", "content": "test", "timestamp": "2025-01-01T00:00:00Z"}
        msg = _extract_message(entry)
        assert msg["timestamp"] == "2025-01-01T00:00:00Z"

    def test_ts_fallback(self):
        entry = {"role": "user", "content": "test", "ts": "1234567890"}
        msg = _extract_message(entry)
        assert msg["timestamp"] == "1234567890"


class TestClaudeCodeParseSession:
    def test_parse_valid_jsonl(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write(json.dumps({"role": "user", "content": "Hello"}) + "\n")
            f.write(json.dumps({"role": "assistant", "content": "Hi there"}) + "\n")
            f.flush()

            result = parse_session_file(Path(f.name))
            assert len(result["messages"]) == 2
            assert result["messages"][0]["role"] == "user"

    def test_parse_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write("")
            f.flush()

            result = parse_session_file(Path(f.name))
            assert result["messages"] == []

    def test_parse_invalid_json_lines(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
            f.write("not json\n")
            f.write(json.dumps({"role": "user", "content": "Valid"}) + "\n")
            f.flush()

            result = parse_session_file(Path(f.name))
            assert len(result["messages"]) == 1


class TestClaudeCodeInferProject:
    def test_project_from_path(self):
        path = Path("/home/user/.claude/projects/my-project/sessions/abc123/file.jsonl")
        assert _infer_project(path) == "my-project"

    def test_no_project_in_path(self):
        path = Path("/tmp/random/file.jsonl")
        assert _infer_project(path) is None


class TestCursorExtractMessages:
    def test_basic_conversation(self):
        conv = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there"},
            ]
        }
        messages = _extract_messages_from_conversation(conv)
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"

    def test_human_role_mapping(self):
        conv = {
            "messages": [
                {"role": "human", "content": "Test"},
            ]
        }
        messages = _extract_messages_from_conversation(conv)
        assert messages[0]["role"] == "user"

    def test_bubbles_format(self):
        conv = {
            "bubbles": [
                {"role": "user", "content": "Question"},
                {"role": "ai", "content": "Answer"},
            ]
        }
        messages = _extract_messages_from_conversation(conv)
        assert len(messages) == 2

    def test_content_blocks(self):
        conv = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Part A"},
                        {"type": "text", "text": "Part B"},
                    ],
                }
            ]
        }
        messages = _extract_messages_from_conversation(conv)
        assert "Part A" in messages[0]["content"]

    def test_empty_messages(self):
        conv = {"messages": []}
        messages = _extract_messages_from_conversation(conv)
        assert messages == []


class TestCursorChatdataFormat:
    def test_list_of_conversations(self):
        data = [
            {
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi"},
                ]
            }
        ]
        sessions = _parse_chatdata_format(data, "test-project", Path("/tmp/test"))
        assert len(sessions) == 1
        assert len(sessions[0]["messages"]) == 2

    def test_dict_with_tabs(self):
        data = {
            "tabs": [
                {
                    "messages": [
                        {"role": "user", "content": "Test"},
                    ]
                }
            ]
        }
        sessions = _parse_chatdata_format(data, "project", Path("/tmp/test"))
        assert len(sessions) == 1


class TestCursorInferProject:
    def test_with_workspace_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace_json = Path(tmpdir) / "workspace.json"
            workspace_json.write_text(json.dumps({"folder": "file:///home/user/my-project"}))

            state_file = Path(tmpdir) / "state.vscdb"
            project = cursor_infer_project(state_file)
            assert project == "my-project"

    def test_fallback_to_dirname(self):
        path = Path("/tmp/abc123hash/state.vscdb")
        project = cursor_infer_project(path)
        assert project == "abc123hash"
