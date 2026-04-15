"""
base_page.py — Base Page Object
Every page class inherits from this. Contains shared wait strategies,
smart locator helpers, soft assertions, and automatic failure artifacts.
"""

from playwright.sync_api import Page, Locator
from utilities.logger import get_logger



class BasePage:
    """
        Foundation for all Page Objects.

        Design decisions:
        - All waits are explicit (no time.sleep anywhere in the framework).
        - Locators are lazy — resolved only when interacted with.
        - Failures auto-capture screenshot + trace for Allure attachment.
        - Soft assertion collector lets a single test report multiple failures.
        """
    # Default timeouts (override per-page if the app needs it)
    DEFAULT_TIMEOUT = 10_000  # ms — element visibility / clickability
    NAVIGATION_TIMEOUT = 30_000  # ms — full page load
    ANIMATION_TIMEOUT = 3_000  # ms — CSS transitions / loaders

    log = get_logger(__name__)

    def __init__(self, page: Page):
        self.page = page
        # gets the name of the class (here, "BasePage" or the child class name when inherited).


    # ---------------------------
    # Navigation
    # ---------------------------
    def go_to(self, url: str):
        self.log.info(f"Navigating to URL: {url}")
        self.page.goto(url,timeout=self.NAVIGATION_TIMEOUT, wait_until='networkidle')

    def reload(self) -> None:
        self.page.reload(wait_until="networkidle", timeout=self.NAVIGATION_TIMEOUT)

    def get_current_url(self) -> str:
        return self.page.url


    # ---------------------------
    # Click wrapper
    # ---------------------------
    def click(self, locator: str | Locator):
        resolved_locator = self.page.locator(locator) if isinstance(locator, str) else locator
        resolved_locator.wait_for(timeout=self.DEFAULT_TIMEOUT, state="visible")
        resolved_locator.click()
        self.log.debug(f"Clicked on: {locator}")



    # ---------------------------
    # Type wrapper
    # ---------------------------
    def type(self, locator: str, value: str, clear=True):
        if clear:
            self.log.info(f"Clearing + typing '{value}' into: {locator}")
            self.page.locator(locator).fill(value)
        else:
            self.log.info(f"Typing '{value}' into: {locator}")
            self.page.locator(locator).type(value)

    # ---------------------------
    # Read text
    # ---------------------------
    def get_text(self, locator: str) -> str:
        self.log.info(f"Getting text from: {locator}")
        return self.page.locator(locator).text_content()

    # ---------------------------
    # Waits
    # ---------------------------
    def wait_for_visible(self, locator: str | Locator):
        self.log.info(f"Waiting for: {locator} to be visible")
        return self.page.locator(locator).wait_for(state="visible")

    def wait_for_clickable(self, locator: str):
        self.log.info(f"Waiting for element to be clickable: {locator}")
        self.page.locator(locator).wait_for(state="visible")

    # ---------------------------
    # Page Title
    # ---------------------------
    def get_title(self):
        return self.page.title()
