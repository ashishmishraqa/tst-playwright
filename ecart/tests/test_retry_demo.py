import pytest
import random
from playwright.sync_api import expect


@pytest.mark.smoke
def test_retry_demo(page):
    """
    Demo test that shows retry functionality.
    This test has a 70% chance of failing on first run,
    but will eventually pass on retry.
    """
    # Simulate flaky behavior - 70% chance of failure
    if random.random() < 0.7:
        # Force a failure to demonstrate retry
        assert False, "Simulated flaky failure - this should retry"

    # If we get here, test passes
    page.goto("https://naveenautomationlabs.com/opencart/")
    expect(page).to_have_title("Your Store")
