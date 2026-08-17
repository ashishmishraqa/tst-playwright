from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from ecart.utilities.secret_manager import SecretsManager
from ecart.utilities.logger import set_log_context, get_logger

log = get_logger(__name__)

def pytest_addoption(parser):
    """Register custom CLI flags used by the Playwright test suite."""
    parser.addoption(
        "--app-browser",
        action="store",
        default="chromium",
        choices=["firefox", "chromium", "edge"],
    )
    parser.addoption(
        "--enable-trace",
        action="store_true",
        default=False,
        help="Enable Playwright trace collection",
    )


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--app-browser")
    worker = (
        request.config.workerinput["workerid"]
        if hasattr(request.config, "workerinput")
        else "master"
    )
    set_log_context(worker_id=worker, browser=browser_name)

    with sync_playwright() as p:
        log.info(f"Launching {browser_name} browser")
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope='session')
def credentials():
    """Return a secret-backed test user payload for auth scenarios."""
    return SecretsManager().get_secret()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Capture failures after the test call phase and attach diagnostics."""
    outcome = yield              # hook pauses here and test executes
    # now capture the test results
    report = outcome.get_result()
    if report.when != "call":
        return

    if report.failed and "page" in item.funcargs:

        page = item.funcargs["page"]
        # Save a screenshot next to the other run artifacts so failure triage
        # has visual evidence without needing a rerun.
        artifact_dir = (
            Path(__file__).resolve().parent.parent.parent / "reports" / "screenshots"
        )
        artifact_dir.mkdir(parents=True, exist_ok=True)
        file_name = item.nodeid.replace("/", "_").replace("::", "__").replace(" ", "_")
        screenshot_path = artifact_dir / f"{file_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)
        log.error(
            "Test failed",
            extra={
                "screenshot": str(screenshot_path),
                "outcome": report.outcome,
            },
        )

    if report.failed:
        set_log_context(test_outcome="failed")
    elif report.passed:
        set_log_context(test_outcome="passed")
