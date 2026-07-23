"""LangGraph wiring for the self-healing agent.

Topology::

    START -> capture_context -> propose_candidates -> validate_candidates
                                       ^                       |
                                       |   (retry: no match,   |
                                       +----- rounds left) ----+
                                                               |
                                                  (report) --> report -> END

The cycle is what makes this a graph rather than a straight function: if a
round of candidates fails validation, the agent re-proposes (a real LLM
proposer can use the previous round's misses to broaden its next guess) until
it heals or exhausts ``max_rounds``.
"""

from __future__ import annotations

from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from self_healing.nodes import (capture_context, propose_candidates, report,
                                should_retry, validate_candidates)
from self_healing.state import HealState


def build_heal_graph():
    """Construct and compile the self-healing state graph."""
    builder = StateGraph(HealState)

    builder.add_node("capture_context", capture_context)
    builder.add_node("propose_candidates", propose_candidates)
    builder.add_node("validate_candidates", validate_candidates)
    builder.add_node("report", report)

    builder.add_edge(START, "capture_context")
    builder.add_edge("capture_context", "propose_candidates")
    builder.add_edge("propose_candidates", "validate_candidates")
    builder.add_conditional_edges(
        "validate_candidates",
        should_retry,
        {"retry": "propose_candidates", "report": "report"},
    )
    builder.add_edge("report", END)

    return builder.compile()


@lru_cache(maxsize=1)
def get_heal_graph():
    """Return a process-wide compiled graph (compilation is not free)."""
    return build_heal_graph()
