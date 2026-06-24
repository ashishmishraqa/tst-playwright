"""Graph nodes for the self-healing agent.

Each node is a plain function ``HealState -> dict`` that returns only the
state keys it changed. Keeping nodes free of LangGraph types makes them
trivial to unit-test in isolation.
"""

from __future__ import annotations

from typing import Any

from self_healing.providers import get_proposer
from self_healing.state import HealState
from utilities.logger import get_logger

log = get_logger(__name__)

# JS that summarizes interactive elements currently in the DOM. Kept small and
# capped so the payload handed to a proposer stays bounded.
_DOM_PROBE = """
() => Array.from(
  document.querySelectorAll('input,button,a,select,textarea,[role]')
).slice(0, 200).map(e => ({
  tag: e.tagName.toLowerCase(),
  id: e.id || null,
  name: e.getAttribute('name'),
  type: e.getAttribute('type'),
  placeholder: e.getAttribute('placeholder'),
  role: e.getAttribute('role'),
  text: (e.innerText || e.value || '').trim().slice(0, 40) || null,
}))
"""


def capture_context(state: HealState) -> dict[str, Any]:
    """Snapshot interactive DOM elements from the live page."""
    page = state["page"]
    try:
        elements = page.evaluate(_DOM_PROBE)
    except Exception as exc:  # pragma: no cover - defensive; DOM probe is best-effort
        log.warning("DOM capture failed during healing: %s", exc)
        elements = []
    note = f"captured {len(elements)} interactive elements"
    return {"elements": elements, "notes": [*state.get("notes", []), note]}


def propose_candidates(state: HealState) -> dict[str, Any]:
    """Ask the configured proposer for alternative selectors."""
    proposer = get_proposer()
    candidates = proposer.propose(
        action=state["action"],
        failed_selector=state["failed_selector"],
        elements=state.get("elements", []),
        max_candidates=state.get("max_candidates", 5),
    )
    # Drop anything already tried in a previous round.
    tried = set(state.get("tried", []))
    candidates = [c for c in candidates if c not in tried]
    note = f"round {state.get('round', 1)}: proposed {candidates}"
    return {"candidates": candidates, "notes": [*state.get("notes", []), note]}


def validate_candidates(state: HealState) -> dict[str, Any]:
    """Try each candidate against the page; accept the first that resolves cleanly.

    "Clean" means exactly one match that is visible — this avoids healing onto
    an ambiguous selector that would flake later.
    """
    page = state["page"]
    tried = list(state.get("tried", []))
    validated: str | None = None

    for selector in state.get("candidates", []):
        tried.append(selector)
        try:
            locator = page.locator(selector)
            if locator.count() == 1 and locator.first.is_visible():
                validated = selector
                break
        except Exception as exc:  # pragma: no cover - invalid selector candidates
            log.debug("candidate %s rejected: %s", selector, exc)

    note = (
        f"validated -> {validated}" if validated else "no candidate validated this round"
    )
    return {
        "validated_selector": validated,
        "tried": tried,
        "round": state.get("round", 1) + 1,
        "notes": [*state.get("notes", []), note],
    }


def report(state: HealState) -> dict[str, Any]:
    """Emit the outcome. Suggest-only: we log the fix, we do not edit source."""
    old = state["failed_selector"]
    new = state.get("validated_selector")
    if new:
        log.warning(
            "SELF-HEAL suggestion: replace %r with %r (action=%s)",
            old,
            new,
            state["action"],
            extra={
                "heal_old_selector": old,
                "heal_new_selector": new,
                "heal_action": state["action"],
                "heal_audit": state.get("notes", []),
            },
        )
    else:
        log.error(
            "SELF-HEAL failed for %r (action=%s) after %s round(s)",
            old,
            state["action"],
            state.get("round", 1) - 1,
            extra={"heal_audit": state.get("notes", [])},
        )
    return {}


def should_retry(state: HealState) -> str:
    """Conditional edge: loop for another round, or stop and report."""
    if state.get("validated_selector"):
        return "report"
    if state.get("round", 1) > state.get("max_rounds", 2):
        return "report"
    if not state.get("candidates"):
        # Proposer is out of fresh ideas; no point looping.
        return "report"
    return "retry"
