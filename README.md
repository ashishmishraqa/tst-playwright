# tst-playwright

Playwright-based test automation for the OpenCart demo app at `naveenautomationlabs.com/opencart`, with additional API and AWS-mock coverage.

## What's in this repo

- UI tests built with Playwright and pytest
- Page Object Model under `ecart/pages`
- Shared fixtures and browser setup under `ecart/tests`
- API tests for Go Rest under `ecart/tests/api_tests`
- Moto-backed AWS Lambda tests under `ecart/tests/mock_aws`
- HTML and Allure reporting
- Parallel execution support via `pytest-xdist`

## Repository Layout

```text
README.md
pyproject.toml
requirements.txt
run_test.sh
setup_venv.sh
dockerfile
ecart/
  configs/
  components/
  pages/
  test_data/
  tests/
  utilities/
  logs/
  allure-results/
  traces/
```

## Requirements

- Python 3.8+
- Playwright browsers
- JavaScript browser dependencies installed through `playwright install`
- Optional: `allure` CLI for live report serving

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

On macOS/Linux or Git Bash, activate with `source .venv/bin/activate`.

The repo also includes `setup_venv.sh`, but it is written for Unix-like shells and changes into `ecart/` before creating the environment.

## Configuration

The main OpenCart URLs and test data live in `ecart/configs/config.py`.

- `TestData.BASE_URL` points to the OpenCart demo site
- `TestData.LOGIN_PAGE` and `TestData.REGISTER_PAGE_URL` are the main UI entry points
- `TestData.BASE_URL_API` is read from the environment for Go Rest API tests
- Secrets are loaded through `utilities.secret_manager.SecretsManager`

If you run the API suite, make sure `BASE_URL_API` is set in your environment.

## Running Tests

Pytest is configured in `pyproject.toml` with:

- `--html=report.html`
- `--self-contained-html`
- `--reruns=1`
- `--reruns-delay=1`

Common commands:

```bash
pytest
pytest ecart/tests/test_home.py
pytest -m smoke
pytest -m regression
pytest --app-browser chromium
pytest --app-browser firefox
pytest --app-browser edge
pytest --headed
pytest -n auto
pytest --enable-trace
```

The custom Playwright options are defined in `ecart/tests/conftest.py`.

## Test Markers

The project currently defines these markers:

- `smoke`
- `regression`
- `critical`
- `ui`

## Test Coverage

- `ecart/tests/e2e/` contains browser-flow tests for login, registration, home, and checkout
- `ecart/tests/` contains core UI tests for the OpenCart flows
- `ecart/tests/api_tests/` contains Go Rest API checks
- `ecart/tests/mock_aws/` validates a Lambda handler against Moto-mocked S3

Examples of implemented flows include:

- Home page title and navigation checks
- Login success and failure paths
- Logout
- Product search
- Cart and checkout flow
- API user creation with schema validation

## Reporting

Pytest writes a self-contained HTML report to `report.html` by default.

Allure artifacts are written to `allure-results/` when the suite is run with `--alluredir=allure-results`.

To generate a live Allure report:

```bash
allure serve allure-results
```

## Helper Script

`run_test.sh` wraps a common execution path:

```bash
./run_test.sh smoke 4 false
```

Arguments:

- marker name
- worker count
- headed mode flag

The script installs Playwright browsers, runs the selected pytest marker with `xdist`, then serves the Allure report if the run passes.

## Notes

- The repository contains generated artifacts such as `allure-results/`, `report.html`, `traces/`, and `.pytest_cache/`
- `ecart/` also contains local logs and cached outputs from prior runs
- `TestCase.md` documents broader OpenCart scenarios that are not all implemented in the current automated suite
