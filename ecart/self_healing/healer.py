"""Public entry point for runtime locator healing.

``heal_locator`` is the single function the test framework calls when an action
fails. It is intentionally forgiving: if LangGraph is not installed, if healing
is disabled, or if anything goes wrong inside the graph, it returns ``None`` so
the caller falls back to normal failure behaviour. Healing must never *mask* a
real bug or break a run that would otherwise just fail cleanly.
"""

from __future__ import annotations

import os
from typing import Any

from self_healing.state import HealState
from utilities.logger import get_logger

log = get_logger(__name__)


def _enabled() -> bool:
    """Healing is opt-out via ``SELF_HEAL=0``; on by default."""
    return os.getenv("SELF_HEAL", "1") not in ("0", "false", "False")


def heal_locator(
    page: Any,
    action: str,
    failed_selector: str,
    max_candidates: int = 5,
    max_rounds: int = 2,
) -> str | None:
    """Attempt to recover a working selector for ``failed_selector``.

    Args:
        page:            Live Playwright ``Page``.
        action:          The failed action (``"click"``, ``"type"``, ...).
        failed_selector: The selector that stopped resolving.
        max_candidates:  Selectors to consider per round.
        max_rounds:      Propose/validate cycles before giving up.

    Returns:
        A validated replacement selector, or ``None`` if healing is disabled,
        unavailable, or unsuccessful.
    """
    if not _enabled():
        return None

    try:
        # Imported lazily so the framework has no hard dependency on langgraph:
        # without it installed, tests simply fail normally instead of erroring
        # on import.
        from self_healing.graph import get_heal_graph
    except ImportError:
        log.warning("self-healing unavailable: langgraph not installed")
        return None

    initial: HealState = {
        "page": page,
        "action": action,
        "failed_selector": failed_selector,
        "max_candidates": max_candidates,
        "max_rounds": max_rounds,
        "round": 1,
        "tried": [],
        "notes": [],
    }

    try:
        result = get_heal_graph().invoke(initial)
    except Exception as exc:  # pragma: no cover - graph must never crash the test
        log.error("self-healing graph raised: %s", exc)
        return None

    return result.get("validated_selector")
