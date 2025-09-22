"""
Global pytest configuration and fixtures for Playwright BDD Framework.
"""

import os
import pytest
import allure
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


def pytest_addoption(parser):
    """Add custom command line options for pytest."""
    parser.addoption("--base-url", action="store", default="https://blankfactor.com/", help="Base URL for the application under test")
    parser.addoption("--browser", action="store", default="chromium", choices=["chromium", "firefox", "webkit"], help="Browser to run tests against")
    parser.addoption("--headless", action="store", default="true", choices=["true", "false"], help="Run browser in headless mode")
    parser.addoption("--slowmo", action="store", default="0", help="Slow down operations by specified amount of milliseconds")


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Get base URL from command line option."""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def browser_name(request) -> str:
    """Get browser name from command line option."""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def is_headless(request) -> bool:
    """Get headless mode setting from command line option."""
    return request.config.getoption("--headless") == "true"


@pytest.fixture(scope="session")
def slow_mo(request) -> int:
    """Get slow motion delay from command line option."""
    return int(request.config.getoption("--slowmo"))


@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    """Start Playwright and yield the instance."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright, browser_name: str, is_headless: bool, slow_mo: int) -> Generator[Browser, None, None]:
    """Launch browser with specified configuration and anti-detection measures."""
    # Base browser arguments
    browser_args = {
        "headless": is_headless, 
        "slow_mo": slow_mo
    }
    
    # Add anti-detection arguments for headless mode
    if is_headless:
        if browser_name == "chromium":
            browser_args["args"] = [
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--disable-web-security",
                "--disable-features=VizDisplayCompositor",
                "--disable-extensions",
                "--disable-plugins",
                "--disable-default-apps",
                "--disable-gpu",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding"
            ]
    
    if browser_name == "chromium":
        browser = playwright.chromium.launch(**browser_args)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(**browser_args)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(**browser_args)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser, is_headless: bool) -> Generator[BrowserContext, None, None]:
    """Create a new browser context for each test with anti-detection measures."""
    
    # Base context options
    context_options = {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos/" if os.getenv("RECORD_VIDEO") else None,
        "record_video_size": {"width": 1280, "height": 720}
    }
    
    # Add anti-detection measures for headless mode
    if is_headless:
        context_options.update({
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "extra_http_headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Cache-Control": "max-age=0"
            },
            "java_script_enabled": True,
            "bypass_csp": True
        })
    
    context = browser.new_context(**context_options)
    
    # Additional JavaScript to hide automation traces
    if is_headless:
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            window.chrome = {
                runtime: {},
            };
        """)
    
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, base_url: str) -> Generator[Page, None, None]:
    """Create a new page for each test with base URL configured."""
    page = context.new_page()
    
    # Set default timeout for actions
    page.set_default_timeout(15000)  # 30 seconds
    page.set_default_navigation_timeout(15000)  # 30 seconds
    
    # Store base_url as page attribute for easy access in tests
    page.base_url = base_url
    yield page


def capture_failure_screenshot(page: Page, step_name: str):
    """Helper function to capture and attach screenshot on step failure."""
    try:
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name=f"Failure Screenshot - {step_name}",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        # If screenshot fails, attach error message
        try:
            allure.attach(
                f"Screenshot capture failed: {str(e)}",
                name="Screenshot Error",
                attachment_type=allure.attachment_type.TEXT
            )
        except:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)