"""Tests for the session file watcher."""

import tempfile
import time
from pathlib import Path
from unittest.mock import MagicMock

from memotrail.core.watcher import SessionFileHandler, SessionWatcher


class TestSessionFileHandler:
    def test_ignores_non_jsonl(self):
        callback = MagicMock()
        handler = SessionFileHandler(callback, debounce_seconds=0.1)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/tmp/test.txt"
        handler.on_created(event)

        time.sleep(0.3)
        callback.assert_not_called()

    def test_triggers_on_jsonl(self):
        callback = MagicMock()
        handler = SessionFileHandler(callback, debounce_seconds=0.1)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/tmp/test.jsonl"
        handler.on_created(event)

        time.sleep(0.3)
        callback.assert_called_once_with(Path("/tmp/test.jsonl"))

    def test_debounce_coalesces_events(self):
        callback = MagicMock()
        handler = SessionFileHandler(callback, debounce_seconds=0.3)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/tmp/test.jsonl"

        # Fire multiple events rapidly
        handler.on_modified(event)
        handler.on_modified(event)
        handler.on_modified(event)

        time.sleep(0.6)
        # Should only call once despite multiple events
        callback.assert_called_once()

    def test_ignores_directories(self):
        callback = MagicMock()
        handler = SessionFileHandler(callback, debounce_seconds=0.1)

        event = MagicMock()
        event.is_directory = True
        event.src_path = "/tmp/sessions.jsonl"
        handler.on_created(event)

        time.sleep(0.3)
        callback.assert_not_called()


class TestSessionWatcher:
    def test_start_stop(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            watcher = SessionWatcher(
                index_callback=MagicMock(),
                watch_dir=Path(tmpdir),
            )
            watcher.start()
            assert watcher.is_running
            watcher.stop()
            assert not watcher.is_running

    def test_nonexistent_dir(self):
        watcher = SessionWatcher(
            index_callback=MagicMock(),
            watch_dir=Path("/tmp/nonexistent_watcher_dir_xyz"),
        )
        watcher.start()
        assert not watcher.is_running
