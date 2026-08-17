from pathlib import Path
import pytest
from self_healing.nodes import log
from utilities.api_utils import APIUtils

AUTH_FILE = Path("playwright/.auth/user.json")


"""create the authentication"""
@pytest.fixture(scope="session")
def auth_state(browser, credentials):
    AUTH_FILE.parent.mkdir(parents=True, exist_ok=True)

    context = browser.new_context()

    try:
        api_utils = APIUtils()
        api_utils.login_via_api(context, credentials)

        #persist the authentication state to a file
        context.storage_state(path=AUTH_FILE)
        log.info('Authentication is stored')

    except Exception as e:
        log.error(f"Error during authentication: {e}")
    finally:
        context.close()
    return AUTH_FILE


@pytest.fixture(scope="function")
def authenticated_page(browser, auth_state):
    # creating a brand-new context with the authentication state
    context = browser.new_context(storage_state = auth_state)

    page = context.new_page()

    yield page

    context.close()


