"""End-to-end demo of the self-healing locator agent.

These tests render a minimal login form via ``set_content`` (no network) and
drive it through ``BasePage`` so the whole path is exercised: a broken selector
raises a Playwright timeout, ``heal_locator`` runs the LangGraph agent, the
stub proposer suggests a working selector from the live DOM, and the click is
retried successfully.

Skipped automatically if ``langgraph`` is not installed.
"""

import pytest

pytest.importorskip("langgraph", reason="self-healing requires langgraph")

from pages.base_page import BasePage  # noqa: E402  (after importorskip)
from self_healing import heal_locator  # noqa: E402

# A tiny OpenCart-like login form. The real email field id is `input-email`.
LOGIN_FORM_HTML = """
<!doctype html><html><body>
  <form>
    <input id="input-email" name="email" type="text" placeholder="E-Mail Address"/>
    <input id="input-password" name="password" type="password"/>
    <input type="submit" value="Login"/>
  </form>
</body></html>
"""


@pytest.fixture
def login_form(page):
    """Render the static login form on the shared page."""
    page.set_content(LOGIN_FORM_HTML)
    return page


def test_heal_locator_suggests_working_selector(login_form):
    """The agent recovers the email field from a stale id."""
    healed = heal_locator(
        login_form, action="click", failed_selector="#input-email-OLD"
    )
    assert healed is not None, "expected a healed selector"
    assert login_form.locator(healed).count() == 1


def test_basepage_click_self_heals(login_form):
    """A broken selector passed to BasePage.click is healed and the click retried."""
    base = BasePage(login_form)

    # `#input-email-OLD` no longer exists; without healing this would time out.
    base.click_on("#input-email-OLD")

    # If the click landed, the email input is now the focused element.
    focused_id = login_form.evaluate("() => document.activeElement.id")
    assert focused_id == "input-email"


def test_unhealable_selector_still_raises(login_form):
    """Garbage with no DOM overlap must not be silently 'healed'."""
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

    base = BasePage(login_form)
    with pytest.raises(PlaywrightTimeoutError):
        base.click_on("#totally-nonexistent-zzz")