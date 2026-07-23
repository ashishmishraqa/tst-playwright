"""
Central logging utilities for the test framework.

This module configures a single run-scoped logger and enriches every record
with test context so CI logs can be correlated with failures, screenshots,
and traces.
"""

import json
import logging
import os
from contextvars import ContextVar
from datetime import datetime, timezone
from pathlib import Path

_logging_configured = False
_log_context: ContextVar[dict[str, str]] = ContextVar("log_context", default={})


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        """Serialize each log record as structured JSON.

        The base record fields are normalized and then augmented with any
        active test context plus custom extras passed through ``logger.*`` calls.
        """
        payload = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process": record.process,
            "thread": record.threadName,
        }

        # Context is injected by pytest hooks so every line can be tied back to
        # a specific run, test, worker, and browser without manual repetition.
        context = _log_context.get()
        if context:
            payload.update(context)

        # Preserve ad hoc structured fields supplied via ``extra={...}``.
        standard_fields = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
        }
        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in standard_fields
        }
        if extras:
            payload.update(extras)

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str, ensure_ascii=True)


def set_log_context(**kwargs) -> None:
    """Merge the provided fields into the current log context."""
    current = dict(_log_context.get())
    for key, value in kwargs.items():
        if value is not None:
            current[key] = str(value)
    _log_context.set(current)


def clear_log_context() -> None:
    """Reset per-test context after a test finishes."""
    _log_context.set({})


def configure_logging(
    run_id: str | None = None, log_dir: str | Path | None = None
) -> Path:
    """Configure root logging once for the current pytest run.

    A run-specific directory keeps logs grouped together, which makes CI
    triage easier when multiple runs or retries are collected on the same host.
    """
    global _logging_configured
    if _logging_configured:
        return Path(getattr(configure_logging, "log_file", ""))

    base_dir = (
        Path(log_dir) if log_dir else Path(__file__).resolve().parent.parent / "logs"
    )
    run_id = run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = base_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_file = run_dir / "pytest.log"

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(console_handler)

    logging.captureWarnings(True)
    _logging_configured = True
    configure_logging.log_file = log_file  # type: ignore[attr-defined]
    os.environ["TEST_LOG_FILE"] = str(log_file)
    os.environ["TEST_RUN_ID"] = run_id
    return log_file


def get_logger(name: str) -> logging.Logger:
    """Return a named logger that inherits the global JSON configuration."""
    return logging.getLogger(name)
