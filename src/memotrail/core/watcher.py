"""File watcher: monitors Claude Code session directories for new/modified files."""

import threading
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileModifiedEvent

from memotrail.utils import get_logger, config

logger = get_logger("memotrail.core.watcher")


class SessionFileHandler(FileSystemEventHandler):
    """Handles new or modified JSONL session files."""

    def __init__(self, on_new_file: callable, debounce_seconds: float = 5.0):
        super().__init__()
        self._on_new_file = on_new_file
        self._debounce = debounce_seconds
        self._pending: dict[str, float] = {}
        self._lock = threading.Lock()
        self._timer: threading.Timer | None = None

    def on_created(self, event: FileCreatedEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".jsonl"):
            self._schedule(event.src_path)

    def on_modified(self, event: FileModifiedEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".jsonl"):
            self._schedule(event.src_path)

    def _schedule(self, path: str) -> None:
        """Debounce file events — wait for writes to settle before indexing."""
        with self._lock:
            self._pending[path] = time.time()

            # Reset the debounce timer
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self._debounce, self._flush)
            self._timer.daemon = True
            self._timer.start()

    def _flush(self) -> None:
        """Process all pending files."""
        with self._lock:
            paths = list(self._pending.keys())
            self._pending.clear()

        for path in paths:
            try:
                self._on_new_file(Path(path))
            except Exception as e:
                logger.error(f"Error indexing {path}: {e}")


class SessionWatcher:
    """Watches Claude Code session directories for new files."""

    def __init__(
        self,
        index_callback: callable,
        watch_dir: Path | None = None,
        debounce_seconds: float = 5.0,
    ):
        self._watch_dir = watch_dir or config.claude_code_log_dir
        self._handler = SessionFileHandler(index_callback, debounce_seconds)
        self._observer: Observer | None = None

    def start(self) -> None:
        """Start watching for new session files."""
        if not self._watch_dir.exists():
            logger.warning(f"Watch directory does not exist: {self._watch_dir}")
            return

        self._observer = Observer()
        self._observer.schedule(self._handler, str(self._watch_dir), recursive=True)
        self._observer.daemon = True
        self._observer.start()
        logger.info(f"Watching for new sessions in {self._watch_dir}")

    def stop(self) -> None:
        """Stop the file watcher."""
        if self._observer:
            self._observer.stop()
            self._observer.join(timeout=5)
            self._observer = None
            logger.info("Session watcher stopped")

    @property
    def is_running(self) -> bool:
        return self._observer is not None and self._observer.is_alive()
