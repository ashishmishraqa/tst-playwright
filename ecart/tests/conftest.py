import json
import pytest
from playwright.sync_api import sync_playwright
from utilities.logger import get_logger
import pathlib


log = get_logger(__name__)

def pytest_addoption(parser):
    parser.addoption("--app-browser", action="store", default="chromium", choices=["firefox", "chromium", "edge"])
    parser.addoption("--enable-trace", action="store_true", default=False, help="Enable Playwright trace collection")

@pytest.fixture(scope="session")
def worker_id(request):
    """Get worker ID for parallel execution."""
    if hasattr(request.config, 'workerinput'):
        return request.config.workerinput['workerid']
    return "master"



@pytest.fixture()
def page(request):
    browser_name = request.config.getoption("--app-browser")
    enable_trace = request.config.getoption("--enable-trace")

    with sync_playwright() as p:
        log.info(f"Launching {browser_name} browser")
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True)
        context = browser.new_context()

        # Enable tracing if requested
        if enable_trace:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            log.info("Playwright tracing enabled")

        page = context.new_page()
        yield page  # return the page object all the test will be executed

        # Stop tracing and save if enabled
        if enable_trace:
            # Save trace with timestamp to avoid conflicts
            import time
            trace_path = f"traces/trace_{int(time.time())}.zip"
            context.tracing.stop(path=trace_path)
            log.info(f"Trace saved to: {trace_path}")

        # Cleanup
        page.close()
        context.close()
        browser.close()


@pytest.fixture()
def fetch_test_data():
    data_path = pathlib.Path(__file__).parent.parent / 'test_data' / 'credentials.json'
    with open(data_path) as f:
        test_data = json.load(f)
        # self.log.info('test data has been fetched')
        return test_data['user_credentials']
