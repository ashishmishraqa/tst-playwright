"""
Pytest configuration and framework-wide fixtures.

This file is responsible for run-level logging setup, test-context enrichment,
and browser/tracing lifecycle management for Playwright tests.
"""

import json
import os
import pathlib
from datetime import datetime, timezone
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from utilities.user_factory import UserFactory
from ecart.configs.settings import TestData
from ecart.pages.auth.home_page import HomePage
from ecart.pages.auth.login_page import LoginPage
from ecart.utilities.logger import (
    clear_log_context,
    configure_logging,
    get_logger,
    set_log_context,
)
from ecart.utilities.secret_manager import SecretsManager

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


def pytest_configure(config):
    """Create a single run id in the controller process and reuse it everywhere."""
    if not hasattr(config, "workerinput"):
        run_id = os.environ.get("TEST_RUN_ID") or datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%SZ"
        )
        config._run_id = run_id
        os.environ["TEST_RUN_ID"] = run_id


def pytest_configure_node(node):
    """Propagate the controller run id to xdist workers."""
    node.workerinput["run_id"] = getattr(node.config, "_run_id", None)


def pytest_sessionstart(session):
    """Initialize logging once before the first test starts."""
    run_id = getattr(session.config, "_run_id", None)
    if hasattr(session.config, "workerinput"):
        run_id = session.config.workerinput.get("run_id", run_id)
    configure_logging(run_id=run_id)
    set_log_context(session_id="pytest")


def pytest_runtest_setup(item):
    """Attach test identity and execution metadata before each test body runs."""
    worker_id = getattr(item.config, "workerinput", {}).get("workerid", "master")
    browser_name = item.config.getoption("--app-browser")
    set_log_context(worker_id=worker_id, browser=browser_name, nodeid=item.nodeid)


def pytest_runtest_call(item):
    """Mark the log context as being inside the test call phase."""
    set_log_context(phase="call")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture failures after the test call phase and attach diagnostics."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    if report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        # Save a screenshot next to the other run artifacts so failure triage
        # has visual evidence without needing a rerun.
        artifact_dir = (
            Path(__file__).resolve().parent.parent / "reports" / "screenshots"
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


def pytest_runtest_teardown(item, nextitem):
    """Clear per-test context so the next test starts from a clean slate."""
    clear_log_context()


@pytest.fixture(scope="function")
def page(request):
    """Provide one Playwright page for a function and manage browser lifecycle."""
    browser_name = request.config.getoption("--app-browser")
    enable_trace = request.config.getoption("--enable-trace")
    worker = (
        request.config.workerinput["workerid"]
        if hasattr(request.config, "workerinput")
        else "master"
    )
    set_log_context(worker_id=worker, browser=browser_name)

    with sync_playwright() as p:
        log.info(f"Launching {browser_name} browser")
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False)
        context = browser.new_context()

        # Tracing is opt-in so normal runs stay fast and lightweight.
        if enable_trace:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            log.info("Playwright tracing enabled")

        page = context.new_page()
        yield page

        # Persist a trace only when requested to avoid unnecessary I/O.
        if enable_trace:
            import time

            trace_dir = Path(__file__).resolve().parent.parent / "traces"
            trace_dir.mkdir(parents=True, exist_ok=True)
            trace_path = trace_dir / f"trace_{int(time.time())}.zip"
            context.tracing.stop(path=trace_path)
            log.info(f"Trace saved to: {trace_path}")

        # Explicit cleanup keeps browser resources stable across repeated runs.
        page.close()
        context.close()
        browser.close()


@pytest.fixture()
def fetch_test_data():
    """Load test credentials from the local JSON data file."""
    data_path = (
        pathlib.Path(__file__).resolve().parent.parent.parent
        / "test_data"
        / "credentials.json"
    )
    with open(data_path) as f:
        test_data = json.load(f)
        return test_data["user_credentials"]


@pytest.fixture
def credentials():
    """Return a secret-backed test user payload for auth scenarios."""
    return SecretsManager().get_secret("valid_user")


@pytest.fixture()
def home_page(page):
    """Fixture to ensure we are on the home page before starting."""
    home = HomePage(page)
    home.navigate_to_home(TestData.BASE_URL)
    yield home


@pytest.fixture()
def login_page(page):
    """Fixture to ensure we are on the login page before starting."""
    login = LoginPage(page)
    login.navigate_to_login_page(TestData.LOGIN_PAGE)
    yield login


@pytest.fixture()
def user_factory():
    """invoke the data factory to create a user registration"""
    return UserFactory()


@pytest.fixture()
def valid_registration_user(user_factory):
    return user_factory.valid_registration_user()
