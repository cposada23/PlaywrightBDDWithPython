# Playwright BDD Testing Framework

A Python testing framework combining **Playwright** for web automation with **pytest-bdd** for Behavior-Driven Development (BDD) testing.

## 📁 Project Structure

```
PythonBDDFramework/
├── conftest.py                    # Global pytest configuration and fixtures
├── pytest.ini                    # Pytest configuration file
├── pyproject.toml                # Project dependencies and metadata
├── run_tests.sh                  # Easy test runner script with debugging defaults
├── test_runner_examples.md       # Examples and usage guide for the test runner
├── README.md                     # This file
├── tests/
│   ├── features/                 # Gherkin feature files
│   │   └── .feature   # Example feature scenarios
│   ├── steps/                    # pytest-bdd step definitions
│   │   └── test_<file>_steps.py # Step implementations
│   └── pages/                    # Page Object Model classes
│       ├── base_page.py          # Base page with common functionality
│       └── <page>_page.py   # Page object implementation
└── reports/                      # Generated test reports and artifacts
    ├── screenshots/              # Screenshots captured during test failures
    └── allure-results/          # Allure report data
```

## 🛠 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd PythonBDDFramework
   ```

2. **Create and activate a virtual environment using uv:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install project dependencies:**
   ```bash
   uv sync
   ```

4. **Install Playwright browsers:**
   ```bash
   uv run playwright install
   ```

## 🧪 Running Tests

### Easy Test Runner (Recommended)

Use the included `run_tests.sh` script for the easiest way to run tests with sensible defaults:

```bash
# Run with debugging defaults (visible browser, slow motion, allure reports)
./run_tests.sh

# Run specific test markers
./run_tests.sh --markers=web

# Run headless for CI/fast execution
./run_tests.sh --headless=true --parallel=true --slowmo=0

```

**📖 For more examples and options, see [test_runner_examples.md](test_runner_examples.md)**

### Manual Test Execution

**Basic pytest commands:**
```bash
# Run all tests
uv run pytest

# Run with parallel execution
uv run pytest -n auto

# Run specific markers
uv run pytest -m web

# Debug mode (visible browser + slow motion)
uv run pytest --headless=false --slowmo=1000
```

## 📊 Test Reports

**Allure Reports (Interactive):**
```bash
uv run pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

*Note: Install Allure with `brew install allure` (macOS) or equivalent for your OS.*

## 🔧 Configuration

### Available Options

The framework supports these command line options:

- `--base-url`: Base URL for the application under test
- `--browser`: Browser to use (chromium, firefox, webkit)
- `--headless`: Run browser in headless mode (true/false)
- `--slowmo`: Slow down operations by milliseconds

## 📝 Writing Tests

### BDD Feature Files

Create feature files in `tests/features/` using Gherkin syntax:

```gherkin
Feature: Website Navigation
  As a user
  I want to navigate the website
  So that I can access information

  @web
  Scenario: Navigate to contact page
    Given I navigate to the home page
    When I click on contact link
    Then I should see the contact form
```

### Step Definitions

Implement step definitions in `tests/steps/` using pytest-bdd decorators:

```python
from pytest_bdd import given, when, then, scenarios
from tests.pages.home_page import HomePage
from conftest import capture_failure_screenshot

scenarios('../features/navigation.feature')

@given("I navigate to the home page")
def i_navigate_to_home_page(home_page: HomePage, base_url: str):
    with allure.step("Navigate to home page"):
        try:
            home_page.navigate(base_url)
        except Exception as e:
            capture_failure_screenshot(home_page.page, "Navigation")
            raise AssertionError(f"Failed to navigate: {e}")
```

### Page Objects

Create page objects in `tests/pages/` extending the `BasePage`:

```python
from tests.pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.contact_link = page.locator('a[href="/contact"]')
    
    def click_contact_link(self):
        self.contact_link.click()
```

### Screenshot Capture

The framework includes automatic screenshot capture on failures using the helper function:

```python
from conftest import capture_failure_screenshot

# Use in exception blocks
except Exception as e:
    capture_failure_screenshot(page, "Step description")
    raise AssertionError(f"Step failed: {e}")
```

## 🐛 Debugging

### Screenshots
Screenshots are automatically captured on test failures and saved to `reports/screenshots/`.

### Visual Debugging
Use the test runner script for easy debugging:
```bash
# Run with visible browser and slow motion
./run_tests.sh --headless=false --slowmo=1000

# Interactive debugging - add page.pause() in your code
page.pause()  # Pauses execution for manual inspection
```

## 🔍 Troubleshooting

**Browser not found:** Run `uv run playwright install`

**Tests are slow:** Use `./run_tests.sh --parallel=true --headless=true`

**Missing screenshots:** Check `reports/screenshots/` directory permissions

**Allure not working:** Install with `brew install allure` (macOS) or equivalent

---
