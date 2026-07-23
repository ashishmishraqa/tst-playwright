"""Pluggable locator proposers.

The agent is deliberately provider-agnostic. A *proposer* takes the failed
selector plus a summary of the live DOM and returns ranked candidate
selectors. The default :class:`StubProposer` is fully offline and requires no
API key, so the graph runs out of the box. Swap in an LLM-backed proposer
later by implementing the same ``propose`` signature and updating
:func:`get_proposer`.
"""

from __future__ import annotations

import os
import re
from typing import Any, Protocol

from utilities.logger import get_logger

log = get_logger(__name__)


class LocatorProposer(Protocol):
    """Interface every proposer must satisfy."""

    def propose(
        self,
        action: str,
        failed_selector: str,
        elements: list[dict[str, Any]],
        max_candidates: int,
    ) -> list[str]:
        """Return up to ``max_candidates`` alternative selectors, best first."""
        ...


def _tokens(value: str | None) -> set[str]:
    """Split a selector or attribute into lowercase alphanumeric tokens."""
    if not value:
        return set()
    return {t for t in re.split(r"[^a-z0-9]+", value.lower()) if t}


def _candidate_selectors(el: dict[str, Any]) -> list[str]:
    """Generate plausible Playwright selectors for a single DOM element.

    Ordered most-specific to least so stable attributes win when scores tie.
    """
    tag = el.get("tag") or "*"
    selectors: list[str] = []

    if el.get("id"):
        selectors.append(f"#{el['id']}")
    if el.get("name"):
        selectors.append(f'{tag}[name="{el["name"]}"]')
    if el.get("type") and el.get("name"):
        selectors.append(f'{tag}[type="{el["type"]}"][name="{el["name"]}"]')
    if el.get("placeholder"):
        selectors.append(f'{tag}[placeholder="{el["placeholder"]}"]')
    if el.get("type"):
        selectors.append(f'{tag}[type="{el["type"]}"]')
    return selectors


class StubProposer:
    """Heuristic, offline proposer.

    Ranks DOM elements by how well their identifying attributes overlap with
    the tokens of the failed selector, then emits candidate selectors for the
    top matches. No network, no model — deterministic and CI-safe.
    """

    def propose(
        self,
        action: str,
        failed_selector: str,
        elements: list[dict[str, Any]],
        max_candidates: int,
    ) -> list[str]:
        wanted = _tokens(failed_selector)

        scored: list[tuple[int, dict[str, Any]]] = []
        for el in elements:
            haystack: set[str] = set()
            for key in ("id", "name", "type", "placeholder", "role", "text"):
                haystack |= _tokens(el.get(key))
            score = len(wanted & haystack)
            if score:
                scored.append((score, el))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        candidates: list[str] = []
        for _score, el in scored:
            for selector in _candidate_selectors(el):
                if selector not in candidates and selector != failed_selector:
                    candidates.append(selector)
                if len(candidates) >= max_candidates:
                    return candidates
        return candidates


def get_proposer() -> LocatorProposer:
    """Return the configured proposer.

    Controlled by the ``HEAL_PROVIDER`` env var. Only ``"stub"`` ships today;
    real providers (anthropic / openai / bedrock) are intended to slot in here
    behind the same interface without touching the graph.
    """
    provider = os.getenv("HEAL_PROVIDER", "stub").lower()
    if provider != "stub":
        log.warning(
            "HEAL_PROVIDER=%s is not implemented yet; falling back to stub", provider
        )
    return StubProposer()
