"""Self-healing locator agent.

A LangGraph-based agent that attempts to recover from broken Playwright
locators at runtime. When an action fails because a selector no longer
matches, the agent inspects the live DOM, proposes alternative selectors,
validates them against the page, and (in suggest-only mode) reports the fix
for human review.

Public entry point: :func:`self_healing.healer.heal_locator`.
"""

from self_healing.healer import heal_locator

__all__ = ["heal_locator"]
