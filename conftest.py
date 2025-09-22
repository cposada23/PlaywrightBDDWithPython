"""
Global pytest configuration and fixtures for Playwright BDD Framework.
"""

import os
import pytest
import allure
from datetime import datetime
from pathlib import Path
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
    """Launch browser with specified configuration."""
    browser_args = {"headless": is_headless, "slow_mo": slow_mo}
    
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
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create a new browser context for each test for isolation."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
        record_video_dir="reports/videos/" if os.getenv("RECORD_VIDEO") else None,
        record_video_size={"width": 1280, "height": 720}
    )
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


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Automatically capture screenshot on test failure."""
    yield
    
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate screenshot filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name.replace("::", "_").replace("[", "_").replace("]", "")
        screenshot_path = screenshot_dir / f"{test_name}_{timestamp}.png"
        
        try:
            # Capture screenshot
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"\n📸 Screenshot saved: {screenshot_path}")
            
            # Attach screenshot to Allure report if available
            if hasattr(allure, 'attach'):
                with open(screenshot_path, "rb") as screenshot_file:
                    allure.attach(
                        screenshot_file.read(),
                        name=f"Screenshot_{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available to fixtures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)