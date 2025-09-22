# Playwright BDD Testing Framework

A comprehensive Python testing framework combining **Playwright** for web automation with **pytest-bdd** for Behavior-Driven Development (BDD) testing. This framework provides a robust foundation for writing and executing web application tests using Gherkin feature files and pytest.

## 🚀 Features

- **Easy Test Runner**: Single script with debugging-friendly defaults (`run_tests.sh`)
- **BDD Support**: Write tests in natural language using Gherkin syntax
- **Playwright Integration**: Fast, reliable web automation with excellent browser support
- **Enhanced Error Handling**: Detailed error messages with automatic screenshot capture
- **Parallel Execution**: Run tests in parallel with pytest-xdist for faster feedback
- **Rich Reporting**: Generate beautiful HTML reports and interactive Allure reports
- **Page Object Model**: Organized, maintainable page object structure
- **Debug Mode**: Visible browser with slow motion for easy debugging
- **Cross-Browser Testing**: Support for Chromium, Firefox, and WebKit
- **Configurable Environments**: Easy testing against different environments
- **Isolated Test Execution**: Each test runs in its own browser context

## 📁 Project Structure

```
PythonBDDFramework/
├── conftest.py                 # Global pytest configuration and fixtures
├── pytest.ini                 # Pytest configuration file
├── pyproject.toml             # Project dependencies and metadata
├── run_tests.sh              # Easy test runner script with debugging defaults
├── test_runner_examples.md   # Examples and usage guide for the test runner
├── README.md                  # This file
├── tests/
│   ├── __init__.py
│   ├── features/              # Gherkin feature files
│   │   └── login.feature      # Example login feature scenarios
│   ├── steps/                 # pytest-bdd step definitions
│   │   ├── __init__.py
│   │   └── test_login_steps.py # Step implementations for login feature
│   └── pages/                 # Page Object Model classes
│       ├── __init__.py
│       ├── base_page.py       # Base page with common functionality
│       └── login_page.py      # Login page object
└── reports/                   # Generated test reports and artifacts
    ├── screenshots/           # Screenshots captured during test failures
    └── videos/               # Recorded videos (when enabled)
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

   Optional: Install system dependencies for browsers:
   ```bash
   uv run playwright install-deps
   ```

## 🧪 Running Tests

### Basic Test Execution

**Run all tests:**
```bash
uv run pytest
```

**Run tests in parallel (recommended):**
```bash
uv run pytest -n auto
```

**Run specific test types:**
```bash
# Run only smoke tests
uv run pytest -m smoke

# Run only BDD feature tests
uv run pytest tests/steps/

# Run specific feature
uv run pytest tests/steps/test_login_steps.py

# Run tests with specific feature file
uv run pytest -k "login"
```

### Browser Configuration

**Run tests in different browsers:**
```bash
# Chrome (default)
uv run pytest --browser=chromium

# Firefox
uv run pytest --browser=firefox

# Safari
uv run pytest --browser=webkit
```

**Debug Mode - Run tests with visible browser:**
```bash
# Run with visible browser (headed mode)
uv run pytest --headless=false

# Run with visible browser and slow motion for debugging
uv run pytest --headless=false --slowmo=1000

# Run with slow motion (helps see what's happening)
uv run pytest --headless=false --slowmo=500
```

### Environment Configuration

**Test against different environments:**
```bash
# Production
uv run pytest --base-url=https://myapp.com

# Staging
uv run pytest --base-url=https://staging.myapp.com

# Local development
uv run pytest --base-url=http://localhost:3000
```

### Advanced Test Execution

**Run tests with custom markers:**
```bash
# Run web UI tests only
uv run pytest -m web

# Run regression tests
uv run pytest -m regression

# Exclude slow tests
uv run pytest -m "not slow"

# Combine markers
uv run pytest -m "smoke and web"
```

**Run tests with increased verbosity:**
```bash
uv run pytest -v --tb=long
```

**Run specific test scenarios:**
```bash
# Run specific scenario by name
uv run pytest -k "valid credentials"

# Run multiple scenarios
uv run pytest -k "login or validation"
```

## 📊 Test Reports

### HTML Reports

**Generate simple HTML reports:**
```bash
uv run pytest -n auto --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in your browser to view the results.

### Allure Reports (Recommended)

**Generate Allure reports:**
```bash
# Run tests and generate allure data
uv run pytest -n auto --alluredir=reports/allure-results

# Serve the interactive report
uv run allure serve reports/allure-results
```

**Install Allure (if not already installed):**
```bash
# macOS
brew install allure

# Linux
sudo apt-get install allure

# Windows (using Chocolatey)
choco install allure
```

### Combining Reports

**Generate both HTML and Allure reports:**
```bash
uv run pytest -n auto --html=reports/report.html --alluredir=reports/allure-results
```

## 🔧 Configuration Options

### pytest.ini Configuration

The framework includes a comprehensive `pytest.ini` file with optimized settings:

- **Test Discovery**: Automatic discovery of test files and functions
- **Markers**: Pre-defined markers for categorizing tests (`smoke`, `web`, `api`, `regression`, `slow`)
- **BDD Settings**: Configuration for pytest-bdd feature file location
- **Logging**: Detailed logging configuration for debugging
- **Warnings**: Filtered common warnings for cleaner output

### Environment Variables

Set these environment variables for additional configuration:

```bash
# Record videos of test execution
export RECORD_VIDEO=true

# Set default base URL
export BASE_URL=https://myapp.com

# Enable debug mode
export DEBUG=true
```

### Command Line Options

The framework supports these custom command line options:

- `--base-url`: Base URL for the application under test
- `--browser`: Browser to use (chromium, firefox, webkit)
- `--headless`: Run browser in headless mode (true/false)
- `--slowmo`: Slow down operations by milliseconds

## 📝 Writing Tests

### BDD Feature Files

Create feature files in `tests/features/` using Gherkin syntax:

```gherkin
Feature: User Authentication
  As a user
  I want to log into the application
  So that I can access my account

  @smoke @web
  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    And I click the login button
    Then I should be redirected to the dashboard
```

### Step Definitions

Implement step definitions in `tests/steps/` using pytest-bdd decorators:

```python
from pytest_bdd import given, when, then, scenarios
from tests.pages.login_page import LoginPage

scenarios('../features/login.feature')

@given("I am on the login page")
def i_am_on_login_page(login_page: LoginPage, base_url: str):
    login_page.navigate_to_login(base_url)

@when("I enter valid credentials")
def i_enter_valid_credentials(login_page: LoginPage, test_data):
    login_page.login(test_data["valid_user"]["username"], 
                    test_data["valid_user"]["password"])
```

### Page Objects

Create page objects in `tests/pages/` extending the `BasePage`:

```python
from tests.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator('input[name="username"]')
        self.password_input = page.locator('input[name="password"]')
        self.login_button = page.locator('button[type="submit"]')
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

### Enhanced Error Handling

The framework provides comprehensive error handling with detailed messages:

```python
# Automatic screenshot capture on failure
try:
    login_page.fill_username("testuser")
except Exception as e:
    login_page.take_screenshot("failed_enter_username")
    raise AssertionError(f"Failed to enter username: {str(e)}")
```

## 🐛 Debugging

### Screenshots

Screenshots are automatically captured on test failures and saved to `reports/screenshots/`.

**Manually capture screenshots:**
```python
# In step definitions or tests
page.screenshot(path="debug_screenshot.png", full_page=True)

# Using page object helper
login_page.take_screenshot("login_page_state")
```

### Video Recording

Enable video recording for test debugging:

```bash
export RECORD_VIDEO=true
uv run pytest
```

Videos are saved to `reports/videos/`.

### Debug Mode

**Run tests with debug output:**
```bash
uv run pytest --capture=no -s -v
```

**Run single test with debugging:**
```bash
uv run pytest tests/steps/test_login_steps.py -s -v
```

**Debug specific scenario:**
```bash
uv run pytest -k "Successful login" --headless=false --slowmo=1000 -s -v
```

### Browser Developer Tools

**Run tests with browser dev tools open:**
```bash
uv run pytest --headless=false --slowmo=1000
```

**Interactive debugging:**
Add `page.pause()` in your step definitions or page objects to pause execution and inspect the page state:

```python
@when("I click the login button")
def i_click_login_button(login_page: LoginPage):
    login_page.page.pause()  # Pauses here for inspection
    login_page.click_login_button()
```

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
      - name: Install Playwright browsers
        run: uv run playwright install --with-deps
      - name: Run tests
        run: uv run pytest -n auto --html=reports/report.html --alluredir=reports/allure-results
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: reports/
```

### Docker Support

Create a `Dockerfile` for containerized testing:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync
RUN uv run playwright install --with-deps

CMD ["uv", "run", "pytest", "-n", "auto"]
```

## 🤝 Contributing

1. Follow the established project structure
2. Write comprehensive tests for new features
3. Use descriptive commit messages
4. Ensure all tests pass before submitting PRs
5. Update documentation for new features

### Code Style

The project follows Python best practices:

- Use type hints where appropriate
- Follow PEP 8 style guidelines
- Write descriptive docstrings
- Use meaningful variable and function names

### Test Guidelines

- Write clear, descriptive scenario names
- Use appropriate test markers (`@smoke`, `@web`, etc.)
- Keep step definitions focused and reusable
- Use page objects for UI interactions
- Add screenshots for visual verification when needed

## 🔍 Troubleshooting

### Common Issues

**Tests fail with "Browser not found" error:**
```bash
uv run playwright install
```

**Tests are slow:**
- Use parallel execution: `pytest -n auto`
- Check if tests are waiting for unnecessary elements
- Consider using `--headless=true` (default)

**Screenshots not captured:**
- Check that `reports/screenshots/` directory exists
- Verify write permissions
- Ensure the screenshot fixture is working

**Allure reports not generating:**
```bash
# Reinstall allure
pip install allure-pytest
# Or install allure command line tool
```

### Getting Help

- Check the pytest documentation: https://pytest.org
- Playwright documentation: https://playwright.dev/python
- pytest-bdd documentation: https://pytest-bdd.readthedocs.io

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏷️ Version

Current version: 1.0.0

---

**Happy Testing! 🧪✨**
