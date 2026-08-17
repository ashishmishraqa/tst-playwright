"""
Pytest configuration and framework-wide fixtures.

This file is responsible for run-level logging setup, test-context enrichment,
and browser/tracing lifecycle management for Playwright tests.
"""

import json
import pathlib
from pathlib import Path

import pytest
from ecart.configs.settings import TestData
from ecart.pages.auth.home_page import HomePage
from ecart.pages.auth.login_page import LoginPage
from ecart.utilities.logger import get_logger
from ecart.utilities.user_factory import UserFactory

log = get_logger(__name__)


# def pytest_configure(config):
#     """Create a single run id in the controller process and reuse it everywhere."""
#     if not hasattr(config, "workerinput"):
#         run_id = os.environ.get("TEST_RUN_ID") or datetime.now(timezone.utc).strftime(
#             "%Y%m%dT%H%M%SZ"
#         )
#         config._run_id = run_id
#         os.environ["TEST_RUN_ID"] = run_id
#
#
# def pytest_configure_node(node):
#     """Propagate the controller run id to xdist workers."""
#     node.workerinput["run_id"] = getattr(node.config, "_run_id", None)
#
#
# def pytest_sessionstart(session):
#     """Initialize logging once before the first test starts."""
#     run_id = getattr(session.config, "_run_id", None)
#     if hasattr(session.config, "workerinput"):
#         run_id = session.config.workerinput.get("run_id", run_id)
#     configure_logging(run_id=run_id)
#     set_log_context(session_id="pytest")
#
#
# def pytest_runtest_setup(item):
#     """Attach test identity and execution metadata before each test body runs."""
#     worker_id = getattr(item.config, "workerinput", {}).get("workerid", "master")
#     browser_name = item.config.getoption("--app-browser")
#     set_log_context(worker_id=worker_id, browser=browser_name, nodeid=item.nodeid)
#
#
# def pytest_runtest_call():
#     """Mark the log context as being inside the test call phase."""
#     set_log_context(phase="call")


# def pytest_runtest_teardown():
#     """Clear per-test context so the next test starts from a clean slate."""
#     clear_log_context()


@pytest.fixture(scope="function")
def page(browser, request):
    """Provide one Playwright page for a function and manage browser lifecycle."""
    # browser_name = request.config.getoption("--app-browser")
    enable_trace = request.config.getoption("--enable-trace")
    # worker = (
    #     request.config.workerinput["workerid"]
    #     if hasattr(request.config, "workerinput")
    #     else "master"
    # )
    # set_log_context(worker_id=worker, browser=browser_name)
    #
    # with sync_playwright() as p:
    #     log.info(f"Launching {browser_name} browser")
    #     browser_type = getattr(p, browser_name)
    #     browser = browser_type.launch(headless=True)
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
