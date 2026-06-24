# Self-Healing Locator Agent

A LangGraph agent that recovers from broken Playwright locators **at runtime**.
When an action fails because a selector no longer matches, the agent inspects
the live DOM, proposes alternatives, validates them, and (in **suggest-only**
mode) logs the fix for human review. It never edits source.

## How it fits the framework

- **Trigger point:** `pages/base_page.py` → `BasePage.click()`. On a Playwright
  timeout for a *string* selector, it calls `heal_locator(...)` and retries with
  the healed selector. Pre-built `Locator` objects are skipped (no recoverable
  selector text).
- **Safety:** healing is best-effort. If `langgraph` is missing, `SELF_HEAL=0`
  is set, or the graph errors, `heal_locator` returns `None` and the test fails
  normally. Healing can never mask a real bug.

## Graph topology

```
START → capture_context → propose_candidates → validate_candidates
                                ^                      |
                                |  (retry: no match,   |
                                +---- rounds left) ----+
                                                       |
                                          (report) → report → END
```

| Node                 | Responsibility                                              |
|----------------------|-------------------------------------------------------------|
| `capture_context`    | Snapshot interactive DOM elements from the live page.       |
| `propose_candidates` | Ask the configured proposer for ranked alternative selectors.|
| `validate_candidates`| Accept the first candidate resolving to exactly one visible element. |
| `report`             | Log the suggestion (old → new) or the failure. No source edits. |

The **cycle** is the point of using a graph: a failed round re-proposes (a real
LLM can use prior misses to broaden) until it heals or hits `max_rounds`.

## Provider-agnostic by design

`providers.py` defines the `LocatorProposer` protocol. The default
`StubProposer` is **fully offline** (token-overlap heuristic, no API key) so the
agent runs in CI today. To wire a real model:

1. `pip install langchain-anthropic` (or `-openai` / `-aws`).
2. Add a class implementing `propose(action, failed_selector, elements, max_candidates)`.
3. Return it from `get_proposer()` behind the `HEAL_PROVIDER` env var.

## Configuration (env vars)

| Var             | Default | Meaning                                  |
|-----------------|---------|------------------------------------------|
| `SELF_HEAL`     | `1`     | Set `0` to disable healing entirely.     |
| `HEAL_PROVIDER` | `stub`  | Proposer to use (`stub` only, for now).  |

## Demo

`ecart/tests/e2e/test_self_healing.py` renders a static login form and drives a
broken selector through `BasePage.click()` to prove the full path offline.