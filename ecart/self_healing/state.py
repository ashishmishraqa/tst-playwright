"""Shared state schema for the self-healing graph.

LangGraph passes a single mutable state object between nodes. We model it as a
``TypedDict`` so each node can read the fields it needs and return only the
keys it updates.
"""

from __future__ import annotations

from typing import Any, TypedDict


class HealState(TypedDict, total=False):
    """State threaded through the self-healing graph.

    Inputs (set by the caller before invoking the graph):
        page:            Live Playwright ``Page`` used for DOM capture + validation.
        action:          The action that failed, e.g. ``"click"`` or ``"type"``.
        failed_selector: The selector string that no longer resolves.
        max_candidates:  Upper bound on selectors the proposer should return.
        max_rounds:      How many propose/validate cycles to attempt.

    Working fields (populated by nodes during the run):
        elements:           Structured summary of interactive DOM elements.
        candidates:         Ranked alternative selectors proposed this round.
        tried:              Selectors already validated (avoids re-checking).
        validated_selector: First candidate that resolves to exactly one
                            visible element, or ``None`` if healing failed.
        round:              Current propose/validate cycle (1-indexed).
        notes:              Human-readable audit trail of what the agent did.
    """

    page: Any
    action: str
    failed_selector: str
    max_candidates: int
    max_rounds: int

    elements: list[dict[str, Any]]
    candidates: list[str]
    tried: list[str]
    validated_selector: str | None
    round: int
    notes: list[str]