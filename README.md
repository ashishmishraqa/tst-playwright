# tst-playwright

End-to-end, API, and integration test automation framework for the OpenCart demo application using Python, pytest, and Playwright.

The framework covers browser workflows for the OpenCart UI, GoRest API checks, Moto-backed AWS Lambda tests, structured logging, HTML/Allure reporting, parallel execution, retry support, and an experimental self-healing locator layer.

## Tech Stack

| Area | Tools |
| --- | --- |
| Language | Python |
| Browser automation | Playwright, pytest-playwright |
| Test runner | pytest |
| API testing | requests, jsonschema |
| Test data | Faker, JSON fixtures, environment variables |
| Reporting | pytest-html, Allure |
| Parallel execution | pytest-xdist |
| Retry handling | pytest-rerunfailures |
| AWS mocking | moto, boto3 |
| Self-healing locator flow | LangGraph, provider protocol |
| Code quality | ruff |

## Repository Structure

```text
tst-playwright/
  ecart/
    components/          # Reusable page fragments such as navbar and modal
    configs/             # TestData, environment loading, API schema
    pages/               # Page Object Model classes
      auth/
      product/
      user/
      base_page.py
    self_healing/         # LangGraph-based locator recovery prototype
    test_data/            # Local JSON test data
    tests/                # pytest test suites and fixtures
      api_tests/
      e2e/
      mock_aws/
      conftest.py
    utilities/            # Logger, secrets, API, Faker, data helpers
  assets/                 # Report styling assets
  pyproject.toml          # pytest configuration and project metadata
  requirements.txt        # Runtime and test dependencies
  run_test.sh             # Shell wrapper for marker-based test execution
  setup_venv.sh           # Unix-like virtualenv setup helper
  dockerfile              # Containerized test runner
  README.md
```

## Architecture

The framework uses a layered test automation architecture:

| Layer | Responsibility |
| --- | --- |
| Tests | Express user journeys and assertions with pytest |
| Fixtures | Provide browser pages, test data, secrets, API sessions, logging context, screenshots, and traces |
| Page objects | Encapsulate UI locators and user actions |
| Base page | Centralizes Playwright navigation, clicks, typing, timeouts, and locator healing hooks |
| Utilities | Handle logging, secrets, API helpers, Faker data, and reusable data operations |
| Config | Stores URLs, titles, products, API base URL, and required environment variables |
| Reporting | Produces HTML, Allure artifacts, screenshots, traces, and JSON logs |

## Design Patterns Used

- Page Object Model: UI behavior is modeled under `ecart/pages`, keeping locators and interactions outside test files.
- Base Page Pattern: `BasePage` provides shared navigation, click, fill, timeout, and self-healing behavior.
- Component Object Pattern: reusable UI parts such as navbar and modal live under `ecart/components`.
- Fixture Pattern / Dependency Injection: pytest fixtures inject browser pages, API sessions, credentials, schemas, and test data.
- Strategy Pattern: self-healing uses a `LocatorProposer` protocol so different locator proposal providers can be swapped.
- Graph Workflow Pattern: locator recovery is modeled as a LangGraph flow with capture, propose, validate, and report nodes.
- Factory-style data generation: `FakerDataGenerator` builds API payloads without hard-coded user data.
- Adapter/Wrapper Pattern: utilities wrap external systems such as AWS Secrets Manager, requests sessions, and logging.

## Design Principles Followed

- Separation of concerns: tests, page actions, configuration, data, logging, and reporting are separated into dedicated modules.
- DRY: common browser operations and test setup are centralized in `BasePage` and pytest fixtures.
- Single Responsibility Principle: page classes model pages, utilities handle infrastructure, and tests focus on behavior.
- Open/Closed Principle: browser options, self-healing providers, and fixtures can be extended with limited changes to tests.
- Fail fast configuration: required environment variables are validated through `TestData.get_env`.
- Explicit waits: page actions use Playwright locators and `expect` checks before interacting.
- Test isolation: each test receives its own page/context lifecycle through the `page` fixture.
- Observability first: failures capture screenshots, traces are optional, and logs include run, worker, browser, and test context.
- CI-friendly execution: parallel execution, retries, Allure artifacts, Docker support, and environment-driven secrets are supported.

## Pytest Plugins Used

The project uses the following pytest plugins from `requirements.txt` and `pyproject.toml`:

| Plugin | Purpose |
| --- | --- |
| `pytest-playwright` | Playwright integration for pytest-based browser automation |
| `pytest-xdist` | Parallel test execution with `-n` workers |
| `pytest-rerunfailures` | Automatic retry for failed tests; configured with `--reruns=1` |
| `pytest-html` | Self-contained HTML report generation at `report.html` |
| `allure-pytest` | Allure result generation with `--alluredir=allure-results` |
| `pytest-dependency` | Test dependency ordering for API flow checks |
| `pytest-dotenv` | Environment variable loading support |
| `pytest-base-url` | Base URL support for browser/API configuration |
| `pytest-asyncio` | Async test support where async pytest tests are added |

The configured pytest markers are:

- `smoke`
- `regression`
- `critical`
- `ui`

## Best Practices Implemented

- Tests are grouped by concern: E2E, API, mock AWS, and core UI tests.
- Locators are stored in page objects instead of being duplicated across test files.
- Browser lifecycle is controlled through pytest fixtures.
- Test credentials and API tokens are read from environment variables or AWS Secrets Manager.
- API payloads use Faker-generated data to avoid repeated static test users.
- API responses are validated with JSON Schema.
- Failed UI tests automatically capture screenshots.
- Playwright tracing is opt-in with `--enable-trace` to keep normal runs lightweight.
- JSON logs are enriched with test metadata for easier CI debugging.
- `pytest-xdist` is supported for faster suite execution.
- `pytest-rerunfailures` is configured to reduce noise from transient failures.
- Allure and HTML reports are both supported.
- Dockerfile is available for reproducible container execution.
- Self-healing locator logic runs in suggest/retry mode and does not edit source code.

## Prerequisites

- Python 3.11 recommended
- pip
- Playwright browser binaries
- Git Bash, WSL, Linux, or macOS shell if using `run_test.sh`
- Optional: Allure CLI for serving Allure reports locally
- Optional: Docker for container execution

## Setup

From the repository root:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux/Git Bash:

```bash
source .venv/bin/activate
```

Install dependencies and browsers:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install
```

Because tests import modules from the `ecart` package root, set `PYTHONPATH` before running tests from the repository root.

Windows PowerShell:

```powershell
$env:PYTHONPATH="ecart"
```

macOS/Linux/Git Bash:

```bash
export PYTHONPATH=ecart
```

## Environment Variables

`ecart/configs/settings.py` loads environment variables from `ecart/.env`.

Create or update `ecart/.env` with values for your environment:

```env
BASE_URL_API=https://gorest.co.in
GO_REST_TOKEN=Bearer <your_gorest_token>
USER_NAME=<opencart_user_email>
PASSWORD=<opencart_user_password>
SELF_HEAL=1
HEAL_PROVIDER=stub
```

Required variables:

| Variable | Used For |
| --- | --- |
| `BASE_URL_API` | GoRest API base URL |
| `GO_REST_TOKEN` | GoRest API bearer token |
| `USER_NAME` | Local UI login username |
| `PASSWORD` | Local UI login password |

Optional variables:

| Variable | Default | Used For |
| --- | --- | --- |
| `SELF_HEAL` | `1` | Enables or disables locator self-healing |
| `HEAL_PROVIDER` | `stub` | Selects the self-healing proposer implementation |
| `AWS_REGION` | `us-east-1` | AWS Secrets Manager region in CI |
| `CI` | unset | Switches secret loading from local env vars to AWS Secrets Manager |

## Running Tests

Run the full configured suite:

```bash
pytest
```

Run smoke tests:

```bash
pytest -m smoke
```

Run regression tests:

```bash
pytest -m regression
```

Run a specific suite:

```bash
pytest ecart/tests/e2e
pytest ecart/tests/api_tests
pytest ecart/tests/mock_aws
```

Run in parallel:

```bash
pytest -n auto
```

Run with a specific browser:

```bash
pytest --app-browser chromium
pytest --app-browser firefox
```

The custom `--app-browser` option also lists `edge`; if you want real Microsoft Edge execution, update the browser launch code to use Playwright's Chromium channel support.

Run with Playwright tracing:

```bash
pytest --enable-trace
```

Run with Allure output:

```bash
pytest --alluredir=allure-results
```

Use the helper script:

```bash
./run_test.sh smoke 4 false
```

Arguments:

| Position | Meaning | Example |
| --- | --- | --- |
| 1 | pytest marker | `smoke` |
| 2 | xdist worker count | `4` |
| 3 | headed mode flag | `false` |
| 4+ | extra pytest arguments | `--lf -x` |

## Reporting and Artifacts

- `report.html`: self-contained pytest HTML report.
- `allure-results/`: raw Allure result files.
- `ecart/reports/screenshots/`: screenshots captured on UI test failure.
- `ecart/traces/`: Playwright traces when `--enable-trace` is used.
- `ecart/logs/<run_id>/pytest.log`: structured JSON test logs.

Serve Allure results:

```bash
allure serve allure-results
```

## Docker Execution

Build the image:

```bash
docker build -t tst-playwright -f dockerfile .
```

Run the tests:

```bash
docker run --rm --env-file ecart/.env tst-playwright
```

## Clone-Time Changes for a New User

After cloning this repository, update these items before running tests:

1. Create `ecart/.env` and set `BASE_URL_API`, `GO_REST_TOKEN`, `USER_NAME`, and `PASSWORD`.
2. Replace OpenCart credentials with a valid account for `https://naveenautomationlabs.com/opencart/`.
3. If using another application URL, update `BASE_URL`, `LOGIN_PAGE`, `REGISTER_PAGE_URL`, and expected titles in `ecart/configs/settings.py`.
4. If using a different API, update `BASE_URL_API`, API endpoints, payload generation, and `ecart/configs/schema.json`.
5. Set `PYTHONPATH=ecart` when running tests from the repository root.
6. Run `playwright install` on the machine or inside the container.
7. In CI, provide the same environment variables as pipeline secrets, or configure AWS Secrets Manager with the expected `valid_user` secret.
8. Do not commit local artifacts such as `report.html`, `allure-results/`, `traces/`, `.pytest_cache/`, `.ruff_cache/`, `.venv/`, or local logs.

## Useful Commands

```bash
# install dependencies
pip install -r requirements.txt

# install browsers
playwright install

# run all tests
pytest

# run smoke tests in parallel
pytest -m smoke -n auto

# run one test file
pytest ecart/tests/e2e/test_login_page.py

# run API tests
pytest ecart/tests/api_tests

# run with trace capture
pytest --enable-trace

# generate Allure artifacts
pytest --alluredir=allure-results

# serve Allure report
allure serve allure-results
```
