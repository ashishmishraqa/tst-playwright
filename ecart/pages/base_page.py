"""Shared Playwright page-object helpers.

The base page provides reusable mechanics only. It intentionally avoids
step-level logging so higher-level page objects can describe user actions in a
clean, readable way.
"""

from playwright.sync_api import Locator, Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from self_healing import heal_locator
from utilities.logger import get_logger


class BasePage:
    """Foundation for all page objects."""

    # Centralized defaults keep timing behavior consistent across pages.
    DEFAULT_TIMEOUT = 10_000
    NAVIGATION_TIMEOUT = 30_000
    ANIMATION_TIMEOUT = 3_000
    ELEMENT_TIMEOUT = 10_000
    VERIFY_TIMEOUT = 5_000

    log = get_logger(__name__)

    def __init__(self, page: Page):
        self.page = page


    """
    To resolve the resolve type if it is a string or Locator
    args: locator received the page classes
    returns: Locator
    """
    def _resolve_locator(self, locator: str | Locator) -> Locator:
        return (
            locator
            if isinstance(locator, Locator)
            else self.page.locator(locator)
        )

    def go_to(self, url: str):
        try:
            self.page.goto(url, timeout=self.NAVIGATION_TIMEOUT, wait_until='domcontentloaded')
        except PlaywrightTimeoutError:
            self.log.exception(f"Timeout while trying to navigate to %s {url}")
            raise


    def click_on(self, locator: str | Locator):
        target = self._resolve_locator(locator)
        expect(target).to_be_visible()
        try:
            target.click()
        except PlaywrightTimeoutError:
            # Self-healing only applies when we have the raw selector string;
            # a pre-built Locator carries no recoverable selector text.
            if not isinstance(locator, str):
                raise
            healed = heal_locator(self.page, action="click", failed_selector=locator)
            if not healed:
                raise
            self.log.warning("Self-heal: retrying click with %r (was %r)", healed, locator)
            healed_locator = self.page.locator(healed)
            healed_locator.wait_for(timeout=self.DEFAULT_TIMEOUT, state="visible")
            healed_locator.click()

    def get_title(self):
        try:
            return self.page.title()
        except PlaywrightTimeoutError:
            self.log.exception("Timeout while trying to get the page title.")
            raise

    def enter_text(self, locator: Locator, value: str):
        target = self._resolve_locator(locator)
        expect(target).to_be_visible()
        expect(target).to_be_editable()
        try:
            target.fill(value, timeout=self.DEFAULT_TIMEOUT)
        except PlaywrightTimeoutError:
            self.log.exception("Timeout while trying to fill the input field.")
            raise
        expect(target).to_have_value(value, timeout=5_000)
