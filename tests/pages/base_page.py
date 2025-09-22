"""
This module contains the BasePage class with common functionality
shared across all page objects.
"""

from abc import ABC
from typing import Optional
from playwright.sync_api import Page, Locator


class BasePage(ABC):
    """Base page object. Common functionality for all pages."""
    
    def __init__(self, page: Page):
        """Initialize the base page with the Playwright page instance."""
        self.page = page
    
    def wait_for_page_load(self, timeout: int = 30000) -> None:
        """Wait for the page to fully load."""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_element_visible(self, locator: Locator, timeout: int = 10000) -> None:
        """Wait for an element to become visible."""
        locator.wait_for(state="visible", timeout=timeout)
    
    def scroll_to_element(self, locator: Locator) -> None:
        """Scroll to make an element visible."""
        locator.scroll_into_view_if_needed()

    def scroll_to_the_bottom_of_the_page(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.keyboard.press("End")
    
    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.page.title()
    
    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.page.url
    
    def take_screenshot(self, name: Optional[str] = None, full_page: bool = True) -> str:
        """Take a screenshot of the current page."""
        from pathlib import Path
        from datetime import datetime
        
        screenshot_dir = Path("reports/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        screenshot_path = screenshot_dir / f"{name}.png"
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        return str(screenshot_path)
    
    def wait_for_url_change(self, timeout: int = 10000) -> None:
        """Wait for the URL to change from the current URL."""
        current_url = self.page.url
        self.page.wait_for_function(
            f"() => window.location.href !== '{current_url}'",
            timeout=timeout
        )
    
    def wait_for_url_contains(self, url_part: str, timeout: int = 10000) -> None:
        """Wait for the URL to contain a specific string."""
        self.page.wait_for_function(
            f"() => window.location.href.includes('{url_part}')",
            timeout=timeout
        )
    
    def is_element_visible(self, locator: Locator) -> bool:
        """Check if an element is visible."""
        return locator.is_visible()
    
    def get_element_text(self, locator: Locator) -> str:
        """Get the text content of an element."""
        return locator.text_content() or ""
    