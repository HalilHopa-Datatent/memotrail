"""Tests for extractors module — summarization and decision extraction."""

from memotrail.extractors.summarizer import summarize_session
from memotrail.extractors.decisions import extract_decisions


class TestSummarizer:
    def test_empty_messages(self):
        assert summarize_session([]) is None

    def test_single_message(self):
        assert summarize_session([{"role": "user", "content": "hi"}]) is None

    def test_basic_summary(self):
        messages = [
            {"role": "user", "content": "Fix the login bug in auth.py"},
            {"role": "assistant", "content": "I fixed the authentication issue in auth.py."},
        ]
        summary = summarize_session(messages)
        assert summary is not None
        assert "login" in summary.lower() or "auth" in summary.lower()

    def test_summary_extracts_files(self):
        messages = [
            {"role": "user", "content": "Update the config.yaml file"},
            {"role": "assistant", "content": "I updated config.yaml with the new settings."},
        ]
        summary = summarize_session(messages)
        assert summary is not None
        assert "config.yaml" in summary

    def test_summary_length_cap(self):
        messages = [
            {"role": "user", "content": "x " * 200},
            {"role": "assistant", "content": "y " * 200},
        ]
        summary = summarize_session(messages)
        assert summary is not None
        assert len(summary) <= 305  # 300 + "..." buffer

    def test_summary_with_actions(self):
        messages = [
            {"role": "user", "content": "Help me refactor the API"},
            {"role": "assistant", "content": "I refactored the endpoint handlers into separate modules."},
        ]
        summary = summarize_session(messages)
        assert summary is not None


class TestDecisionExtractor:
    def test_no_decisions(self):
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        decisions = extract_decisions(messages)
        assert decisions == []

    def test_explicit_decision(self):
        messages = [
            {"role": "user", "content": "Which database should we use?"},
            {"role": "assistant", "content": "Let's use PostgreSQL for the main database because it supports JSON."},
        ]
        decisions = extract_decisions(messages)
        assert len(decisions) >= 1
        assert any("PostgreSQL" in d.decision_text for d in decisions)

    def test_technology_switch(self):
        messages = [
            {"role": "user", "content": "We need better caching"},
            {"role": "assistant", "content": "I switched to Redis for caching instead of memcached."},
        ]
        decisions = extract_decisions(messages)
        assert len(decisions) >= 1

    def test_decision_category(self):
        messages = [
            {"role": "user", "content": "How should we structure this?"},
            {"role": "assistant", "content": "Let's use the repository pattern for data access."},
        ]
        decisions = extract_decisions(messages)
        assert len(decisions) >= 1
        assert decisions[0].category in ("architecture", "approach", "general")

    def test_decision_has_context(self):
        messages = [
            {"role": "user", "content": "What framework to use?"},
            {"role": "assistant", "content": "We decided to use FastAPI for the backend."},
        ]
        decisions = extract_decisions(messages)
        assert len(decisions) >= 1
        assert decisions[0].context is not None
        assert len(decisions[0].context) > 0

    def test_deduplication(self):
        messages = [
            {"role": "assistant", "content": "Let's use React. Let's use React for the frontend."},
        ]
        decisions = extract_decisions(messages)
        # Should not have duplicate "use React" entries
        texts = [d.decision_text.lower() for d in decisions]
        assert len(texts) == len(set(texts))

    def test_cap_at_ten(self):
        messages = [
            {"role": "assistant", "content": " ".join(
                [f"We decided to use tool{i} for feature{i}." for i in range(20)]
            )},
        ]
        decisions = extract_decisions(messages)
        assert len(decisions) <= 10
