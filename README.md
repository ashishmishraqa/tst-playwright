## Instruction
1. Clone the repository
        git clone https://github.com/ashishmishraqa/tst-playwright.git
        cd tst-playwright
2. Create a virtual environment
        python -m venv .venv
3. Activate a virtual environment
        source .venv/bin/activate (macOS/Linux (bash/zsh))
        .venv\Scripts\Activate.ps1(Windows - PowerShell)
        .venv\Scripts\activate.bat(Windows)
        source .venv/Scripts/activate (git bash)
4. Upgrade pip(recommended)
        python -m pip install --upgrade pip
5. Execute pip install -r requirements.txt
6. to install all the browsers that Playwright supports 
   playwright install


## Running Tests

To run all tests:
    
    bash pytest

To run tests in a specific file:

    bash pytest ecart/tests/test_home.py

To run tests with a specific marker (if configured):
    
    bash pytest -m "smoke"

To run tests in headed mode (to see the browser):

    bash pytest --headed

To run tests in a specific browser (e.g., firefox):
    
    bash pytest --browser firefox

Run all tests and generate Allure results

        pytest --alluredir=allure-results

Run specific test file

        pytest ecart/tests/test_home.py --alluredir=allure-results

Run with markers

        pytest -m smoke --alluredir=allure-results

## Project Structure

- `ecart/configs`: Configuration files.
- `ecart/pages`: Page Object Models (POM).
- `ecart/test_data`: Test data files.
- `ecart/tests`: Test scripts.
- `ecart/utils`: Utility functions.
- `requirements.txt`: Python dependencies.

## reporting flow
        
        Running Tests ──→ allure-results/ ──→ allure serve ──→ 📊 Live Report
                               ↓
                         allure generate ──→ allure-report/ ──→ 📊 Static HTML

## Best Practices 
1. Avoid hard code test data
2. Externalize Test data
3. Implement POM
4. Centralize reusable code
5. Define global environment variable
6. 


# Set up Playwright MCP

install Claude code 

        
