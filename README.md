# tst-playwright

Playwright Test Automation Framework for E-commerce (eCart) application testing.

## Table of Contents
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Test Flow](#test-flow)
- [Running Tests](#running-tests)
  - [Different Modes](#different-modes)
  - [Examples](#examples)
- [Reporting](#reporting)
- [Best Practices](#best-practices)

## Setup

### Prerequisites
- Python 3.8+
- Git

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/ashishmishraqa/tst-playwright.git
   cd tst-playwright
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate virtual environment:
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (CMD): `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
   - Git Bash: `source .venv/Scripts/activate`

4. Upgrade pip and install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Install Playwright browsers:
   ```bash
   playwright install
   ```

### Alternative Setup
- Use `setup_venv.sh` script (Linux/macOS):
  ```bash
  ./setup_venv.sh
  ```
- For Windows, manually follow steps 2-5 above.

Prefer manual setup for better control and cross-platform compatibility. The script assumes Unix-like environment.

## Project Structure
```
tst-playwright/
├── ecart/
│   ├── configs/          # Configuration files
│   ├── pages/            # Page Object Models (POM)
│   │   ├── base_page.py  # Base page class with common methods
│   │   └── ...           # Specific page classes
│   ├── test_data/        # Test data files (JSON, etc.)
│   ├── tests/            # Test scripts
│   │   ├── conftest.py   # Pytest fixtures and configuration
│   │   └── ...           # Test files
│   ├── utilities/        # Utility functions (logger, etc.)
│   └── logs/             # Log files
├── allure-results/       # Allure test results
├── traces/               # Playwright traces
├── pyproject.toml        # Project configuration (pytest settings)
├── requirements.txt      # Python dependencies
├── run_test.sh           # Test runner script
├── setup_venv.sh         # Setup script
└── README.md
```

## Test Flow

1. **Initialization**: Pytest loads `conftest.py`, sets up fixtures (browser, page, test data)
2. **Test Execution**:
   - Browser launches (chromium/firefox/edge, headless by default)
   - Navigate to application URL
   - Interact with elements using POM (Page Object Model)
   - Assertions validate expected behavior
   - Automatic cleanup (close browser, save traces if enabled)
3. **Reporting**: Results saved to `allure-results/`, can be served as live report

### Key Components
- **BasePage**: Common methods (click, type, wait) with explicit waits
- **Page Objects**: Application-specific pages inherit from BasePage
- **Fixtures**: Provide browser instances, test data, worker isolation
- **Markers**: Categorize tests (smoke, regression, etc.)

## Running Tests

### Basic Commands
- Run all tests: `pytest`
- Run specific file: `pytest ecart/tests/test_file.py`
- Run with marker: `pytest -m smoke`

### Different Modes

#### By Test Category (Markers)
- Smoke tests: `pytest -m smoke`
- Regression tests: `pytest -m regression`
- Critical tests: `pytest -m critical`
- UI tests: `pytest -m ui`

#### By Browser
- Chromium (default): `pytest --app-browser chromium`
- Firefox: `pytest --app-browser firefox`
- Edge: `pytest --app-browser edge`

#### Execution Mode
- Headless (default): `pytest` (no browser UI)
- Headed: `pytest --headed` (visible browser)

#### Parallel Execution
- Auto workers: `pytest -n auto` (uses all CPU cores)
- Specific workers: `pytest -n 4` (4 parallel processes)

#### Tracing
- Enable traces: `pytest --enable-trace` (saves to `traces/`)

#### Reporting
- Generate Allure results: `pytest --alluredir=allure-results`
- Serve live report: `allure serve allure-results`

### Examples

#### Full Regression Suite
```bash
pytest -m regression -n auto --alluredir=allure-results
```

#### Smoke Tests in Firefox, Headed
```bash
pytest -m smoke --app-browser firefox --headed
```

#### Single Test with Tracing
```bash
pytest ecart/tests/test_ui_validations.py --enable-trace
```

#### Using Run Script
```bash
./run_test.sh smoke 4 false  # marker, workers, headed
```

Prefer `pytest` commands directly for flexibility. Use `run_test.sh` for quick CI/CD integration.

## Reporting

### Allure Reports
- Results stored in `allure-results/`
- Live report: `allure serve allure-results`
- Static HTML: `allure generate allure-results -o allure-report`

### HTML Reports
- Generate: `pytest --html=report.html`
- Self-contained: `pytest --html=report.html --self-contained-html`

Prefer Allure for detailed, interactive reports with history and trends. HTML reports are simpler for quick checks.

## Best Practices
- Avoid hardcoded test data; use external files
- Implement Page Object Model for maintainability
- Centralize reusable code in utilities
- Define environment variables for config
- Use explicit waits instead of sleep
- Enable tracing for debugging failures
- Run tests in parallel for speed
- Categorize tests with markers
